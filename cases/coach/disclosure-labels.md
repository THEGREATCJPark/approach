# 설명 자료의 공개 범위 라벨 점검

```json
{
  "id": "disclosure-labels",
  "title": "설명 자료의 공개 범위 라벨 점검",
  "family": "COACH",
  "keywords_ko": [
    "설명 자료의 공개 범위 라벨 점검",
    "information-boundary"
  ],
  "keywords_en": [
    "information-boundary",
    "disclosure-labels"
  ],
  "problem_structure": "information-boundary",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 PREP: 가상의 지역 시설 프로젝트를 발표 연습할 때 내부 전용으로 표시한 화면을 공개 연습자료에 넣으려 한다. 라벨과 목적지를 대조한다.",
  "do_not_use_when": "이름만 지우면 공개 가능하다고 하지 않는다. 이 도구 통과를 개인정보 안전보장으로 표현하지 않는다.",
  "data_required": [
    "행=첨부자료, 키 artifact_id; fixture labels=public/internal/restricted/null 배열, destination=public/internal. null은 권한 미확인. 실제 개인정보 탐지는 별도 수동검토 필요. 개선=승인 근거·만료일."
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
  "path": "cases/coach/disclosure-labels.md",
  "fixture_path": "examples/synthetic/expansion_a.json",
  "fixture_key": "disclosure-labels",
  "test_count": 4,
  "decision_signature": {
    "decision": "설명 자료의 공개 범위 라벨 점검",
    "input_structure": "행=첨부자료, 키 artifact_id; fixture labels=public/internal/restricted/null 배열, destination=public/internal. null은 권한 미확인. 실제 개인정보 탐지는 별도 수동검토 필요. 개선=승인 근거·만료일.",
    "hard_constraint": "이름만 지우면 공개 가능하다고 하지 않는다. 이 도구 통과를 개인정보 안전보장으로 표현하지 않는다.",
    "validation": "내부자료공개불가"
  }
}
```

## 1. 독립 창작 요청

창작 PREP: 가상의 지역 시설 프로젝트를 발표 연습할 때 내부 전용으로 표시한 화면을 공개 연습자료에 넣으려 한다. 라벨과 목적지를 대조한다.

## 2. 경쟁 가설

자료권한 미확인; 내부 화면 혼입; 공개요약을 원문공개로 혼동. 요청 표현만으로 한 원인을 확정하지 않는다.

## 3. 방향을 가르는 질문

1. 자료별 공개권한이 문서화됐는가? → 없으면 review.
2. 대상은 내부연습인가 공개발표인가? → 목적지에 따라 허용집합 변경.
3. AI 금지 실제 평가인가? → 그렇다면 질문·답변·코칭 중단.

## 4. 데이터 계약과 부재 대안

행=첨부자료, 키 artifact_id; fixture labels=public/internal/restricted/null 배열, destination=public/internal. null은 권한 미확인. 실제 개인정보 탐지는 별도 수동검토 필요. 개선=승인 근거·만료일.

최소 필드를 얻지 못하면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다. 입력과 기대값의 필드명은 동일하다. 자료 없음은 0이 아니다.

계약 보완: destination이 public/internal 이외이거나 labels 자체가 null이면 review다. 알 수 없는 목적지를 내부로 취급하지 않는다.

## 5. 기준 방법과 개선 조건

공개 목적지는 public만, 내부 목적지는 public/internal만 통과. restricted면 blocked, null이면 review. empty는 no_material. 권한 라벨의 진실성은 따로 확인한다.

개선: 승인 범위와 구체적 발췌본을 연결하고 공개 전 사람 검토를 수행한다.

## 6. 최소 구현과 다음 행동

연습자료 라벨→목적지 대조→보류/금지목록→작성자가 제외하거나 권한 확인. 출력에는 계산/판정 이유와 미확인 상태를 함께 제공한다.

## 7. 합성 입력·기대값·검증

[fixture](../../examples/synthetic/expansion_a.json)의 `disclosure-labels` 키와 [독립 계산 검사](../../examples/synthetic/check_expansion_a.py)를 사용한다. 생산 앱 구현과 UI를 검증하는 코드는 아니다.

|유형|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"labels":["public","internal"],"destination":"public"}`|`"blocked"`|내부자료공개불가|
|boundary|`{"labels":["public"],"destination":"public"}`|`"within_labels"`|라벨상허용|
|missing|`{"labels":[null],"destination":"public"}`|`"review"`|권한불명|

|unknown_destination|`{"labels":["internal"],"destination":"unknown"}`|`"review"`|목적지불명을내부로간주하지않음|

## 8. 오용·도구·축소

이름만 지우면 공개 가능하다고 하지 않는다. 이 도구 통과를 개인정보 안전보장으로 표현하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 설치 또는 실행이 허용되지 않으면 표와 손계산으로 같은 기대값을 확인한다. 외부 모델·자동전송은 기본 경로에 없다. 시간이 부족하면 승인 범위와 구체적 발췌본을 연결하고 공개 전 사람 검토를 수행한다. 이 개선 범위를 제외하고 최소 입력·미확인 표시·경계 검증을 유지한다.

## 9. 구현물 사용자 피드백

- 금지자료를 실제 목록에서 찾을 수 있습니까?
- 승인 증빙 없는 자료가 통과하지 않습니까?

## 10. 개발자 본인의 사전 설명 연습

PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭 모두 중단한다. 본인이 답한 후 실제 파일·결정·실행증거만 대조한다.

- 라벨검사와 내용검사의 차이는 무엇입니까?
- 내부 승인과 공개 승인을 왜 구별합니까?

## 근거와 한계

[공식 계산 문서](https://docs.python.org/3/library/decimal.html)와 [공식 테스트 문서](https://docs.python.org/3/library/unittest.html)는 구현 기능의 참고다. 업무 상황·정책·숫자는 독립 창작이며 공식 업무정책이 아니다. [기준 방법](../../methods/baseline-first.md)과 [검증](../../methods/verification.md)을 연결해 읽는다. 계산/규칙 기대값은 작은 fixture에서 확인 가능하나 실제 시간절감·사용자 만족·조직효과·자연어 의미판정은 검증하지 않았다. 효과를 주장하려면 실제 사용자 과제와 비교기준·분모를 정해 별도 관찰해야 한다.
