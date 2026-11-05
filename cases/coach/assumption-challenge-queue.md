# 근거가 약한 가정의 사전 설명 점검 순서

```json
{
  "id": "assumption-challenge-queue",
  "title": "근거가 약한 가정의 사전 설명 점검 순서",
  "family": "COACH",
  "keywords_ko": [
    "근거가 약한 가정의 사전 설명 점검 순서",
    "risk-first"
  ],
  "keywords_en": [
    "risk-first",
    "assumption-challenge-queue"
  ],
  "problem_structure": "risk-first",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 창작 배송 분류 도구를 만든 개발자가 모든 결정을 같은 시간으로 설명 연습하지 않고, 틀리면 설계를 바꿔야 하는 가정부터 점검한다.",
  "do_not_use_when": "점수곱을 객관적 위험확률로 해석하지 않는다. 실제 평가 질문을 예측하거나 답을 생성하지 않는다.",
  "data_required": [
    "행=가정, 키 assumption_id; fixture rows=[id,impact,uncertainty], 각 점수 정수1~3의 합의된 서열. null은 미평가. 개선=가정별 검증로그. 점수곱은 보정된 위험확률 아님."
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
  "path": "cases/coach/assumption-challenge-queue.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "assumption-challenge-queue",
  "test_count": 3,
  "decision_signature": {
    "decision": "근거가 약한 가정의 사전 설명 점검 순서",
    "input_structure": "행=가정, 키 assumption_id; fixture rows=[id,impact,uncertainty], 각 점수 정수1~3의 합의된 서열. null은 미평가. 개선=가정별 검증로그. 점수곱은 보정된 위험확률 아님.",
    "hard_constraint": "점수곱을 객관적 위험확률로 해석하지 않는다. 실제 평가 질문을 예측하거나 답을 생성하지 않는다.",
    "validation": "6>4"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 창작 배송 분류 도구를 만든 개발자가 모든 결정을 같은 시간으로 설명 연습하지 않고, 틀리면 설계를 바꿔야 하는 가정부터 점검한다.

## 2. 경쟁 가설

핵심가정미검증; 영향작은구현설명과다; 점수를성공확률로오인. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. impact와uncertainty는 누가 정의했는가? → 임의점수면 토론용 순서로만 사용.
2. 이미 반증된 가정은 무엇인가? → 연습보다 설계 수정 우선.
3. AI 금지 후속 평가인가? → 질문생성·답변·코칭 중단.

## 4. 데이터 계약과 부재 대안

행=가정, 키 assumption_id; fixture rows=[id,impact,uncertainty], 각 점수 정수1~3의 합의된 서열. null은 미평가. 개선=가정별 검증로그. 점수곱은 보정된 위험확률 아님.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

토론용 우선순위 impact×uncertainty 내림차순, 동률 ID순. 미평가 있으면 unknown으로 담당자 합의 요구. 출력은 점검순서이며 답변 초안을 만들지 않는다.

개선: 검증비용과 되돌릴 수 없는 영향을 별도 열로 검토하고 우선순위 민감도를 확인한다.

## 6. 최소 구현과 다음 행동

합성 결정로그→가정/점수합의→점검순서→본인이 증거를 찾아 설명. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `assumption-challenge-queue` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"rows":[["a",3,2],["b",2,2]]}`|`["a", "b"]`|6>4|
|boundary|`{"rows":[["b",2,2],["a",2,2]]}`|`["a", "b"]`|동점ID순|
|missing|`{"rows":[["a",3,null]]}`|`"unknown"`|불확실성미평가|

## 8. 오용·도구·축소

점수곱을 객관적 위험확률로 해석하지 않는다. 실제 평가 질문을 예측하거나 답을 생성하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 검증비용과 되돌릴 수 없는 영향을 별도 열로 검토하고 우선순위 민감도를 확인한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 첫 가정이 틀리면 설계가 실제로 바뀝니까?
- 동점 가정의 순서가 업무상 중요한가요?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 왜 이 가정부터 확인했는지 실제 로그로 설명하십시오.
- 점수체계의 한계는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
