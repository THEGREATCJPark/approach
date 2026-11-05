# 고정 활동을 포함한 3일 서비스 편성

```json
{
  "id": "rotation-budget",
  "title": "고정 활동을 포함한 3일 서비스 편성",
  "family": "PLANNING",
  "keywords_ko": [
    "기간계획",
    "예산",
    "반복"
  ],
  "keywords_en": [
    "scheduling",
    "constraints"
  ],
  "problem_structure": "finite constraint search",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 작은 방문 체험실이 3일간 하루 활동 하나를 열되 같은 활동 연속 운영을 피하고 예산 안에서 준비하려 한다.",
  "do_not_use_when": "인기 추천 문제와 기간 편성은 다르다. 후보를 무작정 추천 점수로 정렬하면 기간 제약을 놓친다. 큰 입력은 하루 수 축소와 수동 검토로 시작한다.",
  "data_required": [
    "최소 필수: activity id, cost(예산 단위), available_days; day 정수0..2와 fixed 활동 id, budget 정수. 한 행은 활동 혹은 고정 슬롯이며 타입 필드로 구분한다. null 비용은 미견적,0은 무료. 참가자 신원은 없어도 가능. 견적 미확정이면 최적 비용 주장 보류."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "pack-order"
  ],
  "depth": "deep",
  "path": "cases/PLANNING/rotation-budget.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "plan": [
          "A",
          "B",
          "A"
        ],
        "cost": 14
      },
      "basis": "4+6+4=14."
    },
    {
      "kind": "경계",
      "input": {
        "budget": 14
      },
      "expected": {
        "plan": [
          "A",
          "B",
          "A"
        ],
        "cost": 14
      },
      "basis": "예산 상한 포함."
    },
    {
      "kind": "정보 부족",
      "input": {
        "missing_cost": true
      },
      "expected": "unknown",
      "basis": "A 비용 미확정이므로 최저비용 확정 불가."
    },
    {
      "kind": "불가능",
      "input": {
        "budget": 13
      },
      "expected": "infeasible",
      "basis": "고정 B 양옆 가장 싼 A도14."
    },
    {
      "kind": "순서변경",
      "input": {
        "reverse": true
      },
      "expected": {
        "plan": [
          "A",
          "B",
          "A"
        ],
        "cost": 14
      },
      "basis": "입력 활동 순서는 동률 규칙을 바꾸지 않는다."
    },
    {
      "kind": "새 표본",
      "input": {
        "fixed": "C",
        "budget": 15
      },
      "expected": {
        "plan": [
          "A",
          "C",
          "A"
        ],
        "cost": 15
      },
      "basis": "4+7+4=15."
    }
  ],
  "fixture": [
    {
      "kind": "activity",
      "id": "A",
      "cost": 4
    },
    {
      "kind": "activity",
      "id": "B",
      "cost": 6
    },
    {
      "kind": "activity",
      "id": "C",
      "cost": 7
    },
    {
      "kind": "fixed",
      "day": 1,
      "id": "B"
    },
    {
      "kind": "rule",
      "days": 3,
      "budget": 15,
      "no_adjacent_repeat": true
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 작은 방문 체험실이 3일간 하루 활동 하나를 열되 같은 활동 연속 운영을 피하고 예산 안에서 준비하려 한다.

- 연속 반복이 참여자의 선택 폭을 줄인다.
- 중간날 고정 예약 때문에 저렴한 편성이 막힌다.
- 예산과 필수 제공 조건이 동시에 불가능하다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 반복 금지는 필수인가 선호인가? | 필수면 후보 제외, 선호면 비용과 별도 우선순위 협의. |
| 이미 공지된 날은 바꿀 수 있는가? | 고정이면 해당 날짜 활동을 제약으로 유지. |
| 최소 비용인가 최대 다양성인가? | 본 예제는 필수조건 충족 후 비용 최소; 목적 변경 시 같은 데이터도 다른 편성. |

## 데이터 계약과 합성 입력
최소 필수: activity id, cost(예산 단위), available_days; day 정수0..2와 fixed 활동 id, budget 정수. 한 행은 활동 혹은 고정 슬롯이며 타입 필드로 구분한다. null 비용은 미견적,0은 무료. 참가자 신원은 없어도 가능. 견적 미확정이면 최적 비용 주장 보류.

```json
[
  {
    "kind": "activity",
    "id": "A",
    "cost": 4
  },
  {
    "kind": "activity",
    "id": "B",
    "cost": 6
  },
  {
    "kind": "activity",
    "id": "C",
    "cost": 7
  },
  {
    "kind": "fixed",
    "day": 1,
    "id": "B"
  },
  {
    "kind": "rule",
    "days": 3,
    "budget": 15,
    "no_adjacent_repeat": true
  }
]
```

축약 fixture의 모든 활동은 day 0,1,2에 이용 가능하다고 고정한다(`available_days=[0,1,2]`). 활동별 제한이 실제로 존재하면 그 필드를 입력과 후보 필터에 추가해야 한다. 여기서는 비용·고정 슬롯·인접 반복 조건만 실행 검증했다.

## 기준 방법과 최소 구현
3^3=27개 작은 조합을 열거하여 고정일·연속반복·예산 위반을 먼저 제거하고 비용 최소안을 고른다. 동률은 활동 id 순으로 결정한다.

기간·활동 수가 커져 열거가 어렵고 설치가 허용될 때만 CP-SAT를 검토한다. 시간 제한 미발견은 infeasible이 아닌 unknown일 수 있다.

활동/고정일/예산 입력 → 후보 검증 → 편성과 비용/위반 목록 → 담당자가 공지 여부 결정

목적: 총비용 최소. 필수: 하루1개, 중간 고정, 인접 중복 없음, 총비용≤예산. 선호는 본 예제에서 없음. 필수조건을 점수로 상쇄하지 않는다.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"plan": ["A", "B", "A"], "cost": 14}` | 4+6+4=14. |
| 경계 | `{"budget": 14}` | `{"plan": ["A", "B", "A"], "cost": 14}` | 예산 상한 포함. |
| 정보 부족 | `{"missing_cost": true}` | `"unknown"` | A 비용 미확정이므로 최저비용 확정 불가. |
| 불가능 | `{"budget": 13}` | `"infeasible"` | 고정 B 양옆 가장 싼 A도14. |
| 순서변경 | `{"reverse": true}` | `{"plan": ["A", "B", "A"], "cost": 14}` | 입력 활동 순서는 동률 규칙을 바꾸지 않는다. |
| 새 표본 | `{"fixed": "C", "budget": 15}` | `{"plan": ["A", "C", "A"], "cost": 15}` | 4+7+4=15. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 중간 B는6, 양옆은 B 금지이고 A4 또는 C7이므로 최저4+6+4=14. 13 이하는 전수 열거 없이도 하한으로 불가능을 확인.

서로 비슷하지만 달라야 하는 두 건: 예산14는 feasible, 예산13은 infeasible. 동일 활동 2일 간격 반복은 허용한다.

## 답변 변화와 범위 통제
- 반복 간격이 하루가 아닌 3일이라는 답변 → A-B-A를 제외하고 모델 재작성.
- 예산 초과가 승인 가능하다는 답변 → 자동 완화하지 않고 승인된 별도 시나리오로 표시.

인기 추천 문제와 기간 편성은 다르다. 후보를 무작정 추천 점수로 정렬하면 기간 제약을 놓친다. 큰 입력은 하루 수 축소와 수동 검토로 시작한다.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 편성에서 고정 공지를 침범한 날이 없는가?
- 불가능 사유만 보고 어떤 조건을 담당자가 재협의할 수 있는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 14라는 하한을 독립적으로 어떻게 증명했는가?
- 목적과 필수조건의 우선순위를 무엇으로 확인했는가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/itertools.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
