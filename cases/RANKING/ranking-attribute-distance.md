# 작업 조건과 가까운 공구 후보 순위

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "ranking-attribute-distance",
  "title": "작업 조건과 가까운 공구 후보 순위",
  "family": "RANKING",
  "keywords_ko": [
    "속성",
    "거리",
    "가중치",
    "공구"
  ],
  "keywords_en": [
    "weighted-distance-ranking",
    "ranking-attribute-distance"
  ],
  "problem_structure": "weighted-distance-ranking",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "두 수치 속성의 단위를 통일한 거리 비교가 필요하다.",
  "do_not_use_when": "필수 안전 규격 위반을 작은 거리로 보상하지 않는다.",
  "data_required": [
    "후보 한 행: id 키, weight_kg 소수, width_mm 정수. target는 두 목표값, scales는 양수 차이 단위(kg,mm). 거리=중량차/scales[0]+폭차/scales[1]."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "ranking-cold-start",
    "ranking-restriction-evidence"
  ],
  "depth": "standard",
  "path": "cases/RANKING/ranking-attribute-distance.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "목표 수치 속성에 가까운 공구를 고른다",
    "input_structure": "후보의 kg·mm 속성과 목표·정규화 단위",
    "hard_constraint": "필수 규격은 별도 필터; 양수 정규화 단위",
    "validation": "단위 정규화 거리와 정확 일치0"
  }
}
```

## 1. 창작 업무 요청

“대여 공구 중 원하는 중량과 작업 폭에 가까운 후보를 찾고 싶다.”

## 2. 다른 원인과 목표

- 두 수치 속성의 단위를 통일한 거리 비교가 필요하다.
- 안전 필수조건을 거리 점수와 혼동할 수 있다.
- 가중치가 사용자 선호를 반영하지 않을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 허용 불가 규격이 있는가? → 있으면 순위 전에 필터한다.
2. 중량1kg 차이와 폭10mm 차이를 동등하게 볼 것인가? → 아니라면 정규화 단위나 가중치를 바꾼다.
3. 정확 일치가 없으면 차선 후보를 보여줄 것인가? → 아니면 허용 오차 밖 후보를 비적합으로 남긴다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

후보 한 행: id 키, weight_kg 소수, width_mm 정수. target는 두 목표값, scales는 양수 차이 단위(kg,mm). 거리=중량차/scales[0]+폭차/scales[1].

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "target": [
    2,
    30
  ],
  "scales": [
    1,
    10
  ],
  "items": [
    [
      "A",
      3,
      30
    ],
    [
      "B",
      2,
      50
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

각 절대 차이를 합의된 단위로 나눠 합하고 오름차순 정렬한다. 점수는 낮을수록 가깝다. 안전성과 품질 승인 여부는 별도 필터이며 거리로 상쇄하지 않는다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

조건 입력 → 후보별 속성 차이와 합산 거리 → 가까운 후보 선택 → 담당자가 실물 적합성을 확인한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"target":[2,30],"scales":[1,10],"items":[["A",3,30],["B",2,50]]}` | `["A", "B"]` | A=1+0=1,B=0+2=2. |
| boundary | `{"target":[2,30],"scales":[1,10],"items":[["A",2,30]]}` | `["A"]` | 정확 일치 거리0. |
| missing | `{"target":[2,null],"scales":[1,10],"items":[["A",2,30]]}` | `"unknown"` | 목표 폭이 없으면 거리 정의가 미완성이다. |
| missing_item_attribute | `{"target":[2,30],"scales":[1,10],"items":[["A",null,30]]}` | `"unknown"` | 후보의 필수 중량 미확인은 계산 보류다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 필수 안전 규격 위반을 작은 거리로 보상하지 않는다.
- kg와mm 차이를 정규화 없이 더하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 속성 차이를 보고 어떤 후보를 제외할지 결정할 수 있는가?
2. 가중치가 달라져 순위가 바뀌는 경우 실제 판단과 맞는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 정규화 단위는 어떤 담당자 답변으로 정했는가?
2. 선호 점수와 필수 제약을 어떤 코드 경계로 분리했는가?

[공식 일반 기술 참고](https://docs.python.org/3/howto/sorting.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
