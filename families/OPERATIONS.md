# OPERATIONS: 시계열 변화·측정 이상 탐지

최초 자료: 시각·측정 단위·조건·정비 이력.
첫 분기 질문: 공정 변화인가 센서 결측인가?
가장 단순한 기준: 조건별 기준선.
적용하지 않을 때: 전환 승인/동등성은 QUALITY.

## 대표 심화 사례

- [누락 센서와 실제 상한 초과 분리](../cases/OPERATIONS/missing-versus-alarm.md): `time series validation`
- [혼합 구성 변화와 유형별 품질 변화 분리](../cases/OPERATIONS/stratified-rate.md): `stratified comparison`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [assumption-mapping](../methods/assumption-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 조건별 집계와 결측 처리를 먼저 확정. 규격과 관리한계는 다름.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
