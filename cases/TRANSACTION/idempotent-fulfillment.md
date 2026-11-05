# 이행 요청 재처리와 payload 충돌

```json
{
  "id": "idempotent-fulfillment",
  "title": "이행 요청 재처리와 payload 충돌",
  "family": "TRANSACTION",
  "keywords_ko": [
    "이행",
    "요청",
    "재처리와",
    "payload",
    "충돌"
  ],
  "keywords_en": [
    "persisted-retry-state",
    "idempotent-fulfillment"
  ],
  "problem_structure": "persisted-retry-state",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 물품 배분 서비스에서 동일 작업 키로 다시 들어온 요청은 기존 처리 결과를 반환하고, 수량이 바뀐 재요청은 충돌로 표시해 달라.",
  "do_not_use_when": "실패응답을 부수효과 없음으로 간주해 재실행하지 않는다. 클라이언트 버튼 잠금만으로 멱등을 보장하지 않는다. 분류테스트를 동시성·정확히한번실행 보장으로 확대하지 않는다. 시간 부족 시 자동재실행을 제외하고 수동검토 안내 유지.",
  "data_required": [
    "최소: key 문자열, quantity 양의 정수, history={key:[quantity,status,effect]}, status done/pending/failed, effect applied/absent/unknown. 한 행 이행요청. null history는 조회실패 unknown, {}는 기록없음 확인. failed의 effect absent는 별도 실행기 대조로 확인된 값이며 응답실패만으로 추정하지 않는다. 개선: atomic DB unique·payload hash·실행기 조정."
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
  "path": "cases/TRANSACTION/idempotent-fulfillment.md",
  "test_count": 5,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "persisted-retry-state",
    "input_structure": "최소: key 문자열, quantity 양의 정수, history={key:[quantity,status,effect]}, status done/pending/failed, effect applied/absent/unknown. 한 행 이행요청. null history는 조회실패 unknown, {}는 기록없음 확인. failed의 effect absent는 별도 실행기 대조로 확인된 값이며 응답실패만으로 추정하지 않는다. 개선: atomic DB unique·payload hash·실행기 조정.",
    "hard_constraint": "실패응답을 부수효과 없음으로 간주해 재실행하지 않는다. 클라이언트 버튼 잠금만으로 멱등을 보장하지 않는다. 분류테스트를 동시성·정확히한번실행 보장으로 확대하지 않는다. 시간 부족 시 자동재실행을 제외하고 수동검토 안내 유지.",
    "validation": "같은 작업 완료기록; 같은키 수량변경; 기록조회 실패; 실패했고 부수효과없음이확인된 경우만재시도; 실패응답이 실제이행없음을 증명하지않음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 물품 배분 서비스에서 동일 작업 키로 다시 들어온 요청은 기존 처리 결과를 반환하고, 수량이 바뀐 재요청은 충돌로 표시해 달라.

가능한 설명: 네트워크 재시도를 두 번 실행한다; 키 재사용이 수정 요청을 가린다; 완료와 접수 결과를 혼동한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 키는 누가 생성하고 유효기간은 얼마입니까? → 범위별 unique 설계.
2. 같은 키 다른수량은 정정입니까? → 이번 예제 conflict, 정정이면 새 버전.
3. 기존 기록이 완료입니까? → pending이면 완료 결과 반환 금지.

## 3. 데이터 계약과 자료 부족 대안

최소: key 문자열, quantity 양의 정수, history={key:[quantity,status,effect]}, status done/pending/failed, effect applied/absent/unknown. 한 행 이행요청. null history는 조회실패 unknown, {}는 기록없음 확인. failed의 effect absent는 별도 실행기 대조로 확인된 값이며 응답실패만으로 추정하지 않는다. 개선: atomic DB unique·payload hash·실행기 조정.

## 4. 기준 방법과 개선 조건

기준: 미등록키=new, 같은키 다른수량=conflict. 같은수량 done은 replay_done, pending은 in_progress. failed라도 effect absent가 확인된 경우만 retry_allowed; applied/unknown이면 manual_review. 개선: 실행기 조회와 원장 대조·원자적 전이. 본 예제는 분류만 검사하며 실제 지급/인도를 하지 않는다. 설치 불가면 작은 상태표 손검사.

## 5. 최소 구현과 다음 행동

요청·기존이력 → 비교 → new/replay_done/in_progress/conflict/unknown → 승인된 실행기 또는 운영자에게 넘김. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)의 이 ID와 [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)를 함께 읽는다.

|종류|입력|기대|근거|
|---|---|---|---|
|normal|`{"key": "k1", "quantity": 3, "history": {"k1": [3, "done", "applied"]}}`|`"replay_done"`|같은 작업 완료기록|
|boundary|`{"key": "k1", "quantity": 4, "history": {"k1": [3, "done", "applied"]}}`|`"conflict"`|같은키 수량변경|
|missing|`{"key": "k1", "quantity": 3, "history": null}`|`"unknown"`|기록조회 실패|
|failed_safe_retry|`{"key": "k1", "quantity": 3, "history": {"k1": [3, "failed", "absent"]}}`|`"retry_allowed"`|실패했고 부수효과없음이확인된 경우만재시도|
|failed_uncertain|`{"key": "k1", "quantity": 3, "history": {"k1": [3, "failed", "unknown"]}}`|`"manual_review"`|실패응답이 실제이행없음을 증명하지않음|

## 7. 흔한 오류와 범위 축소

실패응답을 부수효과 없음으로 간주해 재실행하지 않는다. 클라이언트 버튼 잠금만으로 멱등을 보장하지 않는다. 분류테스트를 동시성·정확히한번실행 보장으로 확대하지 않는다. 시간 부족 시 자동재실행을 제외하고 수동검토 안내 유지.

## 8. 구현물 사용자 피드백

- 재시도 응답에서 기존 결과임을 알 수 있습니까?
- 수량 변경 충돌을 해결하는 별도 절차가 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 같은 키 다른 payload의 기대 결과 근거는 무엇입니까?
- 동시 신규 요청 두 개를 이 예제가 보장하지 않는 이유는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
