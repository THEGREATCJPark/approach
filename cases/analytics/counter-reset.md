# 누적 관측계의 초기화와 단기 사용량

```json
{
  "id": "counter-reset",
  "title": "누적 관측계의 초기화와 단기 사용량",
  "family": "ANALYTICS",
  "keywords_ko": [
    "누적",
    "차분",
    "초기화",
    "계량"
  ],
  "keywords_en": [
    "difference",
    "counter-reset"
  ],
  "problem_structure": "difference",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공방의 공용 압축기 사용계가 누적값만 저장한다. 운영자는 구간별 가동량을 알고 싶지만 계기 교체 때 숫자가 작아졌다.",
  "do_not_use_when": "음수 차분을 절댓값으로 바꾸거나 모든 감소를 고장으로 판정하지 않는다. 보간을 사실처럼 표시하지 않는다.",
  "data_required": [
    "최소: meter_id, timestamp UTC, cumulative 정수(분), reset 불리언. 행은 관측 1건, 키는 meter_id+timestamp. null은 미관측. 개선: 교체 시각/끝값. 계기별로 정렬 후 인접 관측만 차분한다."
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
  "depth": "deep",
  "path": "cases/analytics/counter-reset.md",
  "test_count": 7,
  "fixture_path": "examples/synthetic/counter-reset.json"
}
```

## 요청과 가설

창작: 공방의 공용 압축기 사용계가 누적값만 저장한다. 운영자는 구간별 가동량을 알고 싶지만 계기 교체 때 숫자가 작아졌다.

가능한 원인: 실제 사용량 감소가 아닌 계기 초기화; 관측 순서 오류; 센서 누락.

## 먼저 가를 질문과 계획 변경

1. 음의 차이가 초기화인가 정정인가? → 초기화 로그가 있으면 구간 보류, 정정이면 버전 재계산.
2. 교체 전 마지막 값이 있는가? → 없으면 교체를 가로지르는 사용량 확정 금지.
3. 초기값 0을 믿을 수 있는가? → 설치 증빙이 없으면 첫 구간 보류.

## 데이터 계약

최소: meter_id, timestamp UTC, cumulative 정수(분), reset 불리언. 행은 관측 1건, 키는 meter_id+timestamp. null은 미관측. 개선: 교체 시각/끝값. 계기별로 정렬 후 인접 관측만 차분한다.

소형 fixture 어댑터: `before`와 `after`는 동일 meter_id에서 시간순으로 고른 두 cumulative 값, `reset`은 두 관측 사이 초기화 여부다. 단일 쌍에서는 timestamp를 고정 전제로 생략한다. 추가 readings 시험에서 순서를 명시적으로 검증한다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 동일 계기에서 시간순 인접 차분. 감소 또는 reset이면 reset_unknown, null이면 unknown. 같은 시점의 상충 관측은 invalid.

개선 조건: 교체 전후 끝값과 기준값이 있을 때만 구간 합산; 기간별 대시보드는 이후 추가한다.

최소 경로: 관측 두 건 선택 → 타임스탬프 검증 → 차분/보류 사유 → 운영자가 계기 교체 기록을 조회한다.

제약과 우선순위: 목적함수 없음. 필수: 동일 계기, 시간순, 같은 단위. 선호: 촘촘한 샘플. 기간 시작 누락을 0으로 채우지 않는다.

추가 fixture 스키마: 추가 순서변경 fixture의 `readings`는 [시간순 정렬용 정수, 누적 분] 행 배열이다. 서로 다른 두 시점만 사용하며 정렬 후 차분한다. 동일 시각 충돌 해소는 별도 계약이 필요하다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/counter-reset.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"before":130,"after":178,"reset":false}`|`48`|178−130=48분|
|boundary|`{"before":130,"after":130,"reset":false}`|`0`|동일 누적값은 0|
|missing|`{"before":null,"after":178,"reset":false}`|`"unknown"`|기준값 없음|
|conflict|`{"before":130,"after":4,"reset":false}`|`"reset_unknown"`|−126은 사용량이 아님|
|reset_crossing|`{"before":130,"after":178,"reset":true}`|`"reset_unknown"`|증가해도 교체를 통과하면 보류|
|new_sample|`{"before":5,"after":17,"reset":false}`|`12`|17−5=12|
|reorder|`{"readings":[[2,178],[1,130]],"reset":false}`|`48`|시간순 정렬 후 178−130=48; 파일 행순 무관|

비교 쌍: normal의 130→178/reset=false는 48이고 reset_crossing의 같은 숫자/reset=true는 reset_unknown이어야 한다.

## 오류·도구·범위

음수 차분을 절댓값으로 바꾸거나 모든 감소를 고장으로 판정하지 않는다. 보간을 사실처럼 표시하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 관측 두 건 선택 → 타임스탬프 검증 → 차분/보류 사유 → 운영자가 계기 교체 기록을 조회한다. 180분에는 교체 전후 끝값과 기준값이 있을 때만 구간 합산; 기간별 대시보드는 이후 추가한다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 보류 구간을 보고 교체 기록을 찾을 수 있습니까?
- 이 구간 길이로 사용량 판단이 가능합니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 초기화 구간을 합계에서 어떻게 분리했습니까?
- 누락 구간 때문에 보장할 수 없는 범위는 무엇입니까?

## 측정과 한계

정상 구간 차분 정확도와 보류율 측정 가능. 에너지 절감은 이 예제로 입증되지 않는다.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/datetime.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
