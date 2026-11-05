#!/usr/bin/env python3
"""Verify 54 independently specified synthetic expectations, without an app or network."""
import json
import platform
from collections import defaultdict, deque
from fractions import Fraction
from itertools import product
from pathlib import Path

FIXTURES = Path(__file__).with_name('expansion_c.json')

def cold_start(x):
    if x['comparable'] is not True:return 'unknown'
    return [r[0] for r in sorted(x['items'],key=lambda r:(-Fraction(r[2]+1,r[1]+2),r[0]))]

def attribute_distance(x):
    if any(v is None for v in x['target']+x['scales']) or any(v is None for r in x['items'] for v in r):return 'unknown'
    if any(v<=0 for v in x['scales']):return 'invalid_scale'
    return [r[0] for r in sorted(x['items'],key=lambda r:(sum(abs(Fraction(str(v))-Fraction(str(t)))/Fraction(str(s)) for v,t,s in zip(r[1:],x['target'],x['scales'])),r[0]))]

def restriction(x):
    if x['banned'] is None:return 'unknown'
    result={}
    for id,components,complete in x['items']:
        result[id]='unknown' if components is None else 'excluded' if set(components)&set(x['banned']) else 'eligible' if complete is True else 'unknown'
    return result

def cooldown(x):
    rows=[r for r in x['items'] if r[2]=='never' or (r[2] is not None and x['today']-r[2]>=x['cooldown'])]
    return dict(eligible=[r[0] for r in sorted(rows,key=lambda r:(-r[1],r[0]))],unknown=sorted(r[0] for r in x['items'] if r[2] is None))

def explanation(x):
    if any(v is None for v in x['features'].values()) or any(x['weights'].get(k) is None for k in x['features']):return 'unknown'
    contributions={k:v*x['weights'][k] for k,v in x['features'].items()}
    return dict(total=sum(contributions.values()),contributions=contributions)

def unlabeled(x):
    if x['eligible'] is None:return 'unknown'
    unique=set(x['recommendations'])
    return dict(duplicates=len(x['recommendations'])-len(unique),invalid=sorted(unique-set(x['eligible'])),unfilled=max(0,x['requested']-len(unique & set(x['eligible']))))

def bins(x):
    boxes=list(x['boxes'].values());caps=x['capacities']
    if any(v is None for v in boxes+caps):return 'unknown'
    for assignment in product(range(len(caps)),repeat=len(boxes)):
        loads=[sum(size for size,vehicle in zip(boxes,assignment) if vehicle==j) for j in range(len(caps))]
        if all(load<=cap for load,cap in zip(loads,caps)):return True
    return False

def windows(x):
    if x['start'] is None or any(v is None for row in x['stops'] for v in row):return 'unknown'
    now=x['start'];wait=0;feasible=True
    for id,travel,opening,closing,service in x['stops']:
        arrival=now+travel;begin=max(arrival,opening)
        wait+=begin-arrival;feasible=feasible and begin<=closing
        now=begin+service
    return dict(feasible=feasible,finish=now,wait=wait)

def depot(x):
    if any(v is None for id,values in x['depots'] for v in values):return 'unknown'
    worst,id=min((max(values),id) for id,values in x['depots'])
    return dict(id=id,worst=worst)

def clusters(x):
    if any(p is None for id,p in x['points']):return 'unknown'
    graph={id:set() for id,p in x['points']}
    for a,pa in x['points']:
        for b,pb in x['points']:
            if a!=b and abs(pa-pb)<=x['radius']:graph[a].add(b)
    remaining=set(graph);groups=[]
    while remaining:
        start=min(remaining);component={start};pending=[start]
        while pending:
            for neighbor in graph[pending.pop()]-component:
                component.add(neighbor);pending.append(neighbor)
        remaining-=component;groups.append(sorted(component))
    return sorted(groups)

def fair(x):
    users=x['users'];caps=x['capacity']
    if any(t is None for id,times in users for t in times):return 'unknown'
    for assignment in product(range(len(caps)),repeat=len(users)):
        if any(assignment.count(j)>cap for j,cap in enumerate(caps)):continue
        if all(times[j]<=x['cap'] for (id,times),j in zip(users,assignment)):return True
    return False

