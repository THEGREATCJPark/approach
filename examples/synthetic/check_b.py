#!/usr/bin/env python3
"""Independent small-fixture checks; no production application is imported.

The expected values were calculated in the case cards before this checker.
No statistical inference, browser testing, or real-user testing is claimed.
"""
import copy
import json
import platform
from collections import Counter
from decimal import Decimal
from graphlib import TopologicalSorter, CycleError
from itertools import product
from pathlib import Path


def prerequisite(rows, change):
    done = change.get('done')
    if done is None:
        return 'unknown'
    if change.get('cycle'):
        rows[0]['requires'] = ['finish']
    if change.get('reverse'):
        rows.reverse()
    graph = {r['id']: set(r['requires']) for r in rows}
    if any(not v <= graph.keys() for v in graph.values()):
        return 'invalid_reference'
    try:
        list(TopologicalSorter(graph).static_order())
    except CycleError:
        return 'invalid_cycle'
    return sorted(k for k, v in graph.items() if k not in done and v <= set(done))


def diagnostic(rows, change):
    if 'only' in change:
        rows = [{'response_id': str(i), 'concept': 'x', 'score': x} for i, x in enumerate(change['only'])]
    if change.get('conflict'):
        rows.append(dict(rows[0], score=0))
    if change.get('duplicate'):
        rows.append(rows[0].copy())
    unique = {}
    for r in rows:
        key = r['response_id']
        if key in unique and unique[key] != r:
            return 'invalid'
        unique[key] = r
    result = {}
    for concept in sorted({r['concept'] for r in rows}):
        scores = [r['score'] for r in unique.values() if r['concept'] == concept and r['score'] is not None]
        result[concept] = 'unknown' if len(scores) < 2 else ('ready' if 4 * sum(scores) >= 3 * len(scores) else 'practice')
    return result


def monitor(rows, change):
    if 'values' in change:
        rows = [{'slot': i, 'temp_c': x} for i, x in enumerate(change['values'])]
    if change.get('conflict'):
        rows.append(dict(rows[0], temp_c=7))
    if change.get('reverse'):
        rows.reverse()
    slots = {}
    for r in rows:
        if r['slot'] in slots and slots[r['slot']] != r['temp_c']:
            return 'invalid'
        slots[r['slot']] = r['temp_c']
    counts = Counter('unknown' if x is None else 'alarm' if x > 8 else 'normal' for x in slots.values())
    return {k: counts[k] for k in ('normal', 'alarm', 'unknown')}


def stratified(rows, change):
    if change.get('zero'):
        rows[0]['total'] = 0
        rows[0]['rework'] = 0
    if change.get('missing'):
        rows[3]['rework'] = None
    if change.get('invalid'):
        rows[0]['rework'] = 21
    if change.get('same_mix'):
        rows[2].update(total=20, rework=3)
        rows[3].update(total=80, rework=28)
    if change.get('reverse'):
        rows.reverse()
    cells = {(r['period'], r['type']): r for r in rows if r['period'] != 'weight'}
    if any(r['rework'] is None or r['total'] is None or r['total'] == 0 for r in cells.values()):
        return 'unknown'
    if any(r['rework'] < 0 or r['rework'] > r['total'] for r in cells.values()):
        return 'invalid'
    weights = {r['type']: Decimal(str(r['weight'])) for r in rows if r['period'] == 'weight'}
    result = {}
    for period in ('before', 'after'):
        sample = [r for (p, _), r in cells.items() if p == period]
        result['raw_' + period] = sum(r['rework'] for r in sample) / sum(r['total'] for r in sample)
    result['standard_after'] = float(sum(w * Decimal(cells['after', t]['rework']) / Decimal(cells['after', t]['total']) for t, w in weights.items()))
    return result


def rotation(rows, change):
    activities = [r for r in rows if r['kind'] == 'activity']
    if change.get('missing_cost'):
        return 'unknown'
    if change.get('reverse'):
        activities.reverse()
    costs = {r['id']: r['cost'] for r in activities}
    budget = change.get('budget', 15)
    fixed = change.get('fixed', 'B')
    feasible = [(sum(costs[x] for x in p), p) for p in product(costs, repeat=3)
                if p[1] == fixed and p[0] != p[1] and p[1] != p[2] and sum(costs[x] for x in p) <= budget]
    if not feasible:
        return 'infeasible'
    cost, plan = min(feasible)
    return {'plan': list(plan), 'cost': cost}


