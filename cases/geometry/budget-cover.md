# 예산 내 점검 거점의 이산 커버리지

```json
{
  "id": "budget-cover",
  "title": "예산 내 점검 거점의 이산 커버리지",
  "family": "GEOMETRY",
  "keywords_ko": [
    "커버리지",
    "예산",
    "거점",
    "최대피복"
  ],
  "keywords_en": [
    "maximum-coverage",
    "budget-cover"
  ],
  "problem_structure": "maximum-coverage",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 식물원 관리자가 이미 현장 측정된 감지 구역 표를 사용해 고정 예산 안에서 점검 거점을 고른다. 같은 구역을 여러 장치가 덮어도 한 번만 세어야 한다.",
  "do_not_use_when": "개별 커버 수 합계로 점수화하지 않는다. 이산 표를 사용한 결과에 실제 시야·보안 효과를 보장하지 않는다.",
  "data_required": [
    "최소: candidate_id, cost 정수(예산 단위), covers 구역 ID 목록; budget. 한 행은 설치 후보. 키 candidate_id. null coverage는 unknown. 개선: 가중치·금지 설치 위치. 감지 기하를 이 표에서 추론하지 않는다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rectangle-union"
  ],
  "depth": "deep",
  "path": "cases/geometry/budget-cover.md",
  "test_count": 6,
  "fixture_path": "examples/synthetic/budget-cover.json"
}
```

## 요청과 가설

창작: 식물원 관리자가 이미 현장 측정된 감지 구역 표를 사용해 고정 예산 안에서 점검 거점을 고른다. 같은 구역을 여러 장치가 덮어도 한 번만 세어야 한다.

가능한 원인: 설치 비용 제약; 중복 커버리지; 중요 구역 가중치 미정.

## 먼저 가를 질문과 계획 변경

1. 모든 구역이 필수입니까 최대한 많이면 됩니까? → 필수이면 set cover feasibility로 전환.
2. 중요 구역 가중치가 있습니까? → 있으면 합집합 원소 가중합 목적.
3. 표가 실제 장애물 가림을 반영합니까? → 아니면 현장/기하 측정부터.

## 데이터 계약

최소: candidate_id, cost 정수(예산 단위), covers 구역 ID 목록; budget. 한 행은 설치 후보. 키 candidate_id. null coverage는 unknown. 개선: 가중치·금지 설치 위치. 감지 기하를 이 표에서 추론하지 않는다.

소형 fixture 어댑터: `candidates`의 행은 [candidate_id,cost,covers], `budget`은 동일 필드다. covers 원소는 중복 제거한 구역 ID 집합으로 해석한다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 작은 후보 집합을 완전 열거하여 예산 이하 부분집합 중 합집합 구역 수 최대, 동률은 비용 최소, 다시 동률은 ID 사전순.

개선 조건: 후보가 많아지면 greedy 기준해와 정수계획을 비교. 시간 제한 솔버에서 feasible과 optimal을 구분한다.

최소 경로: 후보/비용/커버 표 → 전수열거 → 선택 후보·고유 커버 수·미포함 구역 → 담당자가 설치 가능성을 확인.

제약과 우선순위: 목적: |합집합 covers| 최대. 필수: 비용≤예산. 선호: 동률 비용 최소. 우선순위는 커버 수 > 비용 > 재현 가능한 ID. 모든 구역 필수라고 몰래 추가하지 않는다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/budget-cover.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"budget":4,"candidates":[["a",2,["u","v"]],["b",2,["v","w"]],["c",3,["x"]]]}`|`["a", "b"]`|비용4,합집합3; c 단독1|
|boundary|`{"budget":0,"candidates":[["a",2,["u"]]]}`|`[]`|빈 집합 비용0|
|missing|`{"budget":4,"candidates":[["a",2,null]]}`|`"unknown"`|커버 표 미확인|
|conflict|`{"budget":-1,"candidates":[["a",2,["u"]]]}`|`"invalid"`|음수 예산|
|duplicate|`{"budget":4,"candidates":[["a",2,["u","u"]],["b",2,["u"]]]}`|`["a"]`|중복 원소는1, 최소비용 동률 ID a|
|new_sample|`{"budget":3,"candidates":[["a",3,["u","v"]],["b",2,["u","v"]]]}`|`["b"]`|커버 같으면 비용2 선택|

비교 쌍: normal의 예산4에서는 a+b를 고르지만 boundary의 예산0에서는 빈 집합이다. new_sample은 동일 커버일 때 더 싼 b를 골라야 한다.

## 오류·도구·범위

개별 커버 수 합계로 점수화하지 않는다. 이산 표를 사용한 결과에 실제 시야·보안 효과를 보장하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 후보/비용/커버 표 → 전수열거 → 선택 후보·고유 커버 수·미포함 구역 → 담당자가 설치 가능성을 확인. 180분에는 후보가 많아지면 greedy 기준해와 정수계획을 비교. 시간 제한 솔버에서 feasible과 optimal을 구분한다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 미포함 구역 중 필수로 바꿔야 할 곳이 있습니까?
- 선택 후보가 실제 설치 가능한지 누가 확인합니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 완전열거로 최적성을 확인한 후보 수 범위는 얼마입니까?
- 최대 피복과 전체 필수 피복의 차이를 설명하십시오.

## 측정과 한계

예산 위반·고유 커버 수·기준해 대비 개선 측정 가능. 실제 감지율은 현장 관측 필요.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/itertools.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
