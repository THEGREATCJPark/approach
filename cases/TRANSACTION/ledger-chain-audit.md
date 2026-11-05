# 변경 이력의 수량 연속성 대조

```json
{
  "id": "ledger-chain-audit",
  "title": "변경 이력의 수량 연속성 대조",
  "family": "TRANSACTION",
  "keywords_ko": [
    "변경",
    "이력의",
    "수량",
    "연속성",
    "대조"
  ],
  "keywords_en": [
    "ledger-reconciliation",
    "ledger-chain-audit"
  ],
  "problem_structure": "ledger-reconciliation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 대여 소품 장부에서 각 변경 전후 수량이 연결되는지 확인하여 누락된 이동 기록을 찾아 달라.",
  "do_not_use_when": "순번 구멍을 자동 추정 사건으로 채우지 않는다. 감사 로그만으로 실물 재고를 검증했다고 주장하지 않는다.",
  "data_required": [
    "최소: opening 정수개, entries=[seq,delta,after] 한 행 확정변경, seq 양의고유정수1부터; null은 unknown. 개선: event_id·근거·권한. fixture는 한 item의 완전한 구간만 검사."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "transaction-reservation"
  ],
  "depth": "standard",
  "path": "cases/TRANSACTION/ledger-chain-audit.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "ledger-reconciliation",
    "input_structure": "최소: opening 정수개, entries=[seq,delta,after] 한 행 확정변경, seq 양의고유정수1부터; null은 unknown. 개선: event_id·근거·권한. fixture는 한 item의 완전한 구간만 검사.",
    "hard_constraint": "순번 구멍을 자동 추정 사건으로 채우지 않는다. 감사 로그만으로 실물 재고를 검증했다고 주장하지 않는다.",
    "validation": "5+3=8,8-2=6; 정확히0 허용; 변경량 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 대여 소품 장부에서 각 변경 전후 수량이 연결되는지 확인하여 누락된 이동 기록을 찾아 달라.

가능한 설명: 중간 사건이 빠졌다; 같은 순번이 중복됐다; 변경량과결과수량이 일치하지 않는다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 순번은 거래별입니까 물품별입니까? → 본 예제 물품하나 연속1부터.
2. 음수재고 허용됩니까? → 본 예제 금지.
3. 정정은 덮어쓰기입니까 반대거래입니까? → 원장 보존정책 확인.

## 3. 데이터 계약과 자료 부족 대안

최소: opening 정수개, entries=[seq,delta,after] 한 행 확정변경, seq 양의고유정수1부터; null은 unknown. 개선: event_id·근거·권한. fixture는 한 item의 완전한 구간만 검사. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: seq 정렬 후 1..n 연속인지 확인하고 opening에 delta를 더한 값이 매 after와 같고 비음수인지 검사. 최종수량 반환.

개선: 여러 물품은 item별 그룹, 해시연결·승인기록 추가. 단순 연속성이 변조없음 증명은 아니다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

기초잔량·원장 → 순번/계산 대조 → 최종잔량 또는 conflict/unknown과 위치 → 운영자가 원본 조사. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"opening":5,"entries":[[1,3,8],[2,-2,6]]}`|`6`|5+3=8,8-2=6|
|boundary|`{"opening":5,"entries":[[1,-5,0]]}`|`0`|정확히0 허용|
|missing|`{"opening":5,"entries":[[1,null,5]]}`|`"unknown"`|변경량 미확인|

## 7. 흔한 오류와 범위 축소

순번 구멍을 자동 추정 사건으로 채우지 않는다. 감사 로그만으로 실물 재고를 검증했다고 주장하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 첫 불일치 위치가 원본 조사에 도움이 됩니까?
- 실물 대조가 필요한 항목을 별도로 표시해야 합니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 원장 합계와 각 단계 연속성 검사의 차이는 무엇입니까?
- 수학적으로 일관된 가짜 장부를 이 검사로 발견할 수 있습니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
