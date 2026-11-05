# 120개 묶음의 독립 검토

작성자와 다른 검토 에이전트가 새 90개 메타데이터의 결정·입력·필수조건·검증 기준을 읽고, 각 영역 한 건씩 15개 카드의 본문을 표본 확인했다. 중복 의심 사례는 추가로 본문·테스트를 대조했다. 모든 문장의 독립 전문가 심사나 실제 사용자 실험을 뜻하지 않는다.

## 구조와 실질적 차이

[구조 검사기](../scripts/validate_repo.py)는 표준 카드의 최소 3개 테스트, input/expected/basis, fixture, decision_signature, 고유 파일 경로, 카탈로그 밖 사례 파일을 검사한다. `0`, `false`, 빈 결과 집합은 정상 기대값으로 허용한다. 기존 심화 10개는 개별 basis 대신 본문의 명시적 손계산 근거를 사용하므로 경고를 남기며 새 표준 카드에 같은 예외를 적용하지 않는다.

[중복 후보 검사](distinctness-results.json)는 명시적 서명 90개와 기존 심화 30개의 파생 메타데이터를 비교했다. 같은 정규화 서명·전체 테스트 묶음은 발견하지 못했다. **이 결과는 독창성이나 의미 중복 부재를 증명하지 않는다.** 실제로 다음 문제는 자동 지문보다 수동 검토에서 발견했다.

| 검토 대상 | 발견 사항 | 반영한 차이 |
|---|---|---|
| policy-effective-version / policy-evidence | 둘 다 유효구간 문서 선택이었다 | 새 카드는 접수 버전 잠금과 소급 정책에 따라 같은 날짜에도 다른 결과·사유를 반환 |
| simultaneous-outcome / interactive-reset | HP·동시 사망 판정이 겹쳤다 | 새 카드는 도착 사건 묶음, 마감·유예시간, 동률 공동승자를 판정 |
| score-event-replay / event-reward-ledger | 키별 고유 금액 합산이 겹쳤다 | 새 득점 카드는 원사건 참조 취소·이중 취소·원사건 누락을 검증 |
| idempotent-fulfillment / transaction-reservation | 재처리 경계가 충분히 드러나지 않았다 | 이행 실패 후 부수효과 없음이 확인돼야 재시도; 불명확하면 수동 검토 |
| dependency-evidence-validity / policy-evidence | 단일 기간 유효성 검사였다 | 같은 방향·종류의 관계에 대해 유효한 지지/반박 출처를 함께 대조 |
| answer-evidence-coverage / report-source-coverage | 링크 존재와 사실 지지의 차이를 테스트해야 했다 | 활성 반대 근거, 폐기 반대 근거, 폐기된 유일 지지의 판정을 추가 |

운영 경보 후 첫 점검은 필수 안전 절차 이후 확률/시간 휴리스틱이다. 품질 승인 관문은 필수 합격 조건을 비용보다 먼저 적용한다. 두 사례는 사용자 결정·필수조건이 다르다. 품질 시험 매트릭스는 실행된 조합의 누락만 검사하며 합격을 판정하지 않는다. 최소 설치비와 고정 예산 최대 피복도 목적과 실행 불가능 조건이 달라 별개로 유지했다.

## 라우터의 가족 분류와 실제 카드 선택

먼저 새 요청을 고정한 뒤 120개 카탈로그로 실행했다. 가족 이름만 맞았다는 이유로 검색 성공이라고 세지 않았다.

| 검사 | 수정 전 | 일반 검색 개선 후 |
|---|---:|---:|
| 새 18개 요청의 주 가족/분류 보류 | 18/18 | 18/18 |
| 위 요청의 명시한 심화 카드 검색 | 16/17 | 16/17 |
| 새 표준 결정 15개 요청의 주 가족 | 14/15 | 15/15 |
| 기존 라우팅 회귀 | 별도 기존 기록 | 21/21 |
| AI 금지 후속 평가 중단 | 별도 기존 기록 | 3/3 |

개선은 긴 문장 키워드의 완전 일치만 검사하던 문제를 줄이기 위한 오프라인 한국어 2·3글자 n-gram과 역문서빈도 기반 검색이다. 명확한 구조어가 없을 때만 일반어를 제외한 카탈로그 키워드로 가족 후보를 찾고 모호하면 보류한다. 외부 모델·API를 쓰지 않는다. 수정 후 결과는 **관측한 문제를 반영한 회귀 결과이며 미관측 성능 추정이 아니다.** 숫자 개선만 보고 전체 성공을 주장하지 않는다.

15개 새 표준 결정 요청에서 선택 카드의 적용 범위를 수동으로 읽은 결과는 **표준 카드 적합 8, 기존 심화 카드로 적합 1, 부분 적합 4, 범위 공백 1, 검색 누락 1**이다. 상세 근거는 [수동 검토](routing-standard-manual-review.json)에 있다.

- 첫 방문자 기본 추천 카드는 있지만 해당 요청에서 상위 두 카드에 나오지 않았다.
- 대기자의 응답 기한 만료 후 승격은 선택된 정원/대기열 카드만으로 해결되지 않는다.
- 자연어 문의 유사 묶기를 정확한 복합키 중복 검사로 대신할 수 없다.
- 개인별 이동시간 상한 검사와 그 상한 자체를 최소화하는 최적화는 추가 단계가 다르다.
- 한 칸 이동 봇은 반복 왕복 방지나 추적/회피 상태를 검증하지 않았다.

[18개 사전 고정 요청](routing-expansion-tests.json), [수정 전](routing-expansion-before.json), [수정 후](routing-expansion-after.json), [표준 15개 요청](routing-standard-tests.json), [표준 수정 전](routing-standard-before.json), [표준 수정 후](routing-standard-after.json), [기존 회귀](routing-original21-after-expansion.json), [AI 금지 모드](routing-no-ai-after-expansion.json)를 구분해 보존한다.

## 본문 표본과 남은 한계

본문 표본: price-volume-bridge, duplicate-ticket-fingerprint, rehearsal-budget, event-reward-ledger, minimum-cover-cost, answer-evidence-coverage, inspection-value-per-minute, planning-service-coverage, policy-effective-version, test-matrix-coverage, ranking-without-labels, mobility-fair-travel-cap, score-event-replay, idempotent-fulfillment, dependency-evidence-validity.

표본에서 담당자 피드백과 개발자 PREP 설명 질문이 구분됐고, 실제 AI 금지 평가에서는 질문 생성·답변·코칭 중단 경계가 있었다. 일부 한글 띄어쓰기와 추가 테스트 행의 Markdown 표 끊김을 작성자에게 돌려 수정했다. 실제 입력·개인정보·비공개 원문을 사용해 사례를 역설계하지 않았다.

작은 계산 오라클은 선언한 합성 입력의 기대값을 검증한다. 완성 앱 120개, DB 동시성, 자연어 이해, 실제 운영 효과를 검증한 것은 아니다. 링크와 라이선스 검사는 별도 출처 기록을 따른다. 자동 비밀정보 검사가 공개 권한을 보장하지 않는다. 실제 과제를 받을 때는 해당 규정·자료·담당자 답변이 우선한다.
