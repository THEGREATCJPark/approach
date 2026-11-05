# ANALYTICS: 기간·단위·분모를 맞춰 숫자 비교

최초 자료: 비교 기간·환율·단위·집계 키.
첫 분기 질문: 합계/비율 분모가 동일한가?
가장 단순한 기준: SQL/표 집계.
적용하지 않을 때: 한 개인에게 후보 순위를 정하면 RANKING.

## 대표 심화 사례

- [개관일 수가 다른 전시실 이용량 비교](../cases/analytics/open-day-rate.md): `aggregation`
- [누적 관측계의 초기화와 단기 사용량](../cases/analytics/counter-reset.md): `difference`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [job-story](../methods/job-story.md) → [검증](../methods/verification.md).

핵심 도구 후보: [sqlite](../tools/sqlite.md). 분모·단위가 확정된 반복 집계에서 SQL로 확장. 표 한 장이면 표준 라이브러리 유지.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
