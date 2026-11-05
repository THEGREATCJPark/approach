# 모든 점검 구역을 덮는 최소 설치비

```json
{
  "id": "minimum-cover-cost",
  "title": "모든 점검 구역을 덮는 최소 설치비",
  "family": "GEOMETRY",
  "keywords_ko": [
    "모든",
    "점검",
    "구역을",
    "덮는",
    "최소",
    "설치비"
  ],
  "keywords_en": [
    "set-cover",
    "minimum-cover-cost"
  ],
  "problem_structure": "set-cover",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "수장고의 필수 점검 구역 세 곳을 모두 덮도록 센서 후보를 선택하되 설치비가 가장 적은 조합을 제시해 달라.",
  "do_not_use_when": "커버 수가 많아도 필수 한 곳이 빠지면 탈락. 후보 20개 이상이면 연습 열거를 중단하고 축소/solver를 검토.",
  "data_required": [
    "최소: required 구역 ID 배열, candidates=[id,cost,covers] 후보 행, cost 정수 토큰, id 고유. null covers는 unknown. [] required는 필수구역 없음. 개선: 정비비·신뢰도. 커버 표 없으면 현장 확인."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "budget-cover"
  ],
  "depth": "standard",
  "path": "cases/geometry/minimum-cover-cost.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "set-cover",
    "input_structure": "최소: required 구역 ID 배열, candidates=[id,cost,covers] 후보 행, cost 정수 토큰, id 고유. null covers는 unknown. [] required는 필수구역 없음. 개선: 정비비·신뢰도. 커버 표 없으면 현장 확인.",
    "hard_constraint": "커버 수가 많아도 필수 한 곳이 빠지면 탈락. 후보 20개 이상이면 연습 열거를 중단하고 축소/solver를 검토.",
    "validation": "b+c 비용 1+2 < a의4; 빈 집합 비용0; 미확인 커버를 빈 집합으로 간주하지 않음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

수장고의 필수 점검 구역 세 곳을 모두 덮도록 센서 후보를 선택하되 설치비가 가장 적은 조합을 제시해 달라.

가능한 설명: 전체 필수 구역을 빠뜨린 계획일 수 있다; 비용 목적과 최대 커버 목적이 혼동됐을 수 있다; 표에 없는 구역이 필수일 수 있다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 모든 구역이 필수입니까? → 일부 선호이면 예산 최대피복으로 변경.
2. 비용에 유지비도 포함합니까? → 포함 시 동일 기간 총비용으로 재계산.
3. 중복 감지가 필수입니까? → 예이면 1회 커버 대신 요구 횟수 제약.

## 3. 데이터 계약과 자료 부족 대안

최소: required 구역 ID 배열, candidates=[id,cost,covers] 후보 행, cost 정수 토큰, id 고유. null covers는 unknown. [] required는 필수구역 없음. 개선: 정비비·신뢰도. 커버 표 없으면 현장 확인. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 후보 부분집합을 열거해 required를 모두 포함하는 합집합만 남기고 비용 최소, 동률 ID 순. 가능한 조합 없으면 infeasible.

개선: 후보 증가 시 set cover 정수계획. 시간 제한의 미발견과 불가능 증명을 구분.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

필수구역·후보표 → 비용 최소 선택 → 비용·미커버·상태 → 담당자가 설치 승인. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"required":["u","v"],"candidates":[["a",4,["u","v"]],["b",1,["u"]],["c",2,["v"]]]}`|`3`|b+c 비용 1+2 < a의4|
|boundary|`{"required":[],"candidates":[["a",4,["u"]]]}`|`0`|빈 집합 비용0|
|missing|`{"required":["u"],"candidates":[["a",2,null]]}`|`"unknown"`|미확인 커버를 빈 집합으로 간주하지 않음|

## 7. 흔한 오류와 범위 축소

커버 수가 많아도 필수 한 곳이 빠지면 탈락. 후보 20개 이상이면 연습 열거를 중단하고 축소/solver를 검토. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 필수구역 집합에서 제외하면 안 되는 구역은 맞습니까?
- 설치비 외에 결정이 바뀌는 비용이 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 예산 최대피복과 이 목적의 차이를 입력으로 설명하십시오.
- infeasible을 증명한 탐색 범위는 어디에 기록했습니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
