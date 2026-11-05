# 보고서 수치의 출처 연결 누락 찾기

```json
{
  "id": "report-source-coverage",
  "title": "보고서 수치의 출처 연결 누락 찾기",
  "family": "ANALYTICS",
  "keywords_ko": [
    "보고서 수치의 출처 연결 누락 찾기",
    "traceability"
  ],
  "keywords_en": [
    "traceability",
    "report-source-coverage"
  ],
  "problem_structure": "traceability",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 공연장 운영 보고서의 각 숫자가 어느 집계 파일에서 왔는지 편집자가 확인한다.",
  "do_not_use_when": "링크 100%를 보고서 정확도 100%로 표시하지 않는다. 검색 결과만 보고 출처를 읽었다고 기록하지 않는다.",
  "data_required": [
    "행=수치 주장, 키 claim_id; fixture links=[claim_id,source_id], available는 로컬 출처 ID 목록. null source_id는 미연결. 파일 내용 사실성은 별도. 개선=페이지/셀/버전. 사람 이름 불필요."
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
  "path": "cases/analytics/report-source-coverage.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "report-source-coverage",
  "test_count": 3,
  "decision_signature": {
    "decision": "보고서 수치의 출처 연결 누락 찾기",
    "input_structure": "행=수치 주장, 키 claim_id; fixture links=[claim_id,source_id], available는 로컬 출처 ID 목록. null source_id는 미연결. 파일 내용 사실성은 별도. 개선=페이지/셀/버전. 사람 이름 불필요.",
    "hard_constraint": "링크 100%를 보고서 정확도 100%로 표시하지 않는다. 검색 결과만 보고 출처를 읽었다고 기록하지 않는다.",
    "validation": "2주장 중1출처 존재"
  }
}
```

## 1. 독립 창작 요청

창작: 작은 공연장 운영 보고서의 각 숫자가 어느 집계 파일에서 왔는지 편집자가 확인한다.

## 2. 경쟁 가설

출처 링크 누락; 오래된 파일; 원문을 읽지 않은 인용. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 출처 존재와 수치 검증을 구별합니까? → coverage와 verified를 별도 열.
2. 모든 문장이 출처 대상인가? → 사실 수치 주장만 분모로 합의.
3. 여러 출처 충돌은 누가 해결합니까? → 담당 검토로 보류.

## 4. 데이터 계약과 부재 대안

행=수치 주장, 키 claim_id; fixture links=[claim_id,source_id], available는 로컬 출처 ID 목록. null source_id는 미연결. 파일 내용 사실성은 별도. 개선=페이지/셀/버전. 사람 이름 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

각 주장 source_id가 존재하는지 확인해 linked/total과 missing ID를 반환한다. 빈 주장 목록은 no_claims. 모든 source ID가 있어도 사실성 검증 완료가 아니다.

개선: 원본 셀 위치와 재계산 근거를 연결한 뒤 사람이 내용 일치를 점검한다.

## 6. 최소 구현과 다음 행동

주장 목록→출처 존재 검사→미연결 목록→편집자가 근거를 추가하거나 주장을 철회. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `report-source-coverage` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"links":[["a","s1"],["b","s2"]],"available":["s1"]}`|`[1, 2, ["b"]]`|2주장 중1출처 존재|
|boundary|`{"links":[],"available":[]}`|`"no_claims"`|0/0을100%로 표시하지 않음|
|missing|`{"links":[["a",null]],"available":["s1"]}`|`[0, 1, ["a"]]`|미연결1건|

## 8. 오용·도구·축소

링크 100%를 보고서 정확도 100%로 표시하지 않는다. 검색 결과만 보고 출처를 읽었다고 기록하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 원본 셀 위치와 재계산 근거를 연결한 뒤 사람이 내용 일치를 점검한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 누락된 주장만 빠르게 찾아 수정할 수 있습니까?
- 존재하지만 적용 기간이 다른 출처를 표시할 곳이 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 검증 범위가 링크 존재에 그치는 이유는 무엇입니까?
- 주장 분모를 어떻게 정의했습니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
