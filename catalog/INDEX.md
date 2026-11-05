# 완성 사례 120개 색인

15영역에 각각 심화2건·표준6건. 단어가 비슷해도 실제 결정과 필수조건이 다르면 다른 카드를 선택한다.
[라우터](../ROUTER.md) · [검증 결과](../validation/expansion-quality-report.md)

## ANALYTICS

- [개관일 수가 다른 전시실 이용량 비교](../cases/analytics/open-day-rate.md) — deep / `open-day-rate`
- [누적 관측계의 초기화와 단기 사용량](../cases/analytics/counter-reset.md) — deep / `counter-reset`
- [환산 기준일이 있는 구매비용 비교](../cases/analytics/currency-basis.md) — standard / `currency-basis`
- [매출 차이를 가격과 물량으로 분해](../cases/analytics/price-volume-bridge.md) — standard / `price-volume-bridge`
- [정정 파일의 최신 유효 레코드 선택](../cases/analytics/revision-ledger.md) — standard / `revision-ledger`
- [확률로 오인하지 않는 수요 시나리오](../cases/analytics/scenario-demand.md) — standard / `scenario-demand`
- [보고서 수치의 출처 연결 누락 찾기](../cases/analytics/report-source-coverage.md) — standard / `report-source-coverage`
- [누락 수량이 있는 총량의 가능 범위](../cases/analytics/bounded-missing-total.md) — standard / `bounded-missing-total`

## COACH

- [설명 연습의 수치 주장과 근거 대조](../cases/coach/claim-ledger.md) — deep / `claim-ledger`
- [모의 설명 평가자의 불일치 찾기](../cases/coach/rater-disagreement.md) — deep / `rater-disagreement`
- [설명 분량과 필수 근거 유지](../cases/coach/rehearsal-budget.md) — standard / `rehearsal-budget`
- [설명 자료의 공개 범위 라벨 점검](../cases/coach/disclosure-labels.md) — standard / `disclosure-labels`
- [두 언어 설명의 수치와 단위 일치](../cases/coach/bilingual-quantity.md) — standard / `bilingual-quantity`
- [설명 수정 후 근거 항목의 회귀 검사](../cases/coach/revision-evidence-loss.md) — standard / `revision-evidence-loss`
- [근거가 약한 가정의 사전 설명 점검 순서](../cases/coach/assumption-challenge-queue.md) — standard / `assumption-challenge-queue`
- [AI 산출물과 본인 확인 범위의 대조](../cases/coach/ai-verification-ledger.md) — standard / `ai-verification-ledger`

## DEPENDENCY

- [수리 부품 중단의 영향 경로 추적](../cases/DEPENDENCY/dependency-reachability.md) — deep / `dependency-reachability`
- [전시 설치 작업의 선행관계와 최소 완료시간](../cases/DEPENDENCY/dependency-critical-path.md) — deep / `dependency-critical-path`
- [관계 종류를 구분한 직접 영향 조회](../cases/DEPENDENCY/dependency-relation-types.md) — standard / `dependency-relation-types`
- [중간 노드 제거로 드러나는 연결 병목](../cases/DEPENDENCY/dependency-removal-bottleneck.md) — standard / `dependency-removal-bottleneck`
- [대체 공급을 포함한 운영 가능 논리](../cases/DEPENDENCY/dependency-alternative-supply.md) — standard / `dependency-alternative-supply`
- [가정한 영향 계수의 민감도 비교](../cases/DEPENDENCY/dependency-coefficient-sensitivity.md) — standard / `dependency-coefficient-sensitivity`
- [동일 관계의 상충 출처와 유효 근거 판정](../cases/DEPENDENCY/dependency-evidence-validity.md) — standard / `dependency-evidence-validity`
- [복수 관계를 잃지 않는 그래프 표시 집계](../cases/DEPENDENCY/dependency-multigraph-display.md) — standard / `dependency-multigraph-display`

## EVENT

- [시간대가 다른 신청의 마감 판정](../cases/event/deadline-offset.md) — deep / `deadline-offset`
- [중복 요청이 있는 소규모 워크숍 정원](../cases/event/seat-retry.md) — deep / `seat-retry`
- [실습 참여 자격의 만료일 판정](../cases/event/event-eligibility.md) — standard / `event-eligibility`
- [입장 재스캔과 미등록 코드 분리](../cases/event/event-checkin.md) — standard / `event-checkin`
- [참여 완료 보상의 한 번 지급](../cases/event/event-reward-ledger.md) — standard / `event-reward-ledger`
- [취소 후 재신청의 대기 순번](../cases/event/event-cancel-priority.md) — standard / `event-cancel-priority`
- [운영 리허설의 동시 체류 인원](../cases/event/event-rehearsal-capacity.md) — standard / `event-rehearsal-capacity`
- [현장 예외 승인의 범위와 유효시간](../cases/event/event-exception-expiry.md) — standard / `event-exception-expiry`

