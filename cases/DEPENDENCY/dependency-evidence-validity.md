# 동일 관계의 상충 출처와 유효 근거 판정

> 독립 창작 사례. 실제 관계·계약·출처를 재현하지 않는다. supported는 현재 확인한 지지 근거가 있다는 뜻이며 관계의 진실성 보증이 아니다.

```json
{
  "id": "dependency-evidence-validity",
  "title": "동일 관계의 상충 출처와 유효 근거 판정",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "출처",
    "상충",
    "관계",
    "근거"
  ],
  "keywords_en": [
    "relation-evidence-conflict"
  ],
  "problem_structure": "relation-evidence-conflict",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "동일한 방향·종류의 관계에 찬성·반대 근거가 함께 존재한다.",
  "do_not_use_when": "출처 권한이나 계약 원문 검토 없이 다수결로 관계의 진실성을 확정하지 않는다.",
  "data_required": [
    "한 행은 관계 한 건에 대한 근거: id 키, relation=[source,target,type], position=support/refute, from_day/to_day 정수 일, source 문서 식별자. 조회 관계와 기준일이 일치하는 [from_day,to_day) 유효 근거만 비교한다. source=null은 근거 연결 미확인."
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
  "path": "cases/DEPENDENCY/dependency-evidence-validity.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_c.json",
  "decision_signature": {
    "decision": "동일 관계의 상충 근거를 확인하고 재검토 대상을 정한다",
    "input_structure": "관계 방향·종류와 복수 출처의 support/refute·기간",
    "hard_constraint": "현재 유효한 근거만 비교; 상충을 다수결로 지우지 않음",
    "validation": "만료 반박 제외·현재 반박 충돌·출처 누락 미확인"
  }
}
```

## 1. 창작 업무 요청

“수리 키트의 공급 관계를 두 자료가 서로 다르게 설명한다. 지금 어떤 관계를 믿고 계획해야 하는지 검토 목록이 필요하다.”

## 2. 다른 원인과 목표

- 오래된 반박 자료가 현재 근거와 섞였을 수 있다.
- 같은 시점의 실제 상충이 있어 권한자 검토가 필요할 수 있다.
- 방향 또는 관계 종류가 다른 두 문장을 같은 관계로 묶었을 수 있다.

## 3. 먼저 확인할 질문과 분기

1. 두 자료가 같은 source→target 및 관계 종류를 말하는가? → 다르면 별도 관계로 분리한다.
2. 근거의 적용 기간과 조회 기준일이 확인됐는가? → 미확인이면 결론을 보류한다.
3. 상충 시 우선하는 권한 있는 자료가 있는가? → 우선 규칙이 확인되면 기록해 적용하고, 없으면 다수결로 결정하지 않는다.

## 4. 데이터 계약

한 행은 관계 한 건에 대한 근거: id 키, relation=[source,target,type], position=support/refute, from_day/to_day 정수 일, source 문서 식별자. 조회 관계와 기준일이 일치하는 [from_day,to_day) 유효 근거만 비교한다. source=null은 근거 연결 미확인.

최소 필수는 관계 키·입장·기간·출처다. 권한·개정 이력은 개선 자료이며 개인 식별 정보는 필요 없다. 자료가 없으면 합성 입력만 계산하고 실제 관계 판정을 보류한다.

```json
{
  "relation": [
    "P",
    "K",
    "supply"
  ],
  "day": 12,
  "evidence": [
    {
      "id": "e1",
      "relation": [
        "P",
        "K",
        "supply"
      ],
      "position": "support",
      "from_day": 10,
      "to_day": 15,
      "source": "note-a"
    },
    {
      "id": "e2",
      "relation": [
        "P",
        "K",
        "supply"
      ],
      "position": "refute",
      "from_day": 0,
      "to_day": 12,
      "source": "note-b"
    }
  ]
}
```

## 5. 기준 방법과 개선 조건

