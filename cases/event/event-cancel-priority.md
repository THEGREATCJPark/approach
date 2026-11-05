# 취소 후 재신청의 대기 순번

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-cancel-priority",
  "title": "취소 후 재신청의 대기 순번",
  "family": "EVENT",
  "problem_structure": "queue cancellation and reentry",
  "keywords_ko": [
    "취소",
    "후",
    "재신청의",
    "대기",
    "순번"
  ],
  "keywords_en": [
    "queue",
    "cancellation",
    "and",
    "reentry"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 모형 제작 공개 수업에서 대기자가 취소 후 다시 신청했을 때 예전 순번을 유지할지 논쟁이 생겼다.",
  "do_not_use_when": "사건 순서를 무시하고 집합 정렬하지 않는다. 시간 부족이면 자동 승격 대신 대기열 변경까지만 구현한다.",
  "data_required": [
    "queue는 활성 대기 person_id 배열, events는 [action,person_id] 수신순 배열. action cancel/join. 행은 대기열 변경 사건, 운영에서는 event_id와 순서키 필요. null ID는 unknown."
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
  "depth": "standard",
  "path": "cases/event/event-cancel-priority.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 모형 제작 공개 수업에서 대기자가 취소 후 다시 신청했을 때 예전 순번을 유지할지 논쟁이 생겼다.",
    "input_structure": "queue는 활성 대기 person_id 배열, events는 [action,person_id] 수신순 배열. action cancel/join. 행은 대기열 변경 사건, 운영에서는 event_id와 순서키 필요. null ID는 unknown.",
    "hard_constraint": "cancel은 활성 대기에서 제거; join은 없을 때 끝에 추가. 취소 뒤 join은 새 순번.",
    "validation": "빈 대기열 첫 신청"
  }
}
```

## 업무 요청과 다른 원인

창작: 모형 제작 공개 수업에서 대기자가 취소 후 다시 신청했을 때 예전 순번을 유지할지 논쟁이 생겼다.

- 취소된 신청의 기존 위치 재사용
- 사람별 기록과 신청별 기록 혼동
- 우선권 정책 미합의

## 담당자에게 먼저 물을 질문

1. 재신청은 새 순번인가? → 이 사례는 맨 뒤이며 유지 정책이면 키와 시간 규칙을 바꾼다.
2. 동일 사람이 중복 신청하면 어떤가? → 활성 신청 한 개만 유지한다.
3. 취소가 정원 배정 후에도 가능한가? → 좌석 승격은 별도 상태 전이로 확장한다.

## 데이터 계약과 자료 부족 대안

queue는 활성 대기 person_id 배열, events는 [action,person_id] 수신순 배열. action cancel/join. 행은 대기열 변경 사건, 운영에서는 event_id와 순서키 필요. null ID는 unknown.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

cancel은 활성 대기에서 제거; join은 없을 때 끝에 추가. 취소 뒤 join은 새 순번.

우선순위·특별 승인 정책이 생기면 정렬키와 승인 이력을 별도 관리한다.

## 최소 구현과 다음 행동

대기열·사건 → 순차 재생 → 새 순번 → 운영자가 재신청자에게 위치 안내

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"queue":["a","b","c"],"events":[["cancel","b"],["join","b"]]}` | `["a", "c", "b"]` | b 제거 후 끝에 재추가 |
| boundary | `{"queue":[],"events":[["join","a"]]}` | `["a"]` | 빈 대기열 첫 신청 |
| missing | `{"queue":["a"],"events":[["join",null]]}` | `"unknown"` | 신청자 식별 불가 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

사건 순서를 무시하고 집합 정렬하지 않는다. 시간 부족이면 자동 승격 대신 대기열 변경까지만 구현한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 재신청자의 새 위치를 납득할 근거가 보이는가?
- 이미 없는 사람의 취소를 어떻게 안내할 것인가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 이 처리에서 입력순서 불변 테스트가 잘못인 이유는 무엇인가?
- 재신청 정책을 바꾸면 어떤 기대값을 바꾸는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
