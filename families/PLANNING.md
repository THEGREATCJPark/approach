# PLANNING: 기간 전체의 제약 충족 계획

최초 자료: 기간·수요·용량·고정 항목.
첫 분기 질문: 개인 순위인가 기간 전체 제약인가?
가장 단순한 기준: 작은 전수 열거.
적용하지 않을 때: 개인 추천이면 RANKING.

## 대표 심화 사례

- [고정 활동을 포함한 3일 서비스 편성](../cases/PLANNING/rotation-budget.md): `finite constraint search`
- [팩 단위 발주와 입고 시점 구별](../cases/PLANNING/pack-order.md): `net requirement arithmetic`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [baseline-first](../methods/baseline-first.md) → [검증](../methods/verification.md).

핵심 도구 후보: [or-tools](../tools/or-tools.md). 작은 열거가 커지면 정수 제약 CP-SAT 검토. optimal/feasible/infeasible/unknown 구별.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