정확히 같은 관계 키의 근거를 모아 유효 기간을 검사한다. 유효한 지지와 반박이 모두 있으면 conflict, 지지만 있으면 supported, 반박만 있으면 refuted, 유효 근거가 없거나 필수 출처가 누락되면 unknown이다. 출처가 있다는 사실은 그 내용이 참이라는 증거를 대신하지 않는다.

[Python 표준 라이브러리](../../tools/python-stdlib.md)의 목록·집합 비교면 충분하다. 실행 불가 시 관계별 출처 표로 대조한다. 외부 모델 호출 없이 시작하며 개선은 권한 있는 버전의 수동 검토와 결정 이력이다.

## 6. 최소 구현과 다음 행동

관계와 기준일 → 현재 지지·반박 출처 ID 및 만료 사유 → 상태별 검토 목록 → 담당자가 상충 자료의 권한자에게 확인한다. conflict 상태에서 자동으로 운영 변경을 실행하지 않는다.

## 7. 정상·경계·정보 부족 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산 근거 |
|---|---|---|---|
| normal | `{"relation":["P","K","supply"],"day":12,"evidence":[{"id":"e1","relation":["P","K","supply"],"position":"support","from_day":10,"to_day":15,"source":"note-a"},{"id":"e2","relation":["P","K","supply"],"position":"refute","from_day":0,"to_day":12,"source":"note-b"}]}` | `{"status": "supported", "support": ["e1"], "refute": []}` | e1 유효. e2는 종료일12 미포함으로 만료. 현재 지지 근거만 남는다. |
| boundary | `{"relation":["P","K","supply"],"day":12,"evidence":[{"id":"e1","relation":["P","K","supply"],"position":"support","from_day":10,"to_day":15,"source":"note-a"},{"id":"e2","relation":["P","K","supply"],"position":"refute","from_day":12,"to_day":20,"source":"note-b"}]}` | `{"status": "conflict", "support": ["e1"], "refute": ["e2"]}` | e2 시작일12 포함. 같은 관계에 지지·반박이 동시에 유효하므로 충돌. |
| missing | `{"relation":["P","K","supply"],"day":12,"evidence":[{"id":"e1","relation":["P","K","supply"],"position":"support","from_day":10,"to_day":15,"source":null}]}` | `{"status": "unknown", "support": [], "refute": []}` | 원 출처에 연결되지 않은 근거로 관계를 확정하지 않는다. |

[실행 오라클](../../examples/synthetic/check_expansion_c.py)로 기대 상태와 출처 ID를 검증한다. 이는 자료 내용의 진실성이나 완성 앱 검증이 아니다.

## 8. 잘못된 적용과 범위 축소

- 지지 출처가 많다는 이유로 반박 한 건을 지우지 않는다.
- 같은 키라도 적용 시점이 다른 근거를 현재 충돌이라고 단정하지 않는다.
- 시간이 부족하면 자동 문장 해석을 빼고 사람이 확인한 관계 키·입장·기간을 받아 대조한다.

## 9. 구현물에 대한 사용자 피드백

1. 어떤 출처가 실제로 충돌하는지 찾아 권한자에게 보낼 확인 질문을 정할 수 있는가?
2. 만료로 제외된 근거와 출처 누락으로 보류된 근거가 구별되는가?

관계 한 건을 직접 검토하게 하고 확인 완료 시간·잘못 인용한 출처 수를 관찰한다. 실제 업무 효과는 합성 계산만으로 주장하지 않는다.

## 10. 개발자 설명 연습과 공개 근거

PREP 전용이다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

1. supported를 확정 사실이라고 부르지 않은 이유는 무엇인가?
2. 상충 근거를 조용히 합치지 않고 상태로 남긴 설계의 증거는 무엇인가?

[공식 일반 기술 참고](https://docs.python.org/3/library/collections.html). 집합과 목록의 일반 계산 구조를 참고했으며 관계·출처·기간은 창작이다. [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md).
