# 신규 공급원 시범 전환량의 노출 상한

```json
{
  "id": "trial-exposure-cap",
  "title": "신규 공급원 시범 전환량의 노출 상한",
  "family": "QUALITY",
  "keywords_ko": [
    "신규 공급원 시범 전환량의 노출 상한",
    "승인된 시범 수량 범위에서 포장 단위 전환량을 계산한다"
  ],
  "keywords_en": [
    "trial-exposure-cap",
    "demand × qualified cap × loss budget × pack size"
  ],
  "problem_structure": "demand × qualified cap × loss budget × pack size",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 소규모 인쇄물 보관 업무가 새 완충재를 시범 도입하려 하지만 한 번에 너무 많은 물량이 노출되지 않도록 수량을 정하려 한다.",
  "do_not_use_when": "발주 부족을 막는 올림과 위험 상한을 지키는 내림을 혼동하지 않는다. 기대손실 예측이라고 부르지 않는다. 상한이 미승인이면 수량 계산을 보류한다.",
  "data_required": [
    "필수 필드는 demand와 qualified_cap(정수 개수), budget와 loss_per_unit(동일 통화), pack(양의 정수 개수)이다. 한 객체는 한 전환 검토 품목이다. null qualified_cap은 미승인이다. 실제 도입에는 별도 승인이 필요하다. 기존 공급 잔여량은 demand에서 trial을 뺀 값이다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [],
  "depth": "standard",
  "path": "cases/QUALITY/trial-exposure-cap.md",
  "decision_signature": {
    "decision": "승인된 시범 수량 범위에서 포장 단위 전환량을 계산한다",
    "input_structure": "demand × qualified cap × loss budget × pack size",
    "hard_constraint": "품질 승인 한도와 손실 예산을 모두 준수한다",
    "validation": "예산 상한과 팩 단위 내림을 반영한다"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 소규모 인쇄물 보관 업무가 새 완충재를 시범 도입하려 하지만 한 번에 너무 많은 물량이 노출되지 않도록 수량을 정하려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 전체 수요를 곧바로 신규 재료로 전환한다.
- 시험 승인 수량과 구매 팩 단위를 혼동한다.
- 손실 예산이 평균 가격만으로 설정되어 있다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 품질 담당자가 승인한 시범 상한은 얼마인가? | 미확정이면 시범량은 unknown이다. 계산이 승인을 대체하지 않는다. |
| 개당 노출금액은 구매가인가 최대 검토 손실인가? | 정의된 동일 기준으로 예산을 환산한다. |
| 팩을 분할할 수 있는가? | 불가하면 상한 이하 팩 수로 내린다. 최소 한 팩도 불가하면 0과 사유를 표시한다. |

## 4. 데이터와 없을 때의 대안
필수 필드는 demand와 qualified_cap(정수 개수), budget와 loss_per_unit(동일 통화), pack(양의 정수 개수)이다. 한 객체는 한 전환 검토 품목이다. null qualified_cap은 미승인이다. 실제 도입에는 별도 승인이 필요하다. 기존 공급 잔여량은 demand에서 trial을 뺀 값이다.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "demand": 120,
  "qualified_cap": 50,
  "budget": 300,
  "loss_per_unit": 8,
  "pack": 10
}
```

## 5. 기준 방법과 개선 조건
수요, 승인 상한, 예산/개당 손실 중 최솟값을 구한 뒤 팩 크기의 배수로 내린다. 기존 공급 잔여량과 검토 노출액을 같이 표시한다.

복수 품목과 공통 예산이 생기면 정수 배정 문제로 확장하되 품목별 품질 상한을 유지한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 승인된 시범 수량 범위에서 포장 단위 전환량을 계산한다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"trial": 30, "existing": 90, "exposure": 240}` | min(120,50,300/8)=37.5;10개팩내림30. |
| 경계 | `{"budget": 320}` | `{"trial": 40, "existing": 80, "exposure": 320}` | 예산경계에서40개. |
| 정보 부족 | `{"qualified_cap": null}` | `"unknown"` | 승인된상한없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
발주 부족을 막는 올림과 위험 상한을 지키는 내림을 혼동하지 않는다. 기대손실 예측이라고 부르지 않는다. 상한이 미승인이면 수량 계산을 보류한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 신규량과 기존량의 합이 수요와 맞는지 확인할 수 있는가?
- 예산이 남아도 더 전환하지 못하는 제약을 알 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 발주 사례와 달리 내림한 이유를 설명할 수 있는가?
- 이 노출액이 실제 손실 예측이 아닌 이유는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/decimal.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
