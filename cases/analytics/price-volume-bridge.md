# 매출 차이를 가격과 물량으로 분해

```json
{
  "id": "price-volume-bridge",
  "title": "매출 차이를 가격과 물량으로 분해",
  "family": "ANALYTICS",
  "keywords_ko": [
    "매출 차이를 가격과 물량으로 분해",
    "decomposition"
  ],
  "keywords_en": [
    "decomposition",
    "price-volume-bridge"
  ],
  "problem_structure": "decomposition",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 인쇄 공방이 두 주의 주문 매출 변화가 단가 조정 때문인지 수량 변화 때문인지 설명한다.",
  "do_not_use_when": "교차효과를 중복 합산하거나 매출 분해를 가격 인상의 인과 효과로 표현하지 않는다.",
  "data_required": [
    "행=동일 품목 두 기간 비교, 키 item_id; p0,p1 십진 단가, q0,q1 정수 수량. fixture 단위는 가상 통화/개. null은 미수집. 개선=품목별 원자료; 고객별 정보 불필요."
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
  "path": "cases/analytics/price-volume-bridge.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "price-volume-bridge",
  "test_count": 3,
  "decision_signature": {
    "decision": "매출 차이를 가격과 물량으로 분해",
    "input_structure": "행=동일 품목 두 기간 비교, 키 item_id; p0,p1 십진 단가, q0,q1 정수 수량. fixture 단위는 가상 통화/개. null은 미수집. 개선=품목별 원자료; 고객별 정보 불필요.",
    "hard_constraint": "교차효과를 중복 합산하거나 매출 분해를 가격 인상의 인과 효과로 표현하지 않는다.",
    "validation": "가격2×5=10,물량12×3=36,96−50=46"
  }
}
```

## 1. 독립 창작 요청

창작: 인쇄 공방이 두 주의 주문 매출 변화가 단가 조정 때문인지 수량 변화 때문인지 설명한다.

## 2. 경쟁 가설

단가 변화; 판매수량 변화; 품목 구성 차이. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 같은 품목인가? → 아니면 품목별 분해 후 합산.
2. 순서에 따른 교차효과 배분을 합의했는가? → 이 예제는 기준물량 가격효과 먼저.
3. 매출에 환불이 포함되는가? → 포함되면 순수량 계약 또는 환불 별도 항목.

## 4. 데이터 계약과 부재 대안

행=동일 품목 두 기간 비교, 키 item_id; p0,p1 십진 단가, q0,q1 정수 수량. fixture 단위는 가상 통화/개. null은 미수집. 개선=품목별 원자료; 고객별 정보 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

가격효과=(p1−p0)q0, 물량효과=p1(q1−q0). 두 효과 합=새 매출−옛 매출. 최적화가 아니라 회계적 항등 분해이며 인과 추정이 아니다.

개선: 품목별 분해와 기준방식 민감도를 제시한다. 복잡한 회귀는 가격 결정 원인을 조사할 때만 검토한다.

## 6. 최소 구현과 다음 행동

기간별 단가/수량→정의 확인→두 효과와 총차이→담당자가 원인 조사할 품목 선택. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `price-volume-bridge` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"p0":10,"p1":12,"q0":5,"q1":8}`|`[10, 36, 46]`|가격2×5=10,물량12×3=36,96−50=46|
|boundary|`{"p0":10,"p1":12,"q0":0,"q1":2}`|`[0, 24, 24]`|기준 수량0 가격효과0|
|missing|`{"p0":10,"p1":null,"q0":5,"q1":8}`|`"unknown"`|신단가 없음|

## 8. 오용·도구·축소

교차효과를 중복 합산하거나 매출 분해를 가격 인상의 인과 효과로 표현하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 품목별 분해와 기준방식 민감도를 제시한다. 복잡한 회귀는 가격 결정 원인을 조사할 때만 검토한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 이 분해 순서가 보고 관례와 맞습니까?
- 매출 변화를 보고 다음에 조사할 것은 무엇입니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 두 효과의 합이 총차이와 같은지 손계산하십시오.
- 분해 순서를 바꾸면 어떤 값이 달라집니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
