# QUALITY: 변경의 승인·동등성 검토

최초 자료: lot·측정 신뢰도·허용차·필수 시험.
첫 분기 질문: 유의차 없음인가 동등성 입증인가?
가장 단순한 기준: 필수 관문·구간 비교.
적용하지 않을 때: 시간 이상 경보는 OPERATIONS.

## 대표 심화 사례

- [필수 승인 누락을 가격으로 상쇄하지 않는 후보 비교](../cases/QUALITY/mandatory-gates.md): `hard gates before ranking`
- [차이 미검출과 동등성 구간 판정 구별](../cases/QUALITY/equivalence-interval.md): `interval containment`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [premortem](../methods/premortem.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 필수 관문과 구간 계산을 분리. 유의차 없음으로 동등성을 주장하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
