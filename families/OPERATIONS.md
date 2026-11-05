# OPERATIONS: 시계열 변화·측정 이상 탐지

최초 자료: 시각·측정 단위·조건·정비 이력.
첫 분기 질문: 공정 변화인가 센서 결측인가?
가장 단순한 기준: 조건별 기준선.
적용하지 않을 때: 전환 승인/동등성은 QUALITY.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [누락 센서와 실제 상한 초과 분리](../cases/OPERATIONS/missing-versus-alarm.md) | 심화 | time series validation |
| [혼합 구성 변화와 유형별 품질 변화 분리](../cases/OPERATIONS/stratified-rate.md) | 심화 | stratified comparison |
| [불규칙 시간 간격의 변화율](../cases/OPERATIONS/time-slope.md) | 표준 | elapsed hours × measurement |
| [방향을 보존한 위치 오차 판정](../cases/OPERATIONS/position-error-vector.md) | 표준 | target/measured xy vectors |
| [동일 시료를 이용한 장비 간 편향](../cases/OPERATIONS/paired-instrument-bias.md) | 표준 | specimen id × instrument A/B pair |
| [작은 양의 변화의 누적 경보](../cases/OPERATIONS/one-sided-cusum.md) | 표준 | ordered samples × fixed reference |
| [정비 전후 비교에서 안정화 구간 제외](../cases/OPERATIONS/maintenance-washout.md) | 표준 | relative day × measurement × washout |
| [경보 후 첫 점검의 탐지 가능성 대비 시간](../cases/OPERATIONS/inspection-value-per-minute.md) | 표준 | inspection id × estimated hit probability × minutes |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [assumption-mapping](../methods/assumption-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 조건별 집계와 결측 처리를 먼저 확정. 규격과 관리한계는 다름.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
