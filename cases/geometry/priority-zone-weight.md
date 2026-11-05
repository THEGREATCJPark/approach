# 중요 구역 가중치로 단일 센서 선택

```json
{
  "id": "priority-zone-weight",
  "title": "중요 구역 가중치로 단일 센서 선택",
  "family": "GEOMETRY",
  "keywords_ko": [
    "중요",
    "구역",
    "가중치로",
    "단일",
    "센서",
    "선택"
  ],
  "keywords_en": [
    "weighted-coverage",
    "priority-zone-weight"
  ],
  "problem_structure": "weighted-coverage",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "소규모 천문 전시관에서 설치 슬롯 한 개에 둘 센서를 골라 달라. 관측점 개수보다 반드시 놓치지 않아야 할 설명 구역이 중요하다.",
  "do_not_use_when": "가중치 합의 없이 중요도를 모델이 만들어내지 않는다. 미등록 구역을 0점 처리하지 않는다.",
  "data_required": [
    "최소: weights={zone_id:정수 중요도}, candidates=[id,covers] 한 행 후보, 슬롯 정확히1. 키 zone_id/candidate_id. 가중치 null 또는 미등록 zone은 unknown. 개선: 설치비. 공통 커버 집합의 가중치는 한 번만 합산."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "budget-cover"
  ],
  "depth": "standard",
  "path": "cases/geometry/priority-zone-weight.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "weighted-coverage",
    "input_structure": "최소: weights={zone_id:정수 중요도}, candidates=[id,covers] 한 행 후보, 슬롯 정확히1. 키 zone_id/candidate_id. 가중치 null 또는 미등록 zone은 unknown. 개선: 설치비. 공통 커버 집합의 가중치는 한 번만 합산.",
    "hard_constraint": "가중치 합의 없이 중요도를 모델이 만들어내지 않는다. 미등록 구역을 0점 처리하지 않는다.",
    "validation": "a=4,b=7; 동점0,ID a; z 중요도 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

소규모 천문 전시관에서 설치 슬롯 한 개에 둘 센서를 골라 달라. 관측점 개수보다 반드시 놓치지 않아야 할 설명 구역이 중요하다.

가능한 설명: 단순 점 개수가 목표를 왜곡한다; 가중치가 합의되지 않았다; 반드시 커버해야 하는 구역을 선호점수로 잘못 다룬다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 가중치는 선호입니까 필수입니까? → 필수면 먼저 필터.
2. 미관측 구역 가중치는 누가 승인합니까? → 미정이면 순위 보류.
3. 동점이면 비용과 ID 중 무엇이 우선입니까? → 본 예제 ID 순을 수정.

## 3. 데이터 계약과 자료 부족 대안

최소: weights={zone_id:정수 중요도}, candidates=[id,covers] 한 행 후보, 슬롯 정확히1. 키 zone_id/candidate_id. 가중치 null 또는 미등록 zone은 unknown. 개선: 설치비. 공통 커버 집합의 가중치는 한 번만 합산. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 각 후보 covers 집합의 가중합 최대, 동률 candidate_id 사전순. 필수 구역은 별도 사전 필터.

개선: 설치 슬롯 여러 개이면 가중 합집합 조합 선택으로 변경; 개별 점수 합산은 중복.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

가중치·커버 입력 → 중복 제거 가중합 → 후보별 점수와 선택 이유 → 담당자가 가중치 승인. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"weights":{"u":7,"v":2,"w":2},"candidates":[["a",["v","w"]],["b",["u"]]]}`|`"b"`|a=4,b=7|
|boundary|`{"weights":{"u":0},"candidates":[["b",["u"]],["a",["u"]]]}`|`"a"`|동점0,ID a|
|missing|`{"weights":{"u":7},"candidates":[["a",["z"]]]}`|`"unknown"`|z 중요도 미확인|

## 7. 흔한 오류와 범위 축소

가중치 합의 없이 중요도를 모델이 만들어내지 않는다. 미등록 구역을 0점 처리하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 점수가 높지만 실무에서 선택하기 어려운 후보가 있습니까?
- 한 구역의 가중치가 바뀌면 선택이 달라져야 합니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 같은 커버 수인데 결과가 달라지는 입력은 무엇입니까?
- 가중치 민감도와 실제 감지 효과는 어떻게 구별했습니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
