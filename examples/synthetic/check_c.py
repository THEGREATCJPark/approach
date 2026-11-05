#!/usr/bin/env python3
"""Small independent oracles for ten synthetic cases; no production app is tested."""
import json
import platform
from collections import deque
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
catalog = ROOT / 'catalog' / 'cases.json'
raw = json.loads(catalog.read_text())
if isinstance(raw, dict):
    raw = raw['cases']
CASES = {x['id']: x for x in raw}
results = []

def check(case, label, actual, expected):
    status = 'pass' if actual == expected else 'fail'
    results.append(dict(case=case, check=label, actual=actual, expected=expected, status=status))
    if status == 'fail':
        raise AssertionError(results[-1])

def fixture(case):
    # Read the card's displayed JSON fixture if catalogs omit large fixtures.
    entry = CASES[case]
    if 'fixture' in entry:
        return entry['fixture']
    body = (ROOT / entry['path']).read_text()
    blocks = body.split('```json\n')
    return json.loads(blocks[2].split('```')[0])

# One oracle check per designed acceptance row (60 rows). Small pure models only.
# These models validate documented expectations, not app behavior or DB concurrency.

def run_six(cid, actuals):
    for row, actual in zip(CASES[cid]['tests'], actuals):
        # Original human-readable expected text remains in the catalog/card.
        check(cid, row['kind'], actual[0], actual[1])

cid='ranking-availability';rows=fixture(cid)
def ranked(rows,k=2):
    eligible=[r for r in rows if r['available'] is not None and r['available']>0 and r['restricted'] is False]
    return [r['id'] for r in sorted(eligible,key=lambda r:(-len(set(r['tags'])&{'빛','물'}),r['id']))][:k]
run_six(cid,[((ranked(rows),[len(set(r['tags'])&{'빛','물'}) for r in sorted(rows,key=lambda r:r['id']) if r['id'] in ranked(rows)]),(['A','D'],[2,0])),(ranked(rows,0),[]),
    ([r['id'] for r in rows if r['available'] is None],['E']),
    (ranked([{**r,'restricted':True} for r in rows]),[]),(ranked(rows[::-1]),['A','D']),
    (ranked(rows+[dict(id='F',available=1,restricted=False,tags=['물'])]),['A','F'])])

cid='ranking-diversity';rows=fixture(cid)
def selection(rows,k,cap):
    if len({r['id'] for r in rows})!=len(rows):return 'duplicate_id'
    eligible=[r for r in rows if r['topic'] is not None]
    choices=[]
    for n in range(k+1):
        for group in combinations(eligible,n):
            if all(sum(s['topic']==r['topic'] for s in group)<=cap for r in group):
                choices.append((n,sum(r['score'] for r in group),sorted(r['id'] for r in group)))
    n,score,ids=max(choices)
    return dict(ids=ids,score=score,unfilled=k-n)
run_six(cid,[(selection(rows,3,2),dict(ids=['A','B','D'],score=23,unfilled=0)),
(selection(rows,3,1),dict(ids=['A','D','E'],score=20,unfilled=0)),
(selection([{**r,'topic':None if r['id']=='D' else r['topic']} for r in rows],3,2),dict(ids=['A','B','E'],score=22,unfilled=0)),
(selection(rows,4,1),dict(ids=['A','D','E'],score=20,unfilled=1)),
(selection(rows+[rows[0]],3,2),'duplicate_id'),
(selection(rows+[dict(id='F',topic='공예',score=10)],3,2),dict(ids=['A','B','F'],score=27,unfilled=0))])

cid='mobility-tour';matrix=fixture(cid)['times']
def tour(m):
    if any(v is None for row in m.values() for v in row.values()):return 'unknown'
    costs=[]
    for p in permutations([n for n in m if n!='O']):
        route=('O',)+p+('O',)
        edges=[m[a][b] for a,b in zip(route,route[1:])]
        if all(e!='blocked' for e in edges):costs.append(sum(edges))
    return min(costs) if costs else 'infeasible'
unknown={a:{b:(None if (a,b)==('O','A') else v) for b,v in row.items()} for a,row in matrix.items()}
blocked={a:{b:('blocked' if a!=b and 'A' in (a,b) else v) for b,v in row.items()} for a,row in matrix.items()}
changed={a:{b:(1 if {a,b}=={'O','C'} else v) for b,v in row.items()} for a,row in matrix.items()}
run_six(cid,[(tour(matrix),16),(tour({'O':{'O':0}}),0),(tour(unknown),'unknown'),
(tour(blocked),'infeasible'),(tour(dict(reversed(list(matrix.items())))),16),(tour(changed),10)])

