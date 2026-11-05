# 업무 구조 라우터

업종 단어보다 출력으로 수행할 행동을 고른다. 혼합 문제는 주 문제 하나와 보조 최대 두 개로 나눈다.
근거가 없으면 분류 보류하고 데이터 한 건을 요청한다. 검색 점수는 성공확률이 아니다.

| 영역 | 해결 행동 | 먼저 볼 자료 | 반증 질문 | 기준 방법 | 다른 경로 |
|---|---|---|---|---|---|
| [ANALYTICS](families/ANALYTICS.md) | 기간·단위·분모를 맞춰 숫자 비교 | 비교 기간·환율·단위·집계 키 | 합계/비율 분모가 동일한가? | SQL/표 집계 | 한 개인에게 후보 순위를 정하면 RANKING |
| [SUPPORT](families/SUPPORT.md) | 문의를 분류·검색·이관 | 문의·기한·정책 문서 버전 | 답변보다 처리 순서가 필요한가? | 규칙 분류/키워드 검색 | 금액 실행은 TRANSACTION |
| [COACH](families/COACH.md) | 본인 설명의 근거·모순 확인 | 연습 구현물·결정/검증 로그 | 사전 연습이며 AI가 허용되는가? | 증거 대조·본인 응답 | 실제 AI 금지 평가는 중단 |
| [EVENT](families/EVENT.md) | 접수·정원·중복·대기 처리 | 신청 ID·시각·정원·상태 | 접수와 참가 확정은 같은가? | 상태 표·멱등 키 | 금액/재고 잠금은 TRANSACTION |
| [GEOMETRY](families/GEOMETRY.md) | 공간 포함·가림·겹침 | 좌표계·축척·장애물·설치 후보 | 면적의 합집합인가 시야인가? | 작은 격자/도형 계산 | 이동 순서는 MOBILITY |
| [LEARNING](families/LEARNING.md) | 수행에서 오개념·선수 지식 확인 | 문항·정답 근거·개념 관계 | 지식 회상인가 실제 적용인가? | 루브릭·소형 진단 | 개발자 설명 연습은 COACH |
| [OPERATIONS](families/OPERATIONS.md) | 시계열 변화·측정 이상 탐지 | 시각·측정 단위·조건·정비 이력 | 공정 변화인가 센서 결측인가? | 조건별 기준선 | 전환 승인/동등성은 QUALITY |
| [PLANNING](families/PLANNING.md) | 기간 전체의 제약 충족 계획 | 기간·수요·용량·고정 항목 | 개인 순위인가 기간 전체 제약인가? | 작은 전수 열거 | 개인 추천이면 RANKING |
| [POLICY](families/POLICY.md) | 규칙·승인·다음 행동 | 정책 버전·권한·증빙·상태 | 누가 예외 승인권자인가? | decision table | 실행 원자성은 TRANSACTION |
| [QUALITY](families/QUALITY.md) | 변경의 승인·동등성 검토 | lot·측정 신뢰도·허용차·필수 시험 | 유의차 없음인가 동등성 입증인가? | 필수 관문·구간 비교 | 시간 이상 경보는 OPERATIONS |
| [RANKING](families/RANKING.md) | 후보 필터 후 개인 순위 | 가용·금지조건·속성·선호 | 하드 조건을 만족한 후보가 있는가? | filter→rank | 기간 편성은 PLANNING |
| [MOBILITY](families/MOBILITY.md) | 방문 순서 또는 출발·도착 배정 | 거리/시간 행렬·창·용량·거점 | 경로가 고정되어 있는가? | 작은 순열·시간 역산 | 경로 고정이면 Routing 불필요 |
| [INTERACTIVE](families/INTERACTIVE.md) | 상태·충돌·시간 진행 | 상태·이벤트·시간 단위·종료 규칙 | 실제 다중 사용자가 필요한가? | 상태 전이·고정 시간 스텝 | 운영 접수는 EVENT |
| [TRANSACTION](families/TRANSACTION.md) | 심사·잠금·실행·재시도 | 요청 키·버전·가용/잠금·정밀도 | 승인과 실행 완료를 구분하는가? | 원자적 상태 전이 | 절차 설명만이면 POLICY |
| [DEPENDENCY](families/DEPENDENCY.md) | 관계 경로·전파·병목 | 방향·관계 종류·출처·계수 | 경로 존재인가 정량 영향인가? | 그래프 탐색 | 근거 없는 계수로 매출 전망 불가 |

예: 같은 식사 요청도 개인 후보 순위는 RANKING, 일주일 영양·예산 제약은 PLANNING, 기간별 비용 비교는 ANALYTICS다.
방문 순서 변경과 고정 경로 출발시각 결정 역시 구별한다.

## 출력할 것

맞는 이유 / 맞지 않을 이유 / 확인할 데이터 / 첫 질문 / 단순 기준 방법 / 카드 경로를 함께 제시한다.
담당자 답이 들어오면 기존 분류에 집착하지 말고 조건을 갱신한다.

```sh
python scripts/route.py "요청 내용"
```

스크립트 없이 이 표와 catalog/cases.json을 읽어도 된다. 실제 데이터·권한이 없을 때 자동 구현하지 않는다.
