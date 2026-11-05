# 시간별 안전 반경과 경계 피해

```json
{
  "id": "shrinking-safe-zone",
  "title": "시간별 안전 반경과 경계 피해",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "시간별",
    "안전",
    "반경과",
    "경계",
    "피해"
  ],
  "keywords_en": [
    "time-dependent-geometry",
    "shrinking-safe-zone"
  ],
  "problem_structure": "time-dependent-geometry",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 탐험 게임의 원형 안전 구역을 시간에 따라 줄이고 경계 밖 플레이어만 피해 대상으로 표시해 달라.",
  "do_not_use_when": "반경을 clamp하지 않아 음수로 만들지 않는다. 점 판정을 캐릭터 전체 충돌로 확대하지 않는다.",
  "data_required": [
    "최소: initial_radius_m, shrink_m_per_s, min_radius_m, elapsed_s, distance_m 모두 비음수; 한 행 player_id의 시점. null 시간/거리 unknown. 개선: 실제 좌표·센터 이동."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "interactive-collision"
  ],
  "depth": "standard",
  "path": "cases/INTERACTIVE/shrinking-safe-zone.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "time-dependent-geometry",
    "input_structure": "최소: initial_radius_m, shrink_m_per_s, min_radius_m, elapsed_s, distance_m 모두 비음수; 한 행 player_id의 시점. null 시간/거리 unknown. 개선: 실제 좌표·센터 이동.",
    "hard_constraint": "반경을 clamp하지 않아 음수로 만들지 않는다. 점 판정을 캐릭터 전체 충돌로 확대하지 않는다.",
    "validation": "반경6,거리7; 최소반경3 경계; 시간 없음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 탐험 게임의 원형 안전 구역을 시간에 따라 줄이고 경계 밖 플레이어만 피해 대상으로 표시해 달라.

가능한 설명: 시간 단위가 다르다; 반경이 음수가 된다; 경계 포함 규칙이 구현마다 다르다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 반경 최솟값은 있습니까? → floor 반영.
2. 경계는 안전합니까? → 본 예제 <= 안전.
3. 피해량 계산까지 필요합니까? → 이번 범위는 대상 판정만, 별도 rate 데이터 필요.

## 3. 데이터 계약과 자료 부족 대안

최소: initial_radius_m, shrink_m_per_s, min_radius_m, elapsed_s, distance_m 모두 비음수; 한 행 player_id의 시점. null 시간/거리 unknown. 개선: 실제 좌표·센터 이동. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: r=max(min_radius,initial-shrink*t), distance<=r이면 safe 아니면 outside.

개선: 여러 축소 단계는 상태표로 정의하고 서버 권위가 필요하면 시간 기준 확정.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

시간·거리 → 현재반경 → safe/outside/unknown → 플레이어가 이동. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"initial_radius_m":10,"shrink_m_per_s":2,"min_radius_m":3,"elapsed_s":2,"distance_m":7}`|`"outside"`|반경6,거리7|
|boundary|`{"initial_radius_m":10,"shrink_m_per_s":2,"min_radius_m":3,"elapsed_s":8,"distance_m":3}`|`"safe"`|최소반경3 경계|
|missing|`{"initial_radius_m":10,"shrink_m_per_s":2,"min_radius_m":3,"elapsed_s":null,"distance_m":3}`|`"unknown"`|시간 없음|

## 7. 흔한 오류와 범위 축소

반경을 clamp하지 않아 음수로 만들지 않는다. 점 판정을 캐릭터 전체 충돌로 확대하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 경계에서 피해가 없는 것이 규칙과 맞습니까?
- 현재 반경과 남은 시간이 이동 판단에 충분합니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 최소반경 이후 시간이 늘어도 결과가 같은 근거는 무엇입니까?
- unknown을 safe로 표시하지 않은 이유는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
