# 중간 노드 제거로 드러나는 연결 병목

> 독립 창작 연습. 실제 사람·조직·과제를 변형한 것이 아니다. 작은 합성 수치의 기대값은 별도 오라클 계산으로 검증한다.

```json
{
  "id": "dependency-removal-bottleneck",
  "title": "중간 노드 제거로 드러나는 연결 병목",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "병목",
    "제거",
    "단절",
    "대체경로"
  ],
  "keywords_en": [
    "node-removal-connectivity",
    "dependency-removal-bottleneck"
  ],
  "problem_structure": "node-removal-connectivity",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "대체 경로가 없는 연결 병목을 찾는다.",
  "do_not_use_when": "연결 단절 후보를 처리량 최대화의 병목이라고 단정하지 않는다.",
  "data_required": [
    "edges는 방향 쌍 배열, source/target은 문자열, remove는 제거 노드, complete는 불리언이다. 간선은 연결 가능성을 뜻하고 용량 정보는 없다."
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
    "dependency-alternative-supply"
  ],
  "depth": "standard",
  "path": "cases/DEPENDENCY/dependency-removal-bottleneck.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "한 중간 노드 제거가 연결을 끊는지 확인한다",
    "input_structure": "방향 그래프·출발·목표·제거 노드",
    "hard_constraint": "제거 전 연결 존재; 관계 완전성",
    "validation": "대체 경로 유무에 따른 전후 도달 비교"
  }
}
```

## 1. 창작 업무 요청

“유통 준비망에서 어느 중간 단계가 사라질 때 최종 수령점과의 연결이 끊기는지 보고 싶다.”

## 2. 다른 원인과 목표

- 대체 경로가 없는 연결 병목을 찾는다.
- 처리 용량 병목과 연결 단절 병목은 다르다.
- 관계가 완전하지 않으면 대체 경로가 없다고 확정할 수 없다.

## 3. 먼저 확인할 질문과 분기

1. 병목은 속도 부족인가 연결 단절인가? → 전자면 용량·수요 자료가 필요하다.
2. 시작점과 보호해야 할 목표점은 무엇인가? → 고정 후 제거 실험을 한다.
3. 관계 목록이 완전한가? → 미확인이면 잠정 후보로 남긴다.

자료에서 이미 확인되는 답은 다시 묻지 않는다. 정책 답변이 충돌하면 기준 시점과 결정 권한을 확인하고 기존 가정을 기록한다.

## 4. 데이터 계약

edges는 방향 쌍 배열, source/target은 문자열, remove는 제거 노드, complete는 불리언이다. 간선은 연결 가능성을 뜻하고 용량 정보는 없다.

위 필드는 최소 필수다. 운영 중 오류·수동 수정 기록은 개선에 유용하고 전체 개인 이력은 첫 실험에 필요하지 않다. 필수 값이 null이면 미확인으로 처리하며 0이나 false로 바꾸지 않는다. 자료를 받을 수 없으면 아래 합성 입력으로 계산만 확인하고 실제 판정은 보류한다.

```json
{
  "edges": [
    [
      "S",
      "A"
    ],
    [
      "A",
      "T"
    ]
  ],
  "source": "S",
  "target": "T",
  "remove": "A",
  "complete": true
}
```

## 5. 기준 방법과 개선 조건

제거 전 도달 가능성을 확인하고 remove의 진출입 간선을 뺀 뒤 다시 탐색한다. 원래 연결이 없으면 새 병목으로 세지 않는다. 개선은 복수 제거 cut 분석이다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 없이 작은 목록·집합·정수 연산으로 시작한다. 실행이 허용되지 않거나 Python이 없으면 후보 표와 손계산을 남긴다. 외부 API·자격증명은 필요 없다. 복잡한 패키지는 데이터 크기와 실패 사례가 기준 방법의 한계를 보여준 뒤 검토한다.

## 6. 최소 구현과 다음 행동

관계표·제거 대상 → 전후 연결 비교 → 담당자가 대체 경로 확보를 검토한다.

완료 기준은 실제 입력 한 건에서 판정·근거·미확인 사유·다음 행동이 이어지는 것이다. 합성 테스트 통과는 실제 사용자 만족이나 업무 효과를 입증하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"edges":[["S","A"],["A","T"]],"source":"S","target":"T","remove":"A","complete":true}` | `true` | 제거 전 S-A-T, 제거 후 경로 없음. |
| boundary | `{"edges":[["S","A"],["A","T"],["S","T"]],"source":"S","target":"T","remove":"A","complete":true}` | `false` | 직접 S-T 대체 경로 유지. |
| missing | `{"edges":[["S","A"],["A","T"]],"source":"S","target":"T","remove":"A","complete":null}` | `"unknown"` | 관계 완전성이 미확인이다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)은 각 기대값을 다시 계산한다. 이는 문서 기대값 검증이며 완성 앱·동시 사용자·현장 운영 테스트가 아니다.

## 8. 잘못된 적용과 범위 축소

- 연결 단절 후보를 처리량 최대화의 병목이라고 단정하지 않는다.
- 단일 제거 검사로 복합 고장 안전성을 보장하지 않는다.

시간이 부족하면 장식·선택 기능을 줄이고 입력 계약, 미확인 처리, 위 기대값 검증을 유지한다. 효과는 동일 업무의 전후 완료 시간·오류 수와 측정 대상 수를 확보한 뒤 판단한다.

## 9. 구현물에 대한 사용자 피드백

1. 대체 경로를 보며 어떤 단계에 우회 절차가 필요한지 결정할 수 있는가?
2. 원래 연결이 없던 대상을 새 장애로 오해하지 않는가?

설명 전에 사용자가 한 건을 처리하게 하고 실패·우회·추가 질문을 관찰한다. 새 요구를 오류 수정·필수 누락·선택 개선으로 분류한다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 질문에는 본인이 먼저 답하고 코드·결정 로그·검증 출력으로 근거를 제시한다.

1. 제거 전 검사가 필요한 이유는 무엇인가?
2. 그래프 완전성의 한계가 결론에 어떤 영향을 주는가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 공개 문서의 계산 구조를 참고했으며 업무 정책·수치는 독립 창작이다. [기준 방법](../../methods/baseline-first.md)과 [독립 검증](../../methods/verification.md)을 함께 읽는다.
