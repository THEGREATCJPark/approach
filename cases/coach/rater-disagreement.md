# 모의 설명 평가자의 불일치 찾기

```json
{
  "id": "rater-disagreement",
  "title": "모의 설명 평가자의 불일치 찾기",
  "family": "COACH",
  "keywords_ko": [
    "평가자",
    "일치도",
    "루브릭",
    "설명 연습"
  ],
  "keywords_en": [
    "agreement",
    "rater-disagreement"
  ],
  "problem_structure": "agreement",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP 전용: 창작 프로젝트 설명을 두 명이 독립 평가했는데 평균점수는 같아도 지적한 항목이 다르다. 항목별 기준을 재합의하려 한다. AI 금지 후속 평가 중에는 질문 생성·답변·코칭을 제공하지 않는다.",
  "do_not_use_when": "일치율 100%를 좋은 루브릭의 증거로 단정하지 않는다. 한쪽 결과를 보고 다른 평가를 수정한 뒤 독립 평가라고 부르지 않는다.",
  "data_required": [
    "최소: item_id, rater_a/rater_b 범주(pass/revise/unknown), evidence_id. 한 행은 동일 항목의 한 쌍. 키 item_id. missing은 쌍 제외하며 분모 공개. 개선: 독립 제3평가. 사용자 개인 신상 불필요."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "claim-ledger"
  ],
  "depth": "deep",
  "path": "cases/coach/rater-disagreement.md",
  "test_count": 6,
  "fixture_path": "examples/synthetic/rater-disagreement.json"
}
```

## 요청과 가설

창작 PREP 전용: 창작 프로젝트 설명을 두 명이 독립 평가했는데 평균점수는 같아도 지적한 항목이 다르다. 항목별 기준을 재합의하려 한다. AI 금지 후속 평가 중에는 질문 생성·답변·코칭을 제공하지 않는다.

가능한 원인: 평가 기준 해석 차이; 관측한 설명 자료 차이; 실제 애매한 답변.

## 먼저 가를 질문과 계획 변경

1. 두 평가자가 같은 기록을 보았습니까? → 아니면 일치도 계산 전에 자료 통일.
2. 점수는 순서척도입니까? → 범주별 혼동표부터, 평균 차이만 사용하지 않음.
3. 불일치가 곧 평가 오류입니까? → 아니면 중재자가 근거를 확인.

## 데이터 계약

최소: item_id, rater_a/rater_b 범주(pass/revise/unknown), evidence_id. 한 행은 동일 항목의 한 쌍. 키 item_id. missing은 쌍 제외하며 분모 공개. 개선: 독립 제3평가. 사용자 개인 신상 불필요.

소형 fixture 어댑터: `pairs` 행은 [rater_a,rater_b]다. 동일 item_id에 조인 완료한 결과라는 전제이며 evidence_id와 원문 자료 동일성은 사람이 확인한다. 자동 조인의 정확성을 이 fixture가 증명하지 않는다.

자료를 받을 수 없으면 아래 합성 fixture로 흐름만 확인하고 실제 판정은 보류한다. 누락은 0이 아니다.

## 방법과 최소 결과물

기준 방법: 완전한 쌍에서 정확 일치 비율과 불일치 항목을 산출한다. 완전쌍 0이면 unknown. 비율을 객관적 정확성으로 해석하지 않는다.

개선 조건: 표본이 충분하고 범주분포를 점검한 뒤 우연 일치를 보정한 지표 검토. 작은 합성 표본으로 신뢰구간 정밀도를 주장하지 않는다.

최소 경로: 독립 점수 파일 → item_id 결합 → 완전쌍과 불일치 목록 → 중재자가 기준 문구를 수정한다.

제약과 우선순위: 목적은 기준 정렬, 최적화 없음. 필수: 동일 자료/독립 평가. 선호: 설명 근거 연결. 누락을 불일치로 자동 세지 않는다.

## 합성 입력과 기대값

[독립 창작 fixture](../../examples/synthetic/rater-disagreement.json)의 각 행은 독립 시험 입력이다. 아래 표는 손계산/규칙 대조한 기대값이다. 작은 계산 검증은 [check_a.py](../../examples/synthetic/check_a.py)에서 실행하며 실제 앱/UI/사용자 검증과 구별한다.

|유형|입력|기대 결과|독립 근거|
|---|---|---|---|
|normal|`{"pairs":[["pass","pass"],["revise","pass"],["unknown","unknown"]]}`|`[2, 3]`|3쌍 중 2일치|
|boundary|`{"pairs":[["pass","pass"]]}`|`[1, 1]`|1쌍 100%이나 표본 작음|
|missing|`{"pairs":[[null,"pass"]]}`|`"unknown"`|완전쌍 0|
|conflict|`{"pairs":[["pass","revise"],["revise","pass"]]}`|`[0, 2]`|평균 같아도 일치 0|
|reorder|`{"pairs":[["unknown","unknown"],["revise","pass"],["pass","pass"]]}`|`[2, 3]`|행순 무관|
|new_sample|`{"pairs":[["revise","revise"],["pass",null],["pass","revise"]]}`|`[1, 2]`|누락쌍 제외|

비교 쌍: normal은 3쌍 중 2일치지만 conflict는 두 평가자의 범주 빈도가 같아도 항목별로 0/2 일치다.

## 오류·도구·범위

일치율 100%를 좋은 루브릭의 증거로 단정하지 않는다. 한쪽 결과를 보고 다른 평가를 수정한 뒤 독립 평가라고 부르지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 외부 패키지/모델/API 없이 작은 데이터를 처리한다. Python 실행이 허용되지 않거나 설치되어 있지 않으면 표를 종이에 계산해 기준 결과부터 확인한다. 설치 실패를 이유로 외부 전송하지 않는다.

연습용 권장 예산: 30분에는 normal과 missing 두 건을 손계산하고 정책을 합의한다. 90분에는 독립 점수 파일 → item_id 결합 → 완전쌍과 불일치 목록 → 중재자가 기준 문구를 수정한다. 180분에는 표본이 충분하고 범주분포를 점검한 뒤 우연 일치를 보정한 지표 검토. 작은 합성 표본으로 신뢰구간 정밀도를 주장하지 않는다. 시간이 부족하면 개선 기능·시각 장식을 줄이고 결측 처리와 경계 검증은 유지한다. 시간은 보장이 아니다.

## 구현물 사용자 피드백

- 불일치 두 항목의 판단 근거를 나란히 볼 수 있습니까?
- 기준 수정 후 새로운 샘플로 다시 평가할 수 있습니까?

## 개발자 설명 연습 — PREP 전용

AI 금지 실제 평가에서는 이 질문을 생성하거나 답변·실시간 코칭을 제공하지 않는다. 아래 질문은 허용된 사전 창작 연습에서 본인이 답하고 실제 파일 증거를 확인하는 용도다.

- 분모에서 제외한 항목은 무엇입니까?
- 일치율과 사실 정확성의 차이를 증거와 함께 설명하십시오.

## 측정과 한계

완전쌍 수·범주별 불일치 수 측정 가능. 학습 효과 또는 채용 성공률 주장 불가.

## 공개 근거

[공식 Python 문서](https://docs.python.org/3/library/collections.html)는 사용한 자료형·계산 기능의 1차 참고다. 업무 상황·수치·정책은 본 카드에서 독립 창작했으며 문서의 실제 업무 사례를 재게시한 것이 아니다. [기준 방법](../../methods/baseline-first.md), [검증](../../methods/verification.md)을 함께 읽는다.
