# RANKING: 후보 필터 후 개인 순위

최초 자료: 가용·금지조건·속성·선호.
첫 분기 질문: 하드 조건을 만족한 후보가 있는가?
가장 단순한 기준: filter→rank.
적용하지 않을 때: 기간 편성은 PLANNING.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [대여 가능한 관찰 키트 우선 추천](../cases/RANKING/ranking-availability.md) | 심화 | filter rank |
| [읽기 목록의 주제 편중 제한](../cases/RANKING/ranking-diversity.md) | 심화 | rank constrained selection |
| [초기 방문자용 안내 카드 기본 순위](../cases/RANKING/ranking-cold-start.md) | 표준 | smoothed-rate-ranking |
| [작업 조건과 가까운 공구 후보 순위](../cases/RANKING/ranking-attribute-distance.md) | 표준 | weighted-distance-ranking |
| [제한 성분 근거가 있는 재료 후보 필터](../cases/RANKING/ranking-restriction-evidence.md) | 표준 | three-state-restriction |
| [최근 선택의 반복 억제 기간](../cases/RANKING/ranking-repeat-cooldown.md) | 표준 | cooldown-ranking |
| [규칙 점수 추천의 기여도 설명](../cases/RANKING/ranking-score-explanation.md) | 표준 | additive-score-explanation |
| [정답 로그 없이 추천 결과의 기본 품질 점검](../cases/RANKING/ranking-without-labels.md) | 표준 | recommendation-invariants |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [baseline-first](../methods/baseline-first.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 가용·금지 조건을 필터한 후 점수와 다양성. 정답 로그 없으면 정확도 주장 불가.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
