# 정답 로그 없이 추천 결과의 기본 품질 점검

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "ranking-without-labels",
  "title": "정답 로그 없이 추천 결과의 기본 품질 점검",
  "family": "RANKING",
  "keywords_ko": [
    "정답없음",
    "추천검증",
    "중복",
    "커버리지"
  ],
  "keywords_en": [
    "recommendation-invariants",
    "ranking-without-labels"
  ],
  "problem_structure": "recommendation-invariants",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "정확도를 주장할 수 없어도 필수조건·중복·설명 누락은 검사할 수 있다.",
  "do_not_use_when": "이 지표를 관련성 정확도나 만족도로 이름 붙이지 않는다.",
  "data_required": [
    "recommendations는 id 배열(순위 순서), eligible는 검증된 제공 가능 id 집합, requested는 비음수 정수 건. 중복수=길이-고유수, 부적합은 eligible 밖 고유id, 부족=max(0,requested-제공 가능한 고유수)."
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
  "path": "cases/RANKING/ranking-without-labels.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "정답 로그 없이 추천 목록 위반을 점검한다",
    "input_structure": "추천 id 배열·가용 집합·요구 개수",
    "hard_constraint": "중복·부적합·부족을 별도 보고",
    "validation": "집합 차이와 길이 차이 대사"
  }
}
```

## 1. 창작 업무 요청

“추천을 만들었지만 어떤 추천이 좋았는지 과거 정답이 없어 검증을 시작하지 못하고 있다.”

## 2. 다른 원인과 목표

- 정확도를 주장할 수 없어도 필수조건·중복·설명 누락은 검사할 수 있다.
- 실제 사용자 효과는 별도 관찰이 필요하다.
- 후보 집합이 비어 있는 이유가 데이터 누락일 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 좋은 추천의 정답이나 피드백이 있는가? → 없으면 정확도 수치를 만들지 않는다.
2. 반드시 제공 가능한 항목의 목록이 있는가? → 없으면 적합성 점검도 보류한다.
3. 목록 크기를 채우는 것이 필수인가? → 부족하면 미충족 건수를 따로 표시한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

recommendations는 id 배열(순위 순서), eligible는 검증된 제공 가능 id 집합, requested는 비음수 정수 건. 중복수=길이-고유수, 부적합은 eligible 밖 고유id, 부족=max(0,requested-제공 가능한 고유수).

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "recommendations": [
    "A",
    "A",
    "X"
  ],
  "eligible": [
    "A",
    "B"
  ],
  "requested": 3
}
```

## 5. 기준 방법과 개선 조건

결과 불변식부터 검사하고 수동 평가 표본을 계획한다. 부족·중복·부적합을 합쳐 임의 종합 정확도로 바꾸지 않는다. 개선은 동의받은 사용자 과제 관찰과 비교 실험이다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

추천 목록 → 독립 점검표 → 위반 항목 수정·근거 부족 표시 → 운영자가 제한된 시범 사용 여부를 정한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"recommendations":["A","A","X"],"eligible":["A","B"],"requested":3}` | `{"duplicates": 1, "invalid": ["X"], "unfilled": 2}` | 중복1; X는 부적합. 유효한 고유 후보는 A 한 개이므로 부족3-1=2. |
| boundary | `{"recommendations":[],"eligible":[],"requested":0}` | `{"duplicates": 0, "invalid": [], "unfilled": 0}` | 요구0인 빈 목록은 계약 충족. |
| missing | `{"recommendations":["A"],"eligible":null,"requested":1}` | `"unknown"` | 제공 가능 기준 미확인. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 이 지표를 관련성 정확도나 만족도로 이름 붙이지 않는다.
- 고유 항목 수가 충분해도 부적합 항목이 있으면 통과로 표시하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 오류 항목을 찾아 수정할 수 있는가?
2. 다음 사용자 관찰에서 무엇을 측정해야 하는지 점검표로 알 수 있는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 정답 없이 검증한 것과 아직 검증하지 못한 것은 무엇인가?
2. 부적합·부족·중복을 분리한 이유는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
