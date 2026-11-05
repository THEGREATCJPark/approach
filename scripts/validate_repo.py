#!/usr/bin/env python3
"""Check offline catalog, references and Markdown links; not a semantic quality audit."""
import argparse
import collections
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FIELDS = 'id title family keywords_ko keywords_en problem_structure deliverable_types provenance applicable_when do_not_use_when data_required method_ids tool_ids related_cases depth path'.split()


def validate_schema(value, schema, location='$'):
    """Small explicitly bounded JSON Schema subset used by catalog/schema.json."""
    errors = []
    annotations = {'$schema', '$comment', 'title', 'description'}
    supported = {'type', 'required', 'properties', 'items', 'enum', 'minLength', 'minItems'}
    unknown = set(schema) - annotations - supported
    if unknown:
        return [f'{location}: unsupported schema keywords {sorted(unknown)}']
    checks = {
        'object': lambda v: isinstance(v, dict),
        'array': lambda v: isinstance(v, list),
        'string': lambda v: isinstance(v, str),
        'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        'integer': lambda v: isinstance(v, int) and not isinstance(v, bool),
        'boolean': lambda v: isinstance(v, bool),
        'null': lambda v: v is None,
    }
    expected = schema.get('type')
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if any(t not in checks for t in types):
            return [f'{location}: unsupported schema type {types}']
        if not any(checks[t](value) for t in types):
            return [f'{location}: expected type {types}']
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{location}: outside enum')
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(f'{location}: below minLength')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{location}: below minItems')
        if 'items' in schema:
            for i, item in enumerate(value):
                errors.extend(validate_schema(item, schema['items'], f'{location}[{i}]'))
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{location}: required {key}')
        for key, subschema in schema.get('properties', {}).items():
            if key in value:
                errors.extend(validate_schema(value[key], subschema, f'{location}.{key}'))
    return errors


def records(root, name, errors):
    path = root / 'catalog' / (name + '.json')
    try:
        obj = json.loads(path.read_text(encoding='utf-8'))
        value = obj if isinstance(obj, list) else obj.get(name)
        if not isinstance(value, list) or any(not isinstance(c, dict) for c in value):
            raise ValueError('expected array of objects or keyed array')
        return value
    except (OSError, ValueError) as exc:
        errors.append(f'{path.relative_to(root)}: {exc}')
        return []


def check(root):
    errors, warnings = [], []
    catalogs = {name: records(root, name, errors) for name in ['cases', 'methods', 'tools']}
    try:
        schema = json.loads((root / 'catalog/schema.json').read_text(encoding='utf-8'))
        errors.extend(validate_schema(catalogs['cases'], schema))
    except (OSError, ValueError) as exc:
        errors.append(f'catalog/schema.json: {exc}')
    ids = {}
    for name, rows in catalogs.items():
        seen = set()
        for row in rows:
            ident = row.get('id')
            if not isinstance(ident, str) or not ident:
                errors.append(f'{name}: missing string id'); continue
            if ident in seen:
                errors.append(f'{name}: duplicate id {ident}')
            seen.add(ident)
            card = row.get('path', f'{name}/{ident}.md')
            if not isinstance(card, str) or not (root / card).is_file():
                errors.append(f'{name}/{ident}: missing card {card}')
        ids[name] = seen
    for case in catalogs['cases']:
        ident = case.get('id', '?')
        for field in FIELDS:
            if field not in case:
                errors.append(f'{ident}: missing field {field}')
            elif case[field] is None or case[field] == '':
                errors.append(f'{ident}: empty field {field}')
        for field in ['keywords_ko', 'keywords_en', 'deliverable_types', 'method_ids', 'tool_ids', 'related_cases']:
            if field in case and not isinstance(case[field], list):
                errors.append(f'{ident}: {field} must be array')
        if case.get('provenance') not in ['synthetic', 'public_reference']:
            errors.append(f'{ident}: invalid provenance')
        for field, name in [('method_ids', 'methods'), ('tool_ids', 'tools'), ('related_cases', 'cases')]:
            refs = case.get(field, [])
            if isinstance(refs, list):
                for ref in refs:
                    if ref not in ids[name]:
                        errors.append(f'{ident}: unresolved {field} {ref}')
        if case.get('depth') in ['deep', 'advanced', '심화']:
            tests = case.get('tests', [])
            if not isinstance(tests, list) or len(tests) < 6:
                errors.append(f'{ident}: deep card needs at least 6 structured tests')
            if not case.get('fixture') and not case.get('fixture_path'):
                errors.append(f'{ident}: deep card needs fixture or fixture_path')
            if case.get('fixture_path') and not (root / case['fixture_path']).is_file():
                errors.append(f'{ident}: fixture_path missing')
        card_path = root / case.get('path', '__missing__')
        if card_path.is_file():
            body = card_path.read_text(encoding='utf-8')
            if len(body) < 1500:
                errors.append(f'{ident}: card suspiciously short (<1500 characters)')
            # Exact metadata block is inspectable without an optional YAML dependency.
            blocks = re.findall(r'```json\s*\n(.*?)\n```', body, re.S)
            metadata = []
            for block in blocks:
                try:
                    parsed = json.loads(block)
                    if isinstance(parsed, dict) and parsed.get('id') == ident:
                        metadata.append(parsed)
                except ValueError:
                    errors.append(f'{ident}: invalid fenced JSON')
            if metadata:
                for field in FIELDS:
                    if field not in metadata[0]:
                        errors.append(f'{ident}: card metadata missing {field}')
                    elif metadata[0][field] != case.get(field):
                        errors.append(f'{ident}: card/catalog disagree at {field}')
            else:
                errors.append(f'{ident}: no matching JSON metadata block')
    link_count = 0
    for path in sorted(root.rglob('*.md')):
        if '.git' in path.parts:
            continue
        body = path.read_text(encoding='utf-8')
        # Ignore illustrative code blocks; inline code links remain intentional references.
        body = re.sub(r'```.*?```', '', body, flags=re.S)
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            target = raw.strip().split(' "')[0].strip('<>')
            if re.match(r'^[a-zA-Z][\w+.-]*:', target) or not target or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            if not target:
                continue
            resolved = (root / target.lstrip('/')) if target.startswith('/') else path.parent / target
            link_count += 1
            if not resolved.exists():
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    counts = collections.Counter(c.get('family', '?') for c in catalogs['cases'])
    return {'status': 'pass' if not errors else 'fail', 'counts': {n: len(r) for n, r in catalogs.items()},
        'deep_cases': sum(c.get('depth') in ['deep', 'advanced', '심화'] for c in catalogs['cases']),
        'families': dict(sorted(counts.items())), 'local_links_checked': link_count,
        'errors': errors, 'warnings': warnings,
        'scope': 'Structural validation only; numerical examples, source verification and manual publication review are separate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'pass')

if __name__ == '__main__':
    main()
