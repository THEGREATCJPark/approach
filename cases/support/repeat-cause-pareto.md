# 반복 문의 원인의 누적 비중

```json
{
  "id": "repeat-cause-pareto",
  "title": "반복 문의 원인의 누적 비중",
  "family": "SUPPORT",
  "keywords_ko": [
    "반복 문의 원인의 누적 비중",
    "pareto"
  ],
  "keywords_en": [
    "pareto",
    "repeat-cause-pareto"
  ],
  "problem_structure": "pareto",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공용 공구함 담당자가 반복 문의의 표준 원인코드를 집계해 먼저 개선할 안내 항목을 정한다.",
  "do_not_use_when": "빈도 상위가 근본 원인이라고 단정하지 않는다. 분모에서 미분류를 조용히 삭제하지 않는다.",
  "data_required": [
    "행=문의 1건, 키 ticket_id; fixture causes는 승인된 주원인 코드 배열, null은 미분류. threshold는 누적 목표 비율 0~1. 개선=처리시간/피해. 고객 ID 불필요."
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
  "path": "cases/support/repeat-cause-pareto.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "repeat-cause-pareto",
  "test_count": 3,
  "decision_signature": {
    "decision": "반복 문의 원인의 누적 비중",
    "input_structure": "행=문의 1건, 키 ticket_id; fixture causes는 승인된 주원인 코드 배열, null은 미분류. threshold는 누적 목표 비율 0~1. 개선=처리시간/피해. 고객 ID 불필요.",
    "hard_constraint": "빈도 상위가 근본 원인이라고 단정하지 않는다. 분모에서 미분류를 조용히 삭제하지 않는다.",
    "validation": "a60%+b20%=80%"
  }
}
```

## 1. 독립 창작 요청

창작: 공용 공구함 담당자가 반복 문의의 표준 원인코드를 집계해 먼저 개선할 안내 항목을 정한다.

## 2. 경쟁 가설

사소한 잦은 문의; 드물지만 큰 피해; 원인코드 미분류. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 빈도가 우선인가 피해가 우선인가? → 피해 우선이면 빈도 Pareto로 결정하지 않는다.
2. 한 문의에 여러 원인이 있습니까? → 본 예제는 주원인1개, 다중이면 분모 정의 변경.
3. unknown을 제외해도 됩니까? → 미분류는 별도 수와 비중으로 공개.

## 4. 데이터 계약과 부재 대안

행=문의 1건, 키 ticket_id; fixture causes는 승인된 주원인 코드 배열, null은 미분류. threshold는 누적 목표 비율 0~1. 개선=처리시간/피해. 고객 ID 불필요.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

## 5. 기준 방법과 개선 조건

원인별 건수 내림차순, 동률 코드순. 전체 관측 건수 기준 목표 비율 이상이 되는 최소 접두 원인 목록을 반환. null 있으면 unknown을 반환하여 분류 보완 요구.

개선: 빈도와 처리시간을 별도 도표로 비교하고 반복 발생의 인과는 업무 관찰로 조사한다.

## 6. 최소 구현과 다음 행동

원인코드→집계/누적비중→개선 후보→담당자가 원문 표본을 확인. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `repeat-cause-pareto` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"causes":["a","a","a","b","c"],"threshold":0.8}`|`["a", "b"]`|a60%+b20%=80%|
|boundary|`{"causes":["a"],"threshold":0}`|`[]`|목표0이면선택없음|
|missing|`{"causes":["a",null],"threshold":0.8}`|`"unknown"`|미분류보완|

## 8. 오용·도구·축소

빈도 상위가 근본 원인이라고 단정하지 않는다. 분모에서 미분류를 조용히 삭제하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 빈도와 처리시간을 별도 도표로 비교하고 반복 발생의 인과는 업무 관찰로 조사한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 상위 원인의 표본이 같은 문제를 뜻합니까?
- 빈도 낮지만 피해 큰 항목을 별도로 볼 수 있습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 누적비중 분모는 무엇입니까?
- 80% 규칙이 보편 법칙이 아닌 이유는 무엇입니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
