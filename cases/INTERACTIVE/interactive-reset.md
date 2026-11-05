# 동시 종료와 재시작의 세션 격리

> 독립 창작 합성 사례. 실제 조직·과제·인물을 재현하지 않는다. 공개 알고리즘 자료는 방법의 참고이며 아래 업무 정책·수치는 이 연습에서 새로 정했다.

```json
{
  "id": "interactive-reset",
  "title": "동시 종료와 재시작의 세션 격리",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "종료",
    "재시작",
    "승패",
    "세션"
  ],
  "keywords_en": [
    "state",
    "machine",
    "event",
    "replay"
  ],
  "problem_structure": "state machine event replay",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "동일 tick 사건을 순차 판정해 순서 의존 결과가 생긴다.",
  "do_not_use_when": "분산 네트워크의 합의 문제를 이 로컬 batch 규칙으로 해결했다고 하지 않는다.",
  "data_required": "경기 상태 session 정수, phase ready/running/ended, hp A/B 정수. damage 사건은 session,tick,player,amount,id. 같은 tick 전체 피해 적용 후 승패 판정. 재시작은 새 session.",
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": ["interactive-collision"],
  "depth": "deep",
  "path": "cases/INTERACTIVE/interactive-reset.md"
}
```

## 요청과 다른 해석

“로컬 대전 연습에서 둘이 동시에 탈락하면 마지막 이벤트만 이기고, 재시작 뒤 이전 타이머가 남는다.”

- 동일 tick 사건을 순차 판정해 순서 의존 결과가 생긴다.
- 세션 id 없이 이전 이벤트를 받아 새 상태를 오염한다.
- 초기 상태를 얕게 복사해 처리 기록이 공유된다.

## 우선 질문과 방향 변화

1. 동시 탈락 규칙은 무엇인가? → 무승부/우선순위 중 정책을 확정한다.
2. 같은 tick 정의는 무엇인가? → 프레임 시각 대신 정수 tick과 묶음 처리 경계를 합의한다.
3. 재시작 시 무엇을 초기화하는가? → 체력·점수·이벤트·타이머를 목록으로 확정한다.

파일에서 이미 확인되는 답은 다시 묻지 않는다. 정책을 결정할 권한자와 기준 시점을 함께 기록한다.

## 데이터 계약과 합성 입력

경기 상태 session 정수, phase ready/running/ended, hp A/B 정수. damage 사건은 session,tick,player,amount,id. 같은 tick 전체 피해 적용 후 승패 판정. 재시작은 새 session.

최소 필수는 아래 판정 필드와 키다. 대표 샘플·스키마로 시작하며 개인 식별 정보는 필요하지 않다. 개선용 데이터는 실제 작업 시간과 오류 기록이다. 전체 이력이나 외부 API는 첫 검증에 없어도 된다. null은 미확인이며 0·false와 다르다. 필수 필드가 없으면 해당 판정을 보류하고 담당자 확인 목록에 남긴다.

```json
{
  "state": {
    "session": 4,
    "phase": "running",
    "hp": {
      "A": 2,
      "B": 2
    }
  },
  "events": [
    {
      "session": 4,
      "tick": 8,
      "player": "A",
      "amount": 2,
      "id": "a"
    },
    {
      "session": 4,
      "tick": 8,
      "player": "B",
      "amount": 2,
      "id": "b"
    }
  ],
  "restart": {
    "session": 5,
    "phase": "ready",
    "hp": {
      "A": 2,
      "B": 2
    }
  }
}
```

## 기준 방법, 제약과 최소 경로

동일 tick 이벤트를 중복 제거 후 모아 피해 합계 적용, 생존 수로 결과를 한 번 판정한다. 종료 상태는 새 게임 명령 외 사건을 무시한다.

필수: 피해 음수 금지, hp 하한0, 이전 session 이벤트 무시. 두 생존이면 running, 한 명이면 해당 승자, 0명이면 draw. 목적함수 없음.

