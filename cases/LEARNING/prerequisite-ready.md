# 선수 개념을 이수한 다음 실습 선택

```json
{
  "id": "prerequisite-ready",
  "title": "선수 개념을 이수한 다음 실습 선택",
  "family": "LEARNING",
  "keywords_ko": [
    "선수지식",
    "학습",
    "의존"
  ],
  "keywords_en": [
    "prerequisite",
    "DAG"
  ],
  "problem_structure": "prerequisite graph",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 공동 제작실의 교육 운영자가 초급 실습 다섯 개 중 오늘 참가자가 바로 수행할 수 있는 실습을 표시해 달라고 한다.",
  "do_not_use_when": "완료 집합만으로 이해도 향상을 주장할 수 없다. 잘못된 구현은 순서대로 나열한 목록을 선수 관계로 간주하는 것. LLM 교육 추천은 첫 도구가 아니다. 규칙 미확정이면 추천 대신 누락 목록까지만 구현.",
  "data_required": [
    "최소 필수: 개념 id 문자열, requires 문자열 배열, 완료 id 집합. 한 행은 개념 하나이고 requires는 같은 표의 id를 참조한다. 빈 requires는 선수 없음, null은 미확인이다. 기준일/유효기간은 있으면 개선; 실명은 없어도 가능. 규칙이 없으면 준비 가능을 판정하지 않고 자료 요청."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "concept-diagnostic"
  ],
  "depth": "deep",
  "path": "cases/LEARNING/prerequisite-ready.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {
        "done": [
          "intro"
        ]
      },
      "expected": [
        "join",
        "measure"
      ],
      "basis": "두 개의 직접 선수가 모두 intro이다."
    },
    {
      "kind": "경계",
      "input": {
        "done": [
          "intro",
          "measure",
          "cut",
          "join",
          "finish"
        ]
      },
      "expected": [],
      "basis": "전부 완료이면 추천할 미완료가 없다."
    },
    {
      "kind": "정보 부족",
      "input": {
        "done": null
      },
      "expected": "unknown",
      "basis": "미기록은 미이수와 다르다."
    },
    {
      "kind": "충돌",
      "input": {
        "done": [],
        "cycle": true
      },
      "expected": "invalid_cycle",
      "basis": "intro가 finish를 선수로 요구하면 순환이다."
    },
    {
      "kind": "순서변경",
      "input": {
        "done": [
          "intro"
        ],
        "reverse": true
      },
      "expected": [
        "join",
        "measure"
      ],
      "basis": "행 순서는 의존 관계를 바꾸지 않는다."
    },
    {
      "kind": "새 표본",
      "input": {
        "done": [
          "intro",
          "measure",
          "join"
        ]
      },
      "expected": [
        "cut"
      ],
      "basis": "finish는 아직 cut이 필요하다."
    }
  ],
  "fixture": [
    {
      "id": "intro",
      "requires": []
    },
    {
      "id": "measure",
      "requires": [
        "intro"
      ]
    },
    {
      "id": "cut",
      "requires": [
        "measure"
      ]
    },
    {
      "id": "join",
      "requires": [
        "intro"
      ]
    },
    {
      "id": "finish",
      "requires": [
        "cut",
        "join"
      ]
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 공동 제작실의 교육 운영자가 초급 실습 다섯 개 중 오늘 참가자가 바로 수행할 수 있는 실습을 표시해 달라고 한다.

- 선수 지식 미이수로 실습 실패가 발생한다.
- 이수 기록이 누락되어 이미 아는 실습을 다시 시킨다.
- 안전 자격의 유효기간이 만료되지만 단순 이수로 취급한다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 이수는 어떤 증거와 기간으로 유효한가? | 시험 기록이면 점수 검증, 유효기간이 있으면 기준일 검증을 추가한다. |
| 동시에 시작할 수 있는 실습을 찾는가, 전체 교육 순서를 짜는가? | 전자는 ready 집합, 후자는 위상 정렬과 자원 일정으로 확장한다. |
| 선수 규칙 자체가 충돌할 때 누가 수정하는가? | 교육 책임자 확인까지 순환을 보류하며 자동 삭제하지 않는다. |

## 데이터 계약과 합성 입력
최소 필수: 개념 id 문자열, requires 문자열 배열, 완료 id 집합. 한 행은 개념 하나이고 requires는 같은 표의 id를 참조한다. 빈 requires는 선수 없음, null은 미확인이다. 기준일/유효기간은 있으면 개선; 실명은 없어도 가능. 규칙이 없으면 준비 가능을 판정하지 않고 자료 요청.

```json
[
  {
    "id": "intro",
    "requires": []
  },
  {
    "id": "measure",
    "requires": [
      "intro"
    ]
  },
  {
    "id": "cut",
    "requires": [
      "measure"
    ]
  },
  {
    "id": "join",
    "requires": [
      "intro"
    ]
  },
  {
    "id": "finish",
    "requires": [
      "cut",
      "join"
    ]
  }
]
```

## 기준 방법과 최소 구현
완료 집합에 모든 선수가 포함된 미완료 노드만 고른다. 먼저 참조 무결성과 전체 순환을 검사한다.

전체 순서가 필요할 때만 위상 정렬을 사용하고, 강사·공간 자원은 별도 일정 모델로 다룬다.

개념 표 + 완료 목록 → 규칙 검사 → 가능한 실습과 막힌 이유 → 운영자가 다음 실습 선택

목적함수 없음. 필수: 참조 유효·무순환·완료 증거. 선호: 짧은 실습 우선은 준비 가능 판정 이후 별도 정렬.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{"done": ["intro"]}` | `["join", "measure"]` | 두 개의 직접 선수가 모두 intro이다. |
| 경계 | `{"done": ["intro", "measure", "cut", "join", "finish"]}` | `[]` | 전부 완료이면 추천할 미완료가 없다. |
| 정보 부족 | `{"done": null}` | `"unknown"` | 미기록은 미이수와 다르다. |
| 충돌 | `{"done": [], "cycle": true}` | `"invalid_cycle"` | intro가 finish를 선수로 요구하면 순환이다. |
| 순서변경 | `{"done": ["intro"], "reverse": true}` | `["join", "measure"]` | 행 순서는 의존 관계를 바꾸지 않는다. |
| 새 표본 | `{"done": ["intro", "measure", "join"]}` | `["cut"]` | finish는 아직 cut이 필요하다. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 완료={intro}일 때 measure의 선수 {intro}와 join의 선수 {intro}는 부분집합이다. cut은 measure, finish는 cut/join이 빠져 제외한다.

서로 비슷하지만 달라야 하는 두 건: 완료 {intro, measure, join}이면 cut만 가능하지만 {intro, measure, cut, join}이면 finish만 가능.

## 답변 변화와 범위 통제
- 자격이 90일 유효하다는 답변 → 완료 집합 생성에 기준일과 만료일 추가.
- 다음 한 개가 아니라 하루 시간표가 필요하다는 답변 → 일정/자원배정으로 주 접근 변경.

완료 집합만으로 이해도 향상을 주장할 수 없다. 잘못된 구현은 순서대로 나열한 목록을 선수 관계로 간주하는 것. LLM 교육 추천은 첫 도구가 아니다. 규칙 미확정이면 추천 대신 누락 목록까지만 구현.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 표에서 막힌 이유를 보고 누구에게 어떤 기록을 요청하겠는가?
- 완료했는데 제외된 실제 유형이 있다면 어떤 증거가 누락됐는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 순환을 제거하지 않고 보류한 코드와 반례는 어디 있는가?
- 준비 가능 판정과 학습 효과 검증이 어떻게 다른가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/graphlib.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
