# 서비스 종류의 최소 재등장 간격

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-repeat-gap",
  "title": "서비스 종류의 최소 재등장 간격",
  "family": "PLANNING",
  "problem_structure": "sequence spacing validation",
  "keywords_ko": [
    "서비스",
    "종류의",
    "최소",
    "재등장",
    "간격"
  ],
  "keywords_en": [
    "sequence",
    "spacing",
    "validation"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 체험 공간이 같은 활동을 연속 며칠 피하는 수준을 넘어 재등장 간격을 명확히 검증하려 한다.",
  "do_not_use_when": "문자열 유사도로 다른 활동을 합치지 않는다. 시간 부족이면 자동 재계획을 제외하고 위반표만 유지한다.",
  "data_required": [
    "schedule은 day0부터 활동 ID 배열, min_gap은 같은 ID 등장 인덱스 차이의 최소 정수. 한 행은 하루 한 활동. null 활동은 unknown이며 휴관 표시와 다르다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rotation-budget"
  ],
  "depth": "standard",
  "path": "cases/PLANNING/planning-repeat-gap.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 체험 공간이 같은 활동을 연속 며칠 피하는 수준을 넘어 재등장 간격을 명확히 검증하려 한다.",
    "input_structure": "schedule은 day0부터 활동 ID 배열, min_gap은 같은 ID 등장 인덱스 차이의 최소 정수. 한 행은 하루 한 활동. null 활동은 unknown이며 휴관 표시와 다르다.",
    "hard_constraint": "활동별 최근 등장 위치를 저장하고 현재−이전<min_gap인 인접 재등장 쌍을 출력한다.",
    "validation": "간격3은 허용"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 체험 공간이 같은 활동을 연속 며칠 피하는 수준을 넘어 재등장 간격을 명확히 검증하려 한다.

- 간격을 쉬는 날 수와 날짜 차이로 혼동
- 기존 고정 일정이 반복 규칙 위반
- 활동 이름 표기 차이

## 담당자에게 먼저 물을 질문

1. 간격은 날짜 차이인가 사이의 빈 날짜 수인가? → 이 사례는 날짜 인덱스 차이이다.
2. 휴관일도 간격에 포함하는가? → 운영일 기준이면 인덱스를 다시 만든다.
3. 위반 때 자동 수정하는가? → 이 사례는 위반 위치만 보고한다.

## 데이터 계약과 자료 부족 대안

schedule은 day0부터 활동 ID 배열, min_gap은 같은 ID 등장 인덱스 차이의 최소 정수. 한 행은 하루 한 활동. null 활동은 unknown이며 휴관 표시와 다르다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

활동별 최근 등장 위치를 저장하고 현재−이전<min_gap인 인접 재등장 쌍을 출력한다.

자동 수정 요구가 생기면 고정일·가용성·비용을 받아 제약 탐색으로 전환한다.

## 최소 구현과 다음 행동

일정·간격 → 반복 검증 → 위반 날짜 쌍 → 운영자가 변경 가능한 날을 선택

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"schedule":["A","B","A","C"],"min_gap":3}` | `[[0, 2]]` | 같은A 간격2<3 |
| boundary | `{"schedule":["A","B","C","A"],"min_gap":3}` | `[]` | 간격3은 허용 |
| missing | `{"schedule":["A",null,"B"],"min_gap":3}` | `"unknown"` | 하루 활동 미정 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

문자열 유사도로 다른 활동을 합치지 않는다. 시간 부족이면 자동 재계획을 제외하고 위반표만 유지한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 위반 쌍에서 실제로 바꿀 수 있는 날짜가 어느 쪽인가?
- 휴관일 계산 정책이 기대와 맞는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- gap3의 경계가 어떤 두 날짜인지 설명할 수 있는가?
- 위반 검출과 실행 가능한 새 일정은 무엇이 다른가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
