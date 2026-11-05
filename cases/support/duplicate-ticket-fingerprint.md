# 명시적 키로 중복 접수 후보 묶기

```json
{
  "id": "duplicate-ticket-fingerprint",
  "title": "명시적 키로 중복 접수 후보 묶기",
  "family": "SUPPORT",
  "keywords_ko": [
    "명시적 키로 중복 접수 후보 묶기",
    "deduplication"
  ],
  "keywords_en": [
    "deduplication",
    "duplicate-ticket-fingerprint"
  ],
  "problem_structure": "deduplication",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 자전거 수리 예약의 반복 제출을 접수번호가 아닌 고객토큰·예약일·증상코드로 묶어 담당자가 확인한다.",
  "do_not_use_when": "문자열 이어붙이기 충돌이나 이름 유사도만으로 같은 사람 판정 금지. 반복 문의와 재시도 중복은 다르다.",
  "data_required": [
    "행=접수, 키 ticket_id; fixture rows=[ticket_id,customer_token,date,issue_code]. 날짜는 ISO일, null 키는 unknown. 개인정보 대신 합성 토큰. 개선=차량키. 토큰/날짜/코드 정확 일치만 그룹."
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
  "path": "cases/support/duplicate-ticket-fingerprint.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "duplicate-ticket-fingerprint",
  "test_count": 5,
  "decision_signature": {
    "decision": "명시적 키로 중복 접수 후보 묶기",
    "input_structure": "행=접수, 키 ticket_id; fixture rows=[ticket_id,customer_token,date,issue_code]. 날짜는 ISO일, null 키는 unknown. 개인정보 대신 합성 토큰. 개선=차량키. 토큰/날짜/코드 정확 일치만 그룹.",
    "hard_constraint": "문자열 이어붙이기 충돌이나 이름 유사도만으로 같은 사람 판정 금지. 반복 문의와 재시도 중복은 다르다.",
    "validation": "같은3필드 a,b만 후보"
  }
}
```

## 1. 독립 창작 요청

창작: 자전거 수리 예약의 반복 제출을 접수번호가 아닌 고객토큰·예약일·증상코드로 묶어 담당자가 확인한다.

## 2. 경쟁 가설

재시도 제출; 같은 날 다른 고장; 키 누락. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 같은 증상코드면 동일 사건입니까? → 아니면 자동병합 금지하고 후보만 제시.
2. 같은 날 다른 차량도 있습니까? → 차량키를 계약에 추가.
3. 오타를 허용해 묶어야 합니까? → fuzzy는 오병합 평가셋 마련 후.

## 4. 데이터 계약과 부재 대안

행=접수, 키 ticket_id; fixture rows=[ticket_id,customer_token,date,issue_code]. 날짜는 ISO일, null 키는 unknown. 개인정보 대신 합성 토큰. 개선=차량키. 토큰/날짜/코드 정확 일치만 그룹.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

계약 보완: ticket_id는 기본키다. 같은 키·같은 payload의 재전송은 한 건으로 정규화하고 같은 키·다른 payload는 conflict로 반환한다. 그 후 서로 다른 ticket_id의 접수만 중복 후보로 묶는다.

## 5. 기준 방법과 개선 조건

세 필드 tuple을 정규 키로 사용해 ticket_id 목록을 묶는다. 그룹은 중복 후보이며 원문 삭제·자동 취소를 하지 않는다. 모든 비교키가 있어야 한다.

개선: 차량키·기간창을 합의하고 잘못 묶인 후보 비율을 확인한 뒤 유사도 탐색을 별도 도입한다.

## 6. 최소 구현과 다음 행동

접수행→정확키 그룹→2건 이상 후보→담당자가 병합 여부 확인. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `duplicate-ticket-fingerprint` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"rows":[["a","u","2031-01-01","flat"],["b","u","2031-01-01","flat"],["c","u","2031-01-01","brake"]]}`|`[["a", "b"]]`|같은3필드 a,b만 후보|
|boundary|`{"rows":[["a","u","2031-01-01","flat"]]}`|`[]`|1건은중복아님|
|missing|`{"rows":[["a",null,"2031-01-01","flat"]]}`|`"unknown"`|토큰미확인|

|replay|`{"rows":[["a","u","2031-01-01","flat"],["a","u","2031-01-01","flat"]]}`|`[]`|동일ticket재전송은한건|
|key_conflict|`{"rows":[["a","u","2031-01-01","flat"],["a","u","2031-01-01","brake"]]}`|`"conflict"`|같은ticket다른payload는충돌|

## 8. 오용·도구·축소

문자열 이어붙이기 충돌이나 이름 유사도만으로 같은 사람 판정 금지. 반복 문의와 재시도 중복은 다르다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 차량키·기간창을 합의하고 잘못 묶인 후보 비율을 확인한 뒤 유사도 탐색을 별도 도입한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 이 후보가 실제 같은 사건인지 비교할 자료가 있습니까?
- 서로 다른 차량이 섞이지 않았습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 정확키 그룹을 자동병합으로 확장하지 않은 이유는 무엇입니까?
- 누락키를 하나의 중복 그룹으로 모으면 어떤 오류가 생깁니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
