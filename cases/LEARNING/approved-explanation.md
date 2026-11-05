# 승인된 짧은 개념 설명 선택

```json
{
  "id": "approved-explanation",
  "title": "승인된 짧은 개념 설명 선택",
  "family": "LEARNING",
  "keywords_ko": [
    "승인된 짧은 개념 설명 선택",
    "주어진 개념에 읽을 수 있는 승인 설명을 선택"
  ],
  "keywords_en": [
    "approved-explanation",
    "concept × version × character length"
  ],
  "problem_structure": "concept × version × character length",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 수선 교실 운영자가 실습대 작은 화면에 개념 설명을 한 개 보여주려 한다. 설명을 줄이다가 주의 조건이 사라진 경험이 있다.",
  "do_not_use_when": "짧은 문구를 무조건 좋다고 평가하지 않는다. 자동 요약 모델부터 설치하지 않는다. 승인 정보가 없으면 개념 목록까지만 제공.",
  "data_required": [
    "한 행은 설명 후보. 필수 id·concept 문자열, approved/active 불리언, text 문자열, max_chars 정수(Unicode 코드포인트 수). id 고유, concept로 요청과 결합. null text/문서목록은 미확인; 빈 목록은 확인된 후보 없음. 실제 줄바꿈 폭은 선택 개선 자료."
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
  "path": "cases/LEARNING/approved-explanation.md",
  "decision_signature": {
    "decision": "주어진 개념에 읽을 수 있는 승인 설명을 선택",
    "input_structure": "concept × version × character length",
    "hard_constraint": "승인·활성 버전이며 길이 예산 이내",
    "validation": "승인되지 않은 짧은 문서가 선택되지 않음"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 수선 교실 운영자가 실습대 작은 화면에 개념 설명을 한 개 보여주려 한다. 설명을 줄이다가 주의 조건이 사라진 경험이 있다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 원문 자체가 너무 길다.
- 폐기된 설명이 검색 상단에 있다.
- 약어가 다른 개념과 충돌한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 설명을 요약해도 되는가? | 승인 문구만 허용이면 그대로 선택; 요약 허용이면 의미 보존 검토를 별도 추가. |
| 어느 버전이 현재 승인인가? | 버전 정보 없으면 표시를 보류. |
| 최대 길이는 문자 수인가 화면 줄 수인가? | 문자면 길이 필터, 실제 줄 수면 렌더링 측정을 추가. |

## 4. 데이터와 없을 때의 대안
한 행은 설명 후보. 필수 id·concept 문자열, approved/active 불리언, text 문자열, max_chars 정수(Unicode 코드포인트 수). id 고유, concept로 요청과 결합. null text/문서목록은 미확인; 빈 목록은 확인된 후보 없음. 실제 줄바꿈 폭은 선택 개선 자료.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "concept": "grain",
  "max_chars": 8,
  "docs": [
    {
      "id": "a",
      "concept": "grain",
      "approved": true,
      "active": true,
      "text": "결 방향 확인"
    },
    {
      "id": "b",
      "concept": "grain",
      "approved": false,
      "active": true,
      "text": "결"
    },
    {
      "id": "c",
      "concept": "grain",
      "approved": true,
      "active": false,
      "text": "옛 설명"
    }
  ]
}
```

## 5. 기준 방법과 개선 조건
정확한 concept 일치 → 승인/활성 필터 → 길이 제한 → 짧은 순·id 순 선택. 문서가 없으면 no_fit, 미확인이면 unknown.

유의어 표를 담당자가 승인한 뒤 검색 범위를 확장한다. 자유 생성 요약은 원문 조건 누락 검토가 가능할 때만 후보.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 주어진 개념에 읽을 수 있는 승인 설명을 선택 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `"a"` | 활성·승인된 a의 길이7이8 이하. |
| 경계 | `{"max_chars": 7}` | `"a"` | 길이7 포함. |
| 정보 부족 | `{"docs": null}` | `"unknown"` | 문서 부재를 짧은 설명 생성으로 대체하지 않음. |
| 불충분 | `{"max_chars": 6}` | `"no_fit"` | 승인되지 않은 b를 대신 선택하지 않음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
짧은 문구를 무조건 좋다고 평가하지 않는다. 자동 요약 모델부터 설치하지 않는다. 승인 정보가 없으면 개념 목록까지만 제공.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 선택된 설명만 읽고 주의 조건을 찾을 수 있는가?
- no_fit일 때 긴 설명 열기나 담당자 확인이 가능한가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 문자 수 제한과 의미 보존을 각각 어떻게 검증했는가?
- 미승인 후보가 짧아도 제외되는 반례는 어디 있는가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/stdtypes.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
