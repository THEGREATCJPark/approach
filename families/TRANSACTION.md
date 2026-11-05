# TRANSACTION: 심사·잠금·실행·재시도

최초 자료: 요청 키·버전·가용/잠금·정밀도.
첫 분기 질문: 승인과 실행 완료를 구분하는가?
가장 단순한 기준: 원자적 상태 전이.
적용하지 않을 때: 절차 설명만이면 POLICY.

## 대표 심화 사례

- [대여 재고의 예약 잠금과 실행 분리](../cases/TRANSACTION/transaction-reservation.md): `state machine idempotency inventory`
- [소수 재료 사용량의 정산 반올림 시점](../cases/TRANSACTION/transaction-rounding.md): `decimal rounding aggregation`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [example-mapping](../methods/example-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 멱등 키·원자적 갱신을 실제 저장소에서 검증할 때 사용. 작은 계산은 동시성 검증 아님.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
