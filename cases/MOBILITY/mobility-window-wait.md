# 대기 허용 경로의 서비스 시작 시간

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "mobility-window-wait",
  "title": "대기 허용 경로의 서비스 시작 시간",
  "family": "MOBILITY",
  "keywords_ko": [
    "시간창",
    "대기",
    "도착",
    "서비스"
  ],
  "keywords_en": [
    "time-window-simulation",
    "mobility-window-wait"
  ],
  "problem_structure": "time-window-simulation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "도착시각과 서비스 시작시각을 구별해야 한다.",
  "do_not_use_when": "서비스 완료 마감인 업무에 시작 마감 규칙을 적용하지 않는다.",
  "data_required": [
    "start 정수 분, stops 각 [id,travel,open,close,service] 분. travel은 직전 서비스 종료 후 이동 분. close 포함. 한 행은 순서가 고정된 방문1회."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "mobility-indivisible-capacity",
    "mobility-depot-minimax"
  ],
  "depth": "standard",
  "path": "cases/MOBILITY/mobility-window-wait.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "고정 경로를 기다리며 방문하면 마감을 지킬 수 있는지 정한다",
    "input_structure": "순서별 이동·시간창·서비스 분",
    "hard_constraint": "대기 허용; 서비스 시작 마감",
    "validation": "도착·대기·시작·완료의 누적 계산"
  }
}
```

## 1. 창작 업무 요청

“정해진 방문 순서에서 일찍 도착해 기다리면 모든 점검을 마칠 수 있는지 확인하고 싶다.”

## 2. 다른 원인과 목표

- 도착시각과 서비스 시작시각을 구별해야 한다.
- 마감이 시작 기준인지 완료 기준인지 다를 수 있다.
- 교통시간이 미확정이면 가능 판정도 미확정이다.

## 3. 먼저 확인할 질문과 분기

1. 마감은 서비스 시작 기준인가? → 이 연습은 시작 기준이며 완료 기준이면 서비스를 포함해 비교한다.
2. 현장 대기가 허용되는가? → 불가면 조기 도착도 위반이다.
3. 이동시간은 앞 방문 서비스 종료부터인가? → 누적 도착시간과 구분한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

start 정수 분, stops 각 [id,travel,open,close,service] 분. travel은 직전 서비스 종료 후 이동 분. close 포함. 한 행은 순서가 고정된 방문1회.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "start": 0,
  "stops": [
    [
      "A",
      5,
      10,
      15,
      3
    ],
    [
      "B",
      4,
      15,
      20,
      2
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

시각에 이동을 더해 도착, max(도착,open)에서 시작, close 초과면 위반, service를 더해 다음 방문으로 진행한다. 기다림을 이동시간에 숨기지 않는다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

경로표 → 도착/대기/시작/완료 표 → 운영자가 약속시간 조정 여부를 결정한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"start":0,"stops":[["A",5,10,15,3],["B",4,15,20,2]]}` | `{"feasible": true, "finish": 19, "wait": 5}` | A도착5 대기5 시작10 종료13;B도착17 종료19. |
| boundary | `{"start":0,"stops":[["A",10,0,10,2]]}` | `{"feasible": true, "finish": 12, "wait": 0}` | 시작10=마감10 허용,완료12는 별개. |
| missing | `{"start":0,"stops":[["A",null,0,10,2]]}` | `"unknown"` | 이동시간 미확인. |
| missing_start | `{"start":null,"stops":[["A",10,0,10,2]]}` | `"unknown"` | 출발 기준시각이 없어 도착시간 계산을 보류한다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 서비스 완료 마감인 업무에 시작 마감 규칙을 적용하지 않는다.
- 경로 순서 최적화로 설명하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 대기와 실제 작업 시간이 구분되어 일정 변경을 결정할 수 있는가?
2. 마감에 정확히 도착하는 사례를 허용하는 것이 업무 규칙과 맞는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 도착·시작·완료 세 시각을 나눈 이유는 무엇인가?
2. 이동시간 변동성을 어떻게 추가 검증할 것인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/itertools.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