사건 batch → hp 둘 다0 → draw → 재시작 → session5 ready hp2/2 → 사용자가 새 시작을 누른다.

## 기대 결과와 반례

| 유형 | 입력 또는 변경 | 기대 결과 |
|---|---|---|
| 정상 | 같은 tick A/B 각각2 피해 | draw,ended |
| 경계 | A만 정확히2 피해 | B 승리 |
| 정보 부족 | tick 누락 | batch 거절, 결과 보류 |
| 충돌 | 피해 amount=-1 | 입력 오류, 회복으로 해석 금지 |
| 순서변경 | 동일 tick 사건 역순 | draw 유지 |
| 새 샘플 | 재시작 후 session4 피해 도착 | session5 hp2/2 유지 |

손계산 근거: 각 체력 max(0,2-2)=0. 생존 수0이므로 draw. 순차로 첫 사망 즉시 끝내면 B 승리로 잘못 판정한다.

비슷하지만 다른 두 건: 같은 tick 두 피해는 무승부, 다음 tick 피해는 첫 tick 종료 후 무시되어 먼저 살아남은 쪽 승리다.

작은 계산 예제는 [check_c.py](../../examples/synthetic/check_c.py)에서 별도 표준 라이브러리 계산으로 확인한다. 각 수용 테스트 행의 기대값은 소형 오라클 계산으로 확인한다. 전체 앱·화면·DB 동시성은 구현하거나 검증하지 않았으며, 기대값 검증과 구현물 테스트 통과는 다르다. 실행 범위는 해당 스크립트 출력과 검증 보고서를 따른다.

## 답변이 바뀌면 수정할 계획

- 동시 탈락 우선권 규칙이면 명시적 tie-break를 추가하고 draw 기대값을 교체한다.
- 네트워크 경기가 필요하면 tick 완결 판정·지연·서버 권위를 별도 설계한다.

## 피할 구현과 축소 기준

- 분산 네트워크의 합의 문제를 이 로컬 batch 규칙으로 해결했다고 하지 않는다.
- 종료 이벤트 순서로 승자를 정하거나 session을 그대로 재사용하지 않는다.
- 시간 부족이면 점수판 장식 대신 종료·초기화·오래된 이벤트 차단을 검증한다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 이 작은 합성 입력에는 패키지 설치·외부 호출이 필요 없다. Python도 실행할 수 없으면 표에 후보를 전부 적고 손계산한다. 대규모 개선 도구는 설치·규정·입력 적합성이 확인된 이후 별도 선택한다.

## 연습 시간 예산과 효과 측정

30분: 동시 피해 표. 90분: 시작/종료/재시작 상태 흐름. 180분: replay와 오래된 tick 차단. 권장 연습 예산이다.

동일 batch 순서별 결과 불일치 수와 재시작 후 잔류 상태 수를 측정한다. 이 합성 예제만으로 실제 조직의 시간 절감·만족도·수익 향상을 주장할 수 없다.

## 구현물에 대한 담당자 피드백

1. 결과 한 건의 근거와 보류 사유를 보고 다음 행동을 선택할 수 있는가? 실제로 선택하는 모습을 관찰한다.
2. 동시 탈락 규칙은 무엇인가?에 대한 합의와 화면 결과가 어긋나는 사례가 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

1. 이 기준 방법을 선택한 이유를 입력 크기·정책·반례 파일을 근거로 설명할 수 있는가?
2. 동시 종료와 재시작의 세션 격리에서 계산 검증이 보장하지 못하는 부분은 무엇이며 어떤 추가 관찰이 필요한가?

## 공개 근거

- [공식 기술 문서](https://docs.python.org/3/library/collections.html) — 일반 계산 구조를 참고했다. 창작 업무 조건의 외부 검증이나 적용 허가를 뜻하지 않는다.
- [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)
