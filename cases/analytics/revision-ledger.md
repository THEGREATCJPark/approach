# 정정 파일의 최신 유효 레코드 선택

```json
{
  "id": "revision-ledger",
  "title": "정정 파일의 최신 유효 레코드 선택",
  "family": "ANALYTICS",
  "keywords_ko": [
    "정정 파일의 최신 유효 레코드 선택",
    "version-reconciliation"
  ],
  "keywords_en": [
    "version-reconciliation",
    "revision-ledger"
  ],
  "problem_structure": "version-reconciliation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공동 창고 월보고가 정정될 때마다 파일이 쌓인다. 분석자는 이전 숫자와 정정 숫자를 동시에 더하지 않으려 한다.",
  "do_not_use_when": "모든 행 sum 또는 파일명 사전순을 최신 정의로 쓰지 않는다. 값 누락을 0으로 채우지 않는다.",
  "data_required": [
    "행=report_key의 승인 버전, fixture rows=[key,version,value]; version 양의 정수, value 정수 단위수량. null value는 미확정이며 삭제와 다르다. 키=(key,version). 개선=승인 시각/tombstone. 파일수정일은 대체 기준 아님."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "open-day-rate"
  ],
  "depth": "standard",
  "path": "cases/analytics/revision-ledger.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "revision-ledger",
  "test_count": 4,
  "decision_signature": {
    "decision": "정정 파일의 최신 유효 레코드 선택",
    "input_structure": "행=report_key의 승인 버전, fixture rows=[key,version,value]; version 양의 정수, value 정수 단위수량. null value는 미확정이며 삭제와 다르다. 키=(key,version). 개선=승인 시각/tombstone. 파일수정일은 대체 기준 아님.",
    "hard_constraint": "모든 행 sum 또는 파일명 사전순을 최신 정의로 쓰지 않는다. 값 누락을 0으로 채우지 않는다.",
    "validation": "최신 a12+b3"
  }
}
```

## 1. 독립 창작 요청

창작: 공동 창고 월보고가 정정될 때마다 파일이 쌓인다. 분석자는 이전 숫자와 정정 숫자를 동시에 더하지 않으려 한다.

## 2. 경쟁 가설

동일 키 버전 중복; 같은 버전 상충; 삭제 정정 누락. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 최신은 파일수정일인가 승인 version인가? → 승인 version 기준으로 선택.
2. 삭제 정정은 합계에서 제외하는가? → tombstone이면 제외하되 이력 유지.
3. 같은 version의 값이 다르면? → 임의 선택 대신 conflict.

## 4. 데이터 계약과 부재 대안

행=report_key의 승인 버전, fixture rows=[key,version,value]; version 양의 정수, value 정수 단위수량. null value는 미확정이며 삭제와 다르다. 키=(key,version). 개선=승인 시각/tombstone. 파일수정일은 대체 기준 아님.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

키별 최대 version을 고른 뒤 동일 버전 상충을 검출한다. 선택값 중 null이면 unknown. 본 최소 예제에는 삭제 버전이 없으므로 삭제 요청은 별도 범위.

개선: 승인자와 삭제 사건을 추가하고 이전 보고값에서 얼마나 바뀌었는지 diff를 제공한다.

## 6. 최소 구현과 다음 행동

정정행→키/버전 검증→선택 레코드와 합계→담당자가 정정 근거 승인. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `revision-ledger` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"rows":[["a",1,10],["a",2,12],["b",1,3]]}`|`15`|최신 a12+b3|
|boundary|`{"rows":[["a",1,0],["a",1,0]]}`|`0`|동일 버전 동일값 재전송은 1건|
|missing|`{"rows":[["a",2,null]]}`|`"unknown"`|최신값 미확정|
|conflict|`{"rows":[["a",2,12],["a",2,13]]}`|`"conflict"`|동일 키버전 상충|

## 8. 오용·도구·축소

모든 행 sum 또는 파일명 사전순을 최신 정의로 쓰지 않는다. 값 누락을 0으로 채우지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 승인자와 삭제 사건을 추가하고 이전 보고값에서 얼마나 바뀌었는지 diff를 제공한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 어떤 버전을 선택했는지 추적 가능합니까?
- 승인 전 정정이 합계에 들어가지 않았습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 상충 버전을 조용히 덮지 않은 근거는 무엇입니까?
- 삭제와 미확정 값을 왜 구별합니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
