# RANKING: 후보 필터 후 개인 순위

최초 자료: 가용·금지조건·속성·선호.
첫 분기 질문: 하드 조건을 만족한 후보가 있는가?
가장 단순한 기준: filter→rank.
적용하지 않을 때: 기간 편성은 PLANNING.

## 대표 심화 사례

- [대여 가능한 관찰 키트 우선 추천](../cases/RANKING/ranking-availability.md): `filter rank`
- [읽기 목록의 주제 편중 제한](../cases/RANKING/ranking-diversity.md): `rank constrained selection`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [baseline-first](../methods/baseline-first.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 가용·금지 조건을 필터한 후 점수와 다양성. 정답 로그 없으면 정확도 주장 불가.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
