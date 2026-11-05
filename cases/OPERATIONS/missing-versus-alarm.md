# 누락 센서와 실제 상한 초과 분리

```json
{
  "id": "missing-versus-alarm",
  "title": "누락 센서와 실제 상한 초과 분리",
  "family": "OPERATIONS",
  "keywords_ko": [
    "센서",
    "누락",
    "경보"
  ],
  "keywords_en": [
    "monitoring",
    "threshold"
  ],
  "problem_structure": "time series validation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 보관 시설 운영자가 시간별 온도 표시가 초록색인데 실제로는 센서가 끊긴 구간을 발견해 상태 표시를 고쳐 달라고 한다.",
  "do_not_use_when": "한계 초과는 원인 분석이 아니다. 지도나 이상탐지 모델이 결측 문제를 고치지는 않는다. 기준 미확정이면 관측/누락 표까지만 만든다.",
  "data_required": [
    "최소 필수: slot(기준 시간대의 정시 슬롯), temp_c(섭씨/null), 센서 id와 기대 슬롯 목록. 한 행은 센서 한 개의 관측 슬롯. null은 미수신. 교정상태는 있으면 개선, 지도는 없어도 가능. 시각 기준이 없으면 연속성 경보 보류."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "stratified-rate"
  ],
  "depth": "deep",
  "path": "cases/OPERATIONS/missing-versus-alarm.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "normal": 4,
        "alarm": 1,
        "unknown": 1
      },
      "basis": "4,5,8,6 정상;9 경보;null 미확인."
    },
    {
      "kind": "경계",
      "input": {
        "values": [
          8
        ]
      },
      "expected": {
        "normal": 1,
        "alarm": 0,
        "unknown": 0
      },
      "basis": "8 초과 규칙이므로 8은 정상."
    },
    {
      "kind": "정보 부족",
      "input": {
        "values": [
          null
        ]
      },
      "expected": {
        "normal": 0,
        "alarm": 0,
        "unknown": 1
      },
      "basis": "누락을 0으로 채우지 않는다."
    },
    {
      "kind": "충돌",
      "input": {
        "conflict": true
      },
      "expected": "invalid",
      "basis": "같은 slot에 4와 7은 출처 충돌."
    },
    {
      "kind": "순서변경",
      "input": {
        "reverse": true
      },
      "expected": {
        "normal": 4,
        "alarm": 1,
        "unknown": 1
      },
      "basis": "시간 키로 대응하면 순서와 무관."
    },
    {
      "kind": "새 표본",
      "input": {
        "values": [
          8.1,
          7.9,
          null
        ]
      },
      "expected": {
        "normal": 1,
        "alarm": 1,
        "unknown": 1
      },
      "basis": "소수 상한 반례."
    }
  ],
  "fixture": [
    {
      "slot": 0,
      "temp_c": 4
    },
    {
      "slot": 1,
      "temp_c": 5
    },
    {
      "slot": 2,
      "temp_c": null
    },
    {
      "slot": 3,
      "temp_c": 8
    },
    {
      "slot": 4,
      "temp_c": 9
    },
    {
      "slot": 5,
      "temp_c": 6
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 보관 시설 운영자가 시간별 온도 표시가 초록색인데 실제로는 센서가 끊긴 구간을 발견해 상태 표시를 고쳐 달라고 한다.

- null을 0으로 치환해 정상으로 표시한다.
- 관측 시점 대신 수신 시점으로 정렬한다.
- 상한 초과와 통신 오류의 대응 담당자가 다르다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 상한은 제품 규격인가 운영 경보 기준인가? | 본 예제는 운영 상한 8도; 제품 합격 판정과 분리. |
| 누락을 몇 분까지 허용하는가? | 유예가 있으면 stale 상태 추가, 없으면 즉시 unknown. |
| 중복 시각의 서로 다른 측정값은 어떻게 다루는가? | 원본 id/교정 이력 확인 전 invalid, 평균으로 덮지 않는다. |

## 데이터 계약과 합성 입력
최소 필수: slot(기준 시간대의 정시 슬롯), temp_c(섭씨/null), 센서 id와 기대 슬롯 목록. 한 행은 센서 한 개의 관측 슬롯. null은 미수신. 교정상태는 있으면 개선, 지도는 없어도 가능. 시각 기준이 없으면 연속성 경보 보류.

```json
[
  {
    "slot": 0,
    "temp_c": 4
  },
  {
    "slot": 1,
    "temp_c": 5
  },
  {
    "slot": 2,
    "temp_c": null
  },
  {
    "slot": 3,
    "temp_c": 8
  },
  {
    "slot": 4,
    "temp_c": 9
  },
  {
    "slot": 5,
    "temp_c": 6
  }
]
```

축약 fixture는 센서 한 개와 기대 슬롯 0..5를 전제로 한다. values 변형에서는 기대 슬롯을 0..len(values)-1로 교체한다. 행 자체가 빠진 경우의 슬롯 생성·시각 파싱은 본 검사 범위 밖이며 운영 구현에 반드시 추가해야 한다.

## 기준 방법과 최소 구현
기대 슬롯과 실제 관측을 대조하고 null은 unknown, 8 초과는 alarm, 그 외 normal로 표시한다.

계절·운영조건 자료와 검증된 기준선이 있을 때만 관리도·변화 감지를 추가한다.

슬롯별 측정 → 결측/중복 검사 → 시계열과 사유 → 통신 점검 또는 온도 점검 작업 선택

목적함수 없음. 필수: 동일 단위·기대 시각·중복 처리. 선호: alarm 먼저 보여주되 unknown을 숨기지 않는다.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"normal": 4, "alarm": 1, "unknown": 1}` | 4,5,8,6 정상;9 경보;null 미확인. |
| 경계 | `{"values": [8]}` | `{"normal": 1, "alarm": 0, "unknown": 0}` | 8 초과 규칙이므로 8은 정상. |
| 정보 부족 | `{"values": [null]}` | `{"normal": 0, "alarm": 0, "unknown": 1}` | 누락을 0으로 채우지 않는다. |
| 충돌 | `{"conflict": true}` | `"invalid"` | 같은 slot에 4와 7은 출처 충돌. |
| 순서변경 | `{"reverse": true}` | `{"normal": 4, "alarm": 1, "unknown": 1}` | 시간 키로 대응하면 순서와 무관. |
| 새 표본 | `{"values": [8.1, 7.9, null]}` | `{"normal": 1, "alarm": 1, "unknown": 1}` | 소수 상한 반례. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 기대 슬롯 6개 중 유효 관측 5개로 완전성은 5/6=83.33%. alarm 비율은 관측 기준 1/5=20%, 전체 슬롯 기준 1/6과 구별한다.

서로 비슷하지만 달라야 하는 두 건: 8.0은 normal, 8.1은 alarm; null은 둘 중 하나가 아닌 unknown.

## 답변 변화와 범위 통제
- 5분 지연이 정상이라는 답변 → 관측 기준시각과 지연 허용을 명시하고 stale 판정 추가.
- 누락 구간이 정기 점검이라는 답변 → 예정 제외 슬롯을 별도 분모로 기록.

한계 초과는 원인 분석이 아니다. 지도나 이상탐지 모델이 결측 문제를 고치지는 않는다. 기준 미확정이면 관측/누락 표까지만 만든다.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- unknown 표시로 통신 담당자를 찾을 수 있는가?
- 경보 사유가 실제 점검 우선순위를 바꾸는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 관리한계와 규격을 혼동하지 않았다는 증거는 무엇인가?
- 5/6과 1/5의 분모를 왜 다르게 정의했는가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/statistics.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
