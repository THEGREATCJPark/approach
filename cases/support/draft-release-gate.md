# 답변 초안의 발송 전 필수 검토

```json
{
  "id": "draft-release-gate",
  "title": "답변 초안의 발송 전 필수 검토",
  "family": "SUPPORT",
  "keywords_ko": [
    "답변 초안의 발송 전 필수 검토",
    "approval-gate"
  ],
  "keywords_en": [
    "approval-gate",
    "draft-release-gate"
  ],
  "problem_structure": "approval-gate",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 지역 도서 교환소의 안내 초안에 근거문서 확인과 수신자 검토가 빠질 수 있어 발송 승인 전 상태를 표시한다.",
  "do_not_use_when": "모두 체크됐다고 자동 발송하지 않는다. 리뷰어 이름만 있으면 검토 완료로 추정하지 않는다.",
  "data_required": [
    "행=초안 한 버전, 키 draft_id+version; evidence_checked,recipient_checked,policy_checked는 true/false/null. fixture checks 배열 순서가 세 필수항목. 개선=검토자/시각. 고객 메시지 원문은 예제 불필요."
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
  "path": "cases/support/draft-release-gate.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "draft-release-gate",
  "test_count": 5,
  "decision_signature": {
    "decision": "답변 초안의 발송 전 필수 검토",
    "input_structure": "행=초안 한 버전, 키 draft_id+version; evidence_checked,recipient_checked,policy_checked는 true/false/null. fixture checks 배열 순서가 세 필수항목. 개선=검토자/시각. 고객 메시지 원문은 예제 불필요.",
    "hard_constraint": "모두 체크됐다고 자동 발송하지 않는다. 리뷰어 이름만 있으면 검토 완료로 추정하지 않는다.",
    "validation": "필수3항목검토"
  }
}
```

## 1. 독립 창작 요청

창작: 지역 도서 교환소의 안내 초안에 근거문서 확인과 수신자 검토가 빠질 수 있어 발송 승인 전 상태를 표시한다.

## 2. 경쟁 가설

근거검토 누락; 수신자 오류; 초안을 발송완료로 혼동. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 누가 최종 발송권한을 가집니까? → 승인권자 확인 전 ready도 발송 아님.
2. 필수검토와 권장검토는 무엇입니까? → 필수 false는 hold.
3. 검토값 null은 무엇입니까? → 미수행이므로 pending.

## 4. 데이터 계약과 부재 대안

행=초안 한 버전, 키 draft_id+version; evidence_checked,recipient_checked,policy_checked는 true/false/null. fixture checks 배열 순서가 세 필수항목. 개선=검토자/시각. 고객 메시지 원문은 예제 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

계약 보완: checks는 정확히 세 개의 true/false/null이어야 한다. 배열 길이가 다르거나 숫자1 같은 다른 타입이면 invalid다. 누락 관문을 생략한 배열이 ready가 되어서는 안 된다.

## 5. 기준 방법과 개선 조건

false가 하나라도 있으면 hold, false 없이 null 있으면 pending, 모두 true면 ready_for_human_send. empty checks는 invalid. 발송 기능은 없다.

개선: 초안 수정시 기존 승인을 무효화하는 버전 결합과 감사기록을 추가한다.

## 6. 최소 구현과 다음 행동

초안/검토 상태→필수관문→보류 사유→승인권자가 수정 또는 수동 발송 결정. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `draft-release-gate` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"checks":[true,true,true]}`|`"ready_for_human_send"`|필수3항목검토|
|boundary|`{"checks":[true,false,true]}`|`"hold"`|1항목반려|
|missing|`{"checks":[true,null,true]}`|`"pending"`|1항목미검토|

|incomplete_schema|`{"checks":[true]}`|`"invalid"`|필수3관문중2개가누락된배열은승인불가|
|invalid_type|`{"checks":[true,1,true]}`|`"invalid"`|숫자1을검토완료true로해석하지않음|

## 8. 오용·도구·축소

모두 체크됐다고 자동 발송하지 않는다. 리뷰어 이름만 있으면 검토 완료로 추정하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 초안 수정시 기존 승인을 무효화하는 버전 결합과 감사기록을 추가한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 누락 항목을 보고 누가 무엇을 해야 하는지 알겠습니까?
- 초안 변경 후 예전 승인이 남지 않습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- ready와sent를 구별하는 이유는 무엇입니까?
- 관문검사로 답변 내용의 사실성을 보장할 수 있습니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
