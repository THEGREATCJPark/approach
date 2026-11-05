# 설명 수정 후 근거 항목의 회귀 검사

```json
{
  "id": "revision-evidence-loss",
  "title": "설명 수정 후 근거 항목의 회귀 검사",
  "family": "COACH",
  "keywords_ko": [
    "설명 수정 후 근거 항목의 회귀 검사",
    "regression-review"
  ],
  "keywords_en": [
    "regression-review",
    "revision-evidence-loss"
  ],
  "problem_structure": "regression-review",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 가상 수리 일정 프로젝트의 설명을 수정했더니 앞선 초안에 있던 실패 사례와 제한사항이 빠졌다. 승인된 필수 근거 목록으로 수정 전후를 비교한다.",
  "do_not_use_when": "이전 초안이 항상 정답이라고 가정하지 않는다. 새 주장 추가를 자동 개선으로 평가하지 않는다.",
  "data_required": [
    "행=설명 버전쌍, 키 revision_id; required/old/new/known은 근거 ID 집합. fixture는 ID 배열. null new는 새초안 미검토. 실제 문장과 ID 연결은 사람이 확인. 개선=문장 위치와 변경사유."
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
  "path": "cases/coach/revision-evidence-loss.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "revision-evidence-loss",
  "test_count": 3,
  "decision_signature": {
    "decision": "설명 수정 후 근거 항목의 회귀 검사",
    "input_structure": "행=설명 버전쌍, 키 revision_id; required/old/new/known은 근거 ID 집합. fixture는 ID 배열. null new는 새초안 미검토. 실제 문장과 ID 연결은 사람이 확인. 개선=문장 위치와 변경사유.",
    "hard_constraint": "이전 초안이 항상 정답이라고 가정하지 않는다. 새 주장 추가를 자동 개선으로 평가하지 않는다.",
    "validation": "b누락,c미확인,b회귀"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 가상 수리 일정 프로젝트의 설명을 수정했더니 앞선 초안에 있던 실패 사례와 제한사항이 빠졌다. 승인된 필수 근거 목록으로 수정 전후를 비교한다.

## 2. 경쟁 가설

분량축소중근거삭제; 새 주장추가; 필수목록변경. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 이전 초안의 모든 근거가 필수인가? → 승인 required 목록만 대상으로 한다.
2. 새 주장에 근거가 있는가? → known_evidence에 없는 ID는 검토.
3. 현재 실제 AI 금지 평가인가? → 질문·답변·코칭 중단.

## 4. 데이터 계약과 부재 대안

행=설명 버전쌍, 키 revision_id; required/old/new/known은 근거 ID 집합. fixture는 ID 배열. null new는 새초안 미검토. 실제 문장과 ID 연결은 사람이 확인. 개선=문장 위치와 변경사유.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

누락=required−new, 미확인추가=new−known, 복구대상=(required∩old)−new. 정렬된 세 목록을 출력한다. 새 근거의 내용 진실성은 별도 검토.

개선: 담당자가 필수목록 변경을 승인하면 버전별 기준을 고정하고 다시 비교한다.

## 6. 최소 구현과 다음 행동

두 초안 근거태그→집합차이→누락/새주장/회귀목록→개발자가 증거 복원 또는 주장 삭제. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `revision-evidence-loss` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"required":["a","b"],"old":["a","b"],"new":["a","c"],"known":["a","b"]}`|`[["b"], ["c"], ["b"]]`|b누락,c미확인,b회귀|
|boundary|`{"required":[],"old":[],"new":[],"known":[]}`|`[[], [], []]`|빈기준명시|
|missing|`{"required":["a"],"old":["a"],"new":null,"known":["a"]}`|`"unknown"`|새초안태깅안됨|

## 8. 오용·도구·축소

이전 초안이 항상 정답이라고 가정하지 않는다. 새 주장 추가를 자동 개선으로 평가하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 담당자가 필수목록 변경을 승인하면 버전별 기준을 고정하고 다시 비교한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 빠진 필수 근거를 원래 문장에서 찾을 수 있습니까?
- 새 주장에 실제 증거가 붙어 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 회귀와 새 요구 변경을 어떻게 구별했습니까?
- ID일치로 문장 내용까지 검증하지 못하는 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
