# 권한 범위를 넘는 보상 요청 이관

```json
{
  "id": "escalation-authority",
  "title": "권한 범위를 넘는 보상 요청 이관",
  "family": "SUPPORT",
  "keywords_ko": [
    "권한 범위를 넘는 보상 요청 이관",
    "authority-routing"
  ],
  "keywords_en": [
    "authority-routing",
    "escalation-authority"
  ],
  "problem_structure": "authority-routing",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공유 공방 접수자가 분실물 보상 요청을 받았을 때 본인 처리 범위와 승인 담당자 이관을 구별한다.",
  "do_not_use_when": "낮은 금액으로 특별사고 이관을 상쇄하지 않는다. 정책을 코드 상수로 추정하지 않는다.",
  "data_required": [
    "행=보상 요청, 키 request_id; amount/limit 정수 예산통화 단위, special 불리언. null amount는 미확정. limit은 승인된 권한표에서 제공. 개선=정책버전·승인자. 이관 제안만 반환."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "repair-slack"
  ],
  "depth": "standard",
  "path": "cases/support/escalation-authority.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "escalation-authority",
  "test_count": 6,
  "decision_signature": {
    "decision": "권한 범위를 넘는 보상 요청 이관",
    "input_structure": "행=보상 요청, 키 request_id; amount/limit 정수 예산통화 단위, special 불리언. null amount는 미확정. limit은 승인된 권한표에서 제공. 개선=정책버전·승인자. 이관 제안만 반환.",
    "hard_constraint": "낮은 금액으로 특별사고 이관을 상쇄하지 않는다. 정책을 코드 상수로 추정하지 않는다.",
    "validation": "80≤100"
  }
}
```

## 1. 독립 창작 요청

창작: 공유 공방 접수자가 분실물 보상 요청을 받았을 때 본인 처리 범위와 승인 담당자 이관을 구별한다.

## 2. 경쟁 가설

금액한도 초과; 사고유형 예외; 금액 미확정. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 한도와 같은 금액은 권한 내입니까? → 포함 규칙 확정.
2. 특별 사고는 금액과 무관하게 이관합니까? → 필수 이관을 먼저 평가.
3. 보상액 미확정이면 추정액으로 진행합니까? → 아니면 estimate_required.

## 4. 데이터 계약과 부재 대안

행=보상 요청, 키 request_id; amount/limit 정수 예산통화 단위, special 불리언. null amount는 미확정. limit은 승인된 권한표에서 제공. 개선=정책버전·승인자. 이관 제안만 반환.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

계약 보완: special=null 또는 일반건의 limit=null은 unknown이다. 특별이관 여부를 모르는 상태에서 낮은 금액만 보고 within_authority를 확정하지 않는다.

## 5. 기준 방법과 개선 조건

special이면 escalate, 그렇지 않고 금액 미확정이면 estimate_required, amount≤limit이면 within_authority, 초과면 escalate. 실제 지급 승인과는 다르다.

개선: 사고유형별 권한표와 다단계 승인 경로를 명시적 결정표로 만든다.

## 6. 최소 구현과 다음 행동

요청금액/유형→권한검사→이관처 및 사유→담당자가 승인 요청. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `escalation-authority` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"amount":80,"limit":100,"special":false}`|`"within_authority"`|80≤100|
|boundary|`{"amount":100,"limit":100,"special":false}`|`"within_authority"`|동일한도포함|
|missing|`{"amount":null,"limit":100,"special":false}`|`"estimate_required"`|금액미확정|
|override|`{"amount":1,"limit":100,"special":true}`|`"escalate"`|특별사고우선|

|unknown_override|`{"amount":80,"limit":100,"special":null}`|`"unknown"`|특별이관조건미확인시권한내확정금지|
|missing_limit|`{"amount":80,"limit":null,"special":false}`|`"unknown"`|권한한도미확인|

## 8. 오용·도구·축소

낮은 금액으로 특별사고 이관을 상쇄하지 않는다. 정책을 코드 상수로 추정하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 사고유형별 권한표와 다단계 승인 경로를 명시적 결정표로 만든다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 이관 사유로 승인 요청을 작성할 수 있습니까?
- 권한표 버전이 실제 적용일과 맞습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 경계 포함을 어떤 근거로 정했습니까?
- 권한 안이라는 결과와 지급 승인 차이는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
