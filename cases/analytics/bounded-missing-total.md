# 누락 수량이 있는 총량의 가능 범위

```json
{
  "id": "bounded-missing-total",
  "title": "누락 수량이 있는 총량의 가능 범위",
  "family": "ANALYTICS",
  "keywords_ko": [
    "누락 수량이 있는 총량의 가능 범위",
    "partial-identification"
  ],
  "keywords_en": [
    "partial-identification",
    "bounded-missing-total"
  ],
  "problem_structure": "partial-identification",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 야외 독서행사에서 일부 시간대 입장 계수가 누락됐다. 담당자는 확정 총량 대신 가능한 범위를 발표하려 한다.",
  "do_not_use_when": "누락을0이라고 확정하거나 관측 평균 대체를 실제 총량으로 발표하지 않는다.",
  "data_required": [
    "행=중복 없는 시간구간, 키 slot_id; counts는 정수 인원 또는 null, cap은 누락구간별 공통 최대 인원 정수. fixture에서 슬롯은 배열 위치. null cap은 상한 미확인. 개선=개별 슬롯 상한."
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
  "path": "cases/analytics/bounded-missing-total.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "bounded-missing-total",
  "test_count": 3,
  "decision_signature": {
    "decision": "누락 수량이 있는 총량의 가능 범위",
    "input_structure": "행=중복 없는 시간구간, 키 slot_id; counts는 정수 인원 또는 null, cap은 누락구간별 공통 최대 인원 정수. fixture에서 슬롯은 배열 위치. null cap은 상한 미확인. 개선=개별 슬롯 상한.",
    "hard_constraint": "누락을0이라고 확정하거나 관측 평균 대체를 실제 총량으로 발표하지 않는다.",
    "validation": "관측13,누락1×10"
  }
}
```

## 1. 독립 창작 요청

창작: 야외 독서행사에서 일부 시간대 입장 계수가 누락됐다. 담당자는 확정 총량 대신 가능한 범위를 발표하려 한다.

## 2. 경쟁 가설

누락이0으로 집계됨; 누락구간 상한 없음; 중복 시간대. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 누락구간별 상한을 근거로 정할 수 있습니까? → 없으면 상한 unknown.
2. 이미 측정된 값은 확정입니까? → 아니면 측정오차 범위까지 분리.
3. 누락이 많은 시간대에 집중됐습니까? → 평균 대체 대신 범위 보고.

## 4. 데이터 계약과 부재 대안

행=중복 없는 시간구간, 키 slot_id; counts는 정수 인원 또는 null, cap은 누락구간별 공통 최대 인원 정수. fixture에서 슬롯은 배열 위치. null cap은 상한 미확인. 개선=개별 슬롯 상한.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

하한=관측 합계, 상한=관측 합계+누락 개수×cap. cap 없고 누락 있으면 상한 null. 음수는 invalid. 하한은 누락값 비음수라는 가정에 의존한다.

개선: 구간별 상한과 센서 오류범위를 반영하고 누락 원인을 별도 분석한다.

## 6. 최소 구현과 다음 행동

구간 계수→누락 수 확인→[하한,상한]과 미관측 수→담당자가 추가 확인 또는 범위 발표. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `bounded-missing-total` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"counts":[8,null,5],"cap":10}`|`[13, 23]`|관측13,누락1×10|
|boundary|`{"counts":[0,0],"cap":10}`|`[0, 0]`|미관측없음|
|missing|`{"counts":[8,null],"cap":null}`|`[8, null]`|상한 근거 없음|

## 8. 오용·도구·축소

누락을0이라고 확정하거나 관측 평균 대체를 실제 총량으로 발표하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 구간별 상한과 센서 오류범위를 반영하고 누락 원인을 별도 분석한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 이 범위로 운영 결정을 할 수 있습니까?
- 상한 근거를 설명할 자료가 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 하한이 성립하는 가정은 무엇입니까?
- 상한 없음과 무한대는 어떻게 다르게 표시했습니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
