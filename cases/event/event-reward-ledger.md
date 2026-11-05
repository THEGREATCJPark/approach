# 참여 완료 보상의 한 번 지급

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-reward-ledger",
  "title": "참여 완료 보상의 한 번 지급",
  "family": "EVENT",
  "problem_structure": "idempotent reward ledger",
  "keywords_ko": [
    "참여",
    "완료",
    "보상의",
    "한",
    "번",
    "지급"
  ],
  "keywords_en": [
    "idempotent",
    "reward",
    "ledger"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 탐방 행사에서 완료 확인 메시지가 재전송되어 같은 기념 토큰이 여러 번 지급될 위험이 있다.",
  "do_not_use_when": "UI 성공 메시지를 지급 완료로 저장하지 않는다. 설치 제한이면 장부 계산만 제공하고 외부 지급은 제외한다.",
  "data_required": [
    "fixture 한 행 [claim_key, tokens]는 같은 행사에서 승인된 지급 요청. tokens는 비음수 정수 개수. claim_key는 참가자×행사의 멱등키. null 수량/키는 unknown. 실제 지급 API는 포함하지 않는다."
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
  "path": "cases/event/event-reward-ledger.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 탐방 행사에서 완료 확인 메시지가 재전송되어 같은 기념 토큰이 여러 번 지급될 위험이 있다.",
    "input_structure": "fixture 한 행 [claim_key, tokens]는 같은 행사에서 승인된 지급 요청. tokens는 비음수 정수 개수. claim_key는 참가자×행사의 멱등키. null 수량/키는 unknown. 실제 지급 API는 포함하지 않는다.",
    "hard_constraint": "처음 본 키의 승인 토큰만 합산하고 같은 내용 재전송은 생략한다. 같은 키 다른 수량은 conflict.",
    "validation": "0개 승인도 기록 가능한 경계"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 탐방 행사에서 완료 확인 메시지가 재전송되어 같은 기념 토큰이 여러 번 지급될 위험이 있다.

- 완료 메시지 중복
- 사람별 지급과 회차별 지급의 혼동
- 지급 실패와 미처리 상태 혼동

## 담당자에게 먼저 물을 질문

1. 보상은 참가자당 한 번인가 회차당 한 번인가? → 키 범위가 바뀐다.
2. 완료 확인과 지급 완료를 따로 저장하는가? → 외부 지급이면 pending/confirmed를 분리한다.
3. 같은 키의 다른 금액은 어떻게 하는가? → 충돌로 보류한다.

## 데이터 계약과 자료 부족 대안

fixture 한 행 [claim_key, tokens]는 같은 행사에서 승인된 지급 요청. tokens는 비음수 정수 개수. claim_key는 참가자×행사의 멱등키. null 수량/키는 unknown. 실제 지급 API는 포함하지 않는다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

처음 본 키의 승인 토큰만 합산하고 같은 내용 재전송은 생략한다. 같은 키 다른 수량은 conflict.

실제 지급 연결 시 outbox·확인 응답·재조정 절차를 추가하고 별도 테스트한다.

## 최소 구현과 다음 행동

승인 요청 → 멱등 장부 → 신규 지급 합계/충돌 → 운영자가 지급 실행 대상을 검토

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"rows":[["a",2],["a",2],["b",3]]}` | `5` | a2를 한 번,b3을 한 번 합산 |
| boundary | `{"rows":[["a",0]]}` | `0` | 0개 승인도 기록 가능한 경계 |
| missing | `{"rows":[["a",null]]}` | `"unknown"` | 승인 수량 없음 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

UI 성공 메시지를 지급 완료로 저장하지 않는다. 설치 제한이면 장부 계산만 제공하고 외부 지급은 제외한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 재전송과 새 회차 참여를 키로 구별할 수 있는가?
- 충돌 기록을 누가 확인해야 하는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 같은 키 다른 수량을 마지막 값으로 덮지 않은 이유는 무엇인가?
- 장부 합계가 실제 지급 성공을 증명하지 못하는 이유는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
