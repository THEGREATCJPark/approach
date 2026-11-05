#!/usr/bin/env python3
"""Flag exact fingerprints and lexical similarity for human review, never certify originality."""
import argparse
import collections
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNATURE_KEYS = ['decision', 'input_structure', 'hard_constraint', 'validation']


def read(path):
    obj = json.loads(path.read_text(encoding='utf-8'))
    return obj if isinstance(obj, list) else obj['cases']


def normalize(value):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return re.sub(r'\s+', '', text).lower()


def tokens(value):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return set(re.findall(r'[가-힣a-zA-Z0-9]{2,}', text.lower())) - set(SIGNATURE_KEYS)


def check(cases):
    errors, legacy, signatures, fingerprints = [], [], {}, collections.defaultdict(list)
    for case in cases:
        ident = case['id']
        signature = case.get('decision_signature')
        if not isinstance(signature, dict) or any(not signature.get(k) for k in SIGNATURE_KEYS):
            if case.get('depth') == 'standard':
                errors.append(f'{ident}: missing complete decision_signature')
            legacy.append(ident)
            signature = {k:case.get(k) for k in ['title','problem_structure','data_required','do_not_use_when']}
        signatures[ident] = signature
        if case.get('decision_signature'):
            fingerprints[normalize(signature)].append(ident)
    exact = [ids for ids in fingerprints.values() if len(ids)>1]
    if exact:
        errors.append('Exact decision_signature collision; review and explain or rewrite cases.')
    test_fingerprints = collections.defaultdict(list)
    for case in cases:
        comparable = [{'input':t.get('input'), 'expected':t.get('expected')} for t in case.get('tests',[]) if isinstance(t,dict)]
        if comparable:
            test_fingerprints[normalize(comparable)].append(case['id'])
    repeated_tests = [ids for ids in test_fingerprints.values() if len(ids)>1]
    similar = []
    for a,b in itertools.combinations(cases,2):
        ta,tb = tokens(signatures[a['id']]),tokens(signatures[b['id']])
        score = len(ta&tb)/len(ta|tb) if ta|tb else 0
        if score >= 0.25:
            similar.append({'a':a['id'],'b':b['id'],'cross_family':a['family']!=b['family'],'jaccard':round(score,4),'shared_terms':sorted(ta&tb)})
    similar.sort(key=lambda r:(-r['jaccard'],r['a'],r['b']))
    return {'status':'fail' if errors else 'manual_review_required','case_count':len(cases),
        'explicit_signatures':len(cases)-len(legacy),'legacy_derived_signatures':legacy,
        'errors':errors,'exact_signature_groups':exact,'identical_test_groups':repeated_tests,
        'lexical_review_candidates':similar[:40],
        'limitations':'Different wording can hide duplicate decisions; shared wording can describe distinct decisions. A clean result proves neither originality nor substantive distinctness. Review decision/input/hard-constraint/validation changes manually.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog',type=Path,default=ROOT/'catalog/cases.json')
    parser.add_argument('--additional',type=Path,action='append',default=[],help='Optional in-progress fragments; duplicate IDs are rejected')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    cases=read(args.catalog)
    for path in args.additional:cases.extend(read(path))
    result=check(cases)
    ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):
        result['errors'].append('Duplicate IDs across input catalogs');result['status']='fail'
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.write_text(text+'\n',encoding='utf-8')
    print(text)
    raise SystemExit(bool(result['errors']))

if __name__=='__main__':main()
