# LEARNING: 수행에서 오개념·선수 지식 확인

최초 자료: 문항·정답 근거·개념 관계.
첫 분기 질문: 지식 회상인가 실제 적용인가?
가장 단순한 기준: 루브릭·소형 진단.
적용하지 않을 때: 개발자 설명 연습은 COACH.

## 완성 사례 8개

| 사례 | 깊이 | 선택할 문제 구조 |
|---|---|---|
| [선수 개념을 이수한 다음 실습 선택](../cases/LEARNING/prerequisite-ready.md) | 심화 | prerequisite graph |
| [미응답과 오답을 분리한 개념별 진단](../cases/LEARNING/concept-diagnostic.md) | 심화 | grouped rubric |
| [승인된 짧은 개념 설명 선택](../cases/LEARNING/approved-explanation.md) | 표준 | concept × version × character length |
| [역할·과정·산출물의 다중 분류 보류](../cases/LEARNING/taxonomy-ambiguity.md) | 표준 | entity id → approved category set |
| [회상 퀴즈의 예정일과 하루 한도](../cases/LEARNING/recall-due-queue.md) | 표준 | question × due_day × enabled |
| [오개념 태그별 승인 피드백 선택](../cases/LEARNING/misconception-feedback.md) | 표준 | attempt → misconception tags → feedback map |
| [답변 주장마다 활성 근거 연결](../cases/LEARNING/answer-evidence-coverage.md) | 표준 | claim ids × source-supported fact ids |
| [적용 과제 전후의 동일 참가자 변화](../cases/LEARNING/paired-transfer-gain.md) | 표준 | participant id × before/after score |

## 조건부 도구·방법

[기준 방법](../methods/baseline-first.md) → [example-mapping](../methods/example-mapping.md) → [검증](../methods/verification.md).

핵심 도구 후보: [networkx](../tools/networkx.md). 선수 관계가 커질 때 경로/사이클 검사. 학습 효과 입증은 별도.
설치가 안 되면 카드의 작은 표·손계산을 사용하고 규모와 검증 한계를 남긴다.

[발견 질문](../interviews/discovery.md) → [데이터 계약](../templates/data-contract.md) → [수용 테스트](../templates/acceptance-tests.md) → [사용자 피드백](../interviews/prototype-feedback.md).

도구 채택 전 [규정 확인](../RULES_GATE.md). 기본값은 새 설치·외부 전송·자동 조작 없음이다.
[라우터로 돌아가기](../ROUTER.md). 이 영역은 심화2건과 표준6건으로 완성했다. 업무 구조가 다른 사례만 선택하고 조건은 실제 담당자에게 확인한다.
