# 확률로 오인하지 않는 수요 시나리오

```json
{
  "id": "scenario-demand",
  "title": "확률로 오인하지 않는 수요 시나리오",
  "family": "ANALYTICS",
  "keywords_ko": [
    "확률로 오인하지 않는 수요 시나리오",
    "scenario-analysis"
  ],
  "keywords_en": [
    "scenario-analysis",
    "scenario-demand"
  ],
  "problem_structure": "scenario-analysis",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 지역 공구대여소가 다음 달 예약 증가율을 아직 모르지만 재고 계획용 하한·기준·상한을 보고 싶다.",
  "do_not_use_when": "세 숫자를 95% 신뢰구간으로 부르거나 평균만 보여주지 않는다. 실측 자료 없이 AI 예측 정확도를 주장하지 않는다.",
  "data_required": [
    "행=계획기간, 키 period; base 정수 예약건, rates는 정렬된 세 개 정수 백분율. null base는 unknown. fixture는 산출 수요를 올림하지 않고 소수 허용한 기대규모로 출력. 개선=대여기간 분포."
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
  "path": "cases/analytics/scenario-demand.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "scenario-demand",
  "test_count": 3,
  "decision_signature": {
    "decision": "확률로 오인하지 않는 수요 시나리오",
    "input_structure": "행=계획기간, 키 period; base 정수 예약건, rates는 정렬된 세 개 정수 백분율. null base는 unknown. fixture는 산출 수요를 올림하지 않고 소수 허용한 기대규모로 출력. 개선=대여기간 분포.",
    "hard_constraint": "세 숫자를 95% 신뢰구간으로 부르거나 평균만 보여주지 않는다. 실측 자료 없이 AI 예측 정확도를 주장하지 않는다.",
    "validation": "80×0.75,1,1.5"
  }
}
```

## 1. 독립 창작 요청

창작: 지역 공구대여소가 다음 달 예약 증가율을 아직 모르지만 재고 계획용 하한·기준·상한을 보고 싶다.

## 2. 경쟁 가설

수요 불확실성; 재고 부족; 시나리오를 예측 확률로 착각. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 증가율은 관측 추정인가 가정인가? → 가정이면 신뢰구간이라고 표시하지 않는다.
2. 단위는 예약건인가 대여일수인가? → 재고는 대여기간을 추가해야 계산 가능.
3. 음수 수요를 허용하는 모델인가? → 최소0 바닥 처리 여부를 정책으로 합의.

## 4. 데이터 계약과 부재 대안

행=계획기간, 키 period; base 정수 예약건, rates는 정렬된 세 개 정수 백분율. null base는 unknown. fixture는 산출 수요를 올림하지 않고 소수 허용한 기대규모로 출력. 개선=대여기간 분포.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

각 rate에 base×(1+rate/100)를 계산한다. 가정 범위에 대한 민감도이며 발생확률은 없다. rates<-100은 invalid. 재고 최적화로 넘기기 전 대여기간 필수.

개선: 기간·취소율 시나리오를 추가하되 조합 수를 제한하고 출처/가정 태그를 유지한다.

## 6. 최소 구현과 다음 행동

기준 예약건과 가정→세 경우 계산→범위와 가정→운영자가 재고 추가조사 결정. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `scenario-demand` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"base":80,"rates":[-25,0,50]}`|`[60, 80, 120]`|80×0.75,1,1.5|
|boundary|`{"base":80,"rates":[-100,0,0]}`|`[0, 80, 80]`|−100%는0|
|missing|`{"base":null,"rates":[-25,0,50]}`|`"unknown"`|기준값 미수집|

## 8. 오용·도구·축소

세 숫자를 95% 신뢰구간으로 부르거나 평균만 보여주지 않는다. 실측 자료 없이 AI 예측 정확도를 주장하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 기간·취소율 시나리오를 추가하되 조합 수를 제한하고 출처/가정 태그를 유지한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 상한이 발생하면 어떤 행동을 하겠습니까?
- 이 증가율 가정을 바꿔야 할 근거가 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 가정과 추정치의 차이를 설명하십시오.
- 재고수량을 바로 산출하지 않은 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
