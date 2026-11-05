# INTERACTIVE: 상태·충돌·시간 진행

최초 자료: 상태·이벤트·시간 단위·종료 규칙.
첫 분기 질문: 실제 다중 사용자가 필요한가?
가장 단순한 기준: 상태 전이·고정 시간 스텝.
적용하지 않을 때: 운영 접수는 EVENT.

## 대표 심화 사례

- [격자 탐험에서 막힌 이동과 자원 감소](../cases/INTERACTIVE/interactive-collision.md): `state transitions collision`
- [동시 종료와 재시작의 세션 격리](../cases/INTERACTIVE/interactive-reset.md): `state machine event replay`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [vertical-slice](../methods/vertical-slice.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 상태·이벤트의 작은 재현부터. 렌더링 엔진은 사용자 요구 확인 후 별도 선택.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
