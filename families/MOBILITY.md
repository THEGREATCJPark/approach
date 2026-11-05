# MOBILITY: 방문 순서 또는 출발·도착 배정

최초 자료: 거리/시간 행렬·창·용량·거점.
첫 분기 질문: 경로가 고정되어 있는가?
가장 단순한 기준: 작은 순열·시간 역산.
적용하지 않을 때: 경로 고정이면 Routing 불필요.

## 대표 심화 사례

- [수리 부품 순회 수거의 방문 순서](../cases/MOBILITY/mobility-tour.md): `routing permutation`
- [고정 순회 점검의 출발 가능 구간](../cases/MOBILITY/mobility-departure.md): `fixed route time windows`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [assumption-mapping](../methods/assumption-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [or-tools](../tools/or-tools.md). 방문 순서 변경은 Routing 후보. 고정 경로 출발시각에는 구간 교집합부터.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