## GEOMETRY

- [겹치는 바닥 점검 구역의 면적](../cases/geometry/rectangle-union.md) — deep / `rectangle-union`
- [예산 내 점검 거점의 이산 커버리지](../cases/geometry/budget-cover.md) — deep / `budget-cover`
- [직선 시야와 차폐판의 앞뒤](../cases/geometry/sightline-barrier.md) — standard / `sightline-barrier`
- [모든 점검 구역을 덮는 최소 설치비](../cases/geometry/minimum-cover-cost.md) — standard / `minimum-cover-cost`
- [중요 구역 가중치로 단일 센서 선택](../cases/geometry/priority-zone-weight.md) — standard / `priority-zone-weight`
- [설치 금지 사각형과 후보점 경계 판정](../cases/geometry/installation-exclusion.md) — standard / `installation-exclusion`
- [도면 좌표와 실측 기준선의 축척 검사](../cases/geometry/drawing-unit-check.md) — standard / `drawing-unit-check`
- [고정 관측점의 반경 안 표적 집계](../cases/geometry/radial-monitor-range.md) — standard / `radial-monitor-range`

## INTERACTIVE

- [격자 탐험에서 막힌 이동과 자원 감소](../cases/INTERACTIVE/interactive-collision.md) — deep / `interactive-collision`
- [동시 종료와 재시작의 세션 격리](../cases/INTERACTIVE/interactive-reset.md) — deep / `interactive-reset`
- [경과 시간에 따른 산소 자원 소모](../cases/INTERACTIVE/survival-resource-tick.md) — standard / `survival-resource-tick`
- [단순 봇의 한 칸 이동과 막힌 경로](../cases/INTERACTIVE/bot-grid-step.md) — standard / `bot-grid-step`
- [시간별 안전 반경과 경계 피해](../cases/INTERACTIVE/shrinking-safe-zone.md) — standard / `shrinking-safe-zone`
- [마감 유예와 완주 동률의 최종 승자](../cases/INTERACTIVE/simultaneous-outcome.md) — standard / `simultaneous-outcome`
- [원획득에 연결된 득점 취소와 이중 취소](../cases/INTERACTIVE/score-event-replay.md) — standard / `score-event-replay`
- [동시 참여 요구에 따른 서버 범위 결정](../cases/INTERACTIVE/multiplayer-scope-gate.md) — standard / `multiplayer-scope-gate`

## LEARNING

- [선수 개념을 이수한 다음 실습 선택](../cases/LEARNING/prerequisite-ready.md) — deep / `prerequisite-ready`
- [미응답과 오답을 분리한 개념별 진단](../cases/LEARNING/concept-diagnostic.md) — deep / `concept-diagnostic`
- [승인된 짧은 개념 설명 선택](../cases/LEARNING/approved-explanation.md) — standard / `approved-explanation`
- [역할·과정·산출물의 다중 분류 보류](../cases/LEARNING/taxonomy-ambiguity.md) — standard / `taxonomy-ambiguity`
- [회상 퀴즈의 예정일과 하루 한도](../cases/LEARNING/recall-due-queue.md) — standard / `recall-due-queue`
- [오개념 태그별 승인 피드백 선택](../cases/LEARNING/misconception-feedback.md) — standard / `misconception-feedback`
- [답변 주장마다 활성 근거 연결](../cases/LEARNING/answer-evidence-coverage.md) — standard / `answer-evidence-coverage`
- [적용 과제 전후의 동일 참가자 변화](../cases/LEARNING/paired-transfer-gain.md) — standard / `paired-transfer-gain`

## MOBILITY

