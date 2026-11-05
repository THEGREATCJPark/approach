# MOBILITY: 방문 순서 또는 출발·도착 배정

최초 자료: 거리/시간 행렬·창·용량·거점.
첫 분기 질문: 경로가 고정되어 있는가?
가장 단순한 기준: 작은 순열·시간 역산.
적용하지 않을 때: 경로 고정이면 Routing 불필요.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [수리 부품 순회 수거의 방문 순서](../cases/MOBILITY/mobility-tour.md) | 심화 | routing permutation |
| [고정 순회 점검의 출발 가능 구간](../cases/MOBILITY/mobility-departure.md) | 심화 | fixed route time windows |
| [분할 불가 수거 상자의 차량 배정](../cases/MOBILITY/mobility-indivisible-capacity.md) | 표준 | bin-assignment |
| [대기 허용 경로의 서비스 시작 시간](../cases/MOBILITY/mobility-window-wait.md) | 표준 | time-window-simulation |
| [가장 먼 방문지를 줄이는 출발 거점](../cases/MOBILITY/mobility-depot-minimax.md) | 표준 | minimax-location |
| [인접 수요 지점의 연결 묶음](../cases/MOBILITY/mobility-demand-clusters.md) | 표준 | proximity-components |
| [개인별 최대 이동시간을 지키는 지점 배정](../cases/MOBILITY/mobility-fair-travel-cap.md) | 표준 | capacity-matching |
| [미배정 수요와 과배정의 수량 대사](../cases/MOBILITY/mobility-unserved-ledger.md) | 표준 | demand-reconciliation |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [assumption-mapping](../methods/assumption-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [or-tools](../tools/or-tools.md). 방문 순서 변경은 Routing 후보. 고정 경로 출발시각에는 구간 교집합부터.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
