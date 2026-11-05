# 중복 요청이 있는 소규모 워크숍 정원

```json
{
  "id": "seat-retry",
  "title": "중복 요청이 있는 소규모 워크숍 정원",
  "family": "EVENT",
  "keywords_ko": [
    "정원",
    "재시도",
    "중복",
    "대기명단"
  ],
  "keywords_en": [
    "state-machine",
    "seat-retry"
  ],
  "problem_structure": "state-machine",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 도자기 워크숍 신청 API가 통신 재시도로 동일 요청을 두 번 받는다. 정원 2명인데 요청 수를 세어 대기자가 생겼다.",
  "do_not_use_when": "버튼 비활성화만으로 멱등성을 보장하지 않는다. 요청순서를 바꿔도 수락자가 같아야 한다는 잘못된 불변식을 쓰지 않는다.",
  "data_required": [
    "최소: ordered requests [request_id,person_id], capacity 정수. 행은 서버 수신순 사건, request_id는 재시도 식별, person_id는 좌석 유일성. null 키는 invalid. 개선: 취소·승격 사건. 원문 이름 대신 내부 키."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "deadline-offset"
  ],
  "depth": "deep",
  "path": "cases/event/seat-retry.md",
  "test_count": 6,
  "fixture_path": "examples/synthetic/seat-retry.json"
}
```

## 요청과 가설

창작: 도자기 워크숍 신청 API가 통신 재시도로 동일 요청을 두 번 받는다. 정원 2명인데 요청 수를 세어 대기자가 생겼다.

가능한 원인: 요청과 사람을 혼동; 멱등키 중복; 동시 정원 검사 경쟁.

## 먼저 가를 질문과 계획 변경

1. 같은 사람의 다른 요청키도 중복입니까? → 이 사례는 person_id 기준 1자리.
2. 취소 후 자동 승격합니까? → 그렇다면 별도 상태 전이/알림 동의 필요.
3. 동시 요청을 처리합니까? → 실제 서비스는 트랜잭션으로 정원 검사를 원자화.

## 데이터 계약

최소: ordered requests [request_id,person_id], capacity 정수. 행은 서버 수신순 사건, request_id는 재시도 식별, person_id는 좌석 유일성. null 키는 invalid. 개선: 취소·승격 사건. 원문 이름 대신 내부 키.

소형 fixture 어댑터: `cap` = capacity, `requests`의 행은 [request_id,person_id]다. 배열 순서가 서버 수신순이다. 다른 요청키로 같은 person_id가 재접수하면 기존 한 좌석을 유지한다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 수신 순서로 첫 person_id만 받아 정원까지 accepted, 이후 unique 사람은 waitlisted. 같은 request_id가 다른 사람을 가리키면 conflict. 이 예제는 단일 순차 재생만 검사한다.

개선 조건: 실제 동시 쓰기는 DB 고유키와 원자적 트랜잭션 및 재시도 정책을 검증한다. 단일 프로세스 set만으로 경쟁 안전하다고 하지 않는다.

최소 경로: 사건 JSON → 중복/충돌 검사 → accepted/waitlisted/오류 → 운영자가 대기 연락 여부 판단.

제약과 우선순위: 필수: 정원 초과 금지, 동일인 중복 좌석 금지. 선호: 수신순 공정성. 목적함수 없음. 취소/승격은 별도 범위.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/seat-retry.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"cap":2,"requests":[["x","p"],["y","q"],["z","r"]]}`|`[["p", "q"], ["r"]]`|첫 두 명 수락|
|boundary|`{"cap":0,"requests":[["x","p"]]}`|`[[], ["p"]]`|정원0 대기|
|missing|`{"cap":2,"requests":[["x",null]]}`|`"invalid"`|사람 키 없음|
|conflict|`{"cap":2,"requests":[["x","p"],["x","q"]]}`|`"conflict"`|같은 요청키 다른 payload|
|duplicate|`{"cap":2,"requests":[["x","p"],["x","p"],["y","p"],["z","q"]]}`|`[["p", "q"], []]`|한 사람 한 좌석|
|new_sample|`{"cap":1,"requests":[["z","r"],["x","p"]]}`|`[["r"], ["p"]]`|수신순 바뀌면 수락자 변경|

비교 쌍: duplicate의 같은 요청키/같은 사람은 정상 중복 제거하고 conflict의 같은 요청키/다른 사람은 conflict다.

## 오류·도구·범위

버튼 비활성화만으로 멱등성을 보장하지 않는다. 요청순서를 바꿔도 수락자가 같아야 한다는 잘못된 불변식을 쓰지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 사건 JSON → 중복/충돌 검사 → accepted/waitlisted/오류 → 운영자가 대기 연락 여부 판단. 180분에는 실제 동시 쓰기는 DB 고유키와 원자적 트랜잭션 및 재시도 정책을 검증한다. 단일 프로세스 set만으로 경쟁 안전하다고 하지 않는다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 대기 사유와 첫 접수 순서를 확인할 수 있습니까?
- 중복과 서로 다른 신청을 구별할 키가 충분합니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 중복 요청과 동시성 테스트가 어떻게 다릅니까?
- 다른 순서에서 수락자가 달라지는 것이 왜 정상입니까?

## 측정과 한계

순차 재생에서 정원 초과·중복 좌석 수 측정 가능. 동시성 안전은 이 예제로 입증되지 않는다.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/sqlite3.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
