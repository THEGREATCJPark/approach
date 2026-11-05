# 마감 유예와 완주 동률의 최종 승자

```json
{
  "id": "simultaneous-outcome",
  "title": "마감 유예와 완주 동률의 최종 승자",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "마감",
    "유예와",
    "완주",
    "동률의",
    "최종",
    "승자"
  ],
  "keywords_en": [
    "deadline-finish-ranking",
    "simultaneous-outcome"
  ],
  "problem_structure": "deadline-finish-ranking",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 다인 달리기 보드게임에서 마감 직후 유예구간에 들어온 완주 기록까지 모아 최종 승자와 동률을 확정해 달라.",
  "do_not_use_when": "수신 순서를 완주 순서로 간주하지 않는다. 유예정책을 임의로 바꾸지 않는다. 시간 부족 시 실시간 수집을 제외하고 확정배치 파일만 처리한다. 경계·동률·배치완료 검사는 유지한다.",
  "data_required": [
    "최소: arrivals=[participant_id,finish_s] 한 행 한 참가자의 확정완주시각, ID 고유, 시간은 같은 라운드시작부터 초. deadline_s>=0, grace_s>=0, batch_complete bool. null finish는 unknown, []는 완주기록없음 확인. 개선: watermark·서버 시각. 배치 미완료는 pending이며 먼저 온 기록만으로 우승 확정하지 않는다."
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
  "path": "cases/INTERACTIVE/simultaneous-outcome.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "deadline-finish-ranking",
    "input_structure": "최소: arrivals=[participant_id,finish_s] 한 행 한 참가자의 확정완주시각, ID 고유, 시간은 같은 라운드시작부터 초. deadline_s>=0, grace_s>=0, batch_complete bool. null finish는 unknown, []는 완주기록없음 확인. 개선: watermark·서버 시각. 배치 미완료는 pending이며 먼저 온 기록만으로 우승 확정하지 않는다.",
    "hard_constraint": "수신 순서를 완주 순서로 간주하지 않는다. 유예정책을 임의로 바꾸지 않는다. 시간 부족 시 실시간 수집을 제외하고 확정배치 파일만 처리한다. 경계·동률·배치완료 검사는 유지한다.",
    "validation": "유예상한11 이내 둘 중10.5가 빠름; 11 경계 포함, 두 명 동률,11.1 제외; 전체 도착배치 미완료로 승자보류"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 다인 달리기 보드게임에서 마감 직후 유예구간에 들어온 완주 기록까지 모아 최종 승자와 동률을 확정해 달라.

숨은 원인: 마감과 전송유예가 혼동된다; 동률 규칙이 없다; 늦게 도착한 더 빠른 완주 기록이 빠졌다. 업무·수치·정책은 독립 창작이다.

## 2. 방향을 가르는 담당자 질문

1. 유예가 실제 완주시간에도 적용됩니까? → 전송지연만 허용이면 event_time과receive_time을 분리.
2. 같은 완주시간은 공동승자입니까? → 본 예제 공동승자, 다른 규칙이면 tiebreaker 필요.
3. 모든 기록이 도착했음을 어떻게 압니까? → 완료신호 없으면 pending.

## 3. 데이터 계약과 자료 부족 대안

최소: arrivals=[participant_id,finish_s] 한 행 한 참가자의 확정완주시각, ID 고유, 시간은 같은 라운드시작부터 초. deadline_s>=0, grace_s>=0, batch_complete bool. null finish는 unknown, []는 완주기록없음 확인. 개선: watermark·서버 시각. 배치 미완료는 pending이며 먼저 온 기록만으로 우승 확정하지 않는다. 자료를 받을 수 없으면 합성 라운드만 확인하고 실시간 공정성 주장은 보류한다.

## 4. 기준 방법과 개선 조건

기준: 배치가 완료된 후 finish<=deadline+grace 기록만 남긴다. 최소 finish와 같은 참가자 ID를 정렬하여 공동승자 목록을 반환한다. 적격 기록이 없으면 빈 목록. 개선: 실제 네트워크에서는 event-time watermark와 시계 오차 상한이 필요. Python 표준 라이브러리로 충분하며 실행 불가 시 표를 손정렬한다.

## 5. 최소 구현과 다음 행동

완주기록·마감·유예 → 적격필터와 최소시각 그룹 → 공동승자/없음/pending → 진행자가 최종결과 공지. 체력·피해를 판정하는 사례와 다른 종료 규칙이다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)의 이 ID와 [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)를 함께 읽는다.

|종류|입력|기대|근거|
|---|---|---|---|
|normal|`{"arrivals": [["a", 10.5], ["b", 10.8]], "deadline_s": 10, "grace_s": 1, "batch_complete": true}`|`["a"]`|유예상한11 이내 둘 중10.5가 빠름|
|boundary|`{"arrivals": [["a", 11], ["b", 11], ["c", 11.1]], "deadline_s": 10, "grace_s": 1, "batch_complete": true}`|`["a", "b"]`|11 경계 포함, 두 명 동률,11.1 제외|
|missing|`{"arrivals": [["a", 9]], "deadline_s": 10, "grace_s": 1, "batch_complete": false}`|`"pending"`|전체 도착배치 미완료로 승자보류|

## 7. 흔한 오류와 범위 축소

수신 순서를 완주 순서로 간주하지 않는다. 유예정책을 임의로 바꾸지 않는다. 시간 부족 시 실시간 수집을 제외하고 확정배치 파일만 처리한다. 경계·동률·배치완료 검사는 유지한다.

## 8. 구현물 사용자 피드백

- 유예구간 참가자를 포함하는 것이 운영 규칙과 맞습니까?
- 공동승자와 pending 표시로 잘못된 조기 공지를 막을 수 있습니까?

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 다음은 PREP 전용이다.

- 같은 완주기록에서 유예시간을 바꾸면 승자가 달라지는 이유는 무엇입니까?
- 배치 완료와 실제 네트워크의 모든 사건 도착은 어떻게 다릅니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
