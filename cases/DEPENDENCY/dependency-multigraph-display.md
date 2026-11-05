# 복수 관계를 잃지 않는 그래프 표시 집계

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "dependency-multigraph-display",
  "title": "복수 관계를 잃지 않는 그래프 표시 집계",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "시각화",
    "복수관계",
    "집계",
    "간선"
  ],
  "keywords_en": [
    "multigraph-projection",
    "dependency-multigraph-display"
  ],
  "problem_structure": "multigraph-projection",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "시각적 간선 수와 원 관계 건수를 분리해야 한다.",
  "do_not_use_when": "시각적 중앙성·선 굵기를 매출 영향이나 인과 관계로 설명하지 않는다.",
  "data_required": [
    "간선 한 행은 [edge_id,source,target,type]다. edge_id는 기본 키, source-target는 방향 쌍이다. 서로 다른 id는 관계 타입이 같아도 별도 근거일 수 있다. 화면은 방향 쌍별 건수와 type 집합을 표시한다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "dependency-relation-types",
    "dependency-removal-bottleneck"
  ],
  "depth": "standard",
  "path": "cases/DEPENDENCY/dependency-multigraph-display.md",
  "test_count": 4,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "시각적 간선 집계에서 원 관계를 보존한다",
    "input_structure": "edge_id와 방향쌍·관계 타입",
    "hard_constraint": "방향쌍 집계하되 원 관계 수 보존",
    "validation": "노드·표시선·관계 수가 다른 예제"
  }
}
```

## 1. 창작 업무 요청

“관계도를 단순화하면서 같은 두 노드 사이의 서로 다른 계약 관계가 하나로 사라진다.”

## 2. 다른 원인과 목표

- 시각적 간선 수와 원 관계 건수를 분리해야 한다.
- 중복 행과 의미가 다른 평행 간선을 혼동한다.
- 그림의 굵기를 영향 규모처럼 읽을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 간선 한 행이 관계 종류인가 계약 한 건인가? → 관계 키 정의에 맞춰 중복을 판정한다.
2. 화면에서 묶어도 세부 관계 열람이 필요한가? → 원 행 연결을 보존한다.
3. 굵기는 관계 건수인가 영향량인가? → 건수라면 범례에 명시하고 금액 추정을 하지 않는다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

간선 한 행은 [edge_id,source,target,type]다. edge_id는 기본 키, source-target는 방향 쌍이다. 서로 다른 id는 관계 타입이 같아도 별도 근거일 수 있다. 화면은 방향 쌍별 건수와 type 집합을 표시한다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "edges": [
    [
      "e1",
      "A",
      "B",
      "supply"
    ],
    [
      "e2",
      "A",
      "B",
      "technology"
    ],
    [
      "e3",
      "B",
      "A",
      "return"
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건

edge_id 중복 검사 후 방향 쌍별로 묶고 원 id 목록을 보존한다. 노드 수·방향 쌍 수·원 간선 수를 별도로 낸다. 배치 알고리즘은 데이터 의미를 수정하지 않는다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

간선표 → 묶음선과 세부 관계표 → 담당자가 어느 관계 근거를 확인할지 선택한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"edges":[["e1","A","B","supply"],["e2","A","B","technology"],["e3","B","A","return"]]}` | `{"nodes": 2, "visual_edges": 2, "relations": 3}` | A→B 두 관계가 선 하나로 표시되고 B→A는 별도 선이다. |
| boundary | `{"edges":[]}` | `{"nodes": 0, "visual_edges": 0, "relations": 0}` | 빈 관계 집합이며 노드 목록도 별도로 제공되지 않았다. |
| missing | `{"edges":[["e1","A",null,"supply"]]}` | `"unknown"` | 대상 노드가 미확인이다. |
| duplicate_edge_id | `{"edges":[["e1","A","B","supply"],["e1","A","B","supply"]]}` | `"duplicate_id"` | 같은 기본 키를 두 관계로 세지 않는다. 정본 선택 전 입력을 수정한다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 시각적 중앙성·선 굵기를 매출 영향이나 인과 관계로 설명하지 않는다.
- 방향을 없애거나 평행 관계 근거를 삭제하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 묶인 선을 열어 원래 관계를 확인할 수 있는가?
2. 선 굵기를 영향량으로 오해하지 않도록 범례가 충분한가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 표시용 집계와 원 데이터를 분리한 이유는 무엇인가?
2. 어떤 시각화 오류가 실제 판단 오류로 이어질 수 있는가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
