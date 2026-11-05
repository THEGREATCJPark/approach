# 차이 미검출과 동등성 구간 판정 구별

```json
{
  "id": "equivalence-interval",
  "title": "차이 미검출과 동등성 구간 판정 구별",
  "family": "QUALITY",
  "keywords_ko": [
    "동등성",
    "허용범위",
    "신뢰구간"
  ],
  "keywords_en": [
    "equivalence",
    "interval"
  ],
  "problem_structure": "interval containment",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 종이 두께 측정 방법을 교체하려는 검증 담당자가 차이가 유의하지 않다는 말만으로 교체를 승인하지 않게 비교표를 만들려 한다.",
  "do_not_use_when": "현재 예제는 임의 합성 구간이며 실제 동등성 검정을 실행하지 않았다. 통계 라이브러리 설치만으로 설계 타당성이 확보되지 않는다. 원자료 없으면 포함 관계까지만 검증.",
  "data_required": [
    "최소 필수: batch_id, lower, upper(같은 두께 단위), margin>0, interval_method, confidence. 한 행은 한 비교의 사전 검증된 차이 구간. null은 미계산. 본 소형 예제는 주어진 구간의 포함 관계만 검사하며 신뢰구간을 추정하지 않는다. 원자료·분산·표본수 없으면 통계 타당성을 주장할 수 없다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "mandatory-gates"
  ],
  "depth": "deep",
  "path": "cases/QUALITY/equivalence-interval.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {
        "lower": -0.2,
        "upper": 0.3
      },
      "expected": "within_margin",
      "basis": "두 끝이−0.5와0.5 내부."
    },
    {
      "kind": "경계",
      "input": {
        "lower": -0.5,
        "upper": 0.3
      },
      "expected": "not_demonstrated",
      "basis": "엄격 내부 포함 정책이므로 경계 접촉 불충분."
    },
    {
      "kind": "정보 부족",
      "input": {
        "lower": null,
        "upper": null
      },
      "expected": "unknown",
      "basis": "구간 없음."
    },
    {
      "kind": "충돌",
      "input": {
        "lower": 0.4,
        "upper": -0.2
      },
      "expected": "invalid",
      "basis": "하한>상한."
    },
    {
      "kind": "재시도",
      "input": {
        "lower": -0.2,
        "upper": 0.3,
        "repeat": true
      },
      "expected": "within_margin",
      "basis": "같은 구간 재평가는 기준 변화 없음."
    },
    {
      "kind": "새 표본",
      "input": {
        "lower": -0.8,
        "upper": 0.9
      },
      "expected": "not_demonstrated",
      "basis": "0을 포함해도 margin을 넘으므로 동등성 입증 아님."
    }
  ],
  "fixture": [
    {
      "batch": "b1",
      "lower": -0.2,
      "upper": 0.3
    },
    {
      "batch": "b2",
      "lower": -0.5,
      "upper": 0.3
    },
    {
      "batch": "b3",
      "lower": -0.8,
      "upper": 0.9
    },
    {
      "batch": "b4",
      "lower": 0.6,
      "upper": 0.9
    },
    {
      "batch": "b5",
      "lower": null,
      "upper": null
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 종이 두께 측정 방법을 교체하려는 검증 담당자가 차이가 유의하지 않다는 말만으로 교체를 승인하지 않게 비교표를 만들려 한다.

- 차이 검정의 비유의 결과를 동등성으로 해석한다.
- 허용차를 결과를 본 뒤 넓힌다.
- 신뢰구간이 다른 측정 단위나 표본 설계에서 계산되었다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 허용 차이와 신뢰수준을 결과 전에 정했는가? | 미정이면 판정 보류; 본 예제 허용차 ±0.5단위와 엄격 내부 포함. |
| 구간은 어떤 표본 설계·계산으로 생성했는가? | 동일 시료 쌍인지 독립 표본인지 확인하고 적절한 통계 검증 없이는 운영 승인 금지. |
| 한 개 지표 통과가 전체 교체 승인인가? | 아니면 측정 신뢰도·다른 필수 승인 gate와 분리. |

## 데이터 계약과 합성 입력
최소 필수: batch_id, lower, upper(같은 두께 단위), margin>0, interval_method, confidence. 한 행은 한 비교의 사전 검증된 차이 구간. null은 미계산. 본 소형 예제는 주어진 구간의 포함 관계만 검사하며 신뢰구간을 추정하지 않는다. 원자료·분산·표본수 없으면 통계 타당성을 주장할 수 없다.

```json
[
  {
    "batch": "b1",
    "lower": -0.2,
    "upper": 0.3
  },
  {
    "batch": "b2",
    "lower": -0.5,
    "upper": 0.3
  },
  {
    "batch": "b3",
    "lower": -0.8,
    "upper": 0.9
  },
  {
    "batch": "b4",
    "lower": 0.6,
    "upper": 0.9
  },
  {
    "batch": "b5",
    "lower": null,
    "upper": null
  }
]
```

축약 fixture의 `batch`는 운영 스키마의 `batch_id`에 대응한다. 컨텍스트의 `margin=0.5`는 고정 합성 값이다. `interval_method`와 `confidence`는 의도적으로 제공하지 않았으며 검증된 통계구간이라는 주장을 하지 않는다. 여기의 within_margin은 숫자 구간의 포함 관계만 뜻한다. 실제 통계 판정 경로라면 방법·신뢰수준·원자료가 없으므로 unknown으로 보류해야 한다.

## 기준 방법과 최소 구현
입력 구간 검증 후 하한>−margin 및 상한<margin이면 within_margin, 아니면 not_demonstrated, 누락은 unknown. 이 출력만으로 실제 동등성 인증을 하지 않는다.

원자료와 표본 설계가 검증되면 적절한 TOST·신뢰구간 계산을 통계 담당자와 선택한다. 차이검정 p값만으로 대체하지 않는다.

검증된 구간+사전 margin → 포함 관계·기준 표시 → 담당자가 추가 표본/방법 검토 또는 다른 승인 단계 진행

목적함수 없음. 필수: 사전 margin, 단위 일치, 검증된 구간 생성 절차. 선호: 폭·표본수 병기. 이 연습은 구간 포함 판정이며 전체 통계 추론 검증이 아니다.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{"lower": -0.2, "upper": 0.3}` | `"within_margin"` | 두 끝이−0.5와0.5 내부. |
| 경계 | `{"lower": -0.5, "upper": 0.3}` | `"not_demonstrated"` | 엄격 내부 포함 정책이므로 경계 접촉 불충분. |
| 정보 부족 | `{"lower": null, "upper": null}` | `"unknown"` | 구간 없음. |
| 충돌 | `{"lower": 0.4, "upper": -0.2}` | `"invalid"` | 하한>상한. |
| 재시도 | `{"lower": -0.2, "upper": 0.3, "repeat": true}` | `"within_margin"` | 같은 구간 재평가는 기준 변화 없음. |
| 새 표본 | `{"lower": -0.8, "upper": 0.9}` | `"not_demonstrated"` | 0을 포함해도 margin을 넘으므로 동등성 입증 아님. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: b1은−0.2>−0.5 및0.3<0.5. b3는0을 포함하지만 폭1.7로 허용폭1.0보다 넓다. 비유의 차이가 동등성의 증거는 아니다.

