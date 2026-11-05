# 두 언어 설명의 수치와 단위 일치

```json
{
  "id": "bilingual-quantity",
  "title": "두 언어 설명의 수치와 단위 일치",
  "family": "COACH",
  "keywords_ko": [
    "두 언어 설명의 수치와 단위 일치",
    "semantic-consistency"
  ],
  "keywords_en": [
    "semantic-consistency",
    "bilingual-quantity"
  ],
  "problem_structure": "semantic-consistency",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 합성 프로젝트 설명을 다른 언어로 바꾸는 과정에서 2분이 2초로 바뀌었다. 문장 전체 번역 품질과 별개로 구조화 수치 의미를 대조한다.",
  "do_not_use_when": "숫자 문자열만 같다고 번역을 승인하지 않는다. 미지원 단위는 추정하지 않는다.",
  "data_required": [
    "행=동일 주장 번역쌍, 키 claim_id; a,b=[수치,단위]이며 수치는 십진수, 단위 s/min. same_scope는 사람이 범위/긍정부정 대조한 bool. null 단위는 unknown. 의미파싱 자체는 구현하지 않는다."
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
  "path": "cases/coach/bilingual-quantity.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "bilingual-quantity",
  "test_count": 4,
  "decision_signature": {
    "decision": "두 언어 설명의 수치와 단위 일치",
    "input_structure": "행=동일 주장 번역쌍, 키 claim_id; a,b=[수치,단위]이며 수치는 십진수, 단위 s/min. same_scope는 사람이 범위/긍정부정 대조한 bool. null 단위는 unknown. 의미파싱 자체는 구현하지 않는다.",
    "hard_constraint": "숫자 문자열만 같다고 번역을 승인하지 않는다. 미지원 단위는 추정하지 않는다.",
    "validation": "2×60=120"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 합성 프로젝트 설명을 다른 언어로 바꾸는 과정에서 2분이 2초로 바뀌었다. 문장 전체 번역 품질과 별개로 구조화 수치 의미를 대조한다.

## 2. 경쟁 가설

단위변환누락; 부정/범위오역; 숫자반올림차이. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 수치는 같은 기간/대상인가? → 아니면 비교 보류.
2. 단위표가 합의됐는가? → 본 예제는 s/min만 변환.
3. 실제 AI 금지 평가인가? → 질문·번역답변·실시간코칭 중단.

## 4. 데이터 계약과 부재 대안

행=동일 주장 번역쌍, 키 claim_id; a,b=[수치,단위]이며 수치는 십진수, 단위 s/min. same_scope는 사람이 범위/긍정부정 대조한 bool. null 단위는 unknown. 의미파싱 자체는 구현하지 않는다.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

동일 범위를 확인한 뒤 초 단위로 환산해 같으면 quantity_match, 다르면 quantity_mismatch. same_scope=false는 semantic_review. 문장 의미 전체의 일치를 보장하지 않는다.

개선: 허용된 사전 연습에서 사람이 부정·조건·대상을 추가 대조하고 수정 이력을 남긴다.

## 6. 최소 구현과 다음 행동

번역쌍 수동구조화→단위변환→차이표→작성자가 원문 근거를 보며 수정. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `bilingual-quantity` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"a":[2,"min"],"b":[120,"s"],"same_scope":true}`|`"quantity_match"`|2×60=120|
|boundary|`{"a":[0,"min"],"b":[0,"s"],"same_scope":true}`|`"quantity_match"`|0변환|
|missing|`{"a":[2,null],"b":[120,"s"],"same_scope":true}`|`"unknown"`|단위미확인|
|conflict|`{"a":[2,"min"],"b":[2,"s"],"same_scope":true}`|`"quantity_mismatch"`|120≠2|

## 8. 오용·도구·축소

숫자 문자열만 같다고 번역을 승인하지 않는다. 미지원 단위는 추정하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 허용된 사전 연습에서 사람이 부정·조건·대상을 추가 대조하고 수정 이력을 남긴다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 단위 오류를 어느 문장에서 고쳐야 하는지 알겠습니까?
- 범위가 다른 주장을 비교에서 분리했습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 2분과120초를 어떤 계산으로 대조했습니까?
- 수치 일치가 번역 정확도와 다른 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
