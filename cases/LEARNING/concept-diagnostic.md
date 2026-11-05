# 미응답과 오답을 분리한 개념별 진단

```json
{
  "id": "concept-diagnostic",
  "title": "미응답과 오답을 분리한 개념별 진단",
  "family": "LEARNING",
  "keywords_ko": [
    "진단",
    "개념별",
    "오답"
  ],
  "keywords_en": [
    "assessment",
    "missing"
  ],
  "problem_structure": "grouped rubric",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 지역 수리 교실의 강사가 한 번의 총점 대신 어느 개념을 다시 설명해야 하는지 보고 싶다고 한다.",
  "do_not_use_when": "숫자 점수만으로 개인 능력을 확정하지 않는다. LLM 자동 평가를 기본으로 쓰지 않는다. 시간 부족이면 개념별 수와 판정만 구현하고 개인화 콘텐츠 생성은 제외.",
  "data_required": [
    "최소 필수: response_id, concept, score(0/1/null). 한 행은 고유 문항 응답 한 건, response_id가 관계키다. null은 미응답. 동일 id는 같은 문항의 재전송으로 정의. 개념 기준·문항 난도는 있으면 개선, 이름은 없어도 가능. 개념 매핑이 없으면 전체 응답률만 제시."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "prerequisite-ready"
  ],
  "depth": "deep",
  "path": "cases/LEARNING/concept-diagnostic.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "safety": "ready",
        "tools": "unknown",
        "units": "practice"
      },
      "basis": "units 1/2, safety 2/2, tools 1개 응답."
    },
    {
      "kind": "경계",
      "input": {
        "only": [
          1,
          1,
          1,
          0
        ]
      },
      "expected": {
        "x": "ready"
      },
      "basis": "3/4=0.75 경계 포함."
    },
    {
      "kind": "정보 부족",
      "input": {
        "only": [
          null,
          1
        ]
      },
      "expected": {
        "x": "unknown"
      },
      "basis": "관측 1개로 최소 2개 미달."
    },
    {
      "kind": "충돌",
      "input": {
        "conflict": true
      },
      "expected": "invalid",
      "basis": "r1에 다른 점수가 같이 있으면 출처 확인."
    },
    {
      "kind": "재전송",
      "input": {
        "duplicate": true
      },
      "expected": {
        "safety": "ready",
        "tools": "unknown",
        "units": "practice"
      },
      "basis": "같은 id 같은 내용은 한 번만 센다."
    },
    {
      "kind": "새 표본",
      "input": {
        "only": [
          0,
          0,
          1
        ]
      },
      "expected": {
        "x": "practice"
      },
      "basis": "1/3은 0.75 미만."
    }
  ],
  "fixture": [
    {
      "response_id": "r1",
      "concept": "units",
      "score": 1
    },
    {
      "response_id": "r2",
      "concept": "units",
      "score": 0
    },
    {
      "response_id": "r3",
      "concept": "safety",
      "score": 1
    },
    {
      "response_id": "r4",
      "concept": "safety",
      "score": 1
    },
    {
      "response_id": "r5",
      "concept": "tools",
      "score": null
    },
    {
      "response_id": "r6",
      "concept": "tools",
      "score": 1
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 지역 수리 교실의 강사가 한 번의 총점 대신 어느 개념을 다시 설명해야 하는지 보고 싶다고 한다.

- 전체 점수는 높지만 특정 개념만 약하다.
- 미응답이 오답으로 계산되어 지식 부족처럼 보인다.
- 중복 제출이 개념별 분모를 부풀린다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 개념당 몇 문항을 풀어야 판정 가능한가? | 본 예제는 서로 다른 문항의 응답 2개 이상; 미달은 unknown. |
| 오답과 미응답이 같은 의미인가? | 아니면 미응답 분리, 제한시간 초과라면 시간 자료도 수집. |
| 같은 응답 id가 두 번 오면 어느 것이 유효한가? | 동일 재전송은 제거, 내용 충돌은 임의 최신값 대신 invalid. |

## 데이터 계약과 합성 입력
최소 필수: response_id, concept, score(0/1/null). 한 행은 고유 문항 응답 한 건, response_id가 관계키다. null은 미응답. 동일 id는 같은 문항의 재전송으로 정의. 개념 기준·문항 난도는 있으면 개선, 이름은 없어도 가능. 개념 매핑이 없으면 전체 응답률만 제시.

```json
[
  {
    "response_id": "r1",
    "concept": "units",
    "score": 1
  },
  {
    "response_id": "r2",
    "concept": "units",
    "score": 0
  },
  {
    "response_id": "r3",
    "concept": "safety",
    "score": 1
  },
  {
    "response_id": "r4",
    "concept": "safety",
    "score": 1
  },
  {
    "response_id": "r5",
    "concept": "tools",
    "score": null
  },
  {
    "response_id": "r6",
    "concept": "tools",
    "score": 1
  }
]
```

## 기준 방법과 최소 구현
고유 id로 중복을 제거한 뒤 응답 수와 정답 수를 함께 표시한다. 2개 이상 응답하고 정답률 0.75 이상이면 ready, 미만이면 practice, 부족하면 unknown.

검증된 문항 난도·신뢰도 자료가 생긴 경우만 더 정교한 평가 모델을 검토한다. 작은 표본의 점수를 능력 확률로 부르지 않는다.

응답 CSV → 유효성·중복 검사 → 개념별 응답수/정답률/판정 → 강사가 보충 설명 또는 추가 진단 선택

목적함수 없음. 필수: 최소 관측수와 고유 id. 선호: 낮은 개념부터 표시. 교육 목표와 임계값은 합성 정책이며 보편 표준이 아니다.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"safety": "ready", "tools": "unknown", "units": "practice"}` | units 1/2, safety 2/2, tools 1개 응답. |
| 경계 | `{"only": [1, 1, 1, 0]}` | `{"x": "ready"}` | 3/4=0.75 경계 포함. |
| 정보 부족 | `{"only": [null, 1]}` | `{"x": "unknown"}` | 관측 1개로 최소 2개 미달. |
| 충돌 | `{"conflict": true}` | `"invalid"` | r1에 다른 점수가 같이 있으면 출처 확인. |
| 재전송 | `{"duplicate": true}` | `{"safety": "ready", "tools": "unknown", "units": "practice"}` | 같은 id 같은 내용은 한 번만 센다. |
| 새 표본 | `{"only": [0, 0, 1]}` | `{"x": "practice"}` | 1/3은 0.75 미만. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 정답률은 응답된 고유 문항만 분모로 쓴다. tools는 관측 1/전체 2이므로 정답률 1이어도 준비 판정하지 않는다.

서로 비슷하지만 달라야 하는 두 건: 점수 [1, null]은 unknown, [1,1]은 ready이다.

## 답변 변화와 범위 통제
- 미응답도 채점 오답이라는 공식 정책이 확인되면 분모와 라벨을 변경하고 이전 결과와 구분.
- 개념별 문항 난도가 다르다는 답변이면 단순 순위 대신 문항 구성 차이를 함께 표시.

숫자 점수만으로 개인 능력을 확정하지 않는다. LLM 자동 평가를 기본으로 쓰지 않는다. 시간 부족이면 개념별 수와 판정만 구현하고 개인화 콘텐츠 생성은 제외.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- unknown을 본 다음 추가 진단을 선택할 수 있는가?
- practice로 묶였지만 다른 설명이 필요한 문항은 무엇인가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 분모와 중복 제거를 정한 근거를 어떤 파일로 설명할 수 있는가?
- 합성 점수 테스트가 실제 교육 효과를 보장하지 않는 이유는 무엇인가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/statistics.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
