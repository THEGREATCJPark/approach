# 미배정 수요와 과배정의 수량 대사

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "mobility-unserved-ledger",
  "title": "미배정 수요와 과배정의 수량 대사",
  "family": "MOBILITY",
  "keywords_ko": [
    "미배정",
    "잔여",
    "수요",
    "대사"
  ],
  "keywords_en": [
    "demand-reconciliation",
    "mobility-unserved-ledger"
  ],
  "problem_structure": "demand-reconciliation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "계획 생성보다 수요와 배정의 독립 대사가 필요하다.",
  "do_not_use_when": "미배정은 계획 불가능의 증명이 아니다.",
  "data_required": [
    "demand는 request_id→정수 상자 수, assignments는 [allocation_id,request_id,qty]. 요청별 배정 합과 수요를 비교한다. 예제는 allocation_id가 고유하고 qty≥0이다. 수요 null은 미확인이다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "mobility-indivisible-capacity",
    "mobility-window-wait"
  ],
  "depth": "standard",
  "path": "cases/MOBILITY/mobility-unserved-ledger.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "계획의 요청별 미배정·과배정을 대사한다",
    "input_structure": "수요량과 분할 배정량·관계키",
    "hard_constraint": "수요와 배정 기준 일치; null 보류",
    "validation": "잔여와 초과를 상쇄하지 않는 요청별 집계"
  }
}
```

## 1. 창작 업무 요청

“수거 계획을 받았는데 어떤 요청이 빠졌는지와 수량이 초과 배정됐는지 확인하기 어렵다.”

## 2. 다른 원인과 목표

- 계획 생성보다 수요와 배정의 독립 대사가 필요하다.
- 분할 배정 행이 중복됐을 수 있다.
- 취소된 수요가 옛 계획에 남아 있을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 배정 행의 단위는 요청 전체인가 일부 수량인가? → 일부면 request_id로 합산한다.
2. 배정 id가 중복되면 재전송인가? → 동일 내용이면 멱등 처리하고, 다르면 충돌로 보류한다.
3. 수요 기준 버전이 계획과 같은가? → 다르면 차이를 확정하기 전에 버전을 맞춘다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

demand는 request_id→정수 상자 수, assignments는 [allocation_id,request_id,qty]. 요청별 배정 합과 수요를 비교한다. 예제는 allocation_id가 고유하고 qty≥0이다. 수요 null은 미확인이다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "demand": {
    "A": 5,
    "B": 2
  },
  "assignments": [
    [
      "x",
      "A",
      3
    ],
    [
      "y",
      "B",
      2
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

수요에 없는 request_id 또는 중복 allocation_id는 입력 오류로 반환한다. 요청별 배정 합을 집계하고 remaining=max(수요-배정,0), over=max(배정-수요,0)를 분리한다. 미배정을 자동으로 불가능이라고 부르지 않는다. 계획 누락일 수 있다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

수요·배정표 → 요청별 잔여/초과 → 담당자가 누락 배정 또는 중복 계획을 수정한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"demand":{"A":5,"B":2},"assignments":[["x","A",3],["y","B",2]]}` | `{"A": {"remaining": 2, "over": 0}, "B": {"remaining": 0, "over": 0}}` | A5-3=2,B2-2=0. |
| boundary | `{"demand":{"A":2},"assignments":[["x","A",3]]}` | `{"A": {"remaining": 0, "over": 1}}` | 초과 1을 음수 잔여로 숨기지 않는다. |
| missing | `{"demand":{"A":null},"assignments":[]}` | `"unknown"` | 수요 미확인으로 잔여 계산을 보류한다. |
| unknown_request | `{"demand":{"A":2},"assignments":[["x","Z",4]]}` | `"invalid_reference"` | 수요에 없는 요청 Z를 조용히 버리지 않고 관계 키 오류로 반환한다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 미배정은 계획 불가능의 증명이 아니다.
- 초과와 잔여를 서로 상쇄한 전체 합으로만 검사하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 어떤 요청을 추가 배정하거나 줄여야 하는지 알 수 있는가?
2. 수요 버전과 계획 버전이 달라진 경우 추적할 수 있는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 대사 검사가 계획 생성 로직과 독립적인 이유는 무엇인가?
2. 전체 수량 합이 맞아도 요청별 오류가 남는 반례는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
