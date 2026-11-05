#!/usr/bin/env python3
"""Independent small synthetic calculations, not production implementations."""
import json
import platform
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction
from collections import Counter
from datetime import date


def solve(case, x):
    # Missingness anywhere in these deliberately tiny fixtures is unknown.
    def missing(v):
        if v is None:
            return True
        if isinstance(v, dict):
            return any(missing(t) for t in v.values())
        if isinstance(v, list):
            return any(missing(t) for t in v)
        return False
    if case == 'policy-effective-version':
        if any(x[k] is None for k in ['filed', 'decided', 'cutoff']):
            return 'unknown'
        if x['filed'] > x['decided'] or x['decided'] < x['cutoff']:
            return 'invalid'
        if x['filed'] >= x['cutoff']:
            return dict(version='v2', reason='filed_under_new')
        if x['retroactive'] is None or x['locked_version'] is None:
            return 'unknown'
        if x['locked_version'] != 'v1':
            return 'invalid'
        return dict(version='v2', reason='explicit_retroactive') if x['retroactive'] else dict(version='v1', reason='kept_at_filing')
    if missing(x):
        return 'unknown'
    if case == 'event-eligibility':
        return 'eligible' if x['required'] == x['certificate'] and date.fromisoformat(x['expires']) >= date.fromisoformat(x['event']) else 'not_eligible'
    if case == 'event-checkin':
        statuses = []
        for i, ticket in enumerate(x['scans']):
            statuses.append('unknown_ticket' if ticket not in x['registered'] else 'duplicate' if ticket in x['scans'][:i] else 'checked_in')
        return dict(unique=len(set(x['scans']) & set(x['registered'])), statuses=statuses)
    if case == 'event-reward-ledger':
        keys = {row[0] for row in x['rows']}
        quantities = [{n for key, n in x['rows'] if key == k} for k in keys]
        if any(len(q) != 1 for q in quantities):
            return 'conflict'
        return sum(next(iter(q)) for q in quantities)
    if case == 'event-cancel-priority':
        queue = x['queue'].copy()
        for action, person in x['events']:
            if action == 'cancel':
                queue = [p for p in queue if p != person]
            elif action == 'join' and person not in queue:
                queue += [person]
        return queue
    if case == 'event-rehearsal-capacity':
        # Count occupancy at each breakpoint directly, independently of sweep events.
        points = {v for pair in x['intervals'] for v in pair}
        peak = max((sum(a <= t < b for a, b in x['intervals']) for t in points), default=0)
        return dict(peak=peak, over=peak > x['cap'])
    if case == 'event-exception-expiry':
        return 'accepted' if x['event'] == x['scope'] and x['approver'] in x['authorized'] and x['now'] < x['expires'] else 'denied'
    if case == 'policy-delegation':
        return 'delegated' if x['start'] <= x['day'] <= x['end'] and x['amount'] <= x['owner_limit'] and x['amount'] <= x['delegate_limit'] else 'original_owner'
    if case == 'policy-duplicate-claim':
        rows = sorted(set(tuple(r) for r in x['rows']))
        return sorted([sorted([a[0], b[0]]) for a,b in combinations(rows,2) if a[0] != b[0] and a[1:] == b[1:]])
    if case == 'policy-next-action':
        if x['role'] not in ['applicant','reviewer'] or x['state'] not in ['draft','submitted','approved']:
            return 'invalid'
        return {('applicant','draft'):['edit','submit'],('applicant','submitted'):['withdraw'],('reviewer','submitted'):['approve','reject']}.get((x['role'],x['state']),[])
    if case == 'policy-separation-duties':
        if x['creator'] == x['approver']:
            return 'manual_escalation'
        return 'eligible' if x['approver'] in x['authorized'] else 'denied'
    if case == 'policy-receipt-allocation':
        if len({k for k,_ in x['rows']}) != len(x['rows']):
            return 'invalid'
        remaining = x['total'] - sum(n for _,n in x['rows'])
        return dict(state='partial' if remaining > 0 else 'complete' if remaining == 0 else 'overallocated', remaining=remaining)
    if case == 'planning-resource-blend':
        choices = []
        for a,b in product(range(x['max_each']+1), repeat=2):
            cost = a*x['a'][0]+b*x['b'][0]
            units = a*x['a'][1]+b*x['b'][1]
            if units >= x['required']:
                choices.append((cost,a+b,a,b,units))
        if not choices:
            return 'infeasible'
        cost,_,a,b,units = min(choices)
        return dict(a=a,b=b,cost=cost,units=units)
    if case == 'planning-repeat-gap':
        # Pair enumeration, rather than the suggested last-seen implementation.
        positions = {value:[i for i,v in enumerate(x['schedule']) if v == value] for value in set(x['schedule'])}
        return sorted([[a,b] for ps in positions.values() for a,b in zip(ps,ps[1:]) if b-a < x['min_gap']])
    if case == 'planning-substitute-stock':
        if not x['approved']:
            return 'blocked'
        q = Fraction(x['need'])/(Fraction(x['replacement_units'])*Fraction(x['yield_']))
        required = -(-q.numerator//q.denominator)
        return dict(required=required,shortage=max(0,required-x['stock']))
    if case == 'planning-outage-repair':
        locations = sorted(k for k in x['capacity'] if k not in x['closed'])
        plans = []
        for p in product(locations,repeat=len(x['assignments'])):
            counts = Counter(p)
            if all(counts[k] <= x['capacity'][k] for k in counts):
                plans.append((sum(a!=b for a,b in zip(p,x['assignments'])),list(p)))
        if not plans:
            return 'infeasible'
        moves,assignment = min(plans)
        return dict(moves=moves,assignment=assignment)
    if case == 'planning-infeasible-witness':
        shortage=max(0,x['demand']-sum(x['capacities']))
        return dict(state='infeasible' if shortage else 'capacity_sufficient',shortage=shortage)
    if case == 'planning-service-coverage':
        # Independent discrete-minute oracle for the integer-minute contract.
        a,b=x['window']
        uncovered = [t for t in range(a,b) if not any(s <= t < e for s,e in x['shifts'])]
        gaps=[]
        for t in uncovered:
            if gaps and gaps[-1][1]==t:
                gaps[-1][1]=t+1
            else:
                gaps.append([t,t+1])
        return dict(gaps=gaps,minutes=len(uncovered))
    raise ValueError(case)


def main():
    fixture=json.loads(Path(__file__).with_name('expansion_d.json').read_text())
    results=[]
    for case, tests in fixture.items():
        for t in tests:
            actual=solve(case,t['input'])
            results.append(dict(case=case,kind=t['kind'],input=t['input'],expected=t['expected'],basis=t['basis'],actual=actual,status='pass' if actual==t['expected'] else 'fail'))
    output=dict(environment=platform.python_version(),scope='independent synthetic oracles; no production app, authentication, concurrency or user outcome validation',case_count=len(fixture),test_count=len(results),results=results)
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0 if all(x['status']=='pass' for x in results) else 1

if __name__=='__main__':
    raise SystemExit(main())
