# COACH: 본인 설명의 근거·모순 확인

최초 자료: 연습 구현물·결정/검증 로그.
첫 분기 질문: 사전 연습이며 AI가 허용되는가?
가장 단순한 기준: 증거 대조·본인 응답.
적용하지 않을 때: 실제 AI 금지 평가는 중단.

## 대표 심화 사례

- [설명 연습의 수치 주장과 근거 대조](../cases/coach/claim-ledger.md): `evidence-review`
- [모의 설명 평가자의 불일치 찾기](../cases/coach/rater-disagreement.md): `agreement`

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [traceability](../methods/traceability.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 근거 표와 실제 파일 대조가 우선. 문자열 일치로 사실성을 확정하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역의 추가6건은 미작성이며 120건 확장 목표와 현재 완료 수를 구별한다.
