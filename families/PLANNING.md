# PLANNING: 기간 전체의 제약 충족 계획

최초 자료: 기간·수요·용량·고정 항목.
첫 분기 질문: 개인 순위인가 기간 전체 제약인가?
가장 단순한 기준: 작은 전수 열거.
적용하지 않을 때: 개인 추천이면 RANKING.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [고정 활동을 포함한 3일 서비스 편성](../cases/PLANNING/rotation-budget.md) | 심화 | finite constraint search |
| [팩 단위 발주와 입고 시점 구별](../cases/PLANNING/pack-order.md) | 심화 | net requirement arithmetic |
| [서비스 묶음의 비용과 최소 성능](../cases/PLANNING/planning-resource-blend.md) | 표준 | small integer covering mix |
| [서비스 종류의 최소 재등장 간격](../cases/PLANNING/planning-repeat-gap.md) | 표준 | sequence spacing validation |
| [대체 자재의 환산량과 손실](../cases/PLANNING/planning-substitute-stock.md) | 표준 | substitution conversion arithmetic |
| [공급 중단 후 기존 계획의 최소 변경](../cases/PLANNING/planning-outage-repair.md) | 표준 | minimum change reassignment |
| [수요와 용량 충돌의 부족량 설명](../cases/PLANNING/planning-infeasible-witness.md) | 표준 | capacity infeasibility witness |
| [고정 근무 구간의 서비스 공백 찾기](../cases/PLANNING/planning-service-coverage.md) | 표준 | interval union gap detection |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [baseline-first](../methods/baseline-first.md) → [검증](../methods/verification.md).

핵심 도구 후보: [or-tools](../tools/or-tools.md). 작은 열거가 커지면 정수 제약 CP-SAT 검토. optimal/feasible/infeasible/unknown 구별.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
