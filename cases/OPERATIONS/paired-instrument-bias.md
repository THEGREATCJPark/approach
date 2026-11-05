# 동일 시료를 이용한 장비 간 편향

```json
{
  "id": "paired-instrument-bias",
  "title": "동일 시료를 이용한 장비 간 편향",
  "family": "OPERATIONS",
  "keywords_ko": [
    "동일 시료를 이용한 장비 간 편향",
    "두 장비 간 차이가 허용 평균편향 범위인지 확인"
  ],
  "keywords_en": [
    "paired-instrument-bias",
    "specimen id × instrument A/B pair"
  ],
  "problem_structure": "specimen id × instrument A/B pair",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 재사용 자재 검사실이 측정기 두 대의 평균값이 다르지만 어느 날 다른 시료를 측정했는지 확인하려 한다.",
  "do_not_use_when": "편향 평균0이 두 장비의 완전한 일치를 의미하지 않는다. t검정 비유의로 교체 승인하지 않는다. 동일시료 키가 없으면 대응 비교 중단.",
  "data_required": [
    "필수 specimen_id, a,b 수치(mm), tolerance 평균편향 허용(mm). 한 행은 같은 시료의 대응 측정. id 고유; null은 미측정. 교정·시각은 실제 장비 승인에 추가로 필요."
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
  "path": "cases/OPERATIONS/paired-instrument-bias.md",
  "decision_signature": {
    "decision": "두 장비 간 차이가 허용 평균편향 범위인지 확인",
    "input_structure": "specimen id × instrument A/B pair",
    "hard_constraint": "서로 다른 시료를 단순 평균 비교하지 않음",
    "validation": "쌍별 차이 평균과 최대 차이를 분리"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 재사용 자재 검사실이 측정기 두 대의 평균값이 다르지만 어느 날 다른 시료를 측정했는지 확인하려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 장비 편향이 존재한다.
- 측정한 시료 구성이 다르다.
- 시간 경과로 시료 자체가 달라졌다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 동일 시료를 두 장비에서 측정했는가? | 아니면 대응 비교 보류 및 시료 구성 확인. |
| 평균편향과 개별차 중 어느 기준이 필요한가? | 개별차 한계라면 평균 통과로 대체하지 않음. |
| 측정 순서·시간은 고정되어 있는가? | 순서효과 가능하면 교차 측정 설계 필요. |

## 4. 데이터와 없을 때의 대안
필수 specimen_id, a,b 수치(mm), tolerance 평균편향 허용(mm). 한 행은 같은 시료의 대응 측정. id 고유; null은 미측정. 교정·시각은 실제 장비 승인에 추가로 필요.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "rows": [
    {
      "id": "s1",
      "a": 10,
      "b": 12
    },
    {
      "id": "s2",
      "a": 20,
      "b": 21
    },
    {
      "id": "s3",
      "a": 30,
      "b": 33
    }
  ],
  "tolerance": 1.5
}
```

## 5. 기준 방법과 개선 조건
시료별 B−A를 구해 평균편향과 최대절대차를 함께 출력한다. 허용범위 판정은 평균에만 붙이고 개별차 합격으로 확대하지 않는다.

반복 측정과 설계가 갖춰지면 일치도 구간·측정시스템 분석을 검토한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 두 장비 간 차이가 허용 평균편향 범위인지 확인 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"mean_bias": 2.0, "max_abs_difference": 3, "status": "outside"}` | 차이2,1,3 평균2>1.5. |
| 경계 | `{"tolerance": 2}` | `{"mean_bias": 2.0, "max_abs_difference": 3, "status": "within"}` | 평균 기준 경계 포함;최대3은 별도. |
| 정보 부족 | `{"rows": [{"id": "s1", "a": 10, "b": null}]}` | `"unknown"` | 대응 측정 없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
편향 평균0이 두 장비의 완전한 일치를 의미하지 않는다. t검정 비유의로 교체 승인하지 않는다. 동일시료 키가 없으면 대응 비교 중단.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 평균 통과인데 개별차가 큰 경우 추가 점검을 선택할 수 있는가?
- 시료 연결이 잘못된 행을 찾아 수정할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 장비 간 비교와 기존 구성효과 비교 사례의 차이는 무엇인가?
- 평균2와최대3이 각각 무엇을 보장하지 않는가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/statistics.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
