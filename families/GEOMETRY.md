# GEOMETRY: 공간 포함·가림·겹침

최초 자료: 좌표계·축척·장애물·설치 후보.
첫 분기 질문: 면적의 합집합인가 시야인가?
가장 단순한 기준: 작은 격자/도형 계산.
적용하지 않을 때: 이동 순서는 MOBILITY.

## 대표 심화 사례

- [겹치는 바닥 점검 구역의 면적](../cases/geometry/rectangle-union.md): `geometry`
- [예산 내 점검 거점의 이산 커버리지](../cases/geometry/budget-cover.md): `maximum-coverage`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [verification](../methods/verification.md) → [검증](../methods/verification.md).

핵심 도구 후보: [shapely](../tools/shapely.md). 복합 polygon의 합집합·교차에 사용. 시야 가림은 별도 알고리즘이며 좌표 단위 필수.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