cid='mobility-departure';rows=fixture(cid)
def departures(rows):
    if any(r[k] is None for r in rows for k in ('offset','open','close')):return 'unknown'
    lo=max(r['open']-r['offset'] for r in rows);hi=min(r['close']-r['offset'] for r in rows)
    return [lo,hi] if lo<=hi else 'infeasible'
run_six(cid,[(departures(rows),[540,550]),([550+r['offset'] for r in rows],[560,575,590]),
(departures([{**r,'offset':None if r['id']=='B' else r['offset']} for r in rows]),'unknown'),
(departures([{**r,'open':600 if r['id']=='C' else r['open'],'close':600 if r['id']=='C' else r['close']} for r in rows]),'infeasible'),
(departures(rows[::-1]),[540,550]),(departures([{**r,'open':r['open']+60,'close':r['close']+60} for r in rows]),[600,610])])

cid='interactive-collision';f=fixture(cid)
def move(events,initial=(1,1,3)):
    x,y,energy=initial;seen=set();reason='none'
    for e in events:
        if e['dx'] is None or e['dy'] is None or abs(e['dx'])+abs(e['dy'])!=1:
            reason='invalid';continue
        if e['id'] in seen:reason='duplicate';continue
        seen.add(e['id']);nx,ny=x+e['dx'],y+e['dy']
        if not(0<=nx<4 and 0<=ny<3):reason='boundary';continue
        if [nx,ny] in f['board']['walls']:reason='wall';continue
        if energy<=0:reason='exhausted';continue
        x,y,energy=nx,ny,energy-1;reason='moved'
    return [x,y,energy,reason]
run_six(cid,[(move(f['events']),[1,2,2,'duplicate']),
(move([dict(id='l',dx=-1,dy=0)],(0,0,3)),[0,0,3,'boundary']),
(move([dict(id='m',dx=None,dy=0)]),[1,1,3,'invalid']),
(move([dict(id='w',dx=1,dy=0)]),[1,1,3,'wall']),
(move([dict(id='d',dx=0,dy=1)]*2),[1,2,2,'duplicate']),
(move([dict(id='u',dx=0,dy=-1)]),[1,0,2,'moved'])])

cid='interactive-reset';f=fixture(cid)
def batch(events,state):
    hp=state['hp'].copy()
    relevant=[e for e in events if e['session']==state['session']]
    if any(e.get('tick') is None or e['amount']<0 for e in relevant):return hp,'invalid'
    if state['phase']!='running':return hp,state['phase']
    for p in hp:
        damage=sum(e['amount'] for e in {e['id']:e for e in relevant}.values() if e['player']==p)
        hp[p]=max(0,hp[p]-damage)
    alive=[p for p,h in hp.items() if h>0]
    return hp,'draw' if not alive else alive[0] if len(alive)==1 else 'running'
run_six(cid,[(batch(f['events'],f['state']),({'A':0,'B':0},'draw')),
(batch(f['events'][:1],f['state']),({'A':0,'B':2},'B')),
(batch([{**f['events'][0],'tick':None}],f['state']),({'A':2,'B':2},'invalid')),
(batch([{**f['events'][0],'amount':-1}],f['state']),({'A':2,'B':2},'invalid')),
(batch(f['events'][::-1],f['state']),({'A':0,'B':0},'draw')),
(batch(f['events'],f['restart']),({'A':2,'B':2},'ready'))])

cid='transaction-reservation';f=fixture(cid)
def reserve(requests,stock,fulfill=None):
    total,locked=stock['total'],stock['locked'];ledger={};statuses=[]
    for r in requests:
        if r['qty'] is None:statuses.append('needs_review');continue
        if r['id'] in ledger:
            old_qty,status=ledger[r['id']]
            statuses.append(status if old_qty==r['qty'] else 'payload_conflict');continue
        status='accepted' if 0<r['qty']<=total-locked else 'rejected'
        if status=='accepted':locked+=r['qty']
        ledger[r['id']]=(r['qty'],status);statuses.append(status)
    if fulfill is not None:
        qty,status=ledger[fulfill]
        if status!='accepted':raise ValueError('not reserved')
        total-=qty;locked-=qty
    return [total,locked,total-locked,statuses]
run_six(cid,[(reserve(f['requests'][:1],f['stock']),[7,5,2,['accepted']]),
(reserve([dict(id='b',qty=5)],f['stock']),[7,7,0,['accepted']]),
(reserve([dict(id='m',qty=None)],f['stock']),[7,2,5,['needs_review']]),
(reserve([dict(id='x',qty=3)],dict(total=7,locked=5)),[7,5,2,['rejected']]),
(reserve(f['requests'][:2],f['stock']),[7,5,2,['accepted','accepted']]),
(reserve(f['requests'][:1],f['stock'],fulfill='r1'),[4,2,2,['accepted']])])

