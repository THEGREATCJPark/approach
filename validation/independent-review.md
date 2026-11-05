# 별도 검토 에이전트의 사용성·내용 검토

검토일: 2026-11-05. 실제 별도 검토 에이전트가 파일을 읽고 계산·라우터 호출을 수행했다. 실제 업무 사용자 관찰, 블라인드 외부 벤치마크, 생산 앱 검증은 아니다. 검토자는 워크플로 문서 작성에 참여했으므로 완전히 독립적인 외부 심사자도 아니다. 다른 작성자의 사례와 루트 진입 문서를 검토했다.

## 최소 탐색 경로

공통으로 AGENTS.md → START_HERE.md → RULES_GATE.md → ROUTER.md를 읽었다. 이 경로는 모드·자료 우선·질문 최대 3개·최소 결과·AI 금지 후속 단계 중단을 찾기에 충분했다. 이후 아래 1~2개 카드만으로 다음 행동을 구성할 수 있었다. 독서 시간·토큰 수·속도 향상은 측정하지 않았다.

| 새 창작 요청 | 수동 선택 파일 | 먼저 확인할 질문 | 최소 결과 |
|---|---|---|---|
| 공유 공구함에서 같은 대여 요청이 두 번 들어와도 남은 수량이 한 번만 줄어야 해. 빌려줄지 판단하는 절차는 이미 정해져 있어. | [transaction-reservation](../cases/TRANSACTION/transaction-reservation.md) | 같은 요청을 식별할 키가 있는가? 수량은 승인 시 잠그는가 인도 시 차감하는가? 실제 동시 요청이 있는가? | 초기 수량·요청 로그 → 중복 판정·잠금 상태 → 가용량과 재전송 결과 표. 순차 예제가 동시성 안전을 증명하지 않음을 표시 |
| 책방에서 세 권을 추천하되 같은 주제는 한 권까지만 넣고 재고 없는 책은 빼줘. 주간 편성은 필요 없어. | [ranking-diversity](../cases/RANKING/ranking-diversity.md), [ranking-availability](../cases/RANKING/ranking-availability.md) | 주제 상한은 필수인가? 재고 시점은 언제인가? 복수 주제·동점은 어떻게 처리하는가? | 가용 필터 → 주제별 1개 제한 조합 → 최대 3권과 부족 사유. 필요 없는 기간 계획은 제외 |
| 청소 작업 구역 두 개가 겹쳐서 실제 닦은 바닥 면적을 계산하고 싶어. 그림보다는 숫자 보고서가 필요해. | [rectangle-union](../cases/geometry/rectangle-union.md) | 기록은 완료 영역인가 계획인가? 공통 평면 단위인가? 직사각형으로 충분한가? | 두 영역·단위 → 합집합과 중복 면적 → 면적 보고서. 화면 앱이나 시야 모델을 추가하지 않음 |

문서만 읽는 경로는 위 표로 점검했다. Python이 없으면 표와 손계산으로 기대값을 확인할 수 있다. 실제 설치 실패 환경을 재현한 것은 아니다.

## 최초 스크립트 결과 — 수정 전 동결

위 세 문장은 기존 routing-tests.json에 없던 새 문장이다. 단, 검토자가 라우터와 카드 일부를 읽은 뒤 작성했으므로 완전한 블라인드 테스트가 아니다. 당시 준비된 part 카탈로그들을 합쳐 route 함수에 전달했고, TASK 모드로 실행했다.

| 요청 | 최초 실제 결과 | 판단 |
|---|---|---|
| 중복 대여 수량 | unclassified, 후보 없음 | 잘못된 도구를 실행하지 않은 것은 안전하지만 일상어 동의어 탐색 누락 |
| 책 3권, 주간 편성 불필요 | PLANNING primary, RANKING secondary | 부정된 주간·편성을 긍정 단서로 세어 주 문제 오분류 |
| 중복 청소 면적 보고 | GEOMETRY primary | 적합. rectangle-union이 첫 카드 |

최초 결과는 올바른 primary 1/3, 보류 1/3, 오분류 1/3이다. 이 작은 목적 표본을 전체 정확도로 일반화하지 않는다. 수정 담당자에게 정확한 문장과 기대 방향을 전달했다. 이후 이 문장에 맞춘 통과는 회귀 수정 증거이며 독립 최초 성공으로 바꾸지 않는다. 수정 후 결과는 별도 라우팅 보고서를 따른다.

명시적으로 mode=NO_AI_REVIEW로 동일 종류의 연습 요청을 호출하면 status=stopped, candidates=[]를 반환함을 실행 확인했다. 자연어만 보고 모드를 자동 판별하는 안전장치는 아니므로 에이전트가 진입 모드를 먼저 확인해야 한다.

## 사례 내용·기대값 검토 범위

15영역 중 아래 20개 카드를 읽었다. 각 영역 대표 하나의 손계산/별도 표준 라이브러리 계산 15건을 실행해 문서 기대값과 일치함을 확인했다. 원래 예제 함수를 가져오지 않았다. 나머지 경계·결측·정책 설명은 정적으로 읽었으며 전체 수용 테스트 실행으로 세지 않는다.

