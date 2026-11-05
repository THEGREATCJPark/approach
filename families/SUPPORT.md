# SUPPORT: 문의를 분류·검색·이관

최초 자료: 문의·기한·정책 문서 버전.
첫 분기 질문: 답변보다 처리 순서가 필요한가?
가장 단순한 기준: 규칙 분류/키워드 검색.
적용하지 않을 때: 금액 실행은 TRANSACTION.

## 대표 심화 사례

- [수리 문의의 마감 여유시간 정렬](../cases/support/repair-slack.md): `triage`
- [문의일 기준으로 유효한 안내문 찾기](../cases/support/policy-evidence.md): `retrieval`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [domain-storytelling](../methods/domain-storytelling.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 근거 문서가 많을 때 FTS5를 비교하되 한국어 토큰화와 검색 실패를 검사.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
