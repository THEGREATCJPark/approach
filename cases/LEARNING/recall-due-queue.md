# 회상 퀴즈의 예정일과 하루 한도

```json
{
  "id": "recall-due-queue",
  "title": "회상 퀴즈의 예정일과 하루 한도",
  "family": "LEARNING",
  "keywords_ko": [
    "회상 퀴즈의 예정일과 하루 한도",
    "오늘 복습할 질문을 예산 내에서 선택"
  ],
  "keywords_en": [
    "recall-due-queue",
    "question × due_day × enabled"
  ],
  "problem_structure": "question × due_day × enabled",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 박물관 안내 교육에서 설명을 반복해서 읽기만 하므로 하루 두 개씩 스스로 답하는 회상 질문을 꺼내 주려 한다.",
  "do_not_use_when": "이 예정일 선택을 학습 효과가 입증된 적응형 모델이라고 부르지 않는다. 시간 부족이면 한도·예정일·힌트 분리만 구현.",
  "data_required": [
    "필수 question_id 문자열, due_day 정수(같은 기준일 이후 일수), enabled 불리언, today 정수, limit 비음수정수. 한 행 질문 하나, id 고유. null due_day는 미확정이며 unknown. 시간대는 실제 날짜로 확장할 때 필요."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [],
  "depth": "standard",
  "path": "cases/LEARNING/recall-due-queue.md",
  "decision_signature": {
    "decision": "오늘 복습할 질문을 예산 내에서 선택",
    "input_structure": "question × due_day × enabled",
    "hard_constraint": "오늘 이전 예정·활성 질문만 선택",
    "validation": "미래 질문 제외와 동률 순서 재현"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 박물관 안내 교육에서 설명을 반복해서 읽기만 하므로 하루 두 개씩 스스로 답하는 회상 질문을 꺼내 주려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 복습 예정일이 없어 최근 본 내용만 반복된다.
- 정답을 먼저 보여 회상 과제가 읽기로 바뀐다.
- 오래된 비활성 질문이 계속 섞인다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 오늘 제한은 질문 개수인가 예상 시간인가? | 개수면 take k, 시간이면 소요시간과 예산 선택 필요. |
| 힌트를 언제 보여주는가? | 답변 뒤만 허용이면 질문·힌트 표시 상태 분리. |
| 예정일 변경 규칙은 무엇인가? | 본 예제는 입력된 예정일 선택만; 학습 성과 기반 간격은 별도 정책. |

## 4. 데이터와 없을 때의 대안
필수 question_id 문자열, due_day 정수(같은 기준일 이후 일수), enabled 불리언, today 정수, limit 비음수정수. 한 행 질문 하나, id 고유. null due_day는 미확정이며 unknown. 시간대는 실제 날짜로 확장할 때 필요.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "today": 10,
  "limit": 2,
  "questions": [
    {
      "id": "q1",
      "due": 9,
      "enabled": true
    },
    {
      "id": "q2",
      "due": 10,
      "enabled": true
    },
    {
      "id": "q3",
      "due": 11,
      "enabled": true
    },
    {
      "id": "q4",
      "due": 8,
      "enabled": false
    }
  ]
}
```

## 5. 기준 방법과 개선 조건
활성·due≤today 필터 후 due,id 순 정렬하고 한도만큼 선택한다. 질문 화면 다음에 자가 답변, 그 뒤 근거 확인.

실제 회상 성공과 지연 시간 자료가 쌓이면 복습 간격 정책을 비교 실험한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 오늘 복습할 질문을 예산 내에서 선택 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `["q1", "q2"]` | 활성이고 due≤10인 두 질문. |
| 경계 | `{"limit": 0}` | `[]` | 하루 한도0이면 선택 없음. |
| 정보 부족 | `{"questions": null}` | `"unknown"` | 예정표 없음. |
| 새 표본 | `{"today": 9}` | `["q1"]` | 오늘10인 q2는 아직 제외. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
이 예정일 선택을 학습 효과가 입증된 적응형 모델이라고 부르지 않는다. 시간 부족이면 한도·예정일·힌트 분리만 구현.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 힌트를 보기 전에 답을 떠올릴 기회가 있는가?
- 선택되지 않은 질문의 예정일을 이해할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 미래 질문을 제외한 경계 검사 근거는 무엇인가?
- 예정일 선택 통과가 장기 기억 향상을 보장하지 않는 이유는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/itertools.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
