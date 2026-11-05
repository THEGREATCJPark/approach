"""Independent, small fixture oracles; not a production app or UI test.
Run from any directory: python examples/synthetic/check_a.py
Expected results are hand-derived in cards and stored separately in JSON.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from itertools import combinations
from fractions import Fraction

HERE = Path(__file__).resolve().parent


def open_day_rate(x):
    if 'groups' in x:
        return {key: float(Fraction(v, d)) for key, v, d in x['groups']}
    v, d = x['visits'], x['days']
    if v is None or d is None or not x['complete']:
        return 'unknown'
    if v < 0 or d < 0 or (d == 0 and v != 0):
        return 'invalid'
    return 'undefined' if d == 0 else float(Fraction(v, d))


def counter_reset(x):
    if 'readings' in x:
        ordered = sorted(x['readings'])
        x = {'before': ordered[0][1], 'after': ordered[-1][1], 'reset': x['reset']}
    if x['before'] is None or x['after'] is None:
        return 'unknown'
    if x['reset'] or x['after'] < x['before']:
        return 'reset_unknown'
    return x['after'] - x['before']


def repair_slack(x):
    if 'tickets' in x:
        return [r[0] for r in sorted(x['tickets'], key=lambda r: (r[1]-r[2],r[0]))]
    if x['safety']:
        return 'escalate'
    if x['work'] is None or x['due'] is None:
        return 'estimate_required'
    return x['due'] - x['work']


def policy_evidence(x):
    if x['date'] is None:
        return 'unknown'
    day = datetime.fromisoformat(x['date'])
    found = [i for i, a, b in x['docs']
             if datetime.fromisoformat(a) <= day < datetime.fromisoformat(b)]
    return 'not_found' if not found else found[0] if len(found) == 1 else 'conflict'


def claim_ledger(x):
    if 'claims' in x:
        return {key: 'supported' if a == b else 'contradicted' for key,a,b in x['claims']}
    if not x['same_meaning']:
        return 'semantic_review'
    if x['evidence'] is None or x['claim'] is None:
        return 'unverified'
    return 'supported' if x['claim'] == x['evidence'] else 'contradicted'


def rater_disagreement(x):
    valid = [(a, b) for a, b in x['pairs'] if a is not None and b is not None]
    return [sum(a == b for a, b in valid), len(valid)] if valid else 'unknown'


def deadline_offset(x):
    a, b = datetime.fromisoformat(x['at']), datetime.fromisoformat(x['end'])
    if a.utcoffset() is None or b.utcoffset() is None:
        return 'unknown'
    result = 'eligible' if a <= b else 'late'
    return [result for _ in range(x['repeat'])] if 'repeat' in x else result


def seat_retry(x):
    requests, people, accepted, waiting = {}, set(), [], []
    if x['cap'] < 0:
        return 'invalid'
    for request, person in x['requests']:
        if request is None or person is None:
            return 'invalid'
        if request in requests and requests[request] != person:
            return 'conflict'
        requests[request] = person
        if person in people:
            continue
        people.add(person)
        (accepted if len(accepted) < x['cap'] else waiting).append(person)
    return [accepted, waiting]


def rectangle_union(x):
    # Independent discrete oracle for integer axis-aligned fixtures only.
    # Every unit cell contributes exactly one square metre.
    cells = set()
    for a, b, c, d in x['rects']:
        if None in (a, b, c, d):
            return 'unknown'
        if a > c or b > d:
            return 'invalid'
        cells.update((i, j) for i in range(a, c) for j in range(b, d))
    return len(cells)


def budget_cover(x):
    if x['budget'] < 0 or any(c < 0 for _, c, _ in x['candidates']):
        return 'invalid'
    if any(s is None for _, _, s in x['candidates']):
        return 'unknown'
    plans = []
    for size in range(len(x['candidates']) + 1):
        for rows in combinations(x['candidates'], size):
            cost = sum(r[1] for r in rows)
            if cost <= x['budget']:
                cover = set().union(*(set(r[2]) for r in rows))
                ids = sorted(r[0] for r in rows)
                plans.append((-len(cover), cost, ids))
    return min(plans)[2]


ORACLES = {f.__name__.replace('_', '-'): f for f in (
    open_day_rate, counter_reset, repair_slack, policy_evidence,
    claim_ledger, rater_disagreement, deadline_offset, seat_retry,
    rectangle_union, budget_cover)}


def main():
    records = []
    for case, oracle in ORACLES.items():
        for t in json.loads((HERE / (case + '.json')).read_text()):
            actual = oracle(t['input'])
            records.append({'case': case, 'kind': t['kind'], 'input': t['input'],
                            'expected': t['expected'], 'basis': t['basis'],
                            'actual': actual,
                            'status': 'pass' if actual == t['expected'] else 'fail'})
    report = {'python': sys.version.split()[0], 'kind': 'independent_fixture_oracle',
              'limitations': 'No production app, concurrency, natural-language semantics, or user outcome tested.',
              'cases': len(ORACLES), 'checks': len(records), 'results': records}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(r['status'] == 'pass' for r in records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
