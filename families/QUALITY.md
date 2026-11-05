# QUALITY: 변경의 승인·동등성 검토

최초 자료: lot·측정 신뢰도·허용차·필수 시험.
첫 분기 질문: 유의차 없음인가 동등성 입증인가?
가장 단순한 기준: 필수 관문·구간 비교.
적용하지 않을 때: 시간 이상 경보는 OPERATIONS.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [필수 승인 누락을 가격으로 상쇄하지 않는 후보 비교](../cases/QUALITY/mandatory-gates.md) | 심화 | hard gates before ranking |
| [차이 미검출과 동등성 구간 판정 구별](../cases/QUALITY/equivalence-interval.md) | 심화 | interval containment |
| [Lot 크기를 반영한 불량률](../cases/QUALITY/lot-pooled-defects.md) | 표준 | lot × inspected count × defect count |
| [동일 시료 반복측정의 산포](../cases/QUALITY/repeatability-range.md) | 표준 | specimen × repeated measurements |
| [비용·공급 위험을 합치지 않은 비지배 후보](../cases/QUALITY/risk-pareto.md) | 표준 | eligible candidate × cost × lead days × risk score |
| [조건별 시험 누락을 찾는 커버리지 표](../cases/QUALITY/test-matrix-coverage.md) | 표준 | required test×condition pairs vs executed pairs |
| [단계 전환의 확대·유지·되돌림 규칙](../cases/QUALITY/rollout-stop-rule.md) | 표준 | stage observation × count × critical events |
| [신규 공급원 시범 전환량의 노출 상한](../cases/QUALITY/trial-exposure-cap.md) | 표준 | demand × qualified cap × loss budget × pack size |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [premortem](../methods/premortem.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 필수 관문과 구간 계산을 분리. 유의차 없음으로 동등성을 주장하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
