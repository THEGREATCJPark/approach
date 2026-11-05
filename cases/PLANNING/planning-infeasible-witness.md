# 수요와 용량 충돌의 부족량 설명

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-infeasible-witness",
  "title": "수요와 용량 충돌의 부족량 설명",
  "family": "PLANNING",
  "problem_structure": "capacity infeasibility witness",
  "keywords_ko": [
    "수요와",
    "용량",
    "충돌의",
    "부족량",
    "설명"
  ],
  "keywords_en": [
    "capacity",
    "infeasibility",
    "witness"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 체험 운영자가 하루 신청 인원을 두 시간대에 배정할 수 없다는 결과만 받아 무엇을 바꿔야 할지 모른다.",
  "do_not_use_when": "솔버 시간초과를 이 확정 부족 증명과 섞지 않는다. 데이터가 부족하면 정원 비교만 하고 자동 거절하지 않는다.",
  "data_required": [
    "demand 정수 명, capacities는 각 시간대 정수 명. 한 원소는 교환 가능한 시간대 수용량. null 수요/용량은 unknown. 모든 참가자가 어느 시간대나 가능하고 다른 제약 없음."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rotation-budget"
  ],
  "depth": "standard",
  "path": "cases/PLANNING/planning-infeasible-witness.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 체험 운영자가 하루 신청 인원을 두 시간대에 배정할 수 없다는 결과만 받아 무엇을 바꿔야 할지 모른다.",
    "input_structure": "demand 정수 명, capacities는 각 시간대 정수 명. 한 원소는 교환 가능한 시간대 수용량. null 수요/용량은 unknown. 모든 참가자가 어느 시간대나 가능하고 다른 제약 없음.",
    "hard_constraint": "부족=max(0,demand−sum(capacities)). 부족>0이면 infeasible와 최소 증설량; 아니면 capacity_sufficient. 복합 제약의 실행 가능성을 보장하지 않는다.",
    "validation": "총합과 수요 같음"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 체험 운영자가 하루 신청 인원을 두 시간대에 배정할 수 없다는 결과만 받아 무엇을 바꿔야 할지 모른다.

- 총용량 자체 부족
- 일부 시간대만 가능한 수요가 몰림
- 필수조건을 선호로 잘못 완화

## 담당자에게 먼저 물을 질문

1. 누구나 모든 시간대에 들어갈 수 있는가? → 이 예제는 그렇고 제한이 있으면 총합 증명만으로 충분하지 않다.
2. 시간대 증설과 수요 거절 중 가능한 것은 무엇인가? → 부족량은 정책 선택의 입력이다.
3. 수요가 확정인가 상한인가? → 불명확하면 확정 불가능 판정을 하지 않는다.

## 데이터 계약과 자료 부족 대안

demand 정수 명, capacities는 각 시간대 정수 명. 한 원소는 교환 가능한 시간대 수용량. null 수요/용량은 unknown. 모든 참가자가 어느 시간대나 가능하고 다른 제약 없음.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

부족=max(0,demand−sum(capacities)). 부족>0이면 infeasible와 최소 증설량; 아니면 capacity_sufficient. 복합 제약의 실행 가능성을 보장하지 않는다.

시간대별 허용 참가자·자격 조건이 있으면 매칭과 최소 절단 같은 별도 불가능 근거를 검토한다.

## 최소 구현과 다음 행동

수요·용량 → 총합 하한 → 부족 인원과 수정 선택 → 담당자가 증설/대기 정책 결정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"demand":11,"capacities":[4,5]}` | `{"state": "infeasible", "shortage": 2}` | 11−9=2명 부족 |
| boundary | `{"demand":9,"capacities":[4,5]}` | `{"state": "capacity_sufficient", "shortage": 0}` | 총합과 수요 같음 |
| missing | `{"demand":null,"capacities":[4,5]}` | `"unknown"` | 수요 미확정 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

솔버 시간초과를 이 확정 부족 증명과 섞지 않는다. 데이터가 부족하면 정원 비교만 하고 자동 거절하지 않는다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 부족 인원을 보고 어느 운영 조건을 바꿀 수 있는가?
- capacity_sufficient를 모든 제약 충족으로 오해하지 않는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 이 불가능 증명이 성립하는 가정은 무엇인가?
- 용량은 충분한데 배정 불가능한 반례는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
