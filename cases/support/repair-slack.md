# 수리 문의의 마감 여유시간 정렬

```json
{
  "id": "repair-slack",
  "title": "수리 문의의 마감 여유시간 정렬",
  "family": "SUPPORT",
  "keywords_ko": [
    "문의",
    "처리기한",
    "우선순위",
    "수리"
  ],
  "keywords_en": [
    "triage",
    "repair-slack"
  ],
  "problem_structure": "triage",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공동 수리점이 접수된 의뢰에서 오늘 먼저 착수할 건을 고르려 한다. 먼저 온 순서와 완료 약속을 지킬 순서가 다르다.",
  "do_not_use_when": "부정확한 예상시간을 확정값으로 쓰지 않는다. 문장 감성점수로 안전 이관을 자동 확정하지 않는다.",
  "data_required": [
    "최소: ticket_id, due_in_minutes, estimate_minutes, safety_flag. 행은 접수 1건. 키 ticket_id. 분 단위, 기준 now를 고정. null estimate는 unknown. 개선: 작업자 기술/부품 준비. 고객 이름 불필요."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "policy-evidence"
  ],
  "depth": "deep",
  "path": "cases/support/repair-slack.md",
  "test_count": 7,
  "fixture_path": "examples/synthetic/repair-slack.json"
}
```

## 요청과 가설

창작: 공동 수리점이 접수된 의뢰에서 오늘 먼저 착수할 건을 고르려 한다. 먼저 온 순서와 완료 약속을 지킬 순서가 다르다.

가능한 원인: 마감이 임박한 건; 처리시간이 긴 건; 안전 긴급건을 일반 순서에 섞음.

## 먼저 가를 질문과 계획 변경

1. 안전 긴급건의 별도 이관 규칙이 있습니까? → 있으면 일반 정렬 전 분리.
2. 기한은 착수인가 완료인가? → 완료면 예상 작업시간을 차감.
3. 작업시간을 모르면 어떻게 합니까? → 별도 견적 대기열을 둔다.

## 데이터 계약

최소: ticket_id, due_in_minutes, estimate_minutes, safety_flag. 행은 접수 1건. 키 ticket_id. 분 단위, 기준 now를 고정. null estimate는 unknown. 개선: 작업자 기술/부품 준비. 고객 이름 불필요.

소형 fixture 어댑터: `due` = due_in_minutes, `work` = estimate_minutes, `safety` = safety_flag. 단일 건의 ticket_id/now는 고정값이며, tickets 배열 첫 열이 ticket_id다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 일반 의뢰의 slack=마감까지 분−작업 분. 작은 순, 같으면 ticket_id로 재현성 확보. 안전건은 escalate, 추정 없음은 estimate_required.

개선 조건: 담당자 가용시간과 선후관계가 확인되면 일정 배정 문제로 전환한다. slack 정렬을 최적 일정이라고 부르지 않는다.

최소 경로: 의뢰 목록 → 긴급/미확인 분리 → 여유시간 정렬 → 담당자가 착수 또는 견적 요청을 선택한다.

제약과 우선순위: 우선순위: 안전 이관 > 정보 확보 > 일반 slack. 필수: 기한 정의. 선호: 균등 대기. 다중 작업자 최적화는 현재 범위 밖.

추가 fixture 스키마: 추가 순서변경 fixture의 `tickets`는 [ID, 기한까지 분, 작업 분] 행 배열이다. 완전하고 비긴급인 두 건만 대상으로 slack 오름차순 ID 목록을 검증한다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/repair-slack.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"due":90,"work":60,"safety":false}`|`30`|90−60=30분|
|boundary|`{"due":60,"work":60,"safety":false}`|`0`|여유 0|
|missing|`{"due":90,"work":null,"safety":false}`|`"estimate_required"`|추정 불명|
|conflict|`{"due":20,"work":40,"safety":false}`|`-20`|20분 지연 위험|
|safety_override|`{"due":90,"work":60,"safety":true}`|`"escalate"`|안전 규칙 우선|
|new_sample|`{"due":100,"work":95,"safety":false}`|`5`|마감은 늦어도 여유 5로 먼저 착수 후보|
|reorder|`{"tickets":[["b",100,95],["a",90,60]]}`|`["b", "a"]`|여유 5분인 b, 30분인 a 순; 입력순 의존 금지|

비교 쌍: normal과 safety_override는 due/work가 같지만 safety=false이면 30, true이면 escalate다.

## 오류·도구·범위

부정확한 예상시간을 확정값으로 쓰지 않는다. 문장 감성점수로 안전 이관을 자동 확정하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 의뢰 목록 → 긴급/미확인 분리 → 여유시간 정렬 → 담당자가 착수 또는 견적 요청을 선택한다. 180분에는 담당자 가용시간과 선후관계가 확인되면 일정 배정 문제로 전환한다. slack 정렬을 최적 일정이라고 부르지 않는다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 정렬 첫 건을 착수하지 않는 상황은 무엇입니까?
- 견적 필요 목록을 누가 처리해야 합니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- FIFO와 다른 순서가 나온 한 건을 계산으로 설명하십시오.
- 이 정렬이 완료기한을 보장하지 못하는 조건은 무엇입니까?

## 측정과 한계

여유시간 계산 오류·누락 분리율 측정 가능. 기한 준수율은 실제 운영 로그 필요.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/functions.html#sorted)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
