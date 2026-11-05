# 교대 인수인계의 다음 행동 누락

```json
{
  "id": "handoff-action-fields",
  "title": "교대 인수인계의 다음 행동 누락",
  "family": "SUPPORT",
  "keywords_ko": [
    "교대 인수인계의 다음 행동 누락",
    "completeness"
  ],
  "keywords_en": [
    "completeness",
    "handoff-action-fields"
  ],
  "problem_structure": "completeness",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 야간 시설 안내원이 미해결 문의를 다음 근무자에게 넘길 때 배경 설명은 길지만 담당자와 기한이 빠진다.",
  "do_not_use_when": "긴 요약문 생성으로 행동 누락을 숨기지 않는다. 개인정보를 과도하게 요약에 포함하지 않는다.",
  "data_required": [
    "행=인수인계 건, 키 ticket_id; status=open/resolved, next_action/owner/due는 문자열 또는 null. due는 이 예제에서 정규화된 기한 문자열이며 날짜 유효성 검사는 별도. 개선=첨부 근거 링크."
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
  "path": "cases/support/handoff-action-fields.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "handoff-action-fields",
  "test_count": 3,
  "decision_signature": {
    "decision": "교대 인수인계의 다음 행동 누락",
    "input_structure": "행=인수인계 건, 키 ticket_id; status=open/resolved, next_action/owner/due는 문자열 또는 null. due는 이 예제에서 정규화된 기한 문자열이며 날짜 유효성 검사는 별도. 개선=첨부 근거 링크.",
    "hard_constraint": "긴 요약문 생성으로 행동 누락을 숨기지 않는다. 개인정보를 과도하게 요약에 포함하지 않는다.",
    "validation": "필수3필드존재"
  }
}
```

## 1. 독립 창작 요청

창작: 야간 시설 안내원이 미해결 문의를 다음 근무자에게 넘길 때 배경 설명은 길지만 담당자와 기한이 빠진다.

## 2. 경쟁 가설

다음 행동 누락; 책임자 미지정; 완료건과 미해결건 혼재. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 해결된 건도 같은 필드를 요구합니까? → 아니면 resolved는 archive_ready.
2. 기한 없음은 무기한인가 미정인가? → 명시적 정책 값과 null 분리.
3. 담당자는 사람 이름인가 역할인가? → 권한 있는 역할키 사용.

## 4. 데이터 계약과 부재 대안

행=인수인계 건, 키 ticket_id; status=open/resolved, next_action/owner/due는 문자열 또는 null. due는 이 예제에서 정규화된 기한 문자열이며 날짜 유효성 검사는 별도. 개선=첨부 근거 링크.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

open은 세 필드 존재를 검사해 missing 목록, 모두 있으면 handoff_ready. resolved는 archive_ready. 내용 적절성을 존재 검사만으로 판단하지 않는다.

개선: 기한 시간대와 역할의 실제 가용성을 검증하고 수신자가 인수 확인할 상태를 추가한다.

## 6. 최소 구현과 다음 행동

인수인계 메모→필드 추출을 사람 확인→누락 목록→현재 담당자가 보완 후 전달. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `handoff-action-fields` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"status":"open","next_action":"재고 확인","owner":"desk","due":"2031-01-02"}`|`"handoff_ready"`|필수3필드존재|
|boundary|`{"status":"resolved","next_action":null,"owner":null,"due":null}`|`"archive_ready"`|완료건별도|
|missing|`{"status":"open","next_action":"재고 확인","owner":null,"due":null}`|`["owner", "due"]`|책임자기한누락|

## 8. 오용·도구·축소

긴 요약문 생성으로 행동 누락을 숨기지 않는다. 개인정보를 과도하게 요약에 포함하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 기한 시간대와 역할의 실제 가용성을 검증하고 수신자가 인수 확인할 상태를 추가한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 추가 질문 없이 첫 행동을 할 수 있습니까?
- 담당 역할과 기한을 실제 운영표에서 찾을 수 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 필드 존재 검사가 보장하지 않는 것은 무엇입니까?
- 완료건을 다르게 처리한 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