def order(row, change):
    row.update({k: v for k, v in change.items() if k != 'repeat'})
    fields = ('demand', 'safety', 'on_hand', 'reserved', 'timely_inbound', 'late_inbound', 'pack')
    if any(row[k] is None for k in fields):
        return 'unknown'
    if row['reserved'] > row['on_hand'] or row['pack'] <= 0 or any(row[k] < 0 for k in fields):
        return 'invalid'
    net = max(0, row['demand'] + row['safety'] - row['on_hand'] + row['reserved'] - row['timely_inbound'])
    packs = (net + row['pack'] - 1) // row['pack']
    ordered = packs * row['pack']
    return {'net': net, 'packs': packs, 'order': ordered, 'surplus': ordered - net}


def approval(_rows, change):
    amount, evidence = change['amount'], change['evidence']
    if amount is not None and amount < 0:
        return 'invalid'
    if amount is None or evidence is None:
        return 'unknown'
    if evidence is False:
        return 'need_evidence'
    return 'staff' if amount <= 100 else 'manager'


def transition(rows, change):
    rows = change.get('events', rows)
    if change.get('duplicate'):
        rows.insert(1, rows[0].copy())
    state = 'draft'
    seen = {}
    rules = {('draft', 'submit'): 'submitted', ('submitted', 'reject'): 'rejected',
             ('rejected', 'edit'): 'draft', ('submitted', 'approve'): 'approved'}
    for r in rows:
        key, action = r['event_id'], r['action']
        if action is None:
            return 'unknown'
        if key in seen:
            if seen[key] != action:
                return 'conflict'
            continue
        if (state, action) not in rules:
            return 'invalid_transition'
        state = rules[state, action]
        seen[key] = action
    return {'state': state, 'applied': len(seen)}


def gates(rows, change):
    if change.get('tie'):
        rows[3]['cost'] = 12
    if change.get('all_unknown'):
        for r in rows:
            r['strength'] = r['archival'] = None
    if change.get('bad_cost'):
        rows[0]['cost'] = -1
    if change.get('approve_m3'):
        rows[2]['archival'] = True
    if change.get('reverse'):
        rows.reverse()
    if any(r['cost'] < 0 for r in rows):
        return 'invalid'
    groups = {'pass': [], 'fail': [], 'unknown': []}
    for r in rows:
        values = [r['strength'], r['archival']]
        status = 'fail' if False in values else 'unknown' if None in values else 'pass'
        groups[status].append(r)
    eligible = groups['pass']
    return {'selected': min(eligible, key=lambda r: (r['cost'], r['id']))['id'] if eligible else None,
            **{k: len(v) for k, v in groups.items()}}


def interval(_rows, change):
    lower, upper = change['lower'], change['upper']
    if lower is None or upper is None:
        return 'unknown'
    lower, upper = Decimal(str(lower)), Decimal(str(upper))
    if lower > upper:
        return 'invalid'
    return 'within_margin' if -Decimal('0.5') < lower <= upper < Decimal('0.5') else 'not_demonstrated'


FUNCTIONS = dict(zip(['prerequisite-ready', 'concept-diagnostic', 'missing-versus-alarm', 'stratified-rate',
                      'rotation-budget', 'pack-order', 'evidence-approval', 'resubmission-state',
                      'mandatory-gates', 'equivalence-interval'],
                     [prerequisite, diagnostic, monitor, stratified, rotation, order, approval, transition, gates, interval]))


def main():
    fixtures = json.loads(Path(__file__).with_name('fixtures_b.json').read_text())
    records = []
    for case_id, data in fixtures.items():
        for test in data['tests']:
            actual = FUNCTIONS[case_id](copy.deepcopy(data['fixture']), copy.deepcopy(test['input']))
            # A repeated calculation must be pure with respect to the source fixture.
            if test['input'].get('repeat'):
                assert actual == FUNCTIONS[case_id](copy.deepcopy(data['fixture']), copy.deepcopy(test['input']))
            records.append({'case': case_id, **test, 'actual': actual,
                            'status': 'pass' if actual == test['expected'] else 'fail'})
    report = {'python': platform.python_version(), 'kind': 'independent_fixture_calculation',
              'case_count': len(fixtures), 'test_count': len(records), 'passed': sum(r['status'] == 'pass' for r in records),
              'limitations': ['No production application imported', 'No user study', 'No confidence interval estimation', 'No concurrent database test'],
              'results': records}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    assert report['passed'] == report['test_count'], 'fixture mismatch'


if __name__ == '__main__':
    main()
