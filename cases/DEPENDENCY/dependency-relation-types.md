# 관계 종류를 구분한 직접 영향 조회

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "dependency-relation-types",
  "title": "관계 종류를 구분한 직접 영향 조회",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "관계종류",
    "공급",
    "기술",
    "직접영향"
  ],
  "keywords_en": [
    "typed-graph-query",
    "dependency-relation-types"
  ],
  "problem_structure": "typed-graph-query",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "종류가 다른 간선을 필터링해야 한다.",
  "do_not_use_when": "모든 관계를 공급 의존으로 바꾸지 않는다.",
  "data_required": [
    "간선 한 행은 [source,target,type]. type는 supply/technology/shared 중 하나이며 관계 키는 (source,target,type)이다. query는 source와 type이다. null type은 분류 미확인이다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "dependency-removal-bottleneck",
    "dependency-alternative-supply"
  ],
  "depth": "standard",
  "path": "cases/DEPENDENCY/dependency-relation-types.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "관계 종류와 방향에 맞는 직접 이웃을 조회한다",
    "input_structure": "source-target-type 삼중 관계",
    "hard_constraint": "간접 탐색 제외; 미확인 type 보류",
    "validation": "supply/technology와 역방향 구분"
  }
}
```

## 1. 창작 업무 요청

“부품 관계표에 공급·기술참고·공동사용이 섞여 있어 공급 중단 후보 조회가 과도하게 넓어진다.”

## 2. 다른 원인과 목표

- 종류가 다른 간선을 필터링해야 한다.
- 관계 방향이 혼재되어 있을 수 있다.
- 간접 영향이 아닌 직접 공급 대상만 필요할 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 찾는 관계는 공급인가 기술 참고인가? → 해당 타입만 조회한다.
2. 직접 대상만 필요한가? → 간접이면 별도 탐색을 명시한다.
3. source는 공급자 방향이 맞는가? → 데이터 사전과 샘플을 대조한다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

간선 한 행은 [source,target,type]. type는 supply/technology/shared 중 하나이며 관계 키는 (source,target,type)이다. query는 source와 type이다. null type은 분류 미확인이다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "source": "P",
  "type": "supply",
  "edges": [
    [
      "P",
      "A",
      "supply"
    ],
    [
      "P",
      "B",
      "technology"
    ],
    [
      "C",
      "P",
      "supply"
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

방향과 종류를 동시에 조건으로 직접 이웃 집합을 구한다. 타입 미확인 관계는 조용히 제외하지 말고 검토 필요로 결과를 보류한다. 개선은 타입별 다중 단계 경로 규칙이다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

관계표 → 종류별 직접 이웃 → 담당자가 공급 관계 검토 목록을 선택한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"source":"P","type":"supply","edges":[["P","A","supply"],["P","B","technology"],["C","P","supply"]]}` | `["A"]` | P에서 나가는 supply 대상은 A뿐이다. |
| boundary | `{"source":"P","type":"supply","edges":[["P","A","technology"]]}` | `[]` | 알려진 관계 중 해당 종류는 0개다. |
| missing | `{"source":"P","type":"supply","edges":[["P","A",null]]}` | `"unknown"` | P의 관계 종류가 미확인이다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 모든 관계를 공급 의존으로 바꾸지 않는다.
- 직접 이웃 수를 경제적 손실로 해석하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 관계 종류 필터를 바꾸면 원하는 대상이 달라지는가?
2. 방향과 종류를 보고 원자료 오류를 찾을 수 있는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 같은 노드 쌍의 다른 관계를 왜 보존했는가?
2. 빈 결과와 미확인을 어떻게 구분했는가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
