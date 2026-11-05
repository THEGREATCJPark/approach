# 분류 규칙이 겹치는 문의의 검토 대기

```json
{
  "id": "support-rule-overlap",
  "title": "분류 규칙이 겹치는 문의의 검토 대기",
  "family": "SUPPORT",
  "keywords_ko": [
    "분류 규칙이 겹치는 문의의 검토 대기",
    "rule-classification"
  ],
  "keywords_en": [
    "rule-classification",
    "support-rule-overlap"
  ],
  "problem_structure": "rule-classification",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 수선 접수 담당자가 양식에 표시된 고장·배송·결제 태그로 담당 팀을 정하지만 한 문의가 두 규칙에 걸린다.",
  "do_not_use_when": "첫 번째 문자열 매치로 팀을 확정하지 않는다. 자연어 분류 정확도는 태그 fixture로 검증되지 않는다.",
  "data_required": [
    "행=문의, 키 ticket_id; tags는 검토된 문자열 배열 또는 null. rules는 이 사례에서 damage→repair,delivery→logistics,payment→billing 고정. 빈 배열은 태그없음, null은 미수집. 개선=승인 우선순위."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "repair-slack"
  ],
  "depth": "standard",
  "path": "cases/support/support-rule-overlap.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "support-rule-overlap",
  "test_count": 4,
  "decision_signature": {
    "decision": "분류 규칙이 겹치는 문의의 검토 대기",
    "input_structure": "행=문의, 키 ticket_id; tags는 검토된 문자열 배열 또는 null. rules는 이 사례에서 damage→repair,delivery→logistics,payment→billing 고정. 빈 배열은 태그없음, null은 미수집. 개선=승인 우선순위.",
    "hard_constraint": "첫 번째 문자열 매치로 팀을 확정하지 않는다. 자연어 분류 정확도는 태그 fixture로 검증되지 않는다.",
    "validation": "한팀 매칭"
  }
}
```

## 1. 독립 창작 요청

창작: 수선 접수 담당자가 양식에 표시된 고장·배송·결제 태그로 담당 팀을 정하지만 한 문의가 두 규칙에 걸린다.

## 2. 경쟁 가설

복합 문의; 잘못된 태그; 규칙 우선순위 없음. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 여러 팀 조건이면 다중 이관인가 주 담당 하나인가? → 하나면 승인된 우선순위 필요.
2. 태그는 고객 입력인가 검토 완료인가? → 미검토면 자동 실행 대신 제안.
3. 빈 태그는 일반 문의인가 미입력인가? → 미입력이면 unknown.

## 4. 데이터 계약과 부재 대안

행=문의, 키 ticket_id; tags는 검토된 문자열 배열 또는 null. rules는 이 사례에서 damage→repair,delivery→logistics,payment→billing 고정. 빈 배열은 태그없음, null은 미수집. 개선=승인 우선순위.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

매칭된 서로 다른 팀이 1개면 팀 제안, 0이면 unclassified, 2개 이상이면 review. 모르는 태그를 억지로 기존 팀에 배정하지 않는다.

개선: 승인 우선순위와 복합 문의 분할 절차가 확인되면 명시적 결정표로 확장한다.

## 6. 최소 구현과 다음 행동

검토 태그→규칙 매칭→제안팀 또는 검토 이유→담당자가 이관 승인. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `support-rule-overlap` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"tags":["damage"]}`|`"repair"`|한팀 매칭|
|boundary|`{"tags":[]}`|`"unclassified"`|태그가 비어있음|
|missing|`{"tags":null}`|`"unknown"`|태그 미수집|
|conflict|`{"tags":["damage","delivery"]}`|`"review"`|두팀 겹침|

## 8. 오용·도구·축소

첫 번째 문자열 매치로 팀을 확정하지 않는다. 자연어 분류 정확도는 태그 fixture로 검증되지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 승인 우선순위와 복합 문의 분할 절차가 확인되면 명시적 결정표로 확장한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 복합 건의 주 담당을 누가 결정합니까?
- 미분류 건이 업무에서 사라지지 않습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 겹친 규칙이 왜 정상 예외 결과입니까?
- 태그 기반 검사와 자연어 이해를 어떻게 구별했습니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
