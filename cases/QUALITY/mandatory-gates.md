# 필수 승인 누락을 가격으로 상쇄하지 않는 후보 비교

```json
{
  "id": "mandatory-gates",
  "title": "필수 승인 누락을 가격으로 상쇄하지 않는 후보 비교",
  "family": "QUALITY",
  "keywords_ko": [
    "품질",
    "필수승인",
    "공급원"
  ],
  "keywords_en": [
    "quality gate",
    "eligibility"
  ],
  "problem_structure": "hard gates before ranking",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 전시물 포장재를 구매하는 담당자가 저렴한 대체재를 비교하되 시험 누락 제품이 최고점으로 선정되지 않게 해 달라고 한다.",
  "do_not_use_when": "공급 중단 위험이나 실제 품질 개선을 이5행으로 입증할 수 없다. ML 점수는 누락 시험을 대체하지 못한다. 시험 증거 부재 시 gate 화면까지만 제공.",
  "data_required": [
    "최소 필수: candidate_id, strength_pass, archival_pass(true/false/null), cost(동일 수량 비용). 한 행은 후보·시험버전 하나. null은 미시험. 보고서 id/시험일은 운영 시 필수 증거; 예제는 합성 값. 공급 리드타임은 있으면 개선, 브랜드명은 없어도 가능."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "equivalence-interval"
  ],
  "depth": "deep",
  "path": "cases/QUALITY/mandatory-gates.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "selected": "m1",
        "pass": 2,
        "fail": 1,
        "unknown": 2
      },
      "basis": "합격m1/m4 중12<15."
    },
    {
      "kind": "경계",
      "input": {
        "tie": true
      },
      "expected": {
        "selected": "m1",
        "pass": 2,
        "fail": 1,
        "unknown": 2
      },
      "basis": "동률은 id 사전순; 품질 우위라는 뜻 아님."
    },
    {
      "kind": "정보 부족",
      "input": {
        "all_unknown": true
      },
      "expected": {
        "selected": null,
        "pass": 0,
        "fail": 0,
        "unknown": 5
      },
      "basis": "검증 후보 없음."
    },
    {
      "kind": "충돌",
      "input": {
        "bad_cost": true
      },
      "expected": "invalid",
      "basis": "음수 비용 입력 거부."
    },
    {
      "kind": "순서변경",
      "input": {
        "reverse": true
      },
      "expected": {
        "selected": "m1",
        "pass": 2,
        "fail": 1,
        "unknown": 2
      },
      "basis": "입력순서는 선택을 바꾸지 않는다."
    },
    {
      "kind": "새 표본",
      "input": {
        "approve_m3": true
      },
      "expected": {
        "selected": "m3",
        "pass": 3,
        "fail": 1,
        "unknown": 1
      },
      "basis": "m3 시험 통과 확인 후6이 최소."
    }
  ],
  "fixture": [
    {
      "id": "m1",
      "strength": true,
      "archival": true,
      "cost": 12
    },
    {
      "id": "m2",
      "strength": false,
      "archival": true,
      "cost": 4
    },
    {
      "id": "m3",
      "strength": true,
      "archival": null,
      "cost": 6
    },
    {
      "id": "m4",
      "strength": true,
      "archival": true,
      "cost": 15
    },
    {
      "id": "m5",
      "strength": null,
      "archival": null,
      "cost": 3
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 전시물 포장재를 구매하는 담당자가 저렴한 대체재를 비교하되 시험 누락 제품이 최고점으로 선정되지 않게 해 달라고 한다.

- 가중 평균에서 저렴한 가격이 안전성 미달을 상쇄한다.
- 미시험을 불합격 또는 합격으로 임의 처리한다.
- 서로 다른 시험 버전의 결과를 같은 조건으로 비교한다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 통과해야 하는 필수 시험은 무엇인가? | 명시된 필수조건만 gate로 두고 임의 추가 금지. |
| 미시험 후보는 탈락인가 보류인가? | 본 예제 unknown으로 보류하고 검증된 후보만 가격 비교. |
| 비용은 같은 수량·배송 조건인가? | 다르면 동일 조건 환산 전 순위 보류. |

## 데이터 계약과 합성 입력
최소 필수: candidate_id, strength_pass, archival_pass(true/false/null), cost(동일 수량 비용). 한 행은 후보·시험버전 하나. null은 미시험. 보고서 id/시험일은 운영 시 필수 증거; 예제는 합성 값. 공급 리드타임은 있으면 개선, 브랜드명은 없어도 가능.

```json
[
  {
    "id": "m1",
    "strength": true,
    "archival": true,
    "cost": 12
  },
  {
    "id": "m2",
    "strength": false,
    "archival": true,
    "cost": 4
  },
  {
    "id": "m3",
    "strength": true,
    "archival": null,
    "cost": 6
  },
  {
    "id": "m4",
    "strength": true,
    "archival": true,
    "cost": 15
  },
  {
    "id": "m5",
    "strength": null,
    "archival": null,
    "cost": 3
  }
]
```

## 기준 방법과 최소 구현
필수조건 하나라도 False면 fail, False 없이 null이 있으면 unknown, 모두 True면 pass. pass 집합 안에서만 비용 최소 후보를 찾는다.

복수 합격 후보의 리드타임·위험을 추가 비교할 때도 필수 gate를 유지하고 가중치 민감도를 별도 제시한다.

후보 시험표 → gate+사유 → 합격 후보 가격 비교 → 담당자가 추가 시험 또는 구매 검토

목적: pass 후보 내 비용 최소. 필수: 두 시험 모두 True, 비교 조건 일치. 선호: 비용. 실패를 낮은 비용으로 상쇄 금지.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"selected": "m1", "pass": 2, "fail": 1, "unknown": 2}` | 합격m1/m4 중12<15. |
| 경계 | `{"tie": true}` | `{"selected": "m1", "pass": 2, "fail": 1, "unknown": 2}` | 동률은 id 사전순; 품질 우위라는 뜻 아님. |
| 정보 부족 | `{"all_unknown": true}` | `{"selected": null, "pass": 0, "fail": 0, "unknown": 5}` | 검증 후보 없음. |
| 충돌 | `{"bad_cost": true}` | `"invalid"` | 음수 비용 입력 거부. |
| 순서변경 | `{"reverse": true}` | `{"selected": "m1", "pass": 2, "fail": 1, "unknown": 2}` | 입력순서는 선택을 바꾸지 않는다. |
| 새 표본 | `{"approve_m3": true}` | `{"selected": "m3", "pass": 3, "fail": 1, "unknown": 1}` | m3 시험 통과 확인 후6이 최소. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 비용3인m5는 미시험,4인m2는 strength 실패,6인m3는 archival 미시험이므로12인m1 선택. 합격 후보만 남기는 필터가 점수보다 먼저이다.

서로 비슷하지만 달라야 하는 두 건: m3 archival=null이면 unknown, True로 검증되면 pass 및 최저가 후보.

## 답변 변화와 범위 통제
- archival이 선호 조건이라는 답변 → 필수/선호 정책을 재승인하고 결과 변화 표시.
- 시험 버전이 다르다는 답변 → 버전 동등성 확인까지 같은 순위에서 제외.

공급 중단 위험이나 실제 품질 개선을 이5행으로 입증할 수 없다. ML 점수는 누락 시험을 대체하지 못한다. 시험 증거 부재 시 gate 화면까지만 제공.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 보류 후보를 보고 어떤 시험을 요청할지 알 수 있는가?
- 가장 싼 후보가 선택되지 않은 이유를 납득할 수 있는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 가격과 필수조건의 우선순위를 테스트로 어떻게 고정했는가?
- 예제 pass가 실제 자재 승인과 다른 이유는 무엇인가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/stdtypes.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
