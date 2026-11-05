# EVENT: 접수·정원·중복·대기 처리

최초 자료: 신청 ID·시각·정원·상태.
첫 분기 질문: 접수와 참가 확정은 같은가?
가장 단순한 기준: 상태 표·멱등 키.
적용하지 않을 때: 금액/재고 잠금은 TRANSACTION.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [시간대가 다른 신청의 마감 판정](../cases/event/deadline-offset.md) | 심화 | decision-table |
| [중복 요청이 있는 소규모 워크숍 정원](../cases/event/seat-retry.md) | 심화 | state-machine |
| [실습 참여 자격의 만료일 판정](../cases/event/event-eligibility.md) | 표준 | dated eligibility decision |
| [입장 재스캔과 미등록 코드 분리](../cases/event/event-checkin.md) | 표준 | set membership with idempotent scan |
| [참여 완료 보상의 한 번 지급](../cases/event/event-reward-ledger.md) | 표준 | idempotent reward ledger |
| [취소 후 재신청의 대기 순번](../cases/event/event-cancel-priority.md) | 표준 | queue cancellation and reentry |
| [운영 리허설의 동시 체류 인원](../cases/event/event-rehearsal-capacity.md) | 표준 | event interval sweep |
| [현장 예외 승인의 범위와 유효시간](../cases/event/event-exception-expiry.md) | 표준 | scoped approval check |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [example-mapping](../methods/example-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 복수 요청의 UNIQUE 키·트랜잭션이 필요할 때 도입. UI 버튼 잠금만으로 보장하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
