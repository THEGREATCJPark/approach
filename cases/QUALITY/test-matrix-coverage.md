# 조건별 시험 누락을 찾는 커버리지 표

```json
{
  "id": "test-matrix-coverage",
  "title": "조건별 시험 누락을 찾는 커버리지 표",
  "family": "QUALITY",
  "keywords_ko": [
    "조건별 시험 누락을 찾는 커버리지 표",
    "승인 검토 전에 필수 시험 조합의 누락을 식별한다"
  ],
  "keywords_en": [
    "test-matrix-coverage",
    "required test×condition pairs vs executed pairs"
  ],
  "problem_structure": "required test×condition pairs vs executed pairs",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 조명 부품 검토 담당자가 시험성적서는 많지만 저온 조건 시험이 빠졌는지 빠르게 확인하고 싶다.",
  "do_not_use_when": "파일 개수를 필수 시험 완료수로 쓰지 않는다. 커버리지 100%를 품질 합격으로 표현하지 않는다. 버전이 없으면 원자료 정리만 한다.",
  "data_required": [
    "필수 필드는 required 배열([test_id, condition_id]), executed(동일 형식), requirement_version이다. 한 행은 시험과 조건의 쌍이며 복합키를 쓴다. null required는 요구사항 미확정이고 빈 executed는 확인된 미실행이다. 합격값 없이는 품질 통과를 판정할 수 없다."
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
  "path": "cases/QUALITY/test-matrix-coverage.md",
  "decision_signature": {
    "decision": "승인 검토 전에 필수 시험 조합의 누락을 식별한다",
    "input_structure": "required test×condition pairs vs executed pairs",
    "hard_constraint": "시험 이름이 같아도 조건이 다르면 별개다",
    "validation": "집합 차이로 누락된 시험과 조건의 쌍을 정확히 출력한다"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 조명 부품 검토 담당자가 시험성적서는 많지만 저온 조건 시험이 빠졌는지 빠르게 확인하고 싶다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 시험 이름만 맞으면 다른 조건도 완료로 간주한다.
- 중복 성적서가 완료 개수를 부풀린다.
- 요구 시험 목록 버전이 바뀌었다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 필수 조합은 어느 버전에서 정하는가? | 버전이 미확정이면 완료 판정을 보류한다. |
| 실행됨과 합격은 별개인가? | 본 예제는 커버리지만 검사한다. 합격 gate는 별도다. |
| 동등한 조건으로 대체 가능한가? | 권한자의 승인 매핑이 없으면 정확한 쌍만 인정한다. |

## 4. 데이터와 없을 때의 대안
필수 필드는 required 배열([test_id, condition_id]), executed(동일 형식), requirement_version이다. 한 행은 시험과 조건의 쌍이며 복합키를 쓴다. null required는 요구사항 미확정이고 빈 executed는 확인된 미실행이다. 합격값 없이는 품질 통과를 판정할 수 없다.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "version": "v1",
  "required": [
    [
      "load",
      "cold"
    ],
    [
      "load",
      "warm"
    ],
    [
      "seal",
      "cold"
    ]
  ],
  "executed": [
    [
      "load",
      "cold"
    ],
    [
      "load",
      "warm"
    ],
    [
      "load",
      "warm"
    ]
  ]
}
```

## 5. 기준 방법과 개선 조건
필수 쌍의 집합에서 실행 쌍의 집합을 빼서 누락 표를 만든다. 중복 성적서는 한 조합의 커버리지로만 계산한다. 사용자는 이 표로 추가 시험을 요청한다.

시험방법 버전과 대체 승인 관계가 확인되면 조합키에 포함하고 추적성을 확장한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 승인 검토 전에 필수 시험 조합의 누락을 식별한다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `[["seal", "cold"]]` | 중복load/warm은한번만;seal/cold누락. |
| 경계 | `{"executed": [["load", "cold"], ["load", "warm"], ["seal", "cold"]]}` | `[]` | 필수조합모두실행;합격을뜻하지않음. |
| 정보 부족 | `{"required": null}` | `"unknown"` | 요구목록미확정. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
파일 개수를 필수 시험 완료수로 쓰지 않는다. 커버리지 100%를 품질 합격으로 표현하지 않는다. 버전이 없으면 원자료 정리만 한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 누락 표로 필요한 추가 시험을 발주할 수 있는가?
- 시험 완료와 합격 결과를 구분할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 집합 차이를 쓴 이유와 중복 반례는 무엇인가?
- 검증 범위가 시험 결과의 진실성을 포함하지 않는 이유는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/stdtypes.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
