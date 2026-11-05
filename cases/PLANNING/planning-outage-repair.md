# 공급 중단 후 기존 계획의 최소 변경

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-outage-repair",
  "title": "공급 중단 후 기존 계획의 최소 변경",
  "family": "PLANNING",
  "problem_structure": "minimum change reassignment",
  "keywords_ko": [
    "공급",
    "중단",
    "후",
    "기존",
    "계획의",
    "최소",
    "변경"
  ],
  "keywords_en": [
    "minimum",
    "change",
    "reassignment"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 지역 순회 교구 창고의 한 보관 위치를 갑자기 사용할 수 없어 이미 배정된 상자를 적게 옮기려 한다.",
  "do_not_use_when": "원 계획을 무시하고 새 최적안만 보여주지 않는다. 대규모일 때는 우선 유효한 수동 이동안과 미해결 용량을 표시한다.",
  "data_required": [
    "assignments는 상자별 위치 ID 배열, capacity는 위치별 정수 상자 수. 한 원소는 동일 크기 상자 하나; 배열 인덱스가 fixture 키. closed는 사용 불가 위치. null 용량은 unknown. 다른 크기는 별도 모델."
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
  "path": "cases/PLANNING/planning-outage-repair.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 지역 순회 교구 창고의 한 보관 위치를 갑자기 사용할 수 없어 이미 배정된 상자를 적게 옮기려 한다.",
    "input_structure": "assignments는 상자별 위치 ID 배열, capacity는 위치별 정수 상자 수. 한 원소는 동일 크기 상자 하나; 배열 인덱스가 fixture 키. closed는 사용 불가 위치. null 용량은 unknown. 다른 크기는 별도 모델.",
    "hard_constraint": "남은 위치 배정을 작은 전수열거해 용량 위반을 제거하고 기존과 다른 상자 수를 최소화한다. 동률은 위치 ID 배열 사전순.",
    "validation": "중단 없고 기존안 유효"
  }
}
```

## 업무 요청과 다른 원인

창작: 지역 순회 교구 창고의 한 보관 위치를 갑자기 사용할 수 없어 이미 배정된 상자를 적게 옮기려 한다.

- 전체 비용만 최소화해 불필요한 이동
- 남은 위치 용량 부족
- 고정된 상자 이동 금지

## 담당자에게 먼저 물을 질문

1. 기존 배정 유지가 비용보다 우선인가? → 이 사례는 이동 수 최소이다.
2. 어느 상자가 이동 금지인가? → 필요하면 hard lock을 별도 입력한다.
3. 남은 용량이 부족하면 어떻게 하는가? → 미배정을 숨기지 않고 infeasible을 반환한다.

## 데이터 계약과 자료 부족 대안

assignments는 상자별 위치 ID 배열, capacity는 위치별 정수 상자 수. 한 원소는 동일 크기 상자 하나; 배열 인덱스가 fixture 키. closed는 사용 불가 위치. null 용량은 unknown. 다른 크기는 별도 모델.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

남은 위치 배정을 작은 전수열거해 용량 위반을 제거하고 기존과 다른 상자 수를 최소화한다. 동률은 위치 ID 배열 사전순.

상자 크기·이동 거리·고정 상자가 필요하면 추가 제약을 넣고 이동수 목적의 우선순위를 유지한다.

## 최소 구현과 다음 행동

기존안·중단 위치·용량 → 재배정 → 변경 위치와 최소 이동 수 → 담당자가 이동 작업 지정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"assignments":["A","A","B"],"capacity":{"A":2,"B":3},"closed":["A"]}` | `{"moves": 2, "assignment": ["B", "B", "B"]}` | A상자2개만 B로 이동 |
| boundary | `{"assignments":["A","B"],"capacity":{"A":1,"B":1},"closed":[]}` | `{"moves": 0, "assignment": ["A", "B"]}` | 중단 없고 기존안 유효 |
| missing | `{"assignments":["A"],"capacity":{"B":null},"closed":["A"]}` | `"unknown"` | 대체 용량 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

원 계획을 무시하고 새 최적안만 보여주지 않는다. 대규모일 때는 우선 유효한 수동 이동안과 미해결 용량을 표시한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 어느 상자를 옮길지 기존안과 비교할 수 있는가?
- 용량 수치가 실제 남은 공간을 뜻하는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 최소 비용 대신 최소 변경을 택한 근거는 무엇인가?
- 실행 가능한 안과 최소임을 증명한 안을 어떻게 구별하는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
