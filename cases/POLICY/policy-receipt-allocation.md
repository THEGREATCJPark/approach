# 공유 증빙의 부서별 배분 잔액

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "policy-receipt-allocation",
  "title": "공유 증빙의 부서별 배분 잔액",
  "family": "POLICY",
  "problem_structure": "bounded allocation sum",
  "keywords_ko": [
    "공유",
    "증빙의",
    "부서별",
    "배분",
    "잔액"
  ],
  "keywords_en": [
    "bounded",
    "allocation",
    "sum"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 공용 작업장이 하나의 재료 영수증을 여러 프로젝트에 나누되 총액을 넘기지 않게 하려 한다.",
  "do_not_use_when": "소수 float 합계로 금액 경계를 판정하지 않는다. 원본 총액이 없으면 합계만 표시하고 완료 판정을 보류한다.",
  "data_required": [
    "total과 rows의 [allocation_id,amount]는 최소 비용단위 정수. 한 행은 증빙의 프로젝트 배분 하나. null 금액은 unknown. 중복 ID는 invalid이며 실제 금액·법률 처리 규칙은 다루지 않는다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "policy-duplicate-claim"
  ],
  "depth": "standard",
  "path": "cases/POLICY/policy-receipt-allocation.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 공용 작업장이 하나의 재료 영수증을 여러 프로젝트에 나누되 총액을 넘기지 않게 하려 한다.",
    "input_structure": "total과 rows의 [allocation_id,amount]는 최소 비용단위 정수. 한 행은 증빙의 프로젝트 배분 하나. null 금액은 unknown. 중복 ID는 invalid이며 실제 금액·법률 처리 규칙은 다루지 않는다.",
    "hard_constraint": "고유 배분액 합계가 total보다 작으면 partial, 같으면 complete, 크면 overallocated; remaining=total−sum.",
    "validation": "합계100"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 공용 작업장이 하나의 재료 영수증을 여러 프로젝트에 나누되 총액을 넘기지 않게 하려 한다.

- 같은 배분 행 재전송
- 부가 비용 포함 기준 차이
- 배분 누락과 초과 혼동

## 담당자에게 먼저 물을 질문

1. 총액은 세금 포함인가? → 같은 기준으로 맞춘다.
2. 미배분 잔액을 허용하는가? → 이 예제는 partial로 표시한다.
3. 배분 ID 재전송은 어떤가? → 같은 ID는 중복 오류로 확인한다.

## 데이터 계약과 자료 부족 대안

total과 rows의 [allocation_id,amount]는 최소 비용단위 정수. 한 행은 증빙의 프로젝트 배분 하나. null 금액은 unknown. 중복 ID는 invalid이며 실제 금액·법률 처리 규칙은 다루지 않는다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

고유 배분액 합계가 total보다 작으면 partial, 같으면 complete, 크면 overallocated; remaining=total−sum.

정정 배분은 버전과 원 배분 연결을 추가하고 확정 전 재검산한다.

## 최소 구현과 다음 행동

증빙 총액·배분 → 유효성·합계 → 잔액/상태 → 담당자가 미배분 또는 초과분 수정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"total":100,"rows":[["a",35],["b",40]]}` | `{"state": "partial", "remaining": 25}` | 100−75=25 |
| boundary | `{"total":100,"rows":[["a",35],["b",65]]}` | `{"state": "complete", "remaining": 0}` | 합계100 |
| missing | `{"total":100,"rows":[["a",null]]}` | `"unknown"` | 배분액 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

소수 float 합계로 금액 경계를 판정하지 않는다. 원본 총액이 없으면 합계만 표시하고 완료 판정을 보류한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 남은 금액을 어느 프로젝트에 배분해야 하는가?
- 초과를 음수 잔액으로만 표시하면 놓치지 않는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 부분 배분과 완료의 경계는 어떻게 검사했는가?
- 합계 일치가 지출의 적법성을 보장하는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
