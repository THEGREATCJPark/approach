#!/usr/bin/env python3
"""Independent finite-fixture arithmetic; no app imports, network or production claims."""
import itertools
import json
from pathlib import Path

def contains_null(x):
    if x is None:
        return True
    if isinstance(x, dict):
        return any(contains_null(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(contains_null(v) for v in x)
    return False

def oracle(case, x):
    # Fixtures stay within each card's explicit input contract.
    if contains_null(x):
        return 'unknown'
    if case == 'sightline-barrier':
        return 'blocked' if any(0 < b <= x['target_x'] for b in x['barrier_x']) else 'visible'
    if case == 'minimum-cover-cost':
        required = set(x['required'])
        feasible_costs = []
        for n in range(len(x['candidates']) + 1):
            for subset in itertools.combinations(x['candidates'], n):
                covered = set().union(*(set(c[2]) for c in subset))
                if required <= covered:
                    feasible_costs.append(sum(c[1] for c in subset))
        return min(feasible_costs) if feasible_costs else 'infeasible'
    if case == 'priority-zone-weight':
        if any(z not in x['weights'] for _, zones in x['candidates'] for z in zones):
            return 'unknown'
        scores = [(sum(x['weights'][z] for z in set(zones)), key) for key, zones in x['candidates']]
        return sorted(scores, key=lambda r: (-r[0], r[1]))[0][1]
    if case == 'installation-exclusion':
        px, py = x['point']
        a, b, c, d = x['forbidden']
        return 'forbidden' if a <= px <= c and b <= py <= d else 'allowed'
    if case == 'drawing-unit-check':
        factors = {'mm': 1, 'cm': 10, 'm': 1000}
        if x['unit'] not in factors:
            return 'unknown'
        difference = abs(x['drawing_length'] * factors[x['unit']] - x['measured_mm'])
        return 'match' if difference <= x['tolerance_mm'] else 'mismatch'
    if case == 'radial-monitor-range':
        cx, cy = x['center']
        return sum((px-cx)**2 + (py-cy)**2 <= x['radius_m']**2 for _, px, py in x['targets'])
    if case == 'survival-resource-tick':
        return x['oxygen'] if x['paused'] else max(0, x['oxygen'] - x['rate'] * x['elapsed_s'])
    if case == 'bot-grid-step':
        a, b = x['pos']
        tx, ty = x['target']
        current = abs(a-tx) + abs(b-ty)
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            candidate = [a+dx, b+dy]
            if candidate not in x['blocked'] and abs(candidate[0]-tx) + abs(candidate[1]-ty) < current:
                return candidate
        return [a,b]
    if case == 'shrinking-safe-zone':
        radius = max(x['min_radius_m'], x['initial_radius_m'] - x['shrink_m_per_s'] * x['elapsed_s'])
        return 'safe' if x['distance_m'] <= radius else 'outside'
    if case == 'simultaneous-outcome':
        if not x['batch_complete']:
            return 'pending'
        eligible = [(name, finish) for name, finish in x['arrivals'] if finish <= x['deadline_s'] + x['grace_s']]
        if not eligible:
            return []
        fastest = min(finish for _, finish in eligible)
        return sorted(name for name, finish in eligible if finish == fastest)
    if case == 'score-event-replay':
        originals, reversed_ids, seen = {}, set(), set()
        total = 0
        for key, delta, reverse in x['events']:
            if key in seen:
                return 'conflict'
            seen.add(key)
            if reverse:
                if reverse not in originals:
                    return 'unknown'
                if reverse in reversed_ids or delta != -originals[reverse]:
                    return 'conflict'
                reversed_ids.add(reverse)
            else:
                if delta <= 0:
                    return 'conflict'
                originals[key] = delta
            total += delta
        return total
    if case == 'multiplayer-scope-gate':
        if x['devices'] == 1 or not x['shared_state']:
            return 'local'
        return {'allowed':'server_needed', 'forbidden':'out_of_scope', 'unknown':'unknown'}[x['server_permission']]
    if case == 'review-execution-separation':
        if x['decision'] == 'approved':
            return 'completed' if x['receipt'] else 'ready'
        if x['decision'] == 'rejected':
            return 'conflict' if x['receipt'] else 'rejected'
        return 'pending'
    if case == 'policy-reason-priority':
        if not x['authorized']:
            return 'AUTH'
        if x['age_days'] > x['limit_days']:
            return 'EXPIRED'
        if x['quantity'] > x['max_quantity']:
            return 'LIMIT'
        return 'PASS'
    if case == 'evidence-manual-review':
        if not set(x['required']) <= set(x['present']):
            return 'manual_missing'
        if x['age_days'] > x['max_age_days']:
            return 'manual_stale'
        if x['defect']:
            return 'manual_defect'
        return 'ready_for_decision'
    if case == 'idempotent-fulfillment':
        old = x['history'].get(x['key'])
        if old is None:
            return 'new'
        if old[0] != x['quantity']:
            return 'conflict'
        if old[1] == 'done':
            return 'replay_done'
        if old[1] == 'pending':
            return 'in_progress'
        return 'retry_allowed' if old[2] == 'absent' else 'manual_review'
    if case == 'valuation-time-alignment':
        if x['quantity_time'] != x['price_time']:
            return 'stale'
        return x['quantity'] * x['unit_price']
    if case == 'ledger-chain-audit':
        balance = x['opening']
        for expected_seq, (seq, delta, after) in enumerate(sorted(x['entries']), 1):
            balance += delta
            if seq != expected_seq or after != balance or balance < 0:
                return 'conflict'
        return balance
    raise ValueError('unknown case: ' + case)

def main():
    fixtures = json.loads(Path(__file__).with_name('expansion_e.json').read_text())
    results = []
    for case, tests in fixtures.items():
        for test in tests:
            actual = oracle(case, test['input'])
            results.append({'case':case, 'type':test['type'], 'input':test['input'], 'expected':test['expected'], 'basis':test.get('basis',test['rationale']), 'actual':actual, 'status':'pass' if actual == test['expected'] else 'fail'})
    print(json.dumps({'case_count':len(fixtures),'test_count':len(results),'results':results}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r['status']=='pass' for r in results) else 1)

if __name__ == '__main__':
    main()
