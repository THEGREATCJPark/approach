# GEOMETRY: 공간 포함·가림·겹침

최초 자료: 좌표계·축척·장애물·설치 후보.
첫 분기 질문: 면적의 합집합인가 시야인가?
가장 단순한 기준: 작은 격자/도형 계산.
적용하지 않을 때: 이동 순서는 MOBILITY.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [겹치는 바닥 점검 구역의 면적](../cases/geometry/rectangle-union.md) | 심화 | geometry |
| [예산 내 점검 거점의 이산 커버리지](../cases/geometry/budget-cover.md) | 심화 | maximum-coverage |
| [직선 시야와 차폐판의 앞뒤](../cases/geometry/sightline-barrier.md) | 표준 | visibility |
| [모든 점검 구역을 덮는 최소 설치비](../cases/geometry/minimum-cover-cost.md) | 표준 | set-cover |
| [중요 구역 가중치로 단일 센서 선택](../cases/geometry/priority-zone-weight.md) | 표준 | weighted-coverage |
| [설치 금지 사각형과 후보점 경계 판정](../cases/geometry/installation-exclusion.md) | 표준 | geometry-filter |
| [도면 좌표와 실측 기준선의 축척 검사](../cases/geometry/drawing-unit-check.md) | 표준 | unit-validation |
| [고정 관측점의 반경 안 표적 집계](../cases/geometry/radial-monitor-range.md) | 표준 | radial-coverage |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [verification](../methods/verification.md) → [검증](../methods/verification.md).

핵심 도구 후보: [shapely](../tools/shapely.md). 복합 polygon의 합집합·교차에 사용. 시야 가림은 별도 알고리즘이며 좌표 단위 필수.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
