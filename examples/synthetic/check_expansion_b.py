#!/usr/bin/env python3
"""Independent arithmetic/rule examples, with manually specified expected values.
No application, external service, statistical inference, or user study is run.
"""
import copy
import json
import math
import platform
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from statistics import mean, median

D = lambda x: Decimal(str(x))

def approved_explanation(x):
    if x['docs'] is None:
        return 'unknown'
    if any(d['text'] is None for d in x['docs']):
        return 'unknown'
    valid = [d for d in x['docs'] if d['concept'] == x['concept'] and d['approved'] and d['active'] and len(d['text']) <= x['max_chars']]
    return min(valid, key=lambda d: (len(d['text']), d['id']))['id'] if valid else 'no_fit'

def taxonomy(x):
    if x['labels'] is None:
        return 'unknown'
    labels = set(x['labels'])
    if not labels:
        return 'unclassified'
    if not labels <= {'role', 'process', 'product'}:
        return 'invalid'
    return next(iter(labels)) if len(labels) == 1 else 'needs_review'

def recall(x):
    if x['questions'] is None or any(q['due'] is None for q in x['questions']):
        return 'unknown'
    return [q['id'] for q in sorted(x['questions'], key=lambda q: (q['due'], q['id'])) if q['enabled'] and q['due'] <= x['today']][:x['limit']]

def misconception(x):
    if x['tags'] is None:
        return 'unknown'
    tags = set(x['tags'])
    if not tags:
        return 'no_targeted_feedback'
    if len(tags) > 1 or not tags <= x['map'].keys():
        return 'needs_review'
    return x['map'][next(iter(tags))]

def evidence(x):
    if x['sources'] is None:
        return 'unknown'
    claims = set(x['claims'])
    if not claims:
        return {'status': 'empty', 'unsupported': []}
    support = set().union(*(set(s['supports']) for s in x['sources'] if s['active']))
    oppose = set().union(*(set(s['opposes']) for s in x['sources'] if s['active']))
    missing = sorted(claims - support)
    status = 'conflict' if claims & oppose else 'incomplete' if missing else 'supported'
    return {'status': status, 'unsupported': missing}

def paired_gain(x):
    rows = x['rows']
    if any(v is not None and (v < 0 or v > x['max_score']) for r in rows for v in (r['before'], r['after'])):
        return 'invalid'
    pairs = [r for r in rows if r['before'] is not None and r['after'] is not None]
    if not pairs:
        return 'unknown'
    return {'paired': len(pairs), 'missing': len(rows) - len(pairs), 'mean_change': mean(r['after'] - r['before'] for r in pairs)}

def slope(x):
    rows = x['rows']
    if len(rows) < 2 or any(v is None for r in rows for v in r):
        return 'unknown'
    ts, vs = zip(*rows)
    mt, mv = mean(ts), mean(vs)
    denominator = sum((t - mt) ** 2 for t in ts)
    if denominator == 0:
        return 'invalid'
    return round(sum((t - mt) * (v - mv) for t, v in rows) / denominator, 12)

def vector(x):
    if x['target'] is None or x['measured'] is None:
        return 'unknown'
    dx, dy = [b - a for a, b in zip(x['target'], x['measured'])]
    squared = dx * dx + dy * dy
    return {'dx': dx, 'dy': dy, 'distance': math.sqrt(squared), 'status': 'within' if squared <= x['radius'] ** 2 else 'outside'}

def instrument(x):
    if not x['rows'] or any(r['a'] is None or r['b'] is None for r in x['rows']):
        return 'unknown'
    diff = [r['b'] - r['a'] for r in x['rows']]
    bias = mean(diff)
    return {'mean_bias': bias, 'max_abs_difference': max(map(abs, diff)), 'status': 'within' if abs(bias) <= x['tolerance'] else 'outside'}

def cusum(x):
    if not x['values'] or any(v is None for v in x['values']):
        return 'unknown'
    s, peak, first = D(0), D(0), None
    for i, value in enumerate(x['values']):
        s = max(D(0), s + D(value) - D(x['baseline']) - D(x['k']))
        peak = max(peak, s)
        if first is None and s > D(x['h']):
            first = i
    return {'first_alarm_index': first, 'max_cusum': float(peak)}

def washout(x):
    before = [v for t, v in x['rows'] if t < 0]
    after = [v for t, v in x['rows'] if t > x['washout_days']]
    if not before or not after or any(v is None for v in before + after):
        return 'unknown'
    a, b = median(before), median(after)
    return {'before_median': a, 'after_median': b, 'change': b - a}

