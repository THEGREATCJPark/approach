# 개관일 수가 다른 전시실 이용량 비교

```json
{
  "id": "open-day-rate",
  "title": "개관일 수가 다른 전시실 이용량 비교",
  "family": "ANALYTICS",
  "keywords_ko": [
    "기간 비교",
    "분모",
    "영업일",
    "실적"
  ],
  "keywords_en": [
    "aggregation",
    "open-day-rate"
  ],
  "problem_structure": "aggregation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 이동 전시 운영자가 두 전시실의 월 방문 합계를 보고 다음 달 안내 인력을 배정하려 한다. 휴관일이 달라 합계가 같은 의미인지 불분명하다.",
  "do_not_use_when": "월 합계만으로 혼잡도를 단정하거나 휴관일을 0 방문일로 넣지 않는다. 예측 모델은 관측 기준 합의 전 사용하지 않는다.",
  "data_required": [
    "최소: room_id 문자열, visits 정수(명), open_days 정수(일), complete 불리언. 한 행은 전시실×비교 기간. 기간과 room_id가 키. complete=false/null은 수집 미완료. 개선: 개관시간·시간대별 인원. 개인정보는 불필요."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "counter-reset"
  ],
  "depth": "deep",
  "path": "cases/analytics/open-day-rate.md",
  "test_count": 7,
  "fixture_path": "examples/synthetic/open-day-rate.json"
}
```

## 요청과 가설

창작: 이동 전시 운영자가 두 전시실의 월 방문 합계를 보고 다음 달 안내 인력을 배정하려 한다. 휴관일이 달라 합계가 같은 의미인지 불분명하다.

가능한 원인: 운영일 수 차이; 하루 수요 차이; 집계 누락.

## 먼저 가를 질문과 계획 변경

1. 인력 배정은 월 총량인가, 열린 날의 혼잡도인가? → 총량이면 원합계, 혼잡도이면 개관일당 수치를 주 지표로 한다.
2. 개관일에 0명은 실제 0인가? → 미수집이면 비교를 보류한다.
3. 부분 개관일이 있는가? → 있으면 일 대신 개관시간 분모로 전환한다.

## 데이터 계약

최소: room_id 문자열, visits 정수(명), open_days 정수(일), complete 불리언. 한 행은 전시실×비교 기간. 기간과 room_id가 키. complete=false/null은 수집 미완료. 개선: 개관시간·시간대별 인원. 개인정보는 불필요.

소형 fixture 어댑터: `visits`는 계약과 동일, `days`는 `open_days`, `complete`는 동일 필드다. 기간과 room_id는 단일 건 시험에서는 고정이며 여러 건 시험의 groups 첫 열이 room_id다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 검증된 개관일당 방문수 visits/open_days를 두 기간에서 비교한다. 분모 0이면 undefined, 결측이면 unknown, 음수이면 invalid로 표시한다.

개선 조건: 시간대별 표준화와 혼잡 분위수를 추가하되 비교 가능한 운영시간이 확보된 뒤 진행한다.

최소 경로: 기간별 집계 파일 → 결측/분모 점검 → 원합계와 일평균 병기 → 담당자가 인력 재배치 후보를 선택한다.

제약과 우선순위: 목적은 비교 기준 확인이며 최적화는 하지 않는다. 필수: 동일 방문 정의와 기간. 선호: 상세 시간대. 필수조건 미충족이면 순위를 숨긴다.

추가 fixture 스키마: 추가 순서변경 fixture의 `groups`는 [전시실 ID, 방문수, 개관일수] 행 배열이며 출력은 ID별 일평균 매핑이다. 이는 단일 집계 계약을 여러 ID에 적용한 독립 계산이다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/open-day-rate.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"visits":480,"days":12,"complete":true}`|`40`|480÷12=40명/일|
|boundary|`{"visits":0,"days":5,"complete":true}`|`0`|측정된 0÷5=0|
|missing|`{"visits":480,"days":null,"complete":true}`|`"unknown"`|분모 미수집|
|conflict|`{"visits":2,"days":0,"complete":true}`|`"invalid"`|개관 0일에 방문 2명은 계약 충돌|
|period_comparison|`{"visits":600,"days":20,"complete":true}`|`30`|합계 600>480이나 30<40|
|new_sample|`{"visits":225,"days":9,"complete":false}`|`"unknown"`|미완료를 25로 확정하지 않음|
|reorder|`{"groups":[["b",600,20],["a",480,12]]}`|`{"a": 40, "b": 30}`|행순서를 뒤집어도 키별 개관일당 값은 a=40,b=30|

비교 쌍: normal의 관측 480/12=40과 missing의 days=null은 각각 40과 unknown이어야 한다. boundary의 실제 visits=0은 0이며 결측과 다르다.

## 오류·도구·범위

월 합계만으로 혼잡도를 단정하거나 휴관일을 0 방문일로 넣지 않는다. 예측 모델은 관측 기준 합의 전 사용하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 기간별 집계 파일 → 결측/분모 점검 → 원합계와 일평균 병기 → 담당자가 인력 재배치 후보를 선택한다. 180분에는 시간대별 표준화와 혼잡 분위수를 추가하되 비교 가능한 운영시간이 확보된 뒤 진행한다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 일평균과 합계가 반대 방향일 때 어느 인력 결정을 내리겠습니까?
- 개관일 누락 표시를 보고 자료 담당자에게 무엇을 요청하겠습니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 분모 선택을 바꾼 담당자 답변을 기록에서 보여줄 수 있습니까?
- 이 계산이 현장 대기시간 감소를 증명하지 못하는 이유는 무엇입니까?

## 측정과 한계

분모 누락 탐지율과 계산 오류 수를 측정할 수 있다. 실제 배치 개선·대기 감소는 현장 전후 관찰 없이는 주장하지 않는다.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/decimal.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
