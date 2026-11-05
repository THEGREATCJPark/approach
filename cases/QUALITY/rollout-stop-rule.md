# 단계 전환의 확대·유지·되돌림 규칙

```json
{
  "id": "rollout-stop-rule",
  "title": "단계 전환의 확대·유지·되돌림 규칙",
  "family": "QUALITY",
  "keywords_ko": [
    "단계 전환의 확대·유지·되돌림 규칙",
    "시범 전환 후 다음 단계로 확대할지 판정한다"
  ],
  "keywords_en": [
    "rollout-stop-rule",
    "stage observation × count × critical events"
  ],
  "problem_structure": "stage observation × count × critical events",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 재활용 상자 포장 방법을 단계적으로 바꾸는 운영팀이 시범 결과에 따라 확대하거나 되돌릴 규칙을 명확히 하려 한다.",
  "do_not_use_when": "100건 통과를 모집단 품질 보증으로 주장하지 않는다. 확대와 되돌림을 외부에서 자동 실행하지 않는다. 집계 미완료이면 unknown을 표시한다.",
  "data_required": [
    "필수 필드는 stage_id, observed(정수 개체수), defective(정수 개체수), critical(정수 사건수)이다. 한 객체는 한 단계의 관측 기간이다. null은 미집계다. critical과 defective의 분모가 같을 필요는 없지만 기간은 동일해야 한다. 예제 기준은 일반 안전 표준이 아니다."
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
  "path": "cases/QUALITY/rollout-stop-rule.md",
  "decision_signature": {
    "decision": "시범 전환 후 다음 단계로 확대할지 판정한다",
    "input_structure": "stage observation × count × critical events",
    "hard_constraint": "중대 사건이 우선이며 최소 관측수와 사전 정지 기준을 지킨다",
    "validation": "경계 비율과 관측 부족을 분리한다"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 재활용 상자 포장 방법을 단계적으로 바꾸는 운영팀이 시범 결과에 따라 확대하거나 되돌릴 규칙을 명확히 하려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 몇 건의 관측만 좋아도 성급히 확대한다.
- 평균 불량률이 중대 사건을 가린다.
- 결과를 본 뒤 정지 기준을 수정한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 어떤 사건은 비율과 관계없이 중단하는가? | 본 예제는 critical이 1 이상이면 즉시 rollback이다. |
| 확대 전 최소 관측수는 얼마인가? | 본 예제는 100이며 부족하면 hold다. |
| 5% 경계는 확대 가능한가? | 이 합성 정책은 5% 이하가 가능하다. 실제 정책 확인은 필수다. |

## 4. 데이터와 없을 때의 대안
필수 필드는 stage_id, observed(정수 개체수), defective(정수 개체수), critical(정수 사건수)이다. 한 객체는 한 단계의 관측 기간이다. null은 미집계다. critical과 defective의 분모가 같을 필요는 없지만 기간은 동일해야 한다. 예제 기준은 일반 안전 표준이 아니다.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "observed": 100,
  "defective": 2,
  "critical": 0
}
```

## 5. 기준 방법과 개선 조건
유효성 확인 후 중대 사건이면 rollback, 관측 미달이면 hold, 비율이 5%를 초과하면 rollback, 그 외에는 advance다. 확대 제안만 표시하고 실제 전환 승인은 담당자가 한다.

제품 위험과 표본 설계를 반영한 신뢰한계나 순차검정이 필요하면 별도 전문 검토를 한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 시범 전환 후 다음 단계로 확대할지 판정한다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `"advance"` | 관측100,불량2%,중대0. |
| 경계 | `{"defective": 5}` | `"advance"` | 5%포함. |
| 정보 부족 | `{"defective": null}` | `"unknown"` | 불량집계미완료. |
| 불충분 | `{"observed": 50}` | `"hold"` | 관측50<100. |
| 중대사건 | `{"critical": 1}` | `"rollback"` | 평균율보다중대사건우선. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
100건 통과를 모집단 품질 보증으로 주장하지 않는다. 확대와 되돌림을 외부에서 자동 실행하지 않는다. 집계 미완료이면 unknown을 표시한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- hold와 rollback에서 필요한 행동을 구분할 수 있는가?
- 중대 사건 한 건이 있으면 즉시 검토로 넘어가는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 사전 기준을 고정했다는 증거는 어디 있는가?
- advance가 통계적 동등성 입증이 아닌 이유는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/decimal.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
