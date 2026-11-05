# POLICY: 규칙·승인·다음 행동

최초 자료: 정책 버전·권한·증빙·상태.
첫 분기 질문: 누가 예외 승인권자인가?
가장 단순한 기준: decision table.
적용하지 않을 때: 실행 원자성은 TRANSACTION.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [증빙 누락과 승인 권한을 분리한 비용 안내](../cases/POLICY/evidence-approval.md) | 심화 | decision table |
| [반려 후 재제출과 중복 이벤트 제어](../cases/POLICY/resubmission-state.md) | 심화 | state machine |
| [대리 승인 위임의 한도와 기간](../cases/POLICY/policy-delegation.md) | 표준 | delegated authority interval |
| [증빙 번호가 겹치는 신청 검토](../cases/POLICY/policy-duplicate-claim.md) | 표준 | composite duplicate detection |
| [정책 개정 중 접수된 신청의 경과조치](../cases/POLICY/policy-effective-version.md) | 표준 | grandfathered pending application transition |
| [처리 상태와 역할별 다음 행동](../cases/POLICY/policy-next-action.md) | 표준 | role state affordance table |
| [작성자와 최종 승인자의 분리](../cases/POLICY/policy-separation-duties.md) | 표준 | separation of duties constraint |
| [공유 증빙의 부서별 배분 잔액](../cases/POLICY/policy-receipt-allocation.md) | 표준 | bounded allocation sum |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [domain-storytelling](../methods/domain-storytelling.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 정책 버전·승인 이력 저장이 필요할 때 사용. 권한은 담당자에게 확인.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
