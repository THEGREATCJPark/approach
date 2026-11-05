# 입장 재스캔과 미등록 코드 분리

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-checkin",
  "title": "입장 재스캔과 미등록 코드 분리",
  "family": "EVENT",
  "problem_structure": "set membership with idempotent scan",
  "keywords_ko": [
    "입장",
    "재스캔과",
    "미등록",
    "코드",
    "분리"
  ],
  "keywords_en": [
    "set",
    "membership",
    "with",
    "idempotent",
    "scan"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 표본 전시의 입구에서 같은 입장권을 다시 읽어 입장 인원이 부풀려진다.",
  "do_not_use_when": "버튼 잠금은 복수 입구 중복을 해결하지 않는다. 시간 부족이면 재입장 분석을 빼고 등록·중복·불명 구분을 유지한다.",
  "data_required": [
    "registered는 확인된 티켓 ID 집합, scans는 수신순 티켓 ID 배열. 단위는 티켓 건이며 사람 수와 다를 수 있다. 한 스캔은 한 입장 사건; null 티켓은 판정 보류. 운영에서는 event_id·서버시각·등록 버전이 필요하다."
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
  "path": "cases/event/event-checkin.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 표본 전시의 입구에서 같은 입장권을 다시 읽어 입장 인원이 부풀려진다.",
    "input_structure": "registered는 확인된 티켓 ID 집합, scans는 수신순 티켓 ID 배열. 단위는 티켓 건이며 사람 수와 다를 수 있다. 한 스캔은 한 입장 사건; null 티켓은 판정 보류. 운영에서는 event_id·서버시각·등록 버전이 필요하다.",
    "hard_constraint": "등록된 코드의 첫 스캔만 checked_in, 이후 duplicate, 미등록은 unknown_ticket. 고유 입장 수를 set 크기로 센다.",
    "validation": "스캔 0건은 관측된 0"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 표본 전시의 입구에서 같은 입장권을 다시 읽어 입장 인원이 부풀려진다.

- 스캐너 재전송
- 동일 티켓의 재입장 정책 미정
- 등록 목록과 스캔 목록의 시점 차이

## 담당자에게 먼저 물을 질문

1. 재입장을 허용하는가? → 허용해도 고유 입장 인원과 출입 횟수는 분리한다.
2. 미등록 코드는 즉시 거절인가 확인 대기인가? → 이 예제는 등록 목록 완전성을 전제로 unknown_ticket이다.
3. 집계는 고유 티켓인가 동행 인원인가? → 동행이면 인원 필드가 필요하다.

## 데이터 계약과 자료 부족 대안

registered는 확인된 티켓 ID 집합, scans는 수신순 티켓 ID 배열. 단위는 티켓 건이며 사람 수와 다를 수 있다. 한 스캔은 한 입장 사건; null 티켓은 판정 보류. 운영에서는 event_id·서버시각·등록 버전이 필요하다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

등록된 코드의 첫 스캔만 checked_in, 이후 duplicate, 미등록은 unknown_ticket. 고유 입장 수를 set 크기로 센다.

복수 입구가 동시에 기록하면 공유 저장소 고유키와 원자적 기록을 별도 검증한다.

## 최소 구현과 다음 행동

등록 목록·스캔 → 존재/중복 검사 → 상태와 고유 입장 수 → 입구 담당자가 입장 또는 확인 창구 안내

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"registered":["a","b"],"scans":["a","a","b"]}` | `{"unique": 2, "statuses": ["checked_in", "duplicate", "checked_in"]}` | 고유 등록 티켓은 a,b 두 개 |
| boundary | `{"registered":["a"],"scans":[]}` | `{"unique": 0, "statuses": []}` | 스캔 0건은 관측된 0 |
| missing | `{"registered":["a"],"scans":[null]}` | `"unknown"` | 식별키 누락 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

버튼 잠금은 복수 입구 중복을 해결하지 않는다. 시간 부족이면 재입장 분석을 빼고 등록·중복·불명 구분을 유지한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 이미 입장한 티켓을 다시 읽으면 무엇을 해야 하는가?
- 미등록과 등록정보 미수신을 구별할 수 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 고유 티켓 수와 실제 사람 수의 차이는 무엇인가?
- 순차 재생에서 확인하지 못한 동시성 문제는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
