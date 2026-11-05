# 시간대가 다른 신청의 마감 판정

```json
{
  "id": "deadline-offset",
  "title": "시간대가 다른 신청의 마감 판정",
  "family": "EVENT",
  "keywords_ko": [
    "마감",
    "시간대",
    "신청",
    "자격"
  ],
  "keywords_en": [
    "decision-table",
    "deadline-offset"
  ],
  "problem_structure": "decision-table",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 온라인 공예 교류회의 접수를 여러 지역에서 받는다. 신청 시각의 표시 날짜가 달라도 동일한 절대 마감 시각을 적용해야 한다.",
  "do_not_use_when": "문자열 날짜 비교나 로컬 시간대 강제 가정을 하지 않는다. 브라우저 자동 접수는 범위 밖이다.",
  "data_required": [
    "최소: application_id, received_at ISO8601 offset, deadline ISO8601 offset. 행은 신청 사건. 키 application_id. null/offset 없음은 unknown. 개선: 서버 수신 로그·재시도 키. 기기 시각만으로 확정하지 않는다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "seat-retry"
  ],
  "depth": "deep",
  "path": "cases/event/deadline-offset.md",
  "test_count": 7,
  "fixture_path": "examples/synthetic/deadline-offset.json"
}
```

## 요청과 가설

창작: 온라인 공예 교류회의 접수를 여러 지역에서 받는다. 신청 시각의 표시 날짜가 달라도 동일한 절대 마감 시각을 적용해야 한다.

가능한 원인: 시간대 표시 차이; 마감 포함 여부 모호; 클라이언트 시간이 잘못됨.

## 먼저 가를 질문과 계획 변경

1. 마감과 같은 순간은 허용합니까? → 허용이면 ≤, 아니면 <.
2. 서버 수신과 버튼 누른 시각 중 무엇입니까? → 신뢰할 서버 수신을 계약에 명시.
3. 시간대 없는 과거 기록은 어떻게 합니까? → 추정 승인 대신 수동 확인.

## 데이터 계약

최소: application_id, received_at ISO8601 offset, deadline ISO8601 offset. 행은 신청 사건. 키 application_id. null/offset 없음은 unknown. 개선: 서버 수신 로그·재시도 키. 기기 시각만으로 확정하지 않는다.

소형 fixture 어댑터: `at` = received_at, `end` = deadline. 단일 application_id의 순수 시각 판정이므로 저장·중복 방지 동작은 포함하지 않는다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: offset을 포함한 시각을 UTC로 비교하며 이 합성 정책은 마감 순간 포함. eligible/late/unknown/invalid를 분리한다.

개선 조건: 기관별 IANA 시간대가 필요하면 서머타임 중복·누락 시각 정책을 먼저 합의한다.

최소 경로: 신청 기록 → 시각 정규화 → 원시각·UTC·정책 버전·판정 → 운영자가 예외 건 확인.

제약과 우선순위: 목적함수 없음. 필수: 서버 시각·시간대·포함 규칙. 선호: 지역별 표시. 규칙 위반을 점수로 상쇄하지 않는다.

추가 fixture 스키마: 추가 재시도 fixture의 `repeat=2`는 같은 순수 판정을 두 번 요청하는 모형이다. 반환 목록의 두 결과가 같은지 확인한다. 실제 접수 저장·통신 재시도 멱등성은 seat-retry 사례에서 별도로 검토한다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/deadline-offset.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"at":"2031-06-01T08:59:00+00:00","end":"2031-06-01T18:00:00+09:00"}`|`"eligible"`|마감 UTC 09:00보다 1분 전|
|boundary|`{"at":"2031-06-01T09:00:00+00:00","end":"2031-06-01T18:00:00+09:00"}`|`"eligible"`|같은 순간 포함|
|missing|`{"at":"2031-06-01T09:00:00","end":"2031-06-01T18:00:00+09:00"}`|`"unknown"`|offset 없음|
|conflict|`{"at":"2031-06-01T09:00:01+00:00","end":"2031-06-01T18:00:00+09:00"}`|`"late"`|1초 초과|
|offset_equivalence|`{"at":"2031-06-01T18:00:00+09:00","end":"2031-06-01T09:00:00+00:00"}`|`"eligible"`|동일 순간 표시 변경|
|new_sample|`{"at":"2031-06-01T04:30:00-04:00","end":"2031-06-01T09:00:00+00:00"}`|`"eligible"`|UTC08:30|
|retry|`{"at":"2031-06-01T09:00:00+00:00","end":"2031-06-01T18:00:00+09:00","repeat":2}`|`["eligible", "eligible"]`|같은 순수 판정 요청 두 번 재시도해도 동일 결과; 접수 부작용은 이 사례 범위 밖|

비교 쌍: boundary의 UTC09:00은 eligible, conflict의 UTC09:00:01은 late다. 1초 차이로 경계 결과가 달라진다.

## 오류·도구·범위

문자열 날짜 비교나 로컬 시간대 강제 가정을 하지 않는다. 브라우저 자동 접수는 범위 밖이다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 신청 기록 → 시각 정규화 → 원시각·UTC·정책 버전·판정 → 운영자가 예외 건 확인. 180분에는 기관별 IANA 시간대가 필요하면 서머타임 중복·누락 시각 정책을 먼저 합의한다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 동일 순간의 두 표시가 같은 결과인지 확인할 수 있습니까?
- 시간대 없는 건의 확인 담당자가 명확합니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 경계값 한 건이 왜 허용되는지 정책을 보여주십시오.
- 서버 수신 지연과 규칙 판정은 어떻게 구분했습니까?

## 측정과 한계

시각 변환/경계 오류율 측정 가능. 공정성 만족도는 사용자 조사 없이 주장 불가.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/datetime.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
