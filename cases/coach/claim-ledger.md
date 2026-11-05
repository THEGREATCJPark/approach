# 설명 연습의 수치 주장과 근거 대조

```json
{
  "id": "claim-ledger",
  "title": "설명 연습의 수치 주장과 근거 대조",
  "family": "COACH",
  "keywords_ko": [
    "설명 연습",
    "사실",
    "근거",
    "주장"
  ],
  "keywords_en": [
    "evidence-review",
    "claim-ledger"
  ],
  "problem_structure": "evidence-review",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP 전용: 독서실 좌석 현황을 만든 개발자가 자기 설명에서 관측 수치와 기대 효과를 섞고 있어, 연습 전에 사실 장부를 만들려 한다. 실제 AI 금지 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다.",
  "do_not_use_when": "키워드 포함만으로 사실 판정하지 않는다. “검사하지 않았다”와 “검사했다”를 같다고 처리하지 않는다. 모범 답변 암기를 유도하지 않는다.",
  "data_required": [
    "최소: claim_id, claimed_value 숫자 또는 null, evidence_value 숫자 또는 null, unit, polarity. 행은 사람이 분해한 주장 1개. 키 claim_id. null은 미확인. 원문 의미 정규화는 사람이 검토하며 숫자 일치만으로 사실성을 보장하지 않는다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rater-disagreement"
  ],
  "depth": "deep",
  "path": "cases/coach/claim-ledger.md",
  "test_count": 7,
  "fixture_path": "examples/synthetic/claim-ledger.json"
}
```

## 요청과 가설

창작 PREP 전용: 독서실 좌석 현황을 만든 개발자가 자기 설명에서 관측 수치와 기대 효과를 섞고 있어, 연습 전에 사실 장부를 만들려 한다. 실제 AI 금지 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다.

가능한 원인: 측정된 사실과 예상을 혼동; 부정 표현의 의미를 놓침; 근거 파일 없는 주장.

## 먼저 가를 질문과 계획 변경

1. 실측 로그가 있는가? → 없으면 수치 주장은 unverified로 둔다.
2. 주장 단위와 집계 범위가 동일한가? → 다르면 비교 보류.
3. 지금 PREP인가 AI 금지 평가인가? → 금지이면 연습 지원 즉시 중단.

## 데이터 계약

최소: claim_id, claimed_value 숫자 또는 null, evidence_value 숫자 또는 null, unit, polarity. 행은 사람이 분해한 주장 1개. 키 claim_id. null은 미확인. 원문 의미 정규화는 사람이 검토하며 숫자 일치만으로 사실성을 보장하지 않는다.

소형 fixture 어댑터: `claim` = claimed_value, `evidence` = evidence_value. `same_meaning`은 unit·범위·polarity를 사람이 대조한 결과이며 원문에서 자동 추출한 값이 아니다. false이면 semantic_review로 보류한다. 단일 건의 claim_id는 고정값이다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 동일 단위·범위·긍정부정 확인 후 구조화한 수치만 비교한다. 일치=supported, 불일치=contradicted, 근거 없음=unverified. 자유문장 자동 사실 판정은 하지 않는다.

개선 조건: 문장별 인용 위치와 가정·예상 태그 추가. 언어 모델 평가자는 별도 검증 데이터와 허용 조건이 있는 준비 환경에서만 검토.

최소 경로: 허용된 합성 작업 기록 → 주장 수동 분해 → 근거 대조 표 → 개발자가 과장을 수정하고 자기 말로 설명한다.

제약과 우선순위: 목적함수 없음. 필수: PREP와 허용된 자료, 동일 의미. 선호: 표현 간결성. 의미 불명확이면 semantic_review.

추가 fixture 스키마: 추가 순서변경 fixture의 `claims`는 [주장 ID, 주장 수치, 근거 수치] 행 배열이다. 이미 동일 의미·단위를 수동 확인한 두 건의 ID별 판정을 검증한다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/claim-ledger.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"claim":8,"evidence":8,"same_meaning":true}`|`"supported"`|동일 범위 8=8|
|boundary|`{"claim":0,"evidence":0,"same_meaning":true}`|`"supported"`|관측 0은 근거|
|missing|`{"claim":8,"evidence":null,"same_meaning":true}`|`"unverified"`|근거 부재|
|conflict|`{"claim":8,"evidence":6,"same_meaning":true}`|`"contradicted"`|8≠6|
|object_key_order|`{"evidence":8,"same_meaning":true,"claim":8}`|`"supported"`|필드순 무관|
|new_expression|`{"claim":8,"evidence":8,"same_meaning":false}`|`"semantic_review"`|부정·기간 차이 등 의미 다르면 숫자 일치로 승인 금지|
|reorder|`{"claims":[["b",8,6],["a",8,8]]}`|`{"a": "supported", "b": "contradicted"}`|주장 행순을 바꾸어도 claim ID별 근거 판정 유지|

비교 쌍: normal은 8=8 및 same_meaning=true로 supported, new_expression은 같은 숫자라도 same_meaning=false이므로 semantic_review다.

## 오류·도구·범위

키워드 포함만으로 사실 판정하지 않는다. “검사하지 않았다”와 “검사했다”를 같다고 처리하지 않는다. 모범 답변 암기를 유도하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 허용된 합성 작업 기록 → 주장 수동 분해 → 근거 대조 표 → 개발자가 과장을 수정하고 자기 말로 설명한다. 180분에는 문장별 인용 위치와 가정·예상 태그 추가. 언어 모델 평가자는 별도 검증 데이터와 허용 조건이 있는 준비 환경에서만 검토. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 이 표에서 실제로 입증된 주장과 예상 주장을 구별할 수 있습니까?
- 근거 링크를 열어 범위를 확인할 수 있습니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 어떤 주장을 약하게 고쳤고 어떤 근거 때문입니까?
- 자동 숫자 대조가 확인하지 못한 의미는 무엇입니까?

## 측정과 한계

구조화 수치 오류 탐지 수 측정 가능. 실제 면접 성과나 표현 능력 향상은 이 테스트로 주장 불가.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/decimal.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
