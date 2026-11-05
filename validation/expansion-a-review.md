# 확장 A 사례의 별도 에이전트 검토

2026-11-05. 작성자가 아닌 별도 에이전트가 확장 A의 18개 카드, 메타데이터·기대값 fixture, check_expansion_a.py 전체 분기를 읽었다. 같은 검토자는 다른 영역 문서를 작성했으므로 외부 블라인드 감사는 아니다. 실제 사용자·생산 앱·자연어 모델을 실행하지 않았다.

## 실제 검토 범위

- ANALYTICS 6개: currency-basis, price-volume-bridge, revision-ledger, scenario-demand, report-source-coverage, bounded-missing-total.
- SUPPORT 6개: support-rule-overlap, duplicate-ticket-fingerprint, draft-release-gate, escalation-authority, handoff-action-fields, repeat-cause-pareto.
- COACH 6개: rehearsal-budget, disclosure-labels, bilingual-quantity, revision-evidence-loss, assumption-challenge-queue, ai-verification-ledger.
- LEARNING의 answer-evidence-coverage를 추가로 읽어 report-source-coverage와 구조 차이를 비교했다.

카드의 요청·세 가지 가설·분기 질문·데이터 계약·기준 계산·최소 결과를 읽고 fixture 및 oracle과 대조했다. COACH의 사람이 제공하는 의미 태그와 수치만 검사한다는 제한, 실제 AI 금지 후속 평가 중 질문·답변·코칭 중단 경계도 확인했다.

## 최초 실행 결과와 추가 반례

처음 확인한 기존 suite는 Python 3.12.14에서 18개 사례, 59개 검사 모두 pass였다. 이 수치에는 아래 새 반례가 포함되어 있지 않았다. 통과만으로 계약 전체가 검증되었다고 볼 수 없음을 실제 반례로 확인했다.

| 함수 | 검토자가 추가한 입력 | 수정 전 실제 출력 | 문제 |
|---|---|---|---|
| draft_release_gate | checks=[true] | ready_for_human_send | 계약상 필수 검토3개인데2개가 누락되어도 발송 준비로 표시 |
| escalation_authority | amount=80,limit=100,special=null | within_authority | 특별 사고 여부 미확인을 false처럼 취급 |
| disclosure_labels | labels=[internal],destination=unknown | within_labels | public이 아닌 목적지를 모두 내부로 간주 |
| duplicate_ticket_fingerprint | 동일 ticket_id a와 동일 비교키 행 두 번 | [[a,a]] | 같은 접수의 재전송을 서로 다른 중복 접수 후보로 표시 |

작성자에게 위 입력을 그대로 전달해 필수 필드·상태 검증과 회귀 fixture를 요청했다. 이 기록은 수정 전 실제 실행 결과다. 이후 수정으로 suite 수가 늘어도 최초 59개 통과가 이 반례까지 확인했다는 의미로 바꾸지 않는다.

## 별도 수치 검산

생산·예제 함수를 가져오지 않고 별도 Fraction/정수 계산으로 아래 8개 대표 관계를 실행 확인했다.

| 사례 | 별도 계산 결과 |
|---|---|
| currency-basis | 12.50×1.24=15.50 |
| price-volume-bridge | (12−10)×5+12×(8−5)=46=96−50 |
| revision-ledger | 최신 값12+3=15 |
| scenario-demand | 80×[0.75,1,1.5]=[60,80,120] |
| bounded-missing-total | 관측8+5=13, 누락 상한10을 더하면23 |
| repeat-cause-pareto | 첫 두 원인의4/5=80% |
| bilingual-quantity | 2분×60=120초 |
| assumption-challenge-queue | 토론용 곱6>4 |

반올림 정책의 모든 입력, 통화 유한성·자릿수 상한, 대규모 실행 성능은 이 검산에 포함하지 않았다.

## 중복 사례와 의미 판정 범위

report-source-coverage는 source_id가 로컬 목록에 존재하는지 확인하는 연결 완전성 검사다. answer-evidence-coverage는 사람이 확인한 supports/opposes와 active 조건을 받아 주장별 근거 충돌을 판정할 수 있다. 알고리즘 일부가 집합 포함 검사로 겹치지만 활성 상태와 반대 근거는 결과를 바꾸는 추가 계약이다.

다만 처음 읽은 LEARNING의 네 fixture는 폐기 출처나 반대 근거를 직접 검사하지 않았다. 담당 작성자에게 “출처가 존재해도 inactive면 incomplete”, “활성 지지와 반대가 동시에 있으면 conflict” 반례를 추가하도록 요청했다. 이러한 결과 차이가 실행으로 확인되기 전에는 문구만으로 차별화가 충분하다고 확정하지 않는다.

COACH 사례는 실제 문장에서 의미·근거 ID를 자동 추출하지 않는다. same_scope나 present 같은 사람 확인값을 받아 처리하며, 코드 통과를 번역 정확성·설명 능력·비밀 탐지 성능으로 과장하지 않는 문구를 확인했다. report-source-coverage의 링크 존재는 내용 사실성 검증이 아니다. ai-verification-ledger도 evidence ID 존재만으로 원문 증거의 진위를 검증하지 않는다.

## 한계

이번 검토는 범용 유효성 검사를 완성하는 작업이 아니다. 유효 입력 중심의 소형 oracle이고 운영 코드가 아니므로, 모든 타입·누락·범위 오류를 처리한다고 주장할 수 없다. 추가 반례에서 발견한 위험한 허용 경로를 우선 수정하도록 요청했다. 공개 적합성은 창작 표시·개인 식별 정보 부재·평가 경계의 정적 검토이며, 비공개 원문 대조나 실제 사용자 효과 측정은 하지 않았다.

## A 작성자 수정 후 재실행

같은 검토자가 위 네 반례를 다시 호출했다. 결과는 각각 invalid, unknown, review, []로 바뀌어 누락을 승인으로 취급하거나 동일 접수를 중복 후보로 세던 문제가 해소되었다. 전체 suite도 직접 다시 실행해 18개 사례 66/66 pass를 확인했다. 추가된 일곱 검사는 필수 검토 개수·비불리언 값, 특별 사고 null·한도 null, 미확인 목적지, 동일 접수 재전송·동일 키 다른 내용이다. 이 수정 통과는 해당 반례의 회귀 증거이며 모든 잘못된 입력의 완전한 처리를 보장하지 않는다.

## 출처 연결 사례의 차별화 재확인

LEARNING 작성자가 추가한 활성 반대 근거, 폐기된 반대 근거, 폐기된 유일 지지 출처 세 fixture를 읽고 check_expansion_b.py를 직접 실행했다. answer-evidence-coverage의 7/7 결과가 통과했으며, 추가된 세 결과는 conflict / supported / incomplete였다. 같은 출처 ID 존재 여부만으로는 이 세 결과를 만들 수 없으므로 A의 report-source-coverage와 다른 계약·검증 조건이 실행 예제에서 확인되었다. 사람이 승인한 지지·반대 연결을 전제로 하며 자연어 사실성 판정을 실행한 것은 아니다.
