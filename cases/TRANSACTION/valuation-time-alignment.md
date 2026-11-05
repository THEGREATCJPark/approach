# 수량 시점과 단가 시점의 일치 검사

```json
{
  "id": "valuation-time-alignment",
  "title": "수량 시점과 단가 시점의 일치 검사",
  "family": "TRANSACTION",
  "keywords_ko": [
    "수량",
    "시점과",
    "단가",
    "시점의",
    "일치",
    "검사"
  ],
  "keywords_en": [
    "temporal-join",
    "valuation-time-alignment"
  ],
  "problem_structure": "temporal-join",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 재료 교환 현황에서 서로 다른 날의 수량과 단가를 섞은 평가액을 확정값으로 보여주지 않게 해 달라.",
  "do_not_use_when": "총량·가용량·평가액을 동일 개념으로 취급하지 않는다. 오래된 단가로 최신 확정액 주장 금지.",
  "data_required": [
    "최소: quantity 정수개, unit_price 정수토큰/개, quantity_time와price_time ISO UTC 문자열. 한 행 item_id. null은 unknown. fixture는 canonical timestamp만 허용. 개선: 유효구간·버전·통화."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "transaction-rounding"
  ],
  "depth": "standard",
  "path": "cases/TRANSACTION/valuation-time-alignment.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "temporal-join",
    "input_structure": "최소: quantity 정수개, unit_price 정수토큰/개, quantity_time와price_time ISO UTC 문자열. 한 행 item_id. null은 unknown. fixture는 canonical timestamp만 허용. 개선: 유효구간·버전·통화.",
    "hard_constraint": "총량·가용량·평가액을 동일 개념으로 취급하지 않는다. 오래된 단가로 최신 확정액 주장 금지.",
    "validation": "4*7=28 동일시점; 수량0이어도 시점게이트 적용; 단가없음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 재료 교환 현황에서 서로 다른 날의 수량과 단가를 섞은 평가액을 확정값으로 보여주지 않게 해 달라.

가능한 설명: 수량과가격 기준시점이 다르다; 단위가 다르다; 최신 값이 비었는데 과거 값을 몰래 사용한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 동일 시점만 허용합니까? → 이번 예제 정확히 같은 timestamp.
2. 단가 단위가 수량 단위와 같습니까? → 아니면 명시 환산.
3. 시점 불일치는 참고값으로 표시할까요? → 확정액은 보류하고 별도 hypothetical 가능.

## 3. 데이터 계약과 자료 부족 대안

최소: quantity 정수개, unit_price 정수토큰/개, quantity_time와price_time ISO UTC 문자열. 한 행 item_id. null은 unknown. fixture는 canonical timestamp만 허용. 개선: 유효구간·버전·통화. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 시점 다르면 stale, 같으면 quantity*unit_price. null은 unknown; 미래시점 검사는 기준now 제공 후 별도.

개선: 실제 시간 문자열은 timezone-aware 정규화, 유효구간 join; 임의 nearest matching 금지.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

수량·단가·시점 → 정합 게이트 → 평가액 또는 stale/unknown → 담당자가 같은 시점 자료 요청. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"quantity":4,"unit_price":7,"quantity_time":"2026-01-01T00:00:00Z","price_time":"2026-01-01T00:00:00Z"}`|`28`|4*7=28 동일시점|
|boundary|`{"quantity":0,"unit_price":7,"quantity_time":"2026-01-01T00:00:00Z","price_time":"2026-01-02T00:00:00Z"}`|`"stale"`|수량0이어도 시점게이트 적용|
|missing|`{"quantity":4,"unit_price":null,"quantity_time":"2026-01-01T00:00:00Z","price_time":"2026-01-01T00:00:00Z"}`|`"unknown"`|단가없음|

## 7. 흔한 오류와 범위 축소

총량·가용량·평가액을 동일 개념으로 취급하지 않는다. 오래된 단가로 최신 확정액 주장 금지. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- stale에서 어떤 자료를 갱신해야 하는지 알 수 있습니까?
- 참고 평가와 확정 평가를 분리할 필요가 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 산술이 맞아도 결과가 유효하지 않은 사례를 설명하십시오.
- timestamp 문자열 비교를 넘어 실제 시스템에 필요한 정규화는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
