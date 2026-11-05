# Lot 크기를 반영한 불량률

```json
{
  "id": "lot-pooled-defects",
  "title": "Lot 크기를 반영한 불량률",
  "family": "QUALITY",
  "keywords_ko": [
    "Lot 크기를 반영한 불량률",
    "전체 검사 부담을 나타내는 개수 합산 비율을 계산한다"
  ],
  "keywords_en": [
    "lot-pooled-defects",
    "lot × inspected count × defect count"
  ],
  "problem_structure": "lot × inspected count × defect count",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 전시 패널 가공 업무에서 작은 lot와 큰 lot의 불량률을 단순 평균하여 전체 위험이 축소되었다.",
  "do_not_use_when": "lot 비율을 단순 평균하여 전체 불량률이라고 하지 않는다. 표본 기반 결과를 전수 사실로 확장하지 않는다. 정의가 미확정이면 lot별 표만 제공한다.",
  "data_required": [
    "필수 필드는 lot_id, inspected(정수 개수), defective(정수 개체수)다. 한 행은 한 lot이고 키는 고유하다. defective는 inspected 이하여야 한다. null은 집계 미완료, 검사수 0은 관측 없음이다. 비용은 개선용 자료다."
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
  "path": "cases/QUALITY/lot-pooled-defects.md",
  "decision_signature": {
    "decision": "전체 검사 부담을 나타내는 개수 합산 비율을 계산한다",
    "input_structure": "lot × inspected count × defect count",
    "hard_constraint": "검사 정의가 동일하고 총 검사수가 양수여야 한다",
    "validation": "비율의 단순 평균과 개수 합산 비율의 차이를 검출한다"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 전시 패널 가공 업무에서 작은 lot와 큰 lot의 불량률을 단순 평균하여 전체 위험이 축소되었다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- lot 크기가 다르다.
- 표본검사와 전수검사가 섞였다.
- 불량 건수와 불량 개체수가 다르다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 분모는 제품수인가 결함수인가? | 개체 불량률이면 중복 결함을 개체별로 통합한다. |
| 전체 부담인가 lot 평균 성능인가? | 전체 부담이면 개수를 합산한다. lot 동등 가중 평균은 다른 지표로 명명한다. |
| 검사 방식과 표본추출이 동일한가? | 다르면 합산 해석 전에 층을 분리한다. |

## 4. 데이터와 없을 때의 대안
필수 필드는 lot_id, inspected(정수 개수), defective(정수 개체수)다. 한 행은 한 lot이고 키는 고유하다. defective는 inspected 이하여야 한다. null은 집계 미완료, 검사수 0은 관측 없음이다. 비용은 개선용 자료다.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "lots": [
    {
      "id": "l1",
      "n": 10,
      "bad": 0
    },
    {
      "id": "l2",
      "n": 90,
      "bad": 18
    }
  ]
}
```

## 5. 기준 방법과 개선 조건
동일한 정의를 사용한 lot들의 불량 개체수 합을 검사 개체수 합으로 나눈다. 총 분모와 lot별 비율도 보여준다.

표본추출 확률이 다르면 단순 합산 대신 표본 설계 기반 추정을 검토한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 전체 검사 부담을 나타내는 개수 합산 비율을 계산한다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `0.18` | 18/100=.18;비율평균.10과다름. |
| 경계 | `{"lots": [{"id": "l1", "n": 10, "bad": 0}]}` | `0.0` | 확인된0불량. |
| 정보 부족 | `{"lots": [{"id": "l1", "n": null, "bad": 0}]}` | `"unknown"` | 검사분모없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
lot 비율을 단순 평균하여 전체 불량률이라고 하지 않는다. 표본 기반 결과를 전수 사실로 확장하지 않는다. 정의가 미확정이면 lot별 표만 제공한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 큰 lot가 결과에 미친 영향이 보이는가?
- 개체수와 결함수를 구분할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 18%와 10%가 갈리는 분모를 설명할 수 있는가?
- 이 자료로 전체 생산품의 불량률을 단정할 수 없는 이유는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/statistics.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
