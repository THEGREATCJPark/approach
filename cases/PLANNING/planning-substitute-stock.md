# 대체 자재의 환산량과 손실

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-substitute-stock",
  "title": "대체 자재의 환산량과 손실",
  "family": "PLANNING",
  "problem_structure": "substitution conversion arithmetic",
  "keywords_ko": [
    "대체",
    "자재의",
    "환산량과",
    "손실"
  ],
  "keywords_en": [
    "substitution",
    "conversion",
    "arithmetic"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 종이 모형 체험실이 지정 자재가 부족할 때 대체 자재를 몇 단위 준비해야 하는지 계산하려 한다.",
  "do_not_use_when": "원자재와 대체품 단위를 더하지 않는다. 수율이 미확정이면 민감도표까지만 만들고 확정 발주 금지.",
  "data_required": [
    "need는 원자재 환산 필요량, replacement_units는 대체1개당 원자재 환산량, yield_(수율)는 0<값≤1인 유효 수율, stock는 대체 재고 개수, approved 불리언/null. fixture 숫자는 소수 문자열로 정확 계산. null은 unknown."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "pack-order"
  ],
  "depth": "standard",
  "path": "cases/PLANNING/planning-substitute-stock.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 종이 모형 체험실이 지정 자재가 부족할 때 대체 자재를 몇 단위 준비해야 하는지 계산하려 한다.",
    "input_structure": "need는 원자재 환산 필요량, replacement_units는 대체1개당 원자재 환산량, yield_(수율)는 0<값≤1인 유효 수율, stock는 대체 재고 개수, approved 불리언/null. fixture 숫자는 소수 문자열로 정확 계산. null은 unknown.",
    "hard_constraint": "유효 환산량=replacement_units×yield. ceil(need/유효량) 개를 산출하고 재고와 비교한다. 승인 False면 blocked, null이면 unknown.",
    "validation": "정확히4개"
  }
}
```

## 업무 요청과 다른 원인

창작: 종이 모형 체험실이 지정 자재가 부족할 때 대체 자재를 몇 단위 준비해야 하는지 계산하려 한다.

- 대체 비율 방향을 뒤집음
- 공정 손실을 무시
- 대체 가능 승인과 재고 계산 혼동

## 담당자에게 먼저 물을 질문

1. 대체1개가 원자재 몇 개를 대신하는가? → 환산 방향을 명시한다.
2. 수율은 기대치인가 보장 최소인가? → 기대치라면 부족 위험을 별도로 표시한다.
3. 대체 사용 승인이 있는가? → 미승인이면 수량 계산이 맞아도 실행 보류다.

## 데이터 계약과 자료 부족 대안

need는 원자재 환산 필요량, replacement_units는 대체1개당 원자재 환산량, yield_(수율)는 0<값≤1인 유효 수율, stock는 대체 재고 개수, approved 불리언/null. fixture 숫자는 소수 문자열로 정확 계산. null은 unknown.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

유효 환산량=replacement_units×yield. ceil(need/유효량) 개를 산출하고 재고와 비교한다. 승인 False면 blocked, null이면 unknown.

수율 분포가 확보되면 보수 시나리오별 필요량을 병기한다.

## 최소 구현과 다음 행동

필요량·환산·수율·승인 → 올림 계산 → 필요 대체량/부족 → 담당자가 승인·추가 확보 판단

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"need":"10","replacement_units":"2","yield_":"0.8","stock":7,"approved":true}` | `{"required": 7, "shortage": 0}` | 10/1.6=6.25이므로7 |
| boundary | `{"need":"8","replacement_units":"2","yield_":"1","stock":4,"approved":true}` | `{"required": 4, "shortage": 0}` | 정확히4개 |
| missing | `{"need":"10","replacement_units":"2","yield_":null,"stock":7,"approved":true}` | `"unknown"` | 수율 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

원자재와 대체품 단위를 더하지 않는다. 수율이 미확정이면 민감도표까지만 만들고 확정 발주 금지.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 환산 방향을 실물 한 개로 설명할 수 있는가?
- 재고 부족 또는 승인 보류 때 다음 행동이 보이는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 올림을 해야 하는 이유를 수치로 설명할 수 있는가?
- 기대 수율 계산이 현장 부족 없음을 보장하는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
