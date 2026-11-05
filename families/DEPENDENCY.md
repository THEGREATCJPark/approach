# DEPENDENCY: 관계 경로·전파·병목

최초 자료: 방향·관계 종류·출처·계수.
첫 분기 질문: 경로 존재인가 정량 영향인가?
가장 단순한 기준: 그래프 탐색.
적용하지 않을 때: 근거 없는 계수로 매출 전망 불가.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [수리 부품 중단의 영향 경로 추적](../cases/DEPENDENCY/dependency-reachability.md) | 심화 | directed graph reachability |
| [전시 설치 작업의 선행관계와 최소 완료시간](../cases/DEPENDENCY/dependency-critical-path.md) | 심화 | directed acyclic graph critical path |
| [관계 종류를 구분한 직접 영향 조회](../cases/DEPENDENCY/dependency-relation-types.md) | 표준 | typed-graph-query |
| [중간 노드 제거로 드러나는 연결 병목](../cases/DEPENDENCY/dependency-removal-bottleneck.md) | 표준 | node-removal-connectivity |
| [대체 공급을 포함한 운영 가능 논리](../cases/DEPENDENCY/dependency-alternative-supply.md) | 표준 | and-or-dependency |
| [가정한 영향 계수의 민감도 비교](../cases/DEPENDENCY/dependency-coefficient-sensitivity.md) | 표준 | linear-scenario-sensitivity |
| [동일 관계의 상충 출처와 유효 근거 판정](../cases/DEPENDENCY/dependency-evidence-validity.md) | 표준 | relation-evidence-conflict |
| [복수 관계를 잃지 않는 그래프 표시 집계](../cases/DEPENDENCY/dependency-multigraph-display.md) | 표준 | multigraph-projection |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [verification](../methods/verification.md) → [검증](../methods/verification.md).

핵심 도구 후보: [networkx](../tools/networkx.md). 방향 경로·사이클에 사용. 관계 존재를 정량 인과 효과로 해석하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
