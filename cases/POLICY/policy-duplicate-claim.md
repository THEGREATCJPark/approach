# 증빙 번호가 겹치는 신청 검토

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "policy-duplicate-claim",
  "title": "증빙 번호가 겹치는 신청 검토",
  "family": "POLICY",
  "problem_structure": "composite duplicate detection",
  "keywords_ko": [
    "증빙",
    "번호가",
    "겹치는",
    "신청",
    "검토"
  ],
  "keywords_en": [
    "composite",
    "duplicate",
    "detection"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 지역 보존 작업실에서 같은 영수증을 여러 신청에 사용했는지 확인하려 한다.",
  "do_not_use_when": "같은 금액이나 이름만으로 중복 확정하지 않는다. 자료가 부족하면 검토 후보까지만 표시한다.",
  "data_required": [
    "rows 각 행 [request_id,issuer,receipt,date]. 금액 판단은 하지 않는다. 날짜 YYYY-MM-DD. null 키는 unknown. 일치해도 부정 청구 확정이 아니라 review_pairs 후보이다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "resubmission-state"
  ],
  "depth": "standard",
  "path": "cases/POLICY/policy-duplicate-claim.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 지역 보존 작업실에서 같은 영수증을 여러 신청에 사용했는지 확인하려 한다.",
    "input_structure": "rows 각 행 [request_id,issuer,receipt,date]. 금액 판단은 하지 않는다. 날짜 YYYY-MM-DD. null 키는 unknown. 일치해도 부정 청구 확정이 아니라 review_pairs 후보이다.",
    "hard_constraint": "서로 다른 request_id가 같은 복합 증빙키를 쓰면 정렬된 신청 ID 쌍을 출력한다. 동일 신청 반복은 제거한다.",
    "validation": "같은 신청 재전송은 별도 청구가 아님"
  }
}
```

## 업무 요청과 다른 원인

창작: 지역 보존 작업실에서 같은 영수증을 여러 신청에 사용했는지 확인하려 한다.

- 재전송된 같은 신청
- 실제로 별도 구매인데 번호만 동일
- 하나의 증빙을 두 번 청구

## 담당자에게 먼저 물을 질문

1. 증빙 유일키는 무엇인가? → 이 사례는 발급처·증빙번호·발급일 조합이다.
2. 같은 신청 ID 재전송인가? → 같으면 재전송, 다르면 검토 후보이다.
3. 부분 청구를 허용하는가? → 허용하면 중복 거절 대신 배분 잔액 검사로 전환한다.

## 데이터 계약과 자료 부족 대안

rows 각 행 [request_id,issuer,receipt,date]. 금액 판단은 하지 않는다. 날짜 YYYY-MM-DD. null 키는 unknown. 일치해도 부정 청구 확정이 아니라 review_pairs 후보이다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

서로 다른 request_id가 같은 복합 증빙키를 쓰면 정렬된 신청 ID 쌍을 출력한다. 동일 신청 반복은 제거한다.

부분 청구 정책이면 증빙 총액과 배분액을 확인하는 receipt-allocation 사례를 연결한다.

## 최소 구현과 다음 행동

신청 표 → 복합키 그룹 → 중복 검토 쌍 → 담당자가 원본·부분청구 여부 확인

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"rows":[["a","shop","r1","2030-01-01"],["b","shop","r1","2030-01-01"]]}` | `[["a", "b"]]` | 다른 신청이 같은 증빙키 |
| boundary | `{"rows":[["a","shop","r1","2030-01-01"],["a","shop","r1","2030-01-01"]]}` | `[]` | 같은 신청 재전송은 별도 청구가 아님 |
| missing | `{"rows":[["a",null,"r1","2030-01-01"]]}` | `"unknown"` | 발급처 없이는 키 미확정 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

같은 금액이나 이름만으로 중복 확정하지 않는다. 자료가 부족하면 검토 후보까지만 표시한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 쌍을 보고 어떤 원본 증빙을 확인하겠는가?
- 부분청구를 중복으로 오해하지 않도록 안내가 충분한가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 검토 후보와 확정 위반을 왜 분리했는가?
- 복합키 한 필드를 빼면 어떤 오탐이 생기는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
