# 대체 공급을 포함한 운영 가능 논리

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "dependency-alternative-supply",
  "title": "대체 공급을 포함한 운영 가능 논리",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "대체",
    "공급중단",
    "AND",
    "OR"
  ],
  "keywords_en": [
    "and-or-dependency",
    "dependency-alternative-supply"
  ],
  "problem_structure": "and-or-dependency",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "필수 조건 AND와 대체 조건 OR를 분리해야 한다.",
  "do_not_use_when": "불리언 가용만으로 대체 용량·납기 충족을 보장하지 않는다.",
  "data_required": [
    "groups는 필수 조건 묶음의 배열이다. 각 묶음은 대체 가능한 공급 상태 true/false/null의 배열이다. 묶음 내 OR, 묶음 간 AND를 적용한다. 모든 묶음이 필수이며 빈 묶음은 충족 불가다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "dependency-relation-types",
    "dependency-removal-bottleneck"
  ],
  "depth": "standard",
  "path": "cases/DEPENDENCY/dependency-alternative-supply.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "대체 공급을 고려해 운영 상태를 판정한다",
    "input_structure": "묶음 내 OR·묶음 간 AND의 삼상태 배열",
    "hard_constraint": "필수 묶음 모두 충족; null 보존",
    "validation": "빈 OR와 미확인 OR의 다른 결과"
  }
}
```

## 1. 창작 업무 요청

“두 대체 공급처 중 하나만 살아 있어도 되는 공정이 단순 영향 그래프에서 모두 중단으로 표시된다.”

## 2. 다른 원인과 목표

- 필수 조건 AND와 대체 조건 OR를 분리해야 한다.
- 공급처 상태 미확인이 전파된다.
- 대체 공급 용량이 충분한지는 별도 질문이다.

## 3. 먼저 확인할 질문과 분기

1. 어느 공급처 하나만 되면 충분한가? → OR, 둘 다 필요하면 AND로 모델링한다.
2. 대체처 용량은 충분한가? → 불충분하면 불리언 논리 대신 수량 모델이 필요하다.
3. 미확인 공급처를 사용 가능으로 볼 수 있는가? → 근거 없으면 unknown을 유지한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

groups는 필수 조건 묶음의 배열이다. 각 묶음은 대체 가능한 공급 상태 true/false/null의 배열이다. 묶음 내 OR, 묶음 간 AND를 적용한다. 모든 묶음이 필수이며 빈 묶음은 충족 불가다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "groups": [
    [
      false,
      true
    ],
    [
      true
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

각 OR에서 true가 하나 있으면 true, 전부 false이거나 빈 배열이면 false, 그 외는 unknown이다. AND에서 false가 하나면 false, 전부 true면 true, 그 외는 unknown이다. 개선은 수량·전환 시간 모델이다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

상태표 → 묶음별 충족 근거 → 전체 가동 가능/불가/미확인 → 담당자가 대체 전환 또는 상태 확인을 한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"groups":[[false,true],[true]]}` | `"available"` | 대체 첫 묶음 true, 필수 둘째 묶음 true. |
| boundary | `{"groups":[[],[true]]}` | `"unavailable"` | 대체 후보 0개인 필수 묶음은 false다. |
| missing | `{"groups":[[false,null],[true]]}` | `"unknown"` | 첫 묶음에 확인된 true가 없고 미확인이 있다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 불리언 가용만으로 대체 용량·납기 충족을 보장하지 않는다.
- 미확인 상태를 false로 영구 저장하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 어느 묶음의 확인이 우선인지 알 수 있는가?
2. 대체 가능성 가정이 실제 전환 절차와 맞는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 단순 도달 가능성과 가동 가능 논리는 어떻게 다른가?
2. unknown이 있어도 확정할 수 있는 경우는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