| 영역 | 읽은 카드 | 독립 재계산한 대표 결과 | 제한 |
|---|---|---|---|
| ANALYTICS | open-day-rate | 480/12=40 | 분모 정책 확인 필요 |
| SUPPORT | repair-slack | 90−60=30 | 최적 일정 보장 아님 |
| COACH | claim-ledger | 동일 의미의 8=8 supported | 자연어 의미 판정 실행 아님 |
| EVENT | seat-retry | p,p,p,q의 고유 좌석 p,q | 동시 쓰기 검증 아님 |
| GEOMETRY | rectangle-union | 6+4−2=8 | 정수 축정렬 사각형 한정 |
| LEARNING | prerequisite-ready, concept-diagnostic | done={intro} → join,measure | 교육 효과 검증 아님 |
| OPERATIONS | stratified-rate, missing-versus-alarm | 원비율26%, 표준화 후31% | 인과 추정 아님 |
| PLANNING | rotation-budget, pack-order | 27개 열거 최저 A,B,A=14 | 대규모 솔버 성능 검증 아님 |
| POLICY | resubmission-state, evidence-approval | 허용 전이5회 후 approved | 실제 승인·경합 검사 아님 |
| QUALITY | equivalence-interval, mandatory-gates | −0.2>−0.5 및0.3<0.5 | 구간 추정·통계 동등성 검정 아님 |
| RANKING | ranking-diversity | 모든 3개 조합 중 cap2 최고23 | 실제 독자 만족도 미측정 |
| MOBILITY | mobility-departure | 구간 교집합[540,550] | 대기 불가 가정 |
| INTERACTIVE | interactive-reset | 같은 tick 피해 후 hp0/0 | ready gate·타이머·네트워크 미검증 |
| TRANSACTION | transaction-rounding | Fraction 원금 합6 | 동시 정산 시스템 아님 |
| DEPENDENCY | dependency-critical-path | max(6,5)+2=8 | 자원 무제한 가정 |

메타데이터의 synthetic, family, 방법·도구 ID, 적용/비적용 조건, 필드 설명을 읽었다. 최종 전체 카탈로그 스키마·링크 검사는 별도의 자동 검증 결과를 따른다.

## 발견하여 작성자에게 전달한 사항

- A 그룹: 계약 필드명과 작은 fixture 별칭이 다름(open_days/days, due_in_minutes/due, capacity/cap 등). 명시적 변환표가 필요하다. 계산 결과 오류와 구별한다.
- A 그룹: 모든 카드에 같은 “normal과 boundary/missing은 달라야 한다” 문장을 쓰면 normal과 boundary 모두8인 면적 예제에서 혼란이 생긴다. 실제 결과가 다른 쌍을 지정해야 한다.
- B 그룹: rotation-budget의 available_days, evidence-approval의 policy_version, equivalence-interval의 margin·confidence·interval_method가 최소 계약에는 있으나 축약 fixture에는 생략되어 있었다. 공통 컨텍스트 또는 생략 범위를 명시해야 한다. 특히 주어진 구간 포함 검사를 실제 통계 검정으로 확대하지 않아야 한다.
- 라우터: 부정문과 일상어 동의어에 대한 최초 실패는 위에 보존했다. 수정 여부와 무관하게 어휘 검색을 의미 해석이나 권한 판정으로 사용하면 안 된다.

이 목록은 발견 당시 기록이다. 수정 담당자의 후속 변경을 자동으로 재검증한 것으로 해석하지 않는다.

## 공개 적합성과 평가 경계

검토한 진입 문서·20개 카드·24개 워크플로 문서에서 실제 인물·비공개 과제 원문·개인 연락처·실제 기관 데이터는 발견하지 않았다. 합성 정책과 일반 알고리즘 조건으로 설명되며 실제 과제와 대응표를 만들지 않는다. 이 정적 검토는 출처의 완전한 독립성을 수학적으로 증명하거나 저장소 이력 전체의 무누출을 보장하지 않는다. 비공개 프로젝트 원문은 이 검토에 읽거나 대조하지 않았다.

AGENTS/START_HERE/RULES_GATE와 설명 연습 진입점 모두 실제 AI 금지 평가의 질문 생성·답변 작성·실시간 코칭 중단을 명시한다. 담당자 피드백을 금지 단계의 우회로로 쓰지 않는다는 문구도 확인했다. TASK의 실제 입력·답변·결과를 공개 참고 저장소에 푸시하지 않도록 안내한다. 자동 전송·실제 사용자 검증·실시간 코칭을 실행하지 않았다.

## 후속 수정 재확인

B 그룹 작성자의 수정 후 해당 세 카드 문구를 다시 읽었다. rotation-budget은 모든 날 가용이라는 고정 컨텍스트, evidence-approval은 합성 v1이며 버전 선택 미검증, equivalence-interval은 interval_method/confidence를 의도적으로 생략한 숫자 포함 검사이며 실제 통계 판정은 unknown이라는 설명을 확인했다. 이로써 발견한 세 축약 fixture의 적용 범위가 명시되었다. 원문에 없는 필드 검증을 실행했다고 주장하는 방식으로 수정하지 않았다.
