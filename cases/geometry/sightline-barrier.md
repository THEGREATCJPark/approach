# 직선 시야와 차폐판의 앞뒤

```json
{
  "id": "sightline-barrier",
  "title": "직선 시야와 차폐판의 앞뒤",
  "family": "GEOMETRY",
  "keywords_ko": [
    "직선",
    "시야와",
    "차폐판의",
    "앞뒤"
  ],
  "keywords_en": [
    "visibility",
    "sightline-barrier"
  ],
  "problem_structure": "visibility",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "작은 식물 표본 전시실에서 같은 높이의 표시등이 차폐판 뒤에서도 보이는지 설치 전에 계산해 달라.",
  "do_not_use_when": "표적 뒤의 판까지 가림으로 세지 않는다. Shapely union만 호출해 시야를 해결했다고 주장하지 않는다.",
  "data_required": [
    "최소: 단일 관측 x=0, target_x 양의 m, barrier_x 배열 m; 행은 한 시선, 키 sight_id. null 배열은 미측정이며 []는 차폐판 없음. 개선: 높이·투과율. 축 원점이 없으면 거리 추정 대신 보류."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rectangle-union"
  ],
  "depth": "standard",
  "path": "cases/geometry/sightline-barrier.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "visibility",
    "input_structure": "최소: 단일 관측 x=0, target_x 양의 m, barrier_x 배열 m; 행은 한 시선, 키 sight_id. null 배열은 미측정이며 []는 차폐판 없음. 개선: 높이·투과율. 축 원점이 없으면 거리 추정 대신 보류.",
    "hard_constraint": "표적 뒤의 판까지 가림으로 세지 않는다. Shapely union만 호출해 시야를 해결했다고 주장하지 않는다.",
    "validation": "3은 (0,8] 안; 9는 표적 뒤; 미측정은 빈 목록 아님"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

작은 식물 표본 전시실에서 같은 높이의 표시등이 차폐판 뒤에서도 보이는지 설치 전에 계산해 달라.

가능한 설명: 표시등 자체가 범위 밖일 수 있다; 관측점과 표시등 사이 차폐판이 가릴 수 있다; 실제 높이 차이가 누락됐을 수 있다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 동일 높이·수평선 가정이 맞습니까? → 아니면 2D/3D 시선 교차 모델로 변경.
2. 차폐판 경계에 닿아도 가림입니까? → 예이면 닫힌 구간으로 판정.
3. 투명판도 차폐입니까? → 투과 정보가 없으면 해당 판정 보류.

## 3. 데이터 계약과 자료 부족 대안

최소: 단일 관측 x=0, target_x 양의 m, barrier_x 배열 m; 행은 한 시선, 키 sight_id. null 배열은 미측정이며 []는 차폐판 없음. 개선: 높이·투과율. 축 원점이 없으면 거리 추정 대신 보류. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 0 < barrier_x <= target_x인 판이 있으면 blocked, 없으면 visible. 현 예제는 수평 1차원 투영으로 한정.

개선: 높이와 다각형이 제공되면 ray와 polygon 교차로 확장; 단순 면적 차집합은 시야가 아니다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

관측/표적/차폐 x 입력 → 구간 포함 검사 → 막은 판 위치와 visible/blocked/unknown → 담당자가 측정 높이를 확인. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"target_x":8,"barrier_x":[3,11]}`|`"blocked"`|3은 (0,8] 안|
|boundary|`{"target_x":8,"barrier_x":[9]}`|`"visible"`|9는 표적 뒤|
|missing|`{"target_x":8,"barrier_x":null}`|`"unknown"`|미측정은 빈 목록 아님|

## 7. 흔한 오류와 범위 축소

표적 뒤의 판까지 가림으로 세지 않는다. Shapely union만 호출해 시야를 해결했다고 주장하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- blocked로 표시한 판이 실제 시선 앞에 있습니까?
- 높이 차이로 재측정할 표적은 무엇입니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 표적 뒤의 판을 제외한 기대값 근거는 어디 있습니까?
- 이 1차원 결과가 실제 가시성을 보장하지 않는 조건은 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
