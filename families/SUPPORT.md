# SUPPORT: 문의를 분류·검색·이관

최초 자료: 문의·기한·정책 문서 버전.
첫 분기 질문: 답변보다 처리 순서가 필요한가?
가장 단순한 기준: 규칙 분류/키워드 검색.
적용하지 않을 때: 금액 실행은 TRANSACTION.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [수리 문의의 마감 여유시간 정렬](../cases/support/repair-slack.md) | 심화 | triage |
| [문의일 기준으로 유효한 안내문 찾기](../cases/support/policy-evidence.md) | 심화 | retrieval |
| [분류 규칙이 겹치는 문의의 검토 대기](../cases/support/support-rule-overlap.md) | 표준 | rule-classification |
| [명시적 키로 중복 접수 후보 묶기](../cases/support/duplicate-ticket-fingerprint.md) | 표준 | deduplication |
| [답변 초안의 발송 전 필수 검토](../cases/support/draft-release-gate.md) | 표준 | approval-gate |
| [권한 범위를 넘는 보상 요청 이관](../cases/support/escalation-authority.md) | 표준 | authority-routing |
| [교대 인수인계의 다음 행동 누락](../cases/support/handoff-action-fields.md) | 표준 | completeness |
| [반복 문의 원인의 누적 비중](../cases/support/repeat-cause-pareto.md) | 표준 | pareto |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [domain-storytelling](../methods/domain-storytelling.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 근거 문서가 많을 때 FTS5를 비교하되 한국어 토큰화와 검색 실패를 검사.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
