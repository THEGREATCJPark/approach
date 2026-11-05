# 설명 분량과 필수 근거 유지

```json
{
  "id": "rehearsal-budget",
  "title": "설명 분량과 필수 근거 유지",
  "family": "COACH",
  "keywords_ko": [
    "설명 분량과 필수 근거 유지",
    "compression-review"
  ],
  "keywords_en": [
    "compression-review",
    "rehearsal-budget"
  ],
  "problem_structure": "compression-review",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 합성 공구 예약 앱을 설명하는 연습자가 짧게 말하라는 요청을 받고 근거 문장까지 삭제했다. 분량과 핵심 보존을 따로 점검한다.",
  "do_not_use_when": "짧을수록 좋다는 점수나 자동 모범답안을 제공하지 않는다. 어절수만으로 전달력 향상을 주장하지 않는다.",
  "data_required": [
    "행=연습 초안버전, 키 draft_id; words는 수동 확인한 공백단위 어절수 정수, limit 정수, essential/present는 근거 ID 배열. null present는 의미 확인 미완료. 실제 자연어 추출은 본 시험 범위 밖."
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
  "depth": "standard",
  "path": "cases/coach/rehearsal-budget.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "rehearsal-budget",
  "test_count": 4,
  "decision_signature": {
    "decision": "설명 분량과 필수 근거 유지",
    "input_structure": "행=연습 초안버전, 키 draft_id; words는 수동 확인한 공백단위 어절수 정수, limit 정수, essential/present는 근거 ID 배열. null present는 의미 확인 미완료. 실제 자연어 추출은 본 시험 범위 밖.",
    "hard_constraint": "짧을수록 좋다는 점수나 자동 모범답안을 제공하지 않는다. 어절수만으로 전달력 향상을 주장하지 않는다.",
    "validation": "근거유지되지만20어절초과"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 합성 공구 예약 앱을 설명하는 연습자가 짧게 말하라는 요청을 받고 근거 문장까지 삭제했다. 분량과 핵심 보존을 따로 점검한다.

## 2. 경쟁 가설

장황한 반복; 핵심 근거 삭제; 어절수를 말하기 시간으로 오인. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 제한은 어절수인가 실제 말하기 시간인가? → 시간이라면 직접 녹음 측정.
2. 반드시 남길 근거항목은 무엇인가? → 작성자가 기록과 대조해 essential IDs 지정.
3. 현재 허용된 사전 연습인가? → 실제 AI 금지 평가이면 모든 질문·초안·코칭 중단.

## 4. 데이터 계약과 부재 대안

행=연습 초안버전, 키 draft_id; words는 수동 확인한 공백단위 어절수 정수, limit 정수, essential/present는 근거 ID 배열. null present는 의미 확인 미완료. 실제 자연어 추출은 본 시험 범위 밖.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

필수 ID 누락이면 restore_evidence, 누락 없이 words>limit이면 shorten, 둘 다 충족하면 within_budget. 이는 표현 품질 점수가 아니다.

개선: 직접 말한 시간을 측정하고 반복 문장을 본인이 수정한 뒤 필수 근거를 다시 확인한다.

## 6. 최소 구현과 다음 행동

허용된 초안→어절/근거 체크→수정 우선순위→본인이 자기 말로 재설명. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `rehearsal-budget` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"words":120,"limit":100,"essential":["e1"],"present":["e1"]}`|`"shorten"`|근거유지되지만20어절초과|
|boundary|`{"words":100,"limit":100,"essential":["e1"],"present":["e1"]}`|`"within_budget"`|한도동일허용|
|missing|`{"words":80,"limit":100,"essential":["e1"],"present":null}`|`"unknown"`|내용확인안됨|
|loss|`{"words":80,"limit":100,"essential":["e1"],"present":[]}`|`"restore_evidence"`|짧아도근거누락|

## 8. 오용·도구·축소

짧을수록 좋다는 점수나 자동 모범답안을 제공하지 않는다. 어절수만으로 전달력 향상을 주장하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 직접 말한 시간을 측정하고 반복 문장을 본인이 수정한 뒤 필수 근거를 다시 확인한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 필수 근거가 빠졌음을 표에서 발견할 수 있습니까?
- 이 분량 기준이 실제 연습 목표와 맞습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 분량보다 근거 복원을 우선한 이유는 무엇입니까?
- 어절수와 시간의 차이를 설명하십시오.

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
