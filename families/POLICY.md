# POLICY: 규칙·승인·다음 행동

최초 자료: 정책 버전·권한·증빙·상태.
첫 분기 질문: 누가 예외 승인권자인가?
가장 단순한 기준: decision table.
적용하지 않을 때: 실행 원자성은 TRANSACTION.

## 대표 심화 사례

- [증빙 누락과 승인 권한을 분리한 비용 안내](../cases/POLICY/evidence-approval.md): `decision table`
- [반려 후 재제출과 중복 이벤트 제어](../cases/POLICY/resubmission-state.md): `state machine`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [domain-storytelling](../methods/domain-storytelling.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 정책 버전·승인 이력 저장이 필요할 때 사용. 권한은 담당자에게 확인.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
