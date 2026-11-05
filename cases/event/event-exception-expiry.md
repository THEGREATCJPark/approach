# 현장 예외 승인의 범위와 유효시간

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-exception-expiry",
  "title": "현장 예외 승인의 범위와 유효시간",
  "family": "EVENT",
  "problem_structure": "scoped approval check",
  "keywords_ko": [
    "현장",
    "예외",
    "승인의",
    "범위와",
    "유효시간"
  ],
  "keywords_en": [
    "scoped",
    "approval",
    "check"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 공예 전시의 현장 운영자가 일반 접수 규칙을 예외 처리한 근거를 확인하려 한다.",
  "do_not_use_when": "승인 메모 텍스트만으로 권한을 추정하지 않는다. 범위 미확정이면 자동 예외를 끄고 검토 목록만 만든다.",
  "data_required": [
    "event/scope/approver는 문자열 코드, authorized는 승인권자 집합, now/expires는 동일 기준의 정수 분. 한 객체는 예외 승인 한 건, 운영 audit_id는 별도 키. null은 unknown."
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
  "depth": "standard",
  "path": "cases/event/event-exception-expiry.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 공예 전시의 현장 운영자가 일반 접수 규칙을 예외 처리한 근거를 확인하려 한다.",
    "input_structure": "event/scope/approver는 문자열 코드, authorized는 승인권자 집합, now/expires는 동일 기준의 정수 분. 한 객체는 예외 승인 한 건, 운영 audit_id는 별도 키. null은 unknown.",
    "hard_constraint": "범위·권한·now<expires를 모두 확인한다. 불일치면 denied, 필수 미확인이면 unknown.",
    "validation": "만료시각은 제외"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 공예 전시의 현장 운영자가 일반 접수 규칙을 예외 처리한 근거를 확인하려 한다.

- 다른 행사 승인을 재사용
- 승인권자 목록의 갱신 누락
- 승인 유효시간 만료

## 담당자에게 먼저 물을 질문

1. 승인은 어느 행사에만 유효한가? → 범위키를 필수로 한다.
2. 누가 예외 승인권자인가? → 현행 목록과 대조한다.
3. 만료 시각에 승인 가능한가? → 이 사례는 expires 이상이면 만료다.

## 데이터 계약과 자료 부족 대안

event/scope/approver는 문자열 코드, authorized는 승인권자 집합, now/expires는 동일 기준의 정수 분. 한 객체는 예외 승인 한 건, 운영 audit_id는 별도 키. null은 unknown.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

범위·권한·now<expires를 모두 확인한다. 불일치면 denied, 필수 미확인이면 unknown.

실제 시스템은 변경 불가능한 승인 이력과 정책 버전을 연결한다.

## 최소 구현과 다음 행동

예외 요청·승인 → 세 조건 검사 → 인정/거절/확인 대기 → 운영자가 책임자 확인

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"event":"e1","scope":"e1","approver":"lead","authorized":["lead"],"now":20,"expires":30}` | `"accepted"` | 범위·권한 일치,20<30 |
| boundary | `{"event":"e1","scope":"e1","approver":"lead","authorized":["lead"],"now":30,"expires":30}` | `"denied"` | 만료시각은 제외 |
| missing | `{"event":"e1","scope":"e1","approver":null,"authorized":["lead"],"now":20,"expires":30}` | `"unknown"` | 승인 주체 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

승인 메모 텍스트만으로 권한을 추정하지 않는다. 범위 미확정이면 자동 예외를 끄고 검토 목록만 만든다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 거절 사유가 범위·권한·만료 중 무엇인지 찾을 수 있는가?
- unknown 건을 누구에게 전달하겠는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 권한 확인과 승인 기록 존재가 왜 다른가?
- 시각 경계를 바꾸면 어떤 반례가 필요한가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