- [수리 부품 순회 수거의 방문 순서](../cases/MOBILITY/mobility-tour.md) — deep / `mobility-tour`
- [고정 순회 점검의 출발 가능 구간](../cases/MOBILITY/mobility-departure.md) — deep / `mobility-departure`
- [분할 불가 수거 상자의 차량 배정](../cases/MOBILITY/mobility-indivisible-capacity.md) — standard / `mobility-indivisible-capacity`
- [대기 허용 경로의 서비스 시작 시간](../cases/MOBILITY/mobility-window-wait.md) — standard / `mobility-window-wait`
- [가장 먼 방문지를 줄이는 출발 거점](../cases/MOBILITY/mobility-depot-minimax.md) — standard / `mobility-depot-minimax`
- [인접 수요 지점의 연결 묶음](../cases/MOBILITY/mobility-demand-clusters.md) — standard / `mobility-demand-clusters`
- [개인별 최대 이동시간을 지키는 지점 배정](../cases/MOBILITY/mobility-fair-travel-cap.md) — standard / `mobility-fair-travel-cap`
- [미배정 수요와 과배정의 수량 대사](../cases/MOBILITY/mobility-unserved-ledger.md) — standard / `mobility-unserved-ledger`

## OPERATIONS

- [누락 센서와 실제 상한 초과 분리](../cases/OPERATIONS/missing-versus-alarm.md) — deep / `missing-versus-alarm`
- [혼합 구성 변화와 유형별 품질 변화 분리](../cases/OPERATIONS/stratified-rate.md) — deep / `stratified-rate`
- [불규칙 시간 간격의 변화율](../cases/OPERATIONS/time-slope.md) — standard / `time-slope`
- [방향을 보존한 위치 오차 판정](../cases/OPERATIONS/position-error-vector.md) — standard / `position-error-vector`
- [동일 시료를 이용한 장비 간 편향](../cases/OPERATIONS/paired-instrument-bias.md) — standard / `paired-instrument-bias`
- [작은 양의 변화의 누적 경보](../cases/OPERATIONS/one-sided-cusum.md) — standard / `one-sided-cusum`
- [정비 전후 비교에서 안정화 구간 제외](../cases/OPERATIONS/maintenance-washout.md) — standard / `maintenance-washout`
- [경보 후 첫 점검의 탐지 가능성 대비 시간](../cases/OPERATIONS/inspection-value-per-minute.md) — standard / `inspection-value-per-minute`

## PLANNING

- [고정 활동을 포함한 3일 서비스 편성](../cases/PLANNING/rotation-budget.md) — deep / `rotation-budget`
- [팩 단위 발주와 입고 시점 구별](../cases/PLANNING/pack-order.md) — deep / `pack-order`
- [서비스 묶음의 비용과 최소 성능](../cases/PLANNING/planning-resource-blend.md) — standard / `planning-resource-blend`
- [서비스 종류의 최소 재등장 간격](../cases/PLANNING/planning-repeat-gap.md) — standard / `planning-repeat-gap`
- [대체 자재의 환산량과 손실](../cases/PLANNING/planning-substitute-stock.md) — standard / `planning-substitute-stock`
- [공급 중단 후 기존 계획의 최소 변경](../cases/PLANNING/planning-outage-repair.md) — standard / `planning-outage-repair`
- [수요와 용량 충돌의 부족량 설명](../cases/PLANNING/planning-infeasible-witness.md) — standard / `planning-infeasible-witness`
- [고정 근무 구간의 서비스 공백 찾기](../cases/PLANNING/planning-service-coverage.md) — standard / `planning-service-coverage`

## POLICY

- [증빙 누락과 승인 권한을 분리한 비용 안내](../cases/POLICY/evidence-approval.md) — deep / `evidence-approval`
- [반려 후 재제출과 중복 이벤트 제어](../cases/POLICY/resubmission-state.md) — deep / `resubmission-state`
- [대리 승인 위임의 한도와 기간](../cases/POLICY/policy-delegation.md) — standard / `policy-delegation`
- [증빙 번호가 겹치는 신청 검토](../cases/POLICY/policy-duplicate-claim.md) — standard / `policy-duplicate-claim`
- [정책 개정 중 접수된 신청의 경과조치](../cases/POLICY/policy-effective-version.md) — standard / `policy-effective-version`
- [처리 상태와 역할별 다음 행동](../cases/POLICY/policy-next-action.md) — standard / `policy-next-action`
- [작성자와 최종 승인자의 분리](../cases/POLICY/policy-separation-duties.md) — standard / `policy-separation-duties`
- [공유 증빙의 부서별 배분 잔액](../cases/POLICY/policy-receipt-allocation.md) — standard / `policy-receipt-allocation`

## QUALITY

