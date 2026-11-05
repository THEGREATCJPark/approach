# 환산 기준일이 있는 구매비용 비교

```json
{
  "id": "currency-basis",
  "title": "환산 기준일이 있는 구매비용 비교",
  "family": "ANALYTICS",
  "keywords_ko": [
    "환산 기준일이 있는 구매비용 비교",
    "normalization"
  ],
  "keywords_en": [
    "normalization",
    "currency-basis"
  ],
  "problem_structure": "normalization",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 극장 소품 담당자가 서로 다른 통화로 받은 재료 견적을 같은 기준일의 예산통화로 비교한다.",
  "do_not_use_when": "숫자만 더하거나 서로 다른 날짜의 환율을 조용히 섞지 않는다. 출처 없는 환율 API를 기본 호출하지 않는다.",
  "data_required": [
    "행=견적 1건, 키 quote_id; amount는 십진 문자열 원통화 금액, rate는 원통화 1단위당 예산통화 십진 문자열, basis는 평가일. null rate는 미확인. fixture는 동일 basis인 amount/rate만 받는다. 개선자료=세금·운송료. 공급자 개인정보는 불필요."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "open-day-rate"
  ],
  "depth": "standard",
  "path": "cases/analytics/currency-basis.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "currency-basis",
  "test_count": 3,
  "decision_signature": {
    "decision": "환산 기준일이 있는 구매비용 비교",
    "input_structure": "행=견적 1건, 키 quote_id; amount는 십진 문자열 원통화 금액, rate는 원통화 1단위당 예산통화 십진 문자열, basis는 평가일. null rate는 미확인. fixture는 동일 basis인 amount/rate만 받는다. 개선자료=세금·운송료. 공급자 개인정보는 불필요.",
    "hard_constraint": "숫자만 더하거나 서로 다른 날짜의 환율을 조용히 섞지 않는다. 출처 없는 환율 API를 기본 호출하지 않는다.",
    "validation": "12.50×1.24=15.5000"
  }
}
```

## 1. 독립 창작 요청

창작: 작은 극장 소품 담당자가 서로 다른 통화로 받은 재료 견적을 같은 기준일의 예산통화로 비교한다.

## 2. 경쟁 가설

환율 기준일 차이; 세금 포함 범위 차이; 통화 코드 누락. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 견적일 환율인가 공통 평가일 환율인가? → 공통일이면 해당 rate_id로 모두 재계산.
2. 세금과 운송료가 포함됐는가? → 아니면 원가 합계 대신 재료값 비교로 범위 표시.
3. 환율이 없는 통화를 제외해도 되는가? → 아니면 전체 순위 보류.

## 4. 데이터 계약과 부재 대안

행=견적 1건, 키 quote_id; amount는 십진 문자열 원통화 금액, rate는 원통화 1단위당 예산통화 십진 문자열, basis는 평가일. null rate는 미확인. fixture는 동일 basis인 amount/rate만 받는다. 개선자료=세금·운송료. 공급자 개인정보는 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

Decimal 문자열 곱 amount×rate를 예산통화 소수 둘째 자리 half-up 반올림. 음수 금액은 이 견적 계약에서 invalid, 환율 미확인은 unknown. 필수조건은 동일 평가일/비용 범위; 선호는 더 낮은 금액.

개선: 세금·배송 조건을 별도 열로 맞춘 뒤 총 도착원가를 계산한다. 환율 전망 모델은 필요하지 않다.

## 6. 최소 구현과 다음 행동

견적→환율 근거 확인→원금액/환율/환산값→담당자가 비교 가능한 견적만 선택. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `currency-basis` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"amount":"12.50","rate":"1.24"}`|`"15.50"`|12.50×1.24=15.5000|
|boundary|`{"amount":"0.005","rate":"1"}`|`"0.01"`|half-up 둘째자리|
|missing|`{"amount":"12.50","rate":null}`|`"unknown"`|환율 없음|

## 8. 오용·도구·축소

숫자만 더하거나 서로 다른 날짜의 환율을 조용히 섞지 않는다. 출처 없는 환율 API를 기본 호출하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 세금·배송 조건을 별도 열로 맞춘 뒤 총 도착원가를 계산한다. 환율 전망 모델은 필요하지 않다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 이 환율 기준일로 실제 예산 결정을 해도 됩니까?
- 비교에서 제외한 비용 항목이 무엇입니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 반올림 시점과 방식은 어디서 정했습니까?
- 환산값이 싸다고 총원가도 싸다고 할 수 없는 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
