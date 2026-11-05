# 대리 승인 위임의 한도와 기간

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "policy-delegation",
  "title": "대리 승인 위임의 한도와 기간",
  "family": "POLICY",
  "problem_structure": "delegated authority interval",
  "keywords_ko": [
    "대리",
    "승인",
    "위임의",
    "한도와",
    "기간"
  ],
  "keywords_en": [
    "delegated",
    "authority",
    "interval"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 소규모 자료관이 담당자 부재 중 대리 승인자가 처리할 수 있는 요청을 구별하려 한다.",
  "do_not_use_when": "위임 한도를 더하거나 직책으로 예외를 만들지 않는다. 버전 조회가 없으면 고정 컨텍스트 계산만 제공한다.",
  "data_required": [
    "amount,owner_limit,delegate_limit는 같은 정수 비용단위; day,start,end는 동일 기준 정수 일. 한 객체는 요청×위임 조합, 운영 키 request_id/delegation_id. null은 unknown."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "evidence-approval"
  ],
  "depth": "standard",
  "path": "cases/POLICY/policy-delegation.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 소규모 자료관이 담당자 부재 중 대리 승인자가 처리할 수 있는 요청을 구별하려 한다.",
    "input_structure": "amount,owner_limit,delegate_limit는 같은 정수 비용단위; day,start,end는 동일 기준 정수 일. 한 객체는 요청×위임 조합, 운영 키 request_id/delegation_id. null은 unknown.",
    "hard_constraint": "유효기간 내이고 amount≤min(owner_limit,delegate_limit)이면 delegated, 아니면 original_owner로 전달.",
    "validation": "한도와 종료일 포함"
  }
}
```

## 업무 요청과 다른 원인

창작: 소규모 자료관이 담당자 부재 중 대리 승인자가 처리할 수 있는 요청을 구별하려 한다.

- 직책만으로 승인권 추정
- 위임 기간 만료
- 원래 권한보다 큰 금액 재위임

## 담당자에게 먼저 물을 질문

1. 위임 시작·종료는 포함인가? → 이 사례는 양끝 포함이다.
2. 원 권한과 위임 한도 중 어느 것이 우선인가? → 작은 한도를 적용한다.
3. 재위임이 가능한가? → 여기서는 제외하며 필요 시 위임 그래프를 검증한다.

## 데이터 계약과 자료 부족 대안

amount,owner_limit,delegate_limit는 같은 정수 비용단위; day,start,end는 동일 기준 정수 일. 한 객체는 요청×위임 조합, 운영 키 request_id/delegation_id. null은 unknown.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

유효기간 내이고 amount≤min(owner_limit,delegate_limit)이면 delegated, 아니면 original_owner로 전달.

다중 위임과 철회가 생기면 적용 시점별 유효 위임 이력을 조회한다.

## 최소 구현과 다음 행동

요청·위임 → 기간/한도 대조 → 다음 승인자 → 사용자가 권한자에게 전달

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"amount":70,"owner_limit":100,"delegate_limit":80,"day":5,"start":1,"end":7}` | `"delegated"` | 70≤80이고1≤5≤7 |
| boundary | `{"amount":80,"owner_limit":100,"delegate_limit":80,"day":7,"start":1,"end":7}` | `"delegated"` | 한도와 종료일 포함 |
| missing | `{"amount":70,"owner_limit":100,"delegate_limit":null,"day":5,"start":1,"end":7}` | `"unknown"` | 위임 한도 없음 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

위임 한도를 더하거나 직책으로 예외를 만들지 않는다. 버전 조회가 없으면 고정 컨텍스트 계산만 제공한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 대리 승인 불가 사유를 보고 원 승인자에게 전달할 수 있는가?
- 위임 철회가 실제 자료에 반영되는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 두 한도 중 작은 값을 쓰는 근거는 무엇인가?
- 기간 안이라도 승인권이 없는 반례는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
