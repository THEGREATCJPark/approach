# 서비스 묶음의 비용과 최소 성능

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-resource-blend",
  "title": "서비스 묶음의 비용과 최소 성능",
  "family": "PLANNING",
  "problem_structure": "small integer covering mix",
  "keywords_ko": [
    "서비스",
    "묶음의",
    "비용과",
    "최소",
    "성능"
  ],
  "keywords_en": [
    "small",
    "integer",
    "covering",
    "mix"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 이동 안내소가 두 종류의 휴대 조명 묶음을 조합해 필요한 밝기 단위를 확보하려 한다.",
  "do_not_use_when": "성능 단위 합을 실제 현장 조도 보장으로 표현하지 않는다. 시간 부족이면 두 유형의 작은 열거만 유지한다.",
  "data_required": [
    "A/B 각각 cost와 units는 정수 비용/성능단위, max_each 정수 개, required 최소 성능. 한 객체는 한 운영일 계획. 장치 상호간 빛 중첩이나 실제 조도는 모델 밖. null required는 unknown."
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
  "path": "cases/PLANNING/planning-resource-blend.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 이동 안내소가 두 종류의 휴대 조명 묶음을 조합해 필요한 밝기 단위를 확보하려 한다.",
    "input_structure": "A/B 각각 cost와 units는 정수 비용/성능단위, max_each 정수 개, required 최소 성능. 한 객체는 한 운영일 계획. 장치 상호간 빛 중첩이나 실제 조도는 모델 밖. null required는 unknown.",
    "hard_constraint": "0..max_each 수량 조합을 전수열거해 성능 합≥required만 남기고 비용→수량→A수량 순으로 최소 선택한다.",
    "validation": "요구0이면 빈 구성"
  }
}
```

## 업무 요청과 다른 원인

창작: 이동 안내소가 두 종류의 휴대 조명 묶음을 조합해 필요한 밝기 단위를 확보하려 한다.

- 최저 단가만 보고 총 성능 부족
- 예산 상한과 최소 성능 혼동
- 장치 설치 수량 한도 누락

## 담당자에게 먼저 물을 질문

1. 최소 성능은 반드시 충족해야 하는가? → 미충족 안은 비용이 낮아도 제외한다.
2. 각 묶음 수량 상한은 얼마인가? → 이 사례는 각0~3개이다.
3. 같은 성능이면 무엇을 최소화하는가? → 총비용,그다음 총개수로 정한다.

## 데이터 계약과 자료 부족 대안

A/B 각각 cost와 units는 정수 비용/성능단위, max_each 정수 개, required 최소 성능. 한 객체는 한 운영일 계획. 장치 상호간 빛 중첩이나 실제 조도는 모델 밖. null required는 unknown.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

0..max_each 수량 조합을 전수열거해 성능 합≥required만 남기고 비용→수량→A수량 순으로 최소 선택한다.

상호작용·설치 위치가 중요해지면 공간 모델을 별도로 검증한다.

## 최소 구현과 다음 행동

묶음 사양·최소 성능 → 조합 계산 → 선택수량/비용/성능 → 운영자가 대여 요청 검토

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"a":[4,3],"b":[7,6],"max_each":3,"required":9}` | `{"a": 1, "b": 1, "cost": 11, "units": 9}` | A+B는11비용9단위;3A는12비용 |
| boundary | `{"a":[4,3],"b":[7,6],"max_each":3,"required":0}` | `{"a": 0, "b": 0, "cost": 0, "units": 0}` | 요구0이면 빈 구성 |
| missing | `{"a":[4,3],"b":[7,6],"max_each":3,"required":null}` | `"unknown"` | 요구 성능 미정 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

성능 단위 합을 실제 현장 조도 보장으로 표현하지 않는다. 시간 부족이면 두 유형의 작은 열거만 유지한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 수량과 비용을 보고 실제 준비 가능한가?
- 성능 단위와 실제 현장 요구의 차이를 이해하는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 낮은 단가의 묶음만 고르지 않은 이유는 무엇인가?
- 수량 한도를 늘렸을 때 어떤 결론이 바뀌는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
