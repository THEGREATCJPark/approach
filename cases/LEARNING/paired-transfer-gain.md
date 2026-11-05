# 적용 과제 전후의 동일 참가자 변화

```json
{
  "id": "paired-transfer-gain",
  "title": "적용 과제 전후의 동일 참가자 변화",
  "family": "LEARNING",
  "keywords_ko": [
    "적용 과제 전후의 동일 참가자 변화",
    "전후 차이가 있는 참가자 집합과 관측 변화 계산"
  ],
  "keywords_en": [
    "paired-transfer-gain",
    "participant id × before/after score"
  ],
  "problem_structure": "participant id × before/after score",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 지역 공예 교육팀이 수업 후 응용 과제 점수가 올랐는지 확인하려는데 전후 응시자가 다르다.",
  "do_not_use_when": "수업 때문에3점 올랐다고 단정하지 않는다. 다른 만점 또는 난도를 정규화 없이 빼지 않는다. 자료 부족이면 응시 커버리지만 보고.",
  "data_required": [
    "필수 participant_id 문자열, before/after 수치 또는 null, max_score. 한 행은 익명 참가자 한 명. id 고유, null은 미응시. 두 시점 같은 척도 가정. 원본 이름은 필요 없음; 참여 조건은 해석 개선."
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
  "path": "cases/LEARNING/paired-transfer-gain.md",
  "decision_signature": {
    "decision": "전후 차이가 있는 참가자 집합과 관측 변화 계산",
    "input_structure": "participant id × before/after score",
    "hard_constraint": "미응시를0점으로 대체하지 않음",
    "validation": "대응쌍 평균과 누락자 수를 함께 보고"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 지역 공예 교육팀이 수업 후 응용 과제 점수가 올랐는지 확인하려는데 전후 응시자가 다르다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 높은 점수 참가자만 사후 응시했다.
- 전후 과제 난도가 다르다.
- 미응시를0점으로 넣어 효과가 부풀려진다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 같은 참가자의 전후 기록을 연결할 수 있는가? | 가능하면 대응 비교, 불가하면 집단 구성이 다른 한계를 명시. |
| 두 과제의 난도와 만점이 같은가? | 아니면 원점수 차이 해석 보류. |
| 사후 미응시 이유가 성과와 관련되는가? | 가능성이 있으면 탈락 편향을 기록하고 인과효과 주장 제한. |

## 4. 데이터와 없을 때의 대안
필수 participant_id 문자열, before/after 수치 또는 null, max_score. 한 행은 익명 참가자 한 명. id 고유, null은 미응시. 두 시점 같은 척도 가정. 원본 이름은 필요 없음; 참여 조건은 해석 개선.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "max_score": 10,
  "rows": [
    {
      "id": "u1",
      "before": 3,
      "after": 5
    },
    {
      "id": "u2",
      "before": 4,
      "after": 8
    },
    {
      "id": "u3",
      "before": 5,
      "after": null
    }
  ]
}
```

## 5. 기준 방법과 개선 조건
양쪽 점수 존재하는 참가자만 차이를 계산하고 대응쌍 수·누락 수·평균 차이를 함께 출력한다. 점수 범위 위반은 invalid.

비교 집단·사전 설계·충분한 표본이 있으면 효과 추정과 불확실성 분석을 검토한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 전후 차이가 있는 참가자 집합과 관측 변화 계산 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"paired": 2, "missing": 1, "mean_change": 3.0}` | 변화2와4의 평균3;u3 제외 사유 기록. |
| 경계 | `{"rows": [{"id": "u1", "before": 5, "after": 5}]}` | `{"paired": 1, "missing": 0, "mean_change": 0.0}` | 변화0은 관측된 결과. |
| 정보 부족 | `{"rows": [{"id": "u1", "before": 5, "after": null}]}` | `"unknown"` | 대응쌍 없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
수업 때문에3점 올랐다고 단정하지 않는다. 다른 만점 또는 난도를 정규화 없이 빼지 않는다. 자료 부족이면 응시 커버리지만 보고.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 누락된 참가자가 결과 해석에서 보이는가?
- 이 결과로 어떤 수업 부분을 추가 관찰할 것인가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 대응쌍 선정 기준과 누락 영향을 재현할 수 있는가?
- 관측 변화와 인과효과를 어떻게 구분했는가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/statistics.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
