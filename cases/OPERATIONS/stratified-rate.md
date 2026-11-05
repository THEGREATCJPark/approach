# 혼합 구성 변화와 유형별 품질 변화 분리

```json
{
  "id": "stratified-rate",
  "title": "혼합 구성 변화와 유형별 품질 변화 분리",
  "family": "OPERATIONS",
  "keywords_ko": [
    "구성",
    "층화",
    "비교"
  ],
  "keywords_en": [
    "Simpson",
    "stratification"
  ],
  "problem_structure": "stratified comparison",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 도서 수선 작업장이 재작업률이 낮아졌다는 보고를 받았지만 작업 종류별로 보면 악화되어 비교 기준을 확인하려 한다.",
  "do_not_use_when": "전체 평균만으로 장비나 작업자를 순위화하지 않는다. 회귀모형보다 정의와 층화 확인이 먼저다. 층이 너무 작으면 순위 대신 관측수와 불확실성을 표시한다.",
  "data_required": [
    "최소 필수: period, type, total(건), rework(건), 기준 weight. 한 행은 기간×유형 집계, 복합키 유일. null은 집계 미완료, 0건은 관측 대상 없음. 작업 시간은 있으면 개선. 정의가 없으면 수치만 병렬 제시하고 개선 판단 보류."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "missing-versus-alarm"
  ],
  "depth": "deep",
  "path": "cases/OPERATIONS/stratified-rate.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "raw_before": 0.26,
        "raw_after": 0.19,
        "standard_after": 0.31
      },
      "basis": "2+24=26;12+7=19;0.2×0.15+0.8×0.35=0.31."
    },
    {
      "kind": "경계",
      "input": {
        "zero": true
      },
      "expected": "unknown",
      "basis": "0건 층은 비율을 만들 수 없다."
    },
    {
      "kind": "정보 부족",
      "input": {
        "missing": true
      },
      "expected": "unknown",
      "basis": "한 층의 집계 누락이면 표준화 비교 보류."
    },
    {
      "kind": "충돌",
      "input": {
        "invalid": true
      },
      "expected": "invalid",
      "basis": "재작업 21건/총20건은 불가능."
    },
    {
      "kind": "순서변경",
      "input": {
        "reverse": true
      },
      "expected": {
        "raw_before": 0.26,
        "raw_after": 0.19,
        "standard_after": 0.31
      },
      "basis": "집계 행 순서와 무관."
    },
    {
      "kind": "새 표본",
      "input": {
        "same_mix": true
      },
      "expected": {
        "raw_before": 0.26,
        "raw_after": 0.31,
        "standard_after": 0.31
      },
      "basis": "after simple 3/20, hard28/80이면 구성 고정."
    }
  ],
  "fixture": [
    {
      "period": "before",
      "type": "simple",
      "total": 20,
      "rework": 2
    },
    {
      "period": "before",
      "type": "hard",
      "total": 80,
      "rework": 24
    },
    {
      "period": "after",
      "type": "simple",
      "total": 80,
      "rework": 12
    },
    {
      "period": "after",
      "type": "hard",
      "total": 20,
      "rework": 7
    },
    {
      "period": "weight",
      "type": "simple",
      "weight": 0.2
    },
    {
      "period": "weight",
      "type": "hard",
      "weight": 0.8
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 도서 수선 작업장이 재작업률이 낮아졌다는 보고를 받았지만 작업 종류별로 보면 악화되어 비교 기준을 확인하려 한다.

- 쉬운 작업 비중이 늘어 전체 비율이 개선된다.
- 유형별 실제 공정이 악화된다.
- 재작업 정의나 분모가 기간별로 다르다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 유형별 분모와 재작업 정의가 같은가? | 다르면 비교 보류와 정의 일치부터 진행. |
| 실제 전체 부담인가 같은 구성에서의 성과인가? | 전자는 원비율, 후자는 고정 가중 표준화 비율. |
| 기준 가중치는 누가 언제 고정하는가? | 합의된 기준기간 비중을 사용하고 유리한 가중치 사후 선택 금지. |

## 데이터 계약과 합성 입력
최소 필수: period, type, total(건), rework(건), 기준 weight. 한 행은 기간×유형 집계, 복합키 유일. null은 집계 미완료, 0건은 관측 대상 없음. 작업 시간은 있으면 개선. 정의가 없으면 수치만 병렬 제시하고 개선 판단 보류.

```json
[
  {
    "period": "before",
    "type": "simple",
    "total": 20,
    "rework": 2
  },
  {
    "period": "before",
    "type": "hard",
    "total": 80,
    "rework": 24
  },
  {
    "period": "after",
    "type": "simple",
    "total": 80,
    "rework": 12
  },
  {
    "period": "after",
    "type": "hard",
    "total": 20,
    "rework": 7
  },
  {
    "period": "weight",
    "type": "simple",
    "weight": 0.2
  },
  {
    "period": "weight",
    "type": "hard",
    "weight": 0.8
  }
]
```

## 기준 방법과 최소 구현
유형별 비율과 전체 원비율을 함께 계산한다. 기준기간 비중을 고정한 표준화 비율을 추가하여 구성 효과를 드러낸다.

표본 불확실성이 필요하면 각 층의 관측 설계와 신뢰구간을 별도로 검토한다.

집계표 → 분모 검증 → 원비율/층별/표준화 비교 → 운영자가 개선 주장 보류 또는 조건별 조사 선택

목적함수 없음. 필수: 동일 정의와 모든 기준 층의 양수 분모. 선호: 원자료 출처·층별 크기를 함께 표시.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"raw_before": 0.26, "raw_after": 0.19, "standard_after": 0.31}` | 2+24=26;12+7=19;0.2×0.15+0.8×0.35=0.31. |
| 경계 | `{"zero": true}` | `"unknown"` | 0건 층은 비율을 만들 수 없다. |
| 정보 부족 | `{"missing": true}` | `"unknown"` | 한 층의 집계 누락이면 표준화 비교 보류. |
| 충돌 | `{"invalid": true}` | `"invalid"` | 재작업 21건/총20건은 불가능. |
| 순서변경 | `{"reverse": true}` | `{"raw_before": 0.26, "raw_after": 0.19, "standard_after": 0.31}` | 집계 행 순서와 무관. |
| 새 표본 | `{"same_mix": true}` | `{"raw_before": 0.26, "raw_after": 0.31, "standard_after": 0.31}` | after simple 3/20, hard28/80이면 구성 고정. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 단순 작업 10%→15%, 어려운 작업30%→35%로 각 5%p 악화. 전체는26%→19%로7%p 개선처럼 보임. 기준구성으로는26%→31%,5%p 악화.

서로 비슷하지만 달라야 하는 두 건: 전체 19%만 보여주면 개선처럼 보이지만 동일 가중치 31%는 악화이다.

## 답변 변화와 범위 통제
- 목적이 재작업 총 인력 예산이라는 답변 → 표준화보다 실제 건수·작업시간을 주 지표로 변경.
- 유형 정의가 바뀌었다는 답변 → 공통 분류로 재집계 전 비교를 중단.

전체 평균만으로 장비나 작업자를 순위화하지 않는다. 회귀모형보다 정의와 층화 확인이 먼저다. 층이 너무 작으면 순위 대신 관측수와 불확실성을 표시한다.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 원비율과 표준화 비율 중 이번 결정에 어느 것이 필요한가?
- 누락된 층이 있을 때 보고서를 승인하지 않도록 명확한가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 구성 변화 계산을 원자료와 연결하여 재현할 수 있는가?
- 이 분석으로 인과효과를 주장할 수 없는 이유는 무엇인가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/statistics.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