def ledger(x):
    if any(q is None for q in x['demand'].values()):return 'unknown'
    quantities=defaultdict(int)
    if any(request_id not in x['demand'] for allocation_id,request_id,qty in x['assignments']):return 'invalid_reference'
    if len({r[0] for r in x['assignments']})!=len(x['assignments']):return 'duplicate_id'
    if any(qty is None for allocation_id,request_id,qty in x['assignments']):return 'unknown'
    for allocation_id,request_id,qty in x['assignments']:quantities[request_id]+=qty
    return {id:dict(remaining=max(0,q-quantities[id]),over=max(0,quantities[id]-q)) for id,q in x['demand'].items()}

def types(x):
    if any(kind is None for a,b,kind in x['edges'] if a==x['source']):return 'unknown'
    return sorted({b for a,b,kind in x['edges'] if a==x['source'] and kind==x['type']})

def removal(x):
    if x['complete'] is not True:return 'unknown'
    def reachable(edges):
        seen={x['source']};queue=deque(seen)
        while queue:
            node=queue.popleft()
            for a,b in edges:
                if a==node and b not in seen:seen.add(b);queue.append(b)
        return x['target'] in seen
    return reachable(x['edges']) and not reachable([(a,b) for a,b in x['edges'] if x['remove'] not in (a,b)])

def alternatives(x):
    values=[]
    for group in x['groups']:
        values.append(True if True in group else None if None in group else False)
    if False in values:return 'unavailable'
    return 'unknown' if None in values else 'available'

def sensitivity(x):
    if x['delta'] is None or any(v is None for v in x['coefficients']):return 'unknown'
    value=Fraction(x['delta'])
    for coefficient in x['coefficients']:value*=Fraction(coefficient)
    # Tests use integral results; preserve exact rational representation otherwise.
    return str(value.numerator) if value.denominator==1 else str(value)

def validity(x):
    relevant=[e for e in x['evidence'] if e['relation']==x['relation']]
    if any(e[k] is None for e in relevant for k in ('from_day','to_day','source')):
        return dict(status='unknown',support=[],refute=[])
    active=[e for e in relevant if e['from_day']<=x['day']<e['to_day']]
    support=sorted(e['id'] for e in active if e['position']=='support')
    refute=sorted(e['id'] for e in active if e['position']=='refute')
    status='conflict' if support and refute else 'supported' if support else 'refuted' if refute else 'unknown'
    return dict(status=status,support=support,refute=refute)

def multigraph(x):
    rows=x['edges']
    if any(v is None for row in rows for v in row):return 'unknown'
    if len({row[0] for row in rows})!=len(rows):return 'duplicate_id'
    return dict(nodes=len({n for id,a,b,kind in rows for n in (a,b)}),visual_edges=len({(a,b) for id,a,b,kind in rows}),relations=len(rows))

ORACLES={
'ranking-cold-start':cold_start,'ranking-attribute-distance':attribute_distance,
'ranking-restriction-evidence':restriction,'ranking-repeat-cooldown':cooldown,
'ranking-score-explanation':explanation,'ranking-without-labels':unlabeled,
'mobility-indivisible-capacity':bins,'mobility-window-wait':windows,
'mobility-depot-minimax':depot,'mobility-demand-clusters':clusters,
'mobility-fair-travel-cap':fair,'mobility-unserved-ledger':ledger,
'dependency-relation-types':types,'dependency-removal-bottleneck':removal,
'dependency-alternative-supply':alternatives,'dependency-coefficient-sensitivity':sensitivity,
'dependency-evidence-validity':validity,'dependency-multigraph-display':multigraph}

def main():
    fixtures=json.loads(FIXTURES.read_text());results=[]
    for case,tests in fixtures.items():
        for test in tests:
            actual=ORACLES[case](test['input'])
            results.append(dict(case=case,kind=test['kind'],input=test['input'],expected=test['expected'],actual=actual,basis=test['basis'],status='pass' if actual==test['expected'] else 'fail'))
    output=dict(environment=platform.python_version(),cases=len(fixtures),checks=len(results),scope='synthetic expected-value oracles; no application, concurrency, or user-effect validation',results=results)
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0 if all(r['status']=='pass' for r in results) else 1

if __name__=='__main__':raise SystemExit(main())
