# DEPENDENCY: 관계 경로·전파·병목

최초 자료: 방향·관계 종류·출처·계수.
첫 분기 질문: 경로 존재인가 정량 영향인가?
가장 단순한 기준: 그래프 탐색.
적용하지 않을 때: 근거 없는 계수로 매출 전망 불가.

## 대표 심화 사례

- [수리 부품 중단의 영향 경로 추적](../cases/DEPENDENCY/dependency-reachability.md): `directed graph reachability`
- [전시 설치 작업의 선행관계와 최소 완료시간](../cases/DEPENDENCY/dependency-critical-path.md): `directed acyclic graph critical path`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [verification](../methods/verification.md) → [검증](../methods/verification.md).

핵심 도구 후보: [networkx](../tools/networkx.md). 방향 경로·사이클에 사용. 관계 존재를 정량 인과 효과로 해석하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
