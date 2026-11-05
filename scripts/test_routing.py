#!/usr/bin/env python3
"""Execute stored author-designed routing scenarios without changing their expectations."""
import argparse
import datetime
import json
import platform
from pathlib import Path
from route import ROOT, route


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'validation/routing-tests.json')
    parser.add_argument('--output', type=Path, help='optional local JSON report path')
    args = parser.parse_args()
    spec = json.loads(args.input.read_text(encoding='utf-8'))
    rows = []
    for case in spec['requests']:
        actual = route(case['request'])
        families = [c['family'] for c in actual['candidates']]
        expected = case['expected_families']
        # Primary must agree; all explicitly requested structures must be retrieved.
        passed = (not families if not expected else bool(families) and families[0] == expected[0] and set(expected).issubset(families))
        rows.append({'type': 'request', 'request': case['request'], 'expected_families': expected, 'actual': actual, 'pass': passed})
    for case in spec['revisions']:
        before, after = route(case['initial']), route(case['clarification'])
        b = before['candidates'][0]['family'] if before['candidates'] else None
        a = after['candidates'][0]['family'] if after['candidates'] else None
        rows.append({'type': 'revision', 'input': case, 'actual_initial': before, 'actual_revised': after, 'pass': b == case['expected_initial'] and a == case['expected_revised'] and a != b})
    result = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'environment': platform.python_version(),
        'design': spec['design'], 'evaluation': 'separate script author executed stored test prompts; not an independent user study',
        'total': len(rows), 'passed': sum(r['pass'] for r in rows), 'failed': sum(not r['pass'] for r in rows), 'results': rows}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + '\n', encoding='utf-8')
    print(text)
    raise SystemExit(result['failed'] != 0)

if __name__ == '__main__':
    main()
