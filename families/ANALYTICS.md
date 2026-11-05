# ANALYTICS: 기간·단위·분모를 맞춰 숫자 비교

최초 자료: 비교 기간·환율·단위·집계 키.
첫 분기 질문: 합계/비율 분모가 동일한가?
가장 단순한 기준: SQL/표 집계.
적용하지 않을 때: 한 개인에게 후보 순위를 정하면 RANKING.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [개관일 수가 다른 전시실 이용량 비교](../cases/analytics/open-day-rate.md) | 심화 | aggregation |
| [누적 관측계의 초기화와 단기 사용량](../cases/analytics/counter-reset.md) | 심화 | difference |
| [환산 기준일이 있는 구매비용 비교](../cases/analytics/currency-basis.md) | 표준 | normalization |
| [매출 차이를 가격과 물량으로 분해](../cases/analytics/price-volume-bridge.md) | 표준 | decomposition |
| [정정 파일의 최신 유효 레코드 선택](../cases/analytics/revision-ledger.md) | 표준 | version-reconciliation |
| [확률로 오인하지 않는 수요 시나리오](../cases/analytics/scenario-demand.md) | 표준 | scenario-analysis |
| [보고서 수치의 출처 연결 누락 찾기](../cases/analytics/report-source-coverage.md) | 표준 | traceability |
| [누락 수량이 있는 총량의 가능 범위](../cases/analytics/bounded-missing-total.md) | 표준 | partial-identification |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [job-story](../methods/job-story.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 분모·단위가 확정된 반복 집계에서 SQL로 확장. 표 한 장이면 표준 라이브러리 유지.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
