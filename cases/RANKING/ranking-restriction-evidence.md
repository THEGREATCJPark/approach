# 제한 성분 근거가 있는 재료 후보 필터

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "ranking-restriction-evidence",
  "title": "제한 성분 근거가 있는 재료 후보 필터",
  "family": "RANKING",
  "keywords_ko": [
    "제한",
    "성분",
    "미확인",
    "금지"
  ],
  "keywords_en": [
    "three-state-restriction",
    "ranking-restriction-evidence"
  ],
  "problem_structure": "three-state-restriction",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "금지 성분의 포함 여부와 근거 완전성이 핵심이다.",
  "do_not_use_when": "실제 건강·안전 적합성을 이 합성 필터만으로 보증하지 않는다.",
  "data_required": [
    "재료 한 행: id 키, components 문자열 집합, complete 불리언. banned는 금지 성분 집합. 값은 성분 코드이며 제품명으로 추정하지 않는다. 결과 eligible/excluded/unknown 세 상태."
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
    "ranking-attribute-distance"
  ],
  "depth": "standard",
  "path": "cases/RANKING/ranking-restriction-evidence.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "성분 근거로 적합·제외·미확인을 분리한다",
    "input_structure": "금지 성분 집합과 후보 성분 목록·완전성",
    "hard_constraint": "불완전 목록은 적합 확정 금지",
    "validation": "금지 교집합 및 complete에 따른 세 상태"
  }
}
```

## 1. 창작 업무 요청

“공예 체험 재료에서 특정 성분을 피해야 하는 참여자에게 안내할 후보를 분리하고 싶다.”

## 2. 다른 원인과 목표

- 금지 성분의 포함 여부와 근거 완전성이 핵심이다.
- 성분 목록이 불완전하면 안전하다고 말할 수 없다.
- 제품군 이름을 성분 근거로 잘못 사용하고 있을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 피해야 할 성분 목록이 확정됐는가? → 미확정이면 개인 적합 판정을 보류한다.
2. 자료는 전체 성분인가 일부 표시인가? → 일부면 확인 필요로 분리한다.
3. 이 도구가 최종 안전 승인까지 하는가? → 아니면 확인된 필터 결과만 제공하고 권한자에게 넘긴다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

재료 한 행: id 키, components 문자열 집합, complete 불리언. banned는 금지 성분 집합. 값은 성분 코드이며 제품명으로 추정하지 않는다. 결과 eligible/excluded/unknown 세 상태.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "banned": [
    "X"
  ],
  "items": [
    [
      "A",
      [
        "Y"
      ],
      true
    ],
    [
      "B",
      [
        "X"
      ],
      true
    ],
    [
      "C",
      [
        "Y"
      ],
      false
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

금지 성분이 하나라도 확인되면 excluded; 없고 목록 complete=true면 eligible; 그 외 unknown. 설명할 수 없는 모델 점수는 쓰지 않는다. 개선은 출처 갱신과 검토 이력이다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

성분 표 → 세 상태와 교집합 근거 → 담당자가 적합 후보를 검토하거나 공급처 자료를 요청한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"banned":["X"],"items":[["A",["Y"],true],["B",["X"],true],["C",["Y"],false]]}` | `{"A": "eligible", "B": "excluded", "C": "unknown"}` | A 완전·교집합없음,B X포함,C 불완전. |
| boundary | `{"banned":["X"],"items":[["A",[],true]]}` | `{"A": "eligible"}` | 완전한 빈 목록은 미수집과 구별한다. 합성 계약상 성분0개다. |
| missing | `{"banned":null,"items":[["A",["Y"],true]]}` | `"unknown"` | 금지 기준 부재. |
| missing_components | `{"banned":["X"],"items":[["A",null,true]]}` | `{"A": "unknown"}` | 성분 목록 자체가 없으면 완전성 표시만으로 통과하지 않는다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 실제 건강·안전 적합성을 이 합성 필터만으로 보증하지 않는다.
- unknown을 eligible로 합치거나 원재료 별칭을 근거 없이 동일시하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 확인 필요 후보에 대해 어떤 추가 자료를 요청해야 하는지 알 수 있는가?
2. 제외 근거가 실제 성분 문서와 연결되는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 왜 불완전한 목록에서 교집합이 없다는 사실만으로 통과시키지 않았는가?
2. 판정 권한과 계산 범위는 어디까지인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
