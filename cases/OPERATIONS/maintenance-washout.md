# 정비 전후 비교에서 안정화 구간 제외

```json
{
  "id": "maintenance-washout",
  "title": "정비 전후 비교에서 안정화 구간 제외",
  "family": "OPERATIONS",
  "keywords_ko": [
    "정비 전후 비교에서 안정화 구간 제외",
    "정비 전후 관측 중앙값 차이를 같은 규칙으로 계산"
  ],
  "keywords_en": [
    "maintenance-washout",
    "relative day × measurement × washout"
  ],
  "problem_structure": "relative day × measurement × washout",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 복사 장비 관리자가 정비 효과를 보고하려는데 정비 당일 시험 가동 수치가 섞여 비교가 뒤집힌다.",
  "do_not_use_when": "전후 차이를 정비의 인과효과로 단정하지 않는다. 분석 도구보다 제외 규칙 기록이 먼저다. 조건이 달라졌으면 수치를 병렬로 보여주는 범위까지 축소한다.",
  "data_required": [
    "필수 relative_day 정수(정비일0), value 수치(분/100건), washout_days 비음수정수. 한 행은 하루 집계, day 고유. 전은day<0,후는day>washout. null 값은 미확인. 조건표는 실제 해석에 필요."
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
  "path": "cases/OPERATIONS/maintenance-washout.md",
  "decision_signature": {
    "decision": "정비 전후 관측 중앙값 차이를 같은 규칙으로 계산",
    "input_structure": "relative day × measurement × washout",
    "hard_constraint": "정비당일·안정화기간을 사전 규칙으로 제외",
    "validation": "극단적인 정비당일 값이 차이에 섞이지 않음"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 복사 장비 관리자가 정비 효과를 보고하려는데 정비 당일 시험 가동 수치가 섞여 비교가 뒤집힌다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 안정화 중 측정이 사후 성능처럼 포함된다.
- 정비 전후 작업 조건이 다르다.
- 효과가 좋아 보이는 날짜만 선택한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 안정화 구간은 며칠로 사전 정의하는가? | 본 예제 day0 제외;합의 없으면 여러 창을 분리 보고. |
| 전후 작업량·재료 조건이 같은가? | 다르면 층화나 비교 보류. |
| 정비 효과의 인과 주장이 필요한가? | 단순 전후로는 부족;비교설계와 다른 변경 이력 필요. |

## 4. 데이터와 없을 때의 대안
필수 relative_day 정수(정비일0), value 수치(분/100건), washout_days 비음수정수. 한 행은 하루 집계, day 고유. 전은day<0,후는day>washout. null 값은 미확인. 조건표는 실제 해석에 필요.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "rows": [
    [
      -3,
      9
    ],
    [
      -2,
      10
    ],
    [
      -1,
      11
    ],
    [
      0,
      100
    ],
    [
      1,
      6
    ],
    [
      2,
      7
    ],
    [
      3,
      8
    ]
  ],
  "washout_days": 0
}
```

## 5. 기준 방법과 개선 조건
사전 창 조건으로 전후 집합을 나누고 중앙값·관측수·제외일을 표시한다. 전후 중 하나가 비면 unknown.

유사 장비 비교군·추세 자료가 있으면 공통 변화와 정비 관련 변화를 구별하는 분석 설계.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 정비 전후 관측 중앙값 차이를 같은 규칙으로 계산 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"before_median": 10, "after_median": 7, "change": -3}` | 정비일100제외;중앙값10→7. |
| 경계 | `{"washout_days": 2}` | `{"before_median": 10, "after_median": 8, "change": -2}` | day2는제외하고day3만후구간. |
| 정보 부족 | `{"washout_days": 3}` | `"unknown"` | 남은후관측없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
전후 차이를 정비의 인과효과로 단정하지 않는다. 분석 도구보다 제외 규칙 기록이 먼저다. 조건이 달라졌으면 수치를 병렬로 보여주는 범위까지 축소한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 제외된 날짜와 이유를 보고 동의할 수 있는가?
- 관측일수가 적은 결과를 운영판단에 쓰려면 무엇이 더 필요한가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 100을 제외한 것이 결과에 유리한 사후 선택이 아니라는 근거는 무엇인가?
- 중앙값 차이가 보장하지 않는 효과는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/statistics.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
