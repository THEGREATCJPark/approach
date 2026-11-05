# COACH: 본인 설명의 근거·모순 확인

최초 자료: 연습 구현물·결정/검증 로그.
첫 분기 질문: 사전 연습이며 AI가 허용되는가?
가장 단순한 기준: 증거 대조·본인 응답.
적용하지 않을 때: 실제 AI 금지 평가는 중단.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [설명 연습의 수치 주장과 근거 대조](../cases/coach/claim-ledger.md) | 심화 | evidence-review |
| [모의 설명 평가자의 불일치 찾기](../cases/coach/rater-disagreement.md) | 심화 | agreement |
| [설명 분량과 필수 근거 유지](../cases/coach/rehearsal-budget.md) | 표준 | compression-review |
| [설명 자료의 공개 범위 라벨 점검](../cases/coach/disclosure-labels.md) | 표준 | information-boundary |
| [두 언어 설명의 수치와 단위 일치](../cases/coach/bilingual-quantity.md) | 표준 | semantic-consistency |
| [설명 수정 후 근거 항목의 회귀 검사](../cases/coach/revision-evidence-loss.md) | 표준 | regression-review |
| [근거가 약한 가정의 사전 설명 점검 순서](../cases/coach/assumption-challenge-queue.md) | 표준 | risk-first |
| [AI 산출물과 본인 확인 범위의 대조](../cases/coach/ai-verification-ledger.md) | 표준 | verification-accounting |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [traceability](../methods/traceability.md) → [검증](../methods/verification.md).

핵심 도구 후보: [python-stdlib](../tools/python-stdlib.md). 근거 표와 실제 파일 대조가 우선. 문자열 일치로 사실성을 확정하지 않음.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
