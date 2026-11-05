#!/usr/bin/env python3
"""Local generic risk scan. A clean scan does not prove publication permission."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {'README.md', 'AGENTS.md', 'START_HERE.md', 'ROUTER.md', 'RULES_GATE.md', 'QUICK_REFERENCE.md', 'THIRD_PARTY_NOTICES.md', '.gitignore', 'LICENSE', 'LICENSE.md'}
TOP_DIRS = {'catalog', 'playbooks', 'families', 'cases', 'methods', 'tools', 'interviews', 'templates', 'examples', 'scripts', 'validation'}
EXTENSIONS = {'.md', '.json', '.py', '.csv', '.txt', '.tsv'}
PATTERNS = {
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github_token': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
    'api_key': r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'phone_like': r'(?<!\d)01[016789][- ]?\d{3,4}[- ]?\d{4}(?!\d)',
    'credential_assignment': r'(?i)(?:password|api_key|access_token)\s*[:=]\s*[\x22\x27][^\x22\x27\s]{8,}[\x22\x27]',
}


def scan(root):
    files, findings = [], []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts or not path.is_file():
            continue
        name = rel.as_posix()
        files.append(name)
        allowed = name in TOP_FILES or (rel.parts[0] in TOP_DIRS and path.suffix in EXTENSIONS)
        if not allowed:
            findings.append({'file': name, 'kind': 'outside_allowlist'})
        try:
            body = path.read_text(encoding='utf-8')
        except UnicodeError:
            findings.append({'file': name, 'kind': 'non_utf8'}); continue
        for kind, pattern in PATTERNS.items():
            for match in re.finditer(pattern, body):
                # Report location only, never echo a suspected secret.
                findings.append({'file': name, 'line': body.count('\n', 0, match.start()) + 1, 'kind': kind})
    return {'files': files, 'file_count': len(files), 'findings': findings,
            'status': 'needs_review' if findings else 'no_generic_pattern_found',
            'limitation': 'No semantic privacy or provenance guarantee. Manually review all publishable files and diff; use no private denylist in this repository.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = scan(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['findings']))

if __name__ == '__main__':
    main()
