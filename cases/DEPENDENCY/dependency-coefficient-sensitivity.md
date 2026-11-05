# 가정한 영향 계수의 민감도 비교

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "dependency-coefficient-sensitivity",
  "title": "가정한 영향 계수의 민감도 비교",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "계수",
    "민감도",
    "시나리오",
    "영향량"
  ],
  "keywords_en": [
    "linear-scenario-sensitivity",
    "dependency-coefficient-sensitivity"
  ],
  "problem_structure": "linear-scenario-sensitivity",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "예측 확정보다 모델 가정의 민감도 비교가 목적이다.",
  "do_not_use_when": "가정 계수의 곱을 검증된 인과 추정이나 손실 예측으로 제시하지 않는다.",
  "data_required": [
    "delta는 소수 문자열 입력 변화량, coefficients는 소수 문자열 배열(무차원)이다. 하나의 직렬 경로만 다루며 output=delta×모든 계수다. null 계수는 미확인이다."
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
  "path": "cases/DEPENDENCY/dependency-coefficient-sensitivity.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "직렬 경로의 계수 가정에 따른 영향량을 계산한다",
    "input_structure": "입력 변화량과 무차원 계수 배열",
    "hard_constraint": "단일 직렬 경로만; 인과성 주장 금지",
    "validation": "분수 곱·확인된0·미확인 계수"
  }
}
```

## 1. 창작 업무 요청

“입력 감소가 여러 단계에 전파된다는 가정의 계수를 바꾸면 결과가 얼마나 달라지는지 보고 싶다.”

## 2. 다른 원인과 목표

- 예측 확정보다 모델 가정의 민감도 비교가 목적이다.
- 계수에 경험 근거가 없을 수 있다.
- 여러 경로를 더하면 같은 영향을 이중 집계할 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 계수는 실측 추정인가 가정인가? → 가정이면 모든 출력에 시나리오라고 표시한다.
2. 경로 효과를 더할 수 있는가? → 공유 원인을 중복 집계할 수 있으면 합산하지 않는다.
3. 단위가 단계마다 일관적인가? → 비율 계수인지 단위 변환 계수인지 확인한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

delta는 소수 문자열 입력 변화량, coefficients는 소수 문자열 배열(무차원)이다. 하나의 직렬 경로만 다루며 output=delta×모든 계수다. null 계수는 미확인이다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "delta": "10",
  "coefficients": [
    "0.5",
    "0.4"
  ]
}
```

## 5. 기준 방법과 개선 조건

Decimal 또는 분수로 직렬 경로의 곱을 계산하고 계수 변경 시나리오와 비교한다. 인과성·실제 예측 정확도를 주장하지 않는다. 네트워크 합산은 별도 검증이 필요하다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

입력 변화·가정 계수 → 시나리오 출력 → 담당자가 민감한 가정부터 추가 조사한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"delta":"10","coefficients":["0.5","0.4"]}` | `"2"` | 10×0.5×0.4=2. |
| boundary | `{"delta":"10","coefficients":["0","0.4"]}` | `"0"` | 확인된 0 계수는 전파 0이다. |
| missing | `{"delta":"10","coefficients":[null,"0.4"]}` | `"unknown"` | 미확인 계수를 0으로 바꾸지 않는다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 가정 계수의 곱을 검증된 인과 추정이나 손실 예측으로 제시하지 않는다.
- 다중 경로 효과를 독립성 검토 없이 합산하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 가정과 관측값을 구분해 추가 조사 대상을 정할 수 있는가?
2. 계수 변경에 따른 결과 차이가 단위와 함께 명확한가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 수치 계산이 맞다는 것과 모델이 현실에 맞다는 것은 어떻게 다른가?
2. 가장 민감한 계수의 근거를 어떻게 확보할 것인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/decimal.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