서로 비슷하지만 달라야 하는 두 건: [-0.49,0.3]은 within_margin, [-0.5,0.3]은 not_demonstrated(본 엄격 정책).

## 답변 변화와 범위 통제
- 경계 포함 정책이 맞다는 답변 → 사전 승인된 ≤판정으로 변경하고 경계 테스트 수정.
- 표본이 독립이 아니라 동일 시료 쌍이라는 답변 → 구간 생성 방법부터 다시 검증.

현재 예제는 임의 합성 구간이며 실제 동등성 검정을 실행하지 않았다. 통계 라이브러리 설치만으로 설계 타당성이 확보되지 않는다. 원자료 없으면 포함 관계까지만 검증.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- not_demonstrated를 품질 불합격으로 오해하지 않는가?
- 허용범위를 누가 정했고 추가로 어떤 증거가 필요한지 보이는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 주어진 구간 판정과 구간 추정의 검증 범위를 구별하여 설명할 수 있는가?
- 차이 미검출과 동등성의 반례를 어떤 fixture로 보여줄 수 있는가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/decimal.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)

- 추가 공개 1차 참고: https://www.statsmodels.org/stable/generated/statsmodels.stats.weightstats.ttost_ind.html (독립표본 동등성 검정 API 설명; 본 예제에서는 실행하지 않음. 쌍체 설계에 그대로 적용하지 않는다.)
