#!/usr/bin/env python3
"""Offline structural retrieval; scores are lexical evidence, never success probabilities."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Terms describe decisions, not industries. Multiple families may be relevant.
TERMS = {
    'ANALYTICS': ['비교 보고', '실적', '집계', '통화', '누적', '단위 변환', '매출', '분석만', '분석 보고', 'aggregation', 'currency', 'analytics'],
    'SUPPORT': ['문의', '이관', '티켓', '정책 검색', '근거 검색', '상담', 'ticket', 'search', 'retrieval'],
    'COACH': ['설명 연습', '모의 면접', '답변 연습', '발표 연습', 'rehearsal', 'coach'],
    'EVENT': ['참여 자격', '체크인', '대기 명단', '정원', '재신청', '등록 취소', 'check-in', 'waitlist'],
    'GEOMETRY': ['커버리지', '가림', '설치 위치', '면적', '도면', '공간 배치', '시야', 'coverage', 'geometry', 'occlusion'],
    'LEARNING': ['선수 지식', '오개념', '학습', '퀴즈', '개념 설명', 'quiz', 'learning', 'prerequisite'],
    'OPERATIONS': ['센서', '관리한계', '추이', '지속 변화', '경보', '이상 탐지', '정비 전후', 'sensor', 'spc', 'drift'],
    'PLANNING': ['기간 계획', '주간', '편성', '반복 간격', '발주', '공급 중단', '일정 고정', '식단 계획', 'weekly', 'planning'],
    'POLICY': ['승인 권한', '증빙', '반려', '재제출', '정책 버전', '비용 처리', '승인 절차', '정책 규칙', 'approval', 'policy'],
    'QUALITY': ['동등성', '측정 신뢰도', '공급원 변경', 'lot', '품질', '허용범위', 'equivalence', 'quality'],
    'RANKING': ['추천', '후보 순위', '개인화', '다양성', '제공 가능', '금지 품목', 'recommend', 'ranking'],
    'MOBILITY': ['방문 순서', '출발시각', '이동시간', '시간창', '경로', '도착', 'routing', 'route', 'departure'],
    'INTERACTIVE': ['게임', '충돌', '재시작', '체력', '승패', '프레임', 'game', 'collision', 'restart'],
    'TRANSACTION': ['가용량', '잠금량', '재고 잠금', '소수 정밀도', '예약 수량', '재시도 중복', '멱등', '재처리', '원자성', 'reservation', 'transaction', 'decimal'],
    'DEPENDENCY': ['의존', '영향 경로', '관계 그래프', '병목', '연쇄', 'dependency', 'graph', 'critical path'],
}

QUESTIONS = {
    'ANALYTICS': '비교 대상의 기간·모집단·단위가 일치하나요?',
    'SUPPORT': '처리 순서를 정하나요, 근거를 찾나요, 담당 부서를 정하나요?',
    'COACH': '시험 전 창작 연습인가요? 본인의 선택을 입증할 실제 준비 기록은 무엇인가요?',
    'EVENT': '정원이 찼을 때 거절·대기·승인 예외 중 어떤 정책이 적용되나요?',
    'GEOMETRY': '단순 면적 중첩인가요, 장애물 뒤 시야까지 판정해야 하나요?',
    'LEARNING': '설명을 읽는 것이 목표인가요, 새 문제를 직접 수행하는 것이 목표인가요?',
    'OPERATIONS': '경보 기준은 규격 위반인가요, 안정된 공정의 변화인가요?',
    'PLANNING': '기간 전체 필수조건과 선호조건 중 무엇을 절대로 완화하면 안 되나요?',
    'POLICY': '이 건에 적용되는 정책 버전·효력 시점·승인권자는 누구인가요?',
    'QUALITY': '차이가 없다는 검정인가요, 사전 합의한 허용범위 내 동등성을 입증하나요?',
    'RANKING': '선택 불가능한 후보를 제외할 필수조건은 무엇인가요?',
    'MOBILITY': '방문 순서를 바꿀 수 있나요, 고정 경로의 출발시각만 조정하나요?',
    'INTERACTIVE': '단일 사용자 상태 전이면 충분한가요, 실제 동시 접속이 필수인가요?',
    'TRANSACTION': '심사 통과와 실제 수량 변경은 어느 단계에서 확정되나요?',
    'DEPENDENCY': '관계 존재만 추적하나요, 수량 영향까지 추정할 근거가 있나요?',
}


def positive_clauses(text):
    """Conservative explicit-clause exclusions, not general Korean negation parsing.

    A clause ending in 필요 없어/필요 없음/아님 is excluded. In X 아니라 Y,
    only Y remains. No inference is made for 없는 재고, 안 되는 조건 etc.
    Excluded text is returned so users can inspect and correct over-exclusion.
    """
    kept, excluded = [], []
    for raw in re.split(r'[.!?;,\n]+', text.lower()):
        clause = raw.strip()
        if not clause:
            continue
        if '아니라' in clause:
            left, clause = clause.rsplit('아니라', 1)
            excluded.append(left.strip() + ' 아니라')
            clause = clause.strip()
        if re.search(r'(?:필요\s*(?:없어(?:요)?|없음|없다)|아님)\s*$', clause):
            excluded.append(clause)
            continue
        if clause:
            kept.append(clause)
    return ' '.join(kept), excluded


def load_cases(root=ROOT):
    path = root / 'catalog/cases.json'
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding='utf-8'))
    return value if isinstance(value, list) else value.get('cases', [])


def route(text, cases=None, mode='PREP', automation='unknown'):
    if mode == 'NO_AI_REVIEW':
        return {'status': 'stopped', 'reason': 'AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단합니다.', 'candidates': []}
    cases = load_cases() if cases is None else cases
    query, excluded = positive_clauses(text)
    scores = []
    for family, terms in TERMS.items():
        hits = [term for term in terms if term in query]
        if hits:
            # Output form ('analysis only') is weaker than a concrete decision structure.
            weight = sum(0.25 if term in ['분석만', '분석 보고'] else 1 for term in hits)
            scores.append((weight, family, hits))
    scores.sort(key=lambda row: (-row[0], row[1]))
    if not scores:
        return {'status': 'unclassified', 'reason': '결정 구조를 판별할 근거가 부족합니다.', 'question': '결과를 보고 누가 어떤 결정을 해야 하나요? 대표 입력과 기대 출력 한 건을 확인하세요.', 'candidates': [], 'excluded_clauses': excluded}
    result = []
    for _, family, hits in scores[:3]:
        available = [c for c in cases if c.get('family', '').upper() == family]
        # Specific card keywords break ties within the family only.
        def relevance(c):
            words = c.get('keywords_ko', []) + c.get('keywords_en', [])
            return sum(1 for word in words if str(word).lower() in query)
        available.sort(key=lambda c: (-relevance(c), c.get('id', '')))
        selected = available[:2]
        c = selected[0] if selected else {}
        result.append({'family': family, 'role': 'primary' if not result else 'secondary',
            'reason': '의사결정 단서: ' + ', '.join(hits),
            'may_not_fit': c.get('do_not_use_when', '표면 용어만 같고 실제 결정이 다르면 분류를 변경하세요.'),
            'data_to_check': c.get('data_required', []),
            'first_question': QUESTIONS[family],
            'baseline_methods': c.get('method_ids', ['baseline-first']),
            'cards': [x.get('path', '') for x in selected]})
    return {'status': 'candidate', 'candidates': result, 'excluded_clauses': excluded,
        'limitations': '어휘 기반 후보 검색이며 완전한 의미·부정문 해석을 하지 못합니다. 제외된 절이 맞는지 확인하고 추가 답변으로 요청을 다시 기술해 재분류하세요. 적합도 확률이나 검증된 자동 설계가 아닙니다.',
        'execution': '브라우저 자동화는 실행하지 않습니다. 계산·단위 검사와 허용된 수동 확인을 사용하세요.' if automation != 'allowed' else '자동화 allowed 기록은 해당 기능의 명시적 허용 근거가 있어야 유효합니다. 이 검색기는 자동화를 실행하지 않습니다.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request', help='현재 확인된 업무 요청; 추가 답변 후 최신 목표로 다시 입력')
    parser.add_argument('--mode', choices=['PREP', 'TASK', 'NO_AI_REVIEW'], default='PREP')
    parser.add_argument('--automation', choices=['allowed', 'forbidden', 'unknown'], default='unknown')
    args = parser.parse_args()
    print(json.dumps(route(args.request, mode=args.mode, automation=args.automation), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