cid='transaction-rounding';rows=fixture(cid)
def positive_half_up(v):return (2*v.numerator+v.denominator)//(2*v.denominator)
def settlement(rows):
    if len({r['line_id'] for r in rows})!=len(rows):return 'duplicate_id'
    if any(r['quantity'] is None or r['rate'] is None for r in rows):return 'unknown'
    if any(Fraction(r['quantity'])<0 or Fraction(r['rate'])<0 for r in rows):return 'invalid_negative'
    amounts=[Fraction(r['quantity'])*Fraction(r['rate']) for r in rows]
    rational=[positive_half_up(sum(amounts)),sum(positive_half_up(v) for v in amounts)]
    # Independently corroborate exact rational oracle with Decimal arithmetic.
    decimals=[Decimal(r['quantity'])*Decimal(r['rate']) for r in rows]
    decimal_result=[int(sum(decimals).quantize(Decimal('1'),rounding=ROUND_HALF_UP)),int(sum(v.quantize(Decimal('1'),rounding=ROUND_HALF_UP) for v in decimals))]
    if rational!=decimal_result:raise AssertionError('rational/Decimal mismatch')
    return [str(sum(amounts)),*rational]
run_six(cid,[(settlement(rows),['6',6,7]),(settlement(rows[:1]),['3/2',2,2]),
(settlement([{**rows[0],'quantity':None}]),'unknown'),
(settlement([{**rows[0],'quantity':'-0.1'}]),'invalid_negative'),
(settlement(rows+[rows[0]]),'duplicate_id'),(settlement([{**rows[0],'quantity':'0.124'}]),['186/125',1,1])])

cid='dependency-reachability';rows=fixture(cid)
def descendants(rows,start='P'):
    nodes={e[k] for e in rows for k in ('source','target')}
    if start not in nodes:return 'node_missing'
    seen={start};queue=deque([start]);unknown=set()
    while queue:
        n=queue.popleft()
        for e in rows:
            if e['source']!=n or e['type']!='required':continue
            if e['verified'] is None:unknown.add(e['target']);continue
            if e['verified'] is True and e['target'] not in seen:
                seen.add(e['target']);queue.append(e['target'])
    return sorted(seen-{start}),sorted(unknown)
def has_reachable_cycle(rows):
    graph={}
    for e in rows:
        if e['type']=='required' and e['verified'] is True:graph.setdefault(e['source'],set()).add(e['target'])
    def visit(n,trail):
        if n in trail:return True
        return any(visit(v,trail|{n}) for v in graph.get(n,()))
    return visit('P',set())
cyclic=rows+[dict(source='K',target='P',type='required',verified=True)]
run_six(cid,[(descendants(rows)[0],['K','S']),(descendants(rows,'Q'),'node_missing'),
(descendants(rows)[1],['Z']),((descendants(cyclic)[0],has_reachable_cycle(cyclic)),(['K','S'],True)),
(descendants(rows+[rows[0]])[0],['K','S']),
(descendants([{**r,'type':'required' if r['target']=='T' else r['type']} for r in rows])[0],['K','S','T'])])

cid='dependency-critical-path';rows=fixture(cid)
def completion(rows):
    if any(r['duration'] is None for r in rows):return 'unknown'
    tasks={r['id']:r for r in rows}
    def finish(node,stack=()):
        if node in stack:raise ValueError('cycle')
        r=tasks[node]
        return r['duration']+max((finish(p,stack+(node,)) for p in r['predecessors']),default=0)
    try:return max(finish(k) for k in tasks)
    except ValueError:return 'cycle'
def critical(rows):
    tasks={r['id']:r for r in rows}
    def paths(n):
        r=tasks[n]
        if not r['predecessors']:return [(r['duration'],[n])]
        return [(cost+r['duration'],path+[n]) for p in r['predecessors'] for cost,path in paths(p)]
    return max((v for n in tasks for v in paths(n)),key=lambda x:x[0])
run_six(cid,[((completion(rows),critical(rows)),(8,(8,['A','B','D']))),
(completion([{**r,'duration':0 if r['id']=='E' else r['duration']} for r in rows]),8),
(completion([{**r,'duration':None if r['id']=='B' else r['duration']} for r in rows]),'unknown'),
(completion([{**r,'predecessors':['D'] if r['id']=='A' else r['predecessors']} for r in rows]),'cycle'),
(completion(rows[::-1]),8),((completion([{**r,'duration':5 if r['id']=='C' else r['duration']} for r in rows]),critical([{**r,'duration':5 if r['id']=='C' else r['duration']} for r in rows])),(9,(9,['A','C','D'])))])

assert len(results)==60
print(json.dumps(dict(environment=platform.python_version(),scope='60 acceptance-row oracle calculations; not app/user/concurrency validation',cases=len({r['case'] for r in results}),checks=len(results),results=results),ensure_ascii=False,indent=2))
