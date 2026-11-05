# AI 산출물과 본인 확인 범위의 대조

```json
{
  "id": "ai-verification-ledger",
  "title": "AI 산출물과 본인 확인 범위의 대조",
  "family": "COACH",
  "keywords_ko": [
    "AI 산출물과 본인 확인 범위의 대조",
    "verification-accounting"
  ],
  "keywords_en": [
    "verification-accounting",
    "ai-verification-ledger"
  ],
  "problem_structure": "verification-accounting",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 가상 재고 보고서를 만든 개발자가 AI가 작성한 부분과 직접 검사한 부분을 구별해 설명하려 한다.",
  "do_not_use_when": "AI코드를 읽었다는 사실만으로 검증완료라 하지 않는다. 사람 작성코드를 자동정확으로 처리하지 않는다.",
  "data_required": [
    "행=산출물 단위, 키 artifact_id; fixture rows=[id,author,status,evidence], author=ai/human/unknown, status=pass/fail/not_run, evidence는 근거ID/null. 개선=명령/환경/날짜. 개인 대화원문 불필요."
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
  "path": "cases/coach/ai-verification-ledger.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "ai-verification-ledger",
  "test_count": 3,
  "decision_signature": {
    "decision": "AI 산출물과 본인 확인 범위의 대조",
    "input_structure": "행=산출물 단위, 키 artifact_id; fixture rows=[id,author,status,evidence], author=ai/human/unknown, status=pass/fail/not_run, evidence는 근거ID/null. 개선=명령/환경/날짜. 개인 대화원문 불필요.",
    "hard_constraint": "AI코드를 읽었다는 사실만으로 검증완료라 하지 않는다. 사람 작성코드를 자동정확으로 처리하지 않는다.",
    "validation": "AI a만근거있는pass"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 가상 재고 보고서를 만든 개발자가 AI가 작성한 부분과 직접 검사한 부분을 구별해 설명하려 한다.

## 2. 경쟁 가설

도구사용기록누락; 테스트이름만보고검증완료추정; 미확인부분과장. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 검증됨의 기준은 무엇인가? → 실행결과 pass와 근거가 함께 있어야 함.
2. 작성주체를 모르면 어떻게 하나요? → unknown을 남겨 추측하지 않는다.
3. 실제 AI 금지 평가인가? → 질문·답변·코칭 중단.

## 4. 데이터 계약과 부재 대안

행=산출물 단위, 키 artifact_id; fixture rows=[id,author,status,evidence], author=ai/human/unknown, status=pass/fail/not_run, evidence는 근거ID/null. 개선=명령/환경/날짜. 개인 대화원문 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

AI 작성행 중 pass이며 evidence가 있는 것만 verified에, 나머지는 unverified에 분리한다. human 작성은 이 집계대상 밖이며 자동 신뢰하지 않는다. author unknown은 ownership_unknown에 기록.

개선: 요구사항별 검사범위와 남은 반례를 추가하고 실행근거 원문을 로컬 허용작업공간에서 확인한다.

## 6. 최소 구현과 다음 행동

작성/검사기록→교차대조→확인됨/미확인/작성주체불명→개발자가 과장없이 자기 기여 설명. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `ai-verification-ledger` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"rows":[["a","ai","pass","e1"],["b","ai","not_run",null],["c","human","pass","e2"]]}`|`[["a"], ["b"], []]`|AI a만근거있는pass|
|boundary|`{"rows":[["a","ai","pass",null]]}`|`[[], ["a"], []]`|pass라도근거없음|
|missing|`{"rows":[["a","unknown","not_run",null]]}`|`[[], [], ["a"]]`|작성주체미확인|

## 8. 오용·도구·축소

AI코드를 읽었다는 사실만으로 검증완료라 하지 않는다. 사람 작성코드를 자동정확으로 처리하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 요구사항별 검사범위와 남은 반례를 추가하고 실행근거 원문을 로컬 허용작업공간에서 확인한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 미실행 산출물이 검증됨으로 표시되지 않습니까?
- 각 pass에 실행증거를 열 수 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- AI에게 맡긴 일과 직접 검증한 일을 구체적 파일로 구분하십시오.
- pass여도 보장하지 못하는 범위는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
