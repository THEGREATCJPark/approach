#!/usr/bin/env python3
"""Run frozen catalog-routing prompts; card decision adequacy remains manual."""
import argparse
import datetime
import json
import platform
from pathlib import Path
from route import ROOT, load_cases, route


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    spec=json.loads(args.input.read_text(encoding='utf-8'))
    cases=load_cases(); by_path={c['path']:c for c in cases}
    rows=[]
    for test in spec['requests']:
        actual=route(test['request'],cases=cases)
        family=actual['candidates'][0]['family'] if actual['candidates'] else actual['status']
        selected=[]
        for candidate in actual['candidates']:
            for path in candidate['cards']:
                c=by_path.get(path,{})
                selected.append({'id':c.get('id'),'title':c.get('title'),'family':c.get('family'),'depth':c.get('depth'),'path':path,'decision_signature':c.get('decision_signature')})
        expected_id=test.get('expected_case_id')
        row={'test':test,'actual_primary':family,'family_pass':family==test['expected_primary'],
             'selected':selected,'excluded_clauses':actual.get('excluded_clauses',[]),
             'decision_review':'pending_manual_review' if 'expected_decision' in test else 'not_applicable',
             'expected_case_retrieved':expected_id in [c['id'] for c in selected] if expected_id else None}
        rows.append(row)
    result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),
        'catalog_count':len(cases),'design':spec['design'],'total':len(rows),'family_passed':sum(r['family_pass'] for r in rows),
        'case_retrieval_evaluated':sum(r['test'].get('expected_case_id') is not None for r in rows),
        'expected_case_retrieved':sum(r['expected_case_retrieved'] is True for r in rows),
        'results':rows,'limitations':'Family retrieval does not prove card suitability or implementation correctness. Manual decision review must inspect selected cards. Test-informed changes must be reported separately.'}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['catalog_count','total','family_passed','case_retrieval_evaluated','expected_case_retrieved']},ensure_ascii=False))

if __name__=='__main__':main()
