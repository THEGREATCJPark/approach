"""Local small synthetic oracles, not app implementation or natural-language judges."""
import json
import sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter


def currency_basis(x):
    if x['amount'] is None or x['rate'] is None:return 'unknown'
    a,r=Decimal(x['amount']),Decimal(x['rate'])
    if a<0 or r<=0:return 'invalid'
    return str((a*r).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))


def price_volume_bridge(x):
    if any(x[k] is None for k in ('p0','p1','q0','q1')):return 'unknown'
    p0,p1,q0,q1=(Decimal(str(x[k])) for k in ('p0','p1','q0','q1'))
    return [float((p1-p0)*q0),float(p1*(q1-q0)),float(p1*q1-p0*q0)]


def revision_ledger(x):
    latest={}
    for key,version,value in x['rows']:
        if key not in latest or version>latest[key][0]:latest[key]=(version,{value})
        elif version==latest[key][0]:latest[key][1].add(value)
    if any(len(vs)>1 for _,vs in latest.values()):return 'conflict'
    vals=[next(iter(vs)) for _,vs in latest.values()]
    return 'unknown' if None in vals else sum(vals)


def scenario_demand(x):
    if x['base'] is None:return 'unknown'
    if any(r < -100 for r in x['rates']):return 'invalid'
    return [float(Decimal(x['base'])*(1+Decimal(r)/100)) for r in x['rates']]


def report_source_coverage(x):
    if not x['links']:return 'no_claims'
    missing=[key for key,source in x['links'] if source is None or source not in x['available']]
    return [len(x['links'])-len(missing),len(x['links']),missing]


def bounded_missing_total(x):
    known=[v for v in x['counts'] if v is not None]
    if any(v<0 for v in known) or (x['cap'] is not None and x['cap']<0):return 'invalid'
    lower=sum(known);n=len(x['counts'])-len(known)
    return [lower,None if n and x['cap'] is None else lower+n*(x['cap'] or 0)]


def support_rule_overlap(x):
    if x['tags'] is None:return 'unknown'
    mapping={'damage':'repair','delivery':'logistics','payment':'billing'}
    teams={mapping[v] for v in x['tags'] if v in mapping}
    return 'unclassified' if not teams else next(iter(teams)) if len(teams)==1 else 'review'


def duplicate_ticket_fingerprint(x):
    groups={};seen={}
    for ticket,*key in x['rows']:
        if ticket in seen:
            if seen[ticket]!=tuple(key):return 'conflict'
            continue
        seen[ticket]=tuple(key)
        if None in key:return 'unknown'
        groups.setdefault(tuple(key),[]).append(ticket)
    return sorted(sorted(v) for v in groups.values() if len(v)>1)


def draft_release_gate(x):
    c=x['checks']
    if len(c)!=3 or any(v is not None and type(v) is not bool for v in c):return 'invalid'
    if False in c:return 'hold'
    if None in c:return 'pending'
    return 'ready_for_human_send'


def escalation_authority(x):
    if x['special'] is None:return 'unknown'
    if x['special']:return 'escalate'
    if x['limit'] is None:return 'unknown'
    if x['amount'] is None:return 'estimate_required'
    return 'within_authority' if x['amount']<=x['limit'] else 'escalate'


def handoff_action_fields(x):
    if x['status']=='resolved':return 'archive_ready'
    missing=[k for k in ('next_action','owner','due') if not x[k]]
    return missing or 'handoff_ready'


def repeat_cause_pareto(x):
    if None in x['causes']:return 'unknown'
    selected=[];n=0
    for code,count in sorted(Counter(x['causes']).items(),key=lambda z:(-z[1],z[0])):
        if n>=x['threshold']*len(x['causes']):break
        selected.append(code);n+=count
    return selected


def rehearsal_budget(x):
    if x['present'] is None:return 'unknown'
    if set(x['essential'])-set(x['present']):return 'restore_evidence'
    return 'shorten' if x['words']>x['limit'] else 'within_budget'


def disclosure_labels(x):
    if x['destination'] not in ('public','internal'):return 'review'
    if x['labels'] is None:return 'review'
    if not x['labels']:return 'no_material'
    permitted={'public'} if x['destination']=='public' else {'public','internal'}
    if any(v is not None and v not in permitted for v in x['labels']):return 'blocked'
    return 'review' if None in x['labels'] else 'within_labels'


def bilingual_quantity(x):
    if not x['same_scope']:return 'semantic_review'
    scale={'s':1,'min':60};a,b=x['a'],x['b']
    if a[1] not in scale or b[1] not in scale:return 'unknown'
    return 'quantity_match' if Decimal(str(a[0]))*scale[a[1]]==Decimal(str(b[0]))*scale[b[1]] else 'quantity_mismatch'


def revision_evidence_loss(x):
    if x['new'] is None:return 'unknown'
    required,old,new,known=(set(x[k]) for k in ('required','old','new','known'))
    return [sorted(required-new),sorted(new-known),sorted((required&old)-new)]


def assumption_challenge_queue(x):
    if any(i is None or u is None for _,i,u in x['rows']):return 'unknown'
    return [key for key,i,u in sorted(x['rows'],key=lambda r:(-r[1]*r[2],r[0]))]


def ai_verification_ledger(x):
    verified=[];unverified=[];unknown=[]
    for key,author,status,evidence in x['rows']:
        if author=='unknown':unknown.append(key)
        elif author=='ai':
            (verified if status=='pass' and evidence else unverified).append(key)
    return [sorted(verified),sorted(unverified),sorted(unknown)]


ORACLES={f.__name__.replace('_','-'):f for f in (
    currency_basis,price_volume_bridge,revision_ledger,scenario_demand,
    report_source_coverage,bounded_missing_total,support_rule_overlap,
    duplicate_ticket_fingerprint,draft_release_gate,escalation_authority,
    handoff_action_fields,repeat_cause_pareto,rehearsal_budget,disclosure_labels,
    bilingual_quantity,revision_evidence_loss,assumption_challenge_queue,ai_verification_ledger)}


def main():
    fixtures=json.loads(Path(__file__).with_name('expansion_a.json').read_text())
    records=[]
    for case,tests in fixtures.items():
        for t in tests:
            actual=ORACLES[case](t['input'])
            records.append(dict(case_id=case,kind=t['kind'],input=t['input'],expected=t['expected'],
                                actual=actual,basis=t['basis'],status='pass' if actual==t['expected'] else 'fail'))
    report=dict(case_count=len(fixtures),test_count=len(records),python=sys.version.split()[0],
                scope='Independent synthetic calculation/rule oracles; no real user, UI, text semantics or organizational impact verified.',results=records)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if all(r['status']=='pass' for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
