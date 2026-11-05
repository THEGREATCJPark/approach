# EVENT: 접수·정원·중복·대기 처리

최초 자료: 신청 ID·시각·정원·상태.
첫 분기 질문: 접수와 참가 확정은 같은가?
가장 단순한 기준: 상태 표·멱등 키.
적용하지 않을 때: 금액/재고 잠금은 TRANSACTION.

## 대표 심화 사례

- [시간대가 다른 신청의 마감 판정](../cases/event/deadline-offset.md): `decision-table`
- [중복 요청이 있는 소규모 워크숍 정원](../cases/event/seat-retry.md): `state-machine`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [example-mapping](../methods/example-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 복수 요청의 UNIQUE 키·트랜잭션이 필요할 때 도입. UI 버튼 잠금만으로 보장하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
