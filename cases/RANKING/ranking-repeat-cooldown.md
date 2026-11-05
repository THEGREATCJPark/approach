# 최근 선택의 반복 억제 기간

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "ranking-repeat-cooldown",
  "title": "최근 선택의 반복 억제 기간",
  "family": "RANKING",
  "keywords_ko": [
    "반복",
    "최근",
    "냉각기간",
    "재추천"
  ],
  "keywords_en": [
    "cooldown-ranking",
    "ranking-repeat-cooldown"
  ],
  "problem_structure": "cooldown-ranking",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "최근 선택 이후 일정 기간 제외하는 정책이 필요하다.",
  "do_not_use_when": "재고 고갈이나 필수 순번 배정 문제를 반복 억제만으로 해결하지 않는다.",
  "data_required": [
    "후보 한 행: id 키, score 정수, last_day 정수 일 또는 never 문자열. today 정수 일, cooldown 비음수 일. 모든 day는 같은 기준일 이후 일수이며 null은 기록 미확인. 출력은 eligible 추천 ID와 unknown 확인 필요 ID를 분리한다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "ranking-cold-start",
    "ranking-attribute-distance"
  ],
  "depth": "standard",
  "path": "cases/RANKING/ranking-repeat-cooldown.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "최근 선택 뒤 재추천 가능한 후보를 고른다",
    "input_structure": "마지막 선택 일수와 cooldown 기간",
    "hard_constraint": "경과일 상한 경계 및 never/null 분리",
    "validation": "정확히7일 포함과 미확인 이력 보류"
  }
}
```

## 1. 창작 업무 요청

“자료실의 추천 전시가 며칠째 같아 일정 기간 다시 제안하지 않았으면 한다.”

## 2. 다른 원인과 목표

- 최근 선택 이후 일정 기간 제외하는 정책이 필요하다.
- 추천 노출과 실제 선택을 혼동했을 수 있다.
- 후보가 적으면 엄격한 제외가 빈 목록을 만든다.

## 3. 먼저 확인할 질문과 분기

1. 기간은 마지막 노출부터인가 선택부터인가? → 기록 종류를 먼저 고정한다.
2. 정확히7일 지난 항목은 허용하는가? → 이 연습은 경과일≥7로 허용한다.
3. 후보가 모자라면 제외를 풀어도 되는가? → 합의 없으면 미충족을 표시한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

후보 한 행: id 키, score 정수, last_day 정수 일 또는 never 문자열. today 정수 일, cooldown 비음수 일. 모든 day는 같은 기준일 이후 일수이며 null은 기록 미확인.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "today": 20,
  "cooldown": 7,
  "items": [
    [
      "A",
      9,
      15
    ],
    [
      "B",
      8,
      10
    ],
    [
      "C",
      7,
      "never"
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

last_day가 never이거나 today-last_day≥cooldown이면 후보로 남기고 score 내림차순 정렬한다. null은 결과의 unknown 확인 목록에 넣고 eligible 추천 목록과 분리한다. 실제 일시를 쓰면 시간대와 일 경계 정책을 추가한다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

선택 이력 → 재추천 가능일·제외 목록 → 오늘 후보 → 담당자가 일정에 반영한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"today":20,"cooldown":7,"items":[["A",9,15],["B",8,10],["C",7,"never"]]}` | `{"eligible": ["B", "C"], "unknown": []}` | A5일 제외,B10일 허용,C 미선택 허용. |
| boundary | `{"today":20,"cooldown":7,"items":[["A",9,13]]}` | `{"eligible": ["A"], "unknown": []}` | 정확히7일은 포함. |
| missing | `{"today":20,"cooldown":7,"items":[["A",9,null]]}` | `{"eligible": [], "unknown": ["A"]}` | 이력 미확인 A는 확정 추천에서 보류. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 재고 고갈이나 필수 순번 배정 문제를 반복 억제만으로 해결하지 않는다.
- 이력 없음(never)과 조회 실패(null)를 합치지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 제외된 후보가 언제 다시 나타나는지 알 수 있는가?
2. 빈 목록일 때 정책을 바꿔야 하는 담당자가 누구인지 드러나는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 기간 경계 테스트가 어떤 off-by-one 오류를 막는가?
2. never와null을 분리한 데이터 계약의 근거는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/howto/sorting.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
