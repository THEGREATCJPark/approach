# 원획득에 연결된 득점 취소와 이중 취소

```json
{
  "id": "score-event-replay",
  "title": "원획득에 연결된 득점 취소와 이중 취소",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "원획득에",
    "연결된",
    "득점",
    "취소와",
    "이중",
    "취소"
  ],
  "keywords_en": [
    "score-reversal-ledger",
    "score-event-replay"
  ],
  "problem_structure": "score-reversal-ledger",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 퍼즐의 득점 장부에서 잘못 지급한 점수를 원래 획득 사건에 연결해 취소하되 동일 획득을 두 번 취소하지 않게 해 달라.",
  "do_not_use_when": "취소 delta가 음수라는 이유만으로 유효하다고 보지 않는다. 원본을 덮어쓰거나 취소를 지우지 않는다. 시간 부족 시 부분취소·취소의 취소를 범위에서 빼고 전액1회 검사 유지.",
  "data_required": [
    "최소: events=[event_id,delta,reverses] 한 행 확정 득점/취소 사건. delta 정수점수, 일반 획득은 reverses 빈문자열, 취소는 앞선 원획득 event_id. event_id 고유, null은 unknown. 원획득은 양의점수, 취소량은 정확한 음수. 개선: 정정버전·권한. 순서가 감사 순서이며 원획득 미도착 취소는 unknown."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "interactive-reset"
  ],
  "depth": "standard",
  "path": "cases/INTERACTIVE/score-event-replay.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "score-reversal-ledger",
    "input_structure": "최소: events=[event_id,delta,reverses] 한 행 확정 득점/취소 사건. delta 정수점수, 일반 획득은 reverses 빈문자열, 취소는 앞선 원획득 event_id. event_id 고유, null은 unknown. 원획득은 양의점수, 취소량은 정확한 음수. 개선: 정정버전·권한. 순서가 감사 순서이며 원획득 미도착 취소는 unknown.",
    "hard_constraint": "취소 delta가 음수라는 이유만으로 유효하다고 보지 않는다. 원본을 덮어쓰거나 취소를 지우지 않는다. 시간 부족 시 부분취소·취소의 취소를 범위에서 빼고 전액1회 검사 유지.",
    "validation": "3+5-3=5, e1 한 번 취소; 같은 원획득 e1 두번취소 금지; 원획득 e1 자료없음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 퍼즐의 득점 장부에서 잘못 지급한 점수를 원래 획득 사건에 연결해 취소하되 동일 획득을 두 번 취소하지 않게 해 달라.

숨은 원인: 취소를 독립 음수점수로만 기록한다; 원획득이 빠졌다; 재취소가 허용돼 점수가 음수가 된다. 모두 독립 창작 조건이다.

## 2. 방향을 가르는 담당자 질문

1. 부분취소도 허용합니까? → 이번 예제 전액1회, 부분이면 잔여취소량 원장 필요.
2. 취소의 취소를 허용합니까? → 본 예제 금지, 필요하면 새 상태모델.
3. 원획득 없이 취소가 오면 어떻게 합니까? → unknown 큐에 보류하고 재조회.

## 3. 데이터 계약과 자료 부족 대안

최소: events=[event_id,delta,reverses] 한 행 확정 득점/취소 사건. delta 정수점수, 일반 획득은 reverses 빈문자열, 취소는 앞선 원획득 event_id. event_id 고유, null은 unknown. 원획득은 양의점수, 취소량은 정확한 음수. 개선: 정정버전·권한. 순서가 감사 순서이며 원획득 미도착 취소는 unknown. 원본 자료가 없으면 음수만 합산해 확정 잔액을 만들지 않는다.

## 4. 기준 방법과 개선 조건

기준: 순서대로 원획득을 저장하고 취소가 그 원획득을 가리키며 금액이 정확히 반대이고 아직 취소되지 않았는지 검사한다. 통과 사건만 총합, 상충은 conflict, 원획득 부재는 unknown. 개선: 지속 원장과 원자적 취소 unique 제약. Python dict/set 기준법으로 충분, 실행 불가면 장부 손대조.

## 5. 최소 구현과 다음 행동

득점·취소 사건 → 원사건 연결 검증 → 잔액 또는 충돌/보류와 참조ID → 운영자가 잘못된 취소 조사. 단순 이벤트 중복합계와 달리 사건 사이 관계가 필요하다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)의 이 ID와 [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)를 함께 읽는다.

|종류|입력|기대|근거|
|---|---|---|---|
|normal|`{"events": [["e1", 3, ""], ["e2", 5, ""], ["r1", -3, "e1"]]}`|`5`|3+5-3=5, e1 한 번 취소|
|boundary|`{"events": [["e1", 3, ""], ["r1", -3, "e1"], ["r2", -3, "e1"]]}`|`"conflict"`|같은 원획득 e1 두번취소 금지|
|missing|`{"events": [["r1", -3, "e1"]]}`|`"unknown"`|원획득 e1 자료없음|

## 7. 흔한 오류와 범위 축소

취소 delta가 음수라는 이유만으로 유효하다고 보지 않는다. 원본을 덮어쓰거나 취소를 지우지 않는다. 시간 부족 시 부분취소·취소의 취소를 범위에서 빼고 전액1회 검사 유지.

## 8. 구현물 사용자 피드백

- 충돌 원획득 ID로 이중 취소를 조사할 수 있습니까?
- 원획득 미확인 상태에서 점수 확정을 보류하는 흐름이 맞습니까?

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. PREP 전용 질문이다.

- 음수점수 단순합산이 이중취소를 발견하지 못하는 이유는 무엇입니까?
- 부분취소 요구가 생기면 어떤 불변식을 새로 검증해야 합니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
