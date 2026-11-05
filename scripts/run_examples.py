#!/usr/bin/env python3
"""Run the eight local synthetic oracle suites. No installation or network access."""
import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = ['check_a', 'check_b', 'check_c'] + [f'check_expansion_{c}' for c in 'abcde']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-reports', action='store_true', help='Write execution evidence under validation; preparation/maintenance only')
    args = parser.parse_args()
    suites = []
    seen_cases = set()
    for name in SUITES:
        command = [sys.executable, str(ROOT / 'examples' / 'synthetic' / (name + '.py'))]
        try:
            if not Path(command[1]).is_file():
                raise FileNotFoundError(f'Missing required suite: {name}.py')
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            if run.returncode != 0:
                raise ValueError(f'{name} exited {run.returncode}: {run.stderr[-1000:]}')
            result = json.loads(run.stdout)
            rows = result['results']
            seen_cases.update(row.get('case_id', row.get('case')) for row in rows)
            passed = sum(row.get('status') == 'pass' for row in rows)
            ok = run.returncode == 0 and bool(rows) and passed == len(rows)
            summary = {'suite': name, 'checks': len(rows), 'passed': passed, 'status': 'pass' if ok else 'fail'}
            if args.write_reports:
                (ROOT / 'validation' / (name + '-results.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
            summary = {'suite': name, 'checks': 0, 'passed': 0, 'status': 'fail', 'error': str(exc)}
        suites.append(summary)
    expected_cases = {case['id'] for case in json.loads((ROOT / 'catalog' / 'cases.json').read_text(encoding='utf-8'))}
    missing_cases = sorted(expected_cases - seen_cases)
    unexpected_cases = sorted(str(case) for case in seen_cases - expected_cases)
    output = {'python': platform.python_version(), 'suites': suites,
              'covered_cases': len(seen_cases), 'missing_cases': missing_cases, 'unexpected_cases': unexpected_cases,
              'checks': sum(s['checks'] for s in suites), 'passed': sum(s['passed'] for s in suites),
              'status': 'pass' if all(s['status'] == 'pass' for s in suites) and not missing_cases and not unexpected_cases else 'fail',
              'scope': 'Small synthetic expected-value oracles only; not production applications, UI, concurrency, or user outcomes.'}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if args.write_reports:
        (ROOT / 'validation' / 'all-examples-results.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(output['status'] != 'pass')


if __name__ == '__main__':
    main()
