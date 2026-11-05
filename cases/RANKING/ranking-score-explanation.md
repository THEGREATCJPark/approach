# 규칙 점수 추천의 기여도 설명

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "ranking-score-explanation",
  "title": "규칙 점수 추천의 기여도 설명",
  "family": "RANKING",
  "keywords_ko": [
    "추천이유",
    "기여도",
    "설명",
    "반사실"
  ],
  "keywords_en": [
    "additive-score-explanation",
    "ranking-score-explanation"
  ],
  "problem_structure": "additive-score-explanation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "점수의 항목별 기여를 보여주면 판단 근거가 명확해진다.",
  "do_not_use_when": "복잡한 모델의 인과 설명을 이 단순 기여도로 대체하지 않는다.",
  "data_required": [
    "한 후보의 features는 항목명→0/1 값, weights는 동일 키→정수 점수. 관계키는 feature 이름. null 값은 미확인. contribution=feature×weight, total은 합."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "ranking-cold-start",
    "ranking-attribute-distance"
  ],
  "depth": "standard",
  "path": "cases/RANKING/ranking-score-explanation.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "추천 점수의 실제 기여도를 설명한다",
    "input_structure": "항목별 0/1 입력과 가중치 매핑",
    "hard_constraint": "미확인 입력에서 총점 확정 금지",
    "validation": "기여도 합계 및 확인된0 기여"
  }
}
```

## 1. 창작 업무 요청

“장비 교육 과정이 추천된 이유를 수강자가 이해하지 못한다.”

## 2. 다른 원인과 목표

- 점수의 항목별 기여를 보여주면 판단 근거가 명확해진다.
- 점수 규칙이 실제 목표와 다를 수 있다.
- 설명을 그럴듯하게 생성하지만 실제 계산과 연결되지 않을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 어떤 입력 항목으로 점수를 계산했는가? → 실제 규칙만 설명한다.
2. 추천 이유가 아니라 이의 제기가 필요한가? → 수정 가능한 입력과 재평가 절차를 추가한다.
3. 부정 조건은 필터인가 감점인가? → 필수 제외라면 점수로 상쇄하지 않는다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

한 후보의 features는 항목명→0/1 값, weights는 동일 키→정수 점수. 관계키는 feature 이름. null 값은 미확인. contribution=feature×weight, total은 합.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "features": {
    "interest": 1,
    "level": 1,
    "schedule": 0
  },
  "weights": {
    "interest": 4,
    "level": 2,
    "schedule": 3
  }
}
```

## 5. 기준 방법과 개선 조건

계산에서 사용한 기여도 배열을 결과와 함께 저장한다. 단일 항목을0으로 바꾼 점수 차이도 확인한다. 자연어 설명은 해당 항목 이름·수치만 사용하며 인과 효과라고 말하지 않는다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

특성·규칙 → 총점과 기여도 → 담당자가 입력 오류를 수정하고 다시 평가한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"features":{"interest":1,"level":1,"schedule":0},"weights":{"interest":4,"level":2,"schedule":3}}` | `{"total": 6, "contributions": {"interest": 4, "level": 2, "schedule": 0}}` | 4+2+0=6. |
| boundary | `{"features":{"interest":0},"weights":{"interest":4}}` | `{"total": 0, "contributions": {"interest": 0}}` | 확인된0의 기여0. |
| missing | `{"features":{"interest":null},"weights":{"interest":4}}` | `"unknown"` | 미확인 관심을 부정으로 해석하지 않는다. |
| missing_weight | `{"features":{"interest":1},"weights":{"interest":null}}` | `"unknown"` | 규칙 가중치가 없으면 점수 보류다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 복잡한 모델의 인과 설명을 이 단순 기여도로 대체하지 않는다.
- 계산과 무관한 추천 이유를 생성하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 어떤 입력을 고쳐야 결과가 바뀌는지 이해할 수 있는가?
2. 점수 기여와 필수 제외 사유가 혼동되지 않는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 설명과 실제 계산이 같은 근거를 사용함을 어떻게 검증했는가?
2. 기여도가 선호의 원인임을 증명하지 않는 이유는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/decimal.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
