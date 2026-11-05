# INTERACTIVE: 상태·충돌·시간 진행

최초 자료: 상태·이벤트·시간 단위·종료 규칙.
첫 분기 질문: 실제 다중 사용자가 필요한가?
가장 단순한 기준: 상태 전이·고정 시간 스텝.
적용하지 않을 때: 운영 접수는 EVENT.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [격자 탐험에서 막힌 이동과 자원 감소](../cases/INTERACTIVE/interactive-collision.md) | 심화 | state transitions collision |
| [동시 종료와 재시작의 세션 격리](../cases/INTERACTIVE/interactive-reset.md) | 심화 | state machine event replay |
| [경과 시간에 따른 산소 자원 소모](../cases/INTERACTIVE/survival-resource-tick.md) | 표준 | time-step |
| [단순 봇의 한 칸 이동과 막힌 경로](../cases/INTERACTIVE/bot-grid-step.md) | 표준 | grid-policy |
| [시간별 안전 반경과 경계 피해](../cases/INTERACTIVE/shrinking-safe-zone.md) | 표준 | time-dependent-geometry |
| [마감 유예와 완주 동률의 최종 승자](../cases/INTERACTIVE/simultaneous-outcome.md) | 표준 | deadline-finish-ranking |
| [원획득에 연결된 득점 취소와 이중 취소](../cases/INTERACTIVE/score-event-replay.md) | 표준 | score-reversal-ledger |
| [동시 참여 요구에 따른 서버 범위 결정](../cases/INTERACTIVE/multiplayer-scope-gate.md) | 표준 | scope-decision-table |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [vertical-slice](../methods/vertical-slice.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 상태·이벤트의 작은 재현부터. 렌더링 엔진은 사용자 요구 확인 후 별도 선택.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
