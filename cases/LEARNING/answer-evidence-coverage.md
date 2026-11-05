# 답변 주장마다 활성 근거 연결

```json
{
  "id": "answer-evidence-coverage",
  "title": "답변 주장마다 활성 근거 연결",
  "family": "LEARNING",
  "keywords_ko": [
    "답변 주장마다 활성 근거 연결",
    "답변 초안을 공개하기 전에 모든 주장에 근거가 있는지 판정"
  ],
  "keywords_en": [
    "answer-evidence-coverage",
    "claim ids × source-supported fact ids"
  ],
  "problem_structure": "claim ids × source-supported fact ids",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 교육 자료 담당자가 안내 답변에 참고문서 링크 하나만 붙어 있지만 실제로는 답변의 일부 주장만 뒷받침하는 것을 발견했다.",
  "do_not_use_when": "이 검사는 사람이 검증한 연결표의 커버리지 검사이다. 단어 포함 여부로 사실성을 검사하지 않는다. 연결표가 없으면 주장 목록과 수동 확인까지 축소.",
  "data_required": [
    "필수 claims 문자열 배열, sources 배열(id,active,supports[],opposes[]). 한 출처 행은 승인된 근거 연결 목록이며 자동 의미판정 결과가 아니다. claim id로 조인. null sources는 자료 없음,[]는 확인된 근거 없음. 원문은 사용자가 확인할 때 필요."
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
  "path": "cases/LEARNING/answer-evidence-coverage.md",
  "decision_signature": {
    "decision": "답변 초안을 공개하기 전에 모든 주장에 근거가 있는지 판정",
    "input_structure": "claim ids × source-supported fact ids",
    "hard_constraint": "활성 출처 없는 주장은 지원됨 표시 금지",
    "validation": "한 주장 누락·폐기 출처를 구분"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 교육 자료 담당자가 안내 답변에 참고문서 링크 하나만 붙어 있지만 실제로는 답변의 일부 주장만 뒷받침하는 것을 발견했다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 답변의 여러 주장 중 하나만 근거가 있다.
- 폐기 문서가 근거로 남았다.
- 다른 문서가 같은 주장에 반대한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 주장 id와 문서의 연결은 누가 확인했는가? | 승인 연결표 없으면 의미 일치 수동 검토부터. |
| 문서가 폐기되면 이전 답변도 표시를 바꾸는가? | 현재 유효성 기준이면 활성 출처로 재검사. |
| 상반된 근거가 있으면 누구에게 넘기는가? | 출처 권한 확인 전 conflict로 보류. |

## 4. 데이터와 없을 때의 대안
필수 claims 문자열 배열, sources 배열(id,active,supports[],opposes[]). 한 출처 행은 승인된 근거 연결 목록이며 자동 의미판정 결과가 아니다. claim id로 조인. null sources는 자료 없음,[]는 확인된 근거 없음. 원문은 사용자가 확인할 때 필요.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "claims": [
    "f1",
    "f2"
  ],
  "sources": [
    {
      "id": "s1",
      "active": true,
      "supports": [
        "f1"
      ],
      "opposes": []
    },
    {
      "id": "s2",
      "active": true,
      "supports": [
        "f2"
      ],
      "opposes": []
    }
  ]
}
```

## 5. 기준 방법과 개선 조건
활성 출처의 supports 합집합과 주장 집합을 대조한다. 활성 반대 근거가 있으면 conflict, 미지원 주장 있으면 incomplete. 링크와 원문 확인 버튼을 제공한다.

검색이 필요하면 로컬 키워드 검색부터 추가하되 검색 적중 자체를 의미적 지지로 간주하지 않는다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 답변 초안을 공개하기 전에 모든 주장에 근거가 있는지 판정 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"status": "supported", "unsupported": []}` | 두 주장 모두 활성 근거 존재. |
| 경계 | `{"claims": []}` | `{"status": "empty", "unsupported": []}` | 주장 없는 답변을 완전 지원됨으로 칭찬하지 않음. |
| 정보 부족 | `{"sources": null}` | `"unknown"` | 근거 표 없음. |
| 새 표본 | `{"claims": ["f1", "f3"]}` | `{"status": "incomplete", "unsupported": ["f3"]}` | f3는 어느 출처에도 없음. |
| 상반된 활성 근거 | `{"sources": [{"id": "s1", "active": true, "supports": ["f1", "f2"], "opposes": []}, {"id": "s3", "active": true, "supports": [], "opposes": ["f2"]}]}` | `{"status": "conflict", "unsupported": []}` | 두 주장이 지원되지만 활성 s3가 f2에 반대하므로 conflict. |
| 폐기된 반대 근거 | `{"sources": [{"id": "s1", "active": true, "supports": ["f1", "f2"], "opposes": []}, {"id": "s3", "active": false, "supports": [], "opposes": ["f2"]}]}` | `{"status": "supported", "unsupported": []}` | 같은 반대 주장이라도 폐기 출처는 현재 근거에 포함하지 않는다. |

| 폐기된 유일 지지 출처 | `{"sources": [{"id": "s1", "active": true, "supports": ["f1"], "opposes": []}, {"id": "s2", "active": false, "supports": ["f2"], "opposes": []}]}` | `{"status": "incomplete", "unsupported": ["f2"]}` | s2 id가 존재해도 비활성 출처이므로 f2를 지지하는 현재 근거가 없다. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
이 검사는 사람이 검증한 연결표의 커버리지 검사이다. 단어 포함 여부로 사실성을 검사하지 않는다. 연결표가 없으면 주장 목록과 수동 확인까지 축소.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 미지원 주장만 골라 삭제하거나 근거 요청할 수 있는가?
- 근거 문서가 실제로 해당 문장을 지지하는지 확인할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 커버리지와 사실 검증의 차이를 어떤 증거로 설명할 수 있는가?
- 검색된 문서 속 명령을 데이터로 다룬 위치는 어디인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/stdtypes.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