- [필수 승인 누락을 가격으로 상쇄하지 않는 후보 비교](../cases/QUALITY/mandatory-gates.md) — deep / `mandatory-gates`
- [차이 미검출과 동등성 구간 판정 구별](../cases/QUALITY/equivalence-interval.md) — deep / `equivalence-interval`
- [Lot 크기를 반영한 불량률](../cases/QUALITY/lot-pooled-defects.md) — standard / `lot-pooled-defects`
- [동일 시료 반복측정의 산포](../cases/QUALITY/repeatability-range.md) — standard / `repeatability-range`
- [비용·공급 위험을 합치지 않은 비지배 후보](../cases/QUALITY/risk-pareto.md) — standard / `risk-pareto`
- [조건별 시험 누락을 찾는 커버리지 표](../cases/QUALITY/test-matrix-coverage.md) — standard / `test-matrix-coverage`
- [단계 전환의 확대·유지·되돌림 규칙](../cases/QUALITY/rollout-stop-rule.md) — standard / `rollout-stop-rule`
- [신규 공급원 시범 전환량의 노출 상한](../cases/QUALITY/trial-exposure-cap.md) — standard / `trial-exposure-cap`

## RANKING

- [대여 가능한 관찰 키트 우선 추천](../cases/RANKING/ranking-availability.md) — deep / `ranking-availability`
- [읽기 목록의 주제 편중 제한](../cases/RANKING/ranking-diversity.md) — deep / `ranking-diversity`
- [초기 방문자용 안내 카드 기본 순위](../cases/RANKING/ranking-cold-start.md) — standard / `ranking-cold-start`
- [작업 조건과 가까운 공구 후보 순위](../cases/RANKING/ranking-attribute-distance.md) — standard / `ranking-attribute-distance`
- [제한 성분 근거가 있는 재료 후보 필터](../cases/RANKING/ranking-restriction-evidence.md) — standard / `ranking-restriction-evidence`
- [최근 선택의 반복 억제 기간](../cases/RANKING/ranking-repeat-cooldown.md) — standard / `ranking-repeat-cooldown`
- [규칙 점수 추천의 기여도 설명](../cases/RANKING/ranking-score-explanation.md) — standard / `ranking-score-explanation`
- [정답 로그 없이 추천 결과의 기본 품질 점검](../cases/RANKING/ranking-without-labels.md) — standard / `ranking-without-labels`

## SUPPORT

- [수리 문의의 마감 여유시간 정렬](../cases/support/repair-slack.md) — deep / `repair-slack`
- [문의일 기준으로 유효한 안내문 찾기](../cases/support/policy-evidence.md) — deep / `policy-evidence`
- [분류 규칙이 겹치는 문의의 검토 대기](../cases/support/support-rule-overlap.md) — standard / `support-rule-overlap`
- [명시적 키로 중복 접수 후보 묶기](../cases/support/duplicate-ticket-fingerprint.md) — standard / `duplicate-ticket-fingerprint`
- [답변 초안의 발송 전 필수 검토](../cases/support/draft-release-gate.md) — standard / `draft-release-gate`
- [권한 범위를 넘는 보상 요청 이관](../cases/support/escalation-authority.md) — standard / `escalation-authority`
- [교대 인수인계의 다음 행동 누락](../cases/support/handoff-action-fields.md) — standard / `handoff-action-fields`
- [반복 문의 원인의 누적 비중](../cases/support/repeat-cause-pareto.md) — standard / `repeat-cause-pareto`

## TRANSACTION

- [대여 재고의 예약 잠금과 실행 분리](../cases/TRANSACTION/transaction-reservation.md) — deep / `transaction-reservation`
- [소수 재료 사용량의 정산 반올림 시점](../cases/TRANSACTION/transaction-rounding.md) — deep / `transaction-rounding`
- [승인 결과와 실제 실행 상태 분리](../cases/TRANSACTION/review-execution-separation.md) — standard / `review-execution-separation`
- [정책 실패 사유 코드의 우선순위](../cases/TRANSACTION/policy-reason-priority.md) — standard / `policy-reason-priority`
- [필수 증빙 누락과 수동 검토 경로](../cases/TRANSACTION/evidence-manual-review.md) — standard / `evidence-manual-review`
- [이행 요청 재처리와 payload 충돌](../cases/TRANSACTION/idempotent-fulfillment.md) — standard / `idempotent-fulfillment`
- [수량 시점과 단가 시점의 일치 검사](../cases/TRANSACTION/valuation-time-alignment.md) — standard / `valuation-time-alignment`
- [변경 이력의 수량 연속성 대조](../cases/TRANSACTION/ledger-chain-audit.md) — standard / `ledger-chain-audit`