def inspection(x):
    if not x['checks'] or any(c['p'] is None or c['minutes'] is None for c in x['checks']):
        return 'unknown'
    if any(c['minutes'] <= 0 or not 0 <= c['p'] <= 1 for c in x['checks']):
        return 'invalid'
    return min(x['checks'], key=lambda c: (-D(c['p']) / D(c['minutes']), c['id']))['id']

def lot(x):
    if not x['lots'] or any(r['n'] is None or r['bad'] is None for r in x['lots']):
        return 'unknown'
    if any(not 0 <= r['bad'] <= r['n'] for r in x['lots']):
        return 'invalid'
    total = sum(r['n'] for r in x['lots'])
    return sum(r['bad'] for r in x['lots']) / total if total else 'unknown'

def repeatability(x):
    if len(x['values']) < 2 or any(v is None for v in x['values']):
        return 'unknown'
    vals = list(map(D, x['values']))
    spread = max(vals) - min(vals)
    return {'range': str(spread), 'status': 'within' if spread <= D(x['max_range']) else 'outside'}

def pareto(x):
    rows = x['rows']
    if any(v is None for r in rows for v in r['v']):
        return 'unknown'
    def dominates(a, b):
        return all(u <= v for u, v in zip(a, b)) and any(u < v for u, v in zip(a, b))
    return sorted(r['id'] for r in rows if not any(dominates(s['v'], r['v']) for s in rows if s['id'] != r['id']))

def coverage(x):
    if x['required'] is None or x['executed'] is None:
        return 'unknown'
    return [list(p) for p in sorted(set(map(tuple, x['required'])) - set(map(tuple, x['executed'])))]

def rollout(x):
    if any(x[k] is None for k in ('observed', 'defective', 'critical')):
        return 'unknown'
    if not 0 <= x['defective'] <= x['observed'] or x['critical'] < 0:
        return 'invalid'
    if x['critical'] >= 1:
        return 'rollback'
    if x['observed'] < 100:
        return 'hold'
    return 'rollback' if 100 * x['defective'] > 5 * x['observed'] else 'advance'

def exposure(x):
    if any(v is None for v in x.values()):
        return 'unknown'
    if x['pack'] <= 0 or x['loss_per_unit'] <= 0 or any(v < 0 for v in x.values()):
        return 'invalid'
    cap = min(D(x['demand']), D(x['qualified_cap']), D(x['budget']) / D(x['loss_per_unit']))
    count = int((cap / D(x['pack'])).to_integral_value(rounding=ROUND_FLOOR)) * x['pack']
    return {'trial': count, 'existing': x['demand'] - count, 'exposure': count * x['loss_per_unit']}

FUNCTIONS = {'approved-explanation': approved_explanation, 'taxonomy-ambiguity': taxonomy, 'recall-due-queue': recall,
             'misconception-feedback': misconception, 'answer-evidence-coverage': evidence, 'paired-transfer-gain': paired_gain,
             'time-slope': slope, 'position-error-vector': vector, 'paired-instrument-bias': instrument,
             'one-sided-cusum': cusum, 'maintenance-washout': washout, 'inspection-value-per-minute': inspection,
             'lot-pooled-defects': lot, 'repeatability-range': repeatability, 'risk-pareto': pareto,
             'test-matrix-coverage': coverage, 'rollout-stop-rule': rollout, 'trial-exposure-cap': exposure}

def main():
    fixtures = json.loads(Path(__file__).with_name('expansion_b.json').read_text())
    results = []
    for case_id, group in fixtures.items():
        for test in group['tests']:
            actual_input = copy.deepcopy(group['fixture'])
            actual_input.update(copy.deepcopy(test['input']))
            actual = FUNCTIONS[case_id](actual_input)
            results.append({'case_id': case_id, 'kind': test['kind'], 'input': actual_input,
                            'expected': test['expected'], 'basis': test['basis'], 'actual': actual,
                            'status': 'pass' if actual == test['expected'] else 'fail'})
    report = {'case_count': len(fixtures), 'test_count': len(results), 'passed': sum(r['status'] == 'pass' for r in results),
              'python': platform.python_version(), 'kind': 'independent_synthetic_calculation', 'results': results,
              'limits': ['No production application imported', 'No real users', 'No statistical inference or safety certification']}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['passed'] == report['test_count'] else 1)

if __name__ == '__main__':
    main()
