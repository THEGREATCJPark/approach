# 고정 관측점의 반경 안 표적 집계

```json
{
  "id": "radial-monitor-range",
  "title": "고정 관측점의 반경 안 표적 집계",
  "family": "GEOMETRY",
  "keywords_ko": [
    "고정",
    "관측점의",
    "반경",
    "안",
    "표적",
    "집계"
  ],
  "keywords_en": [
    "radial-coverage",
    "radial-monitor-range"
  ],
  "problem_structure": "radial-coverage",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "야외 조각 정원의 안내 신호기 한 대가 주어진 반경 안의 표적을 몇 개 포함하는지 도면에서 확인해 달라.",
  "do_not_use_when": "반경 안이라는 이유로 실제 감지 성공률을 주장하지 않는다. 위경도 값에 평면 거리 공식을 바로 쓰지 않는다.",
  "data_required": [
    "최소: center=[x,y] m, radius_m>=0, targets=[id,x,y] 고유 ID; 한 행 표적. 좌표 null은 unknown. 개선: 장애물·실측 신호세기. 같은 좌표라도 다른 표적 ID는 별도 대상."
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
  "path": "cases/geometry/radial-monitor-range.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "radial-coverage",
    "input_structure": "최소: center=[x,y] m, radius_m>=0, targets=[id,x,y] 고유 ID; 한 행 표적. 좌표 null은 unknown. 개선: 장애물·실측 신호세기. 같은 좌표라도 다른 표적 ID는 별도 대상.",
    "hard_constraint": "반경 안이라는 이유로 실제 감지 성공률을 주장하지 않는다. 위경도 값에 평면 거리 공식을 바로 쓰지 않는다.",
    "validation": "25<=25,36>25; 같은 점만 거리0; 좌표 없음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

야외 조각 정원의 안내 신호기 한 대가 주어진 반경 안의 표적을 몇 개 포함하는지 도면에서 확인해 달라.

가능한 설명: 유클리드 반경과 보행거리 혼동이다; 경계 표적 포함 규칙 문제다; 실제 차폐를 원형 범위가 대변하지 못한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 직선 거리입니까 이동 거리입니까? → 이동이면 경로 그래프로 변경.
2. 장애물이 있습니까? → 있으면 반경 판정 뒤 별도 시야 검사.
3. 반경 경계를 포함합니까? → 본 예제 <=를 정책에 맞게 변경.

## 3. 데이터 계약과 자료 부족 대안

최소: center=[x,y] m, radius_m>=0, targets=[id,x,y] 고유 ID; 한 행 표적. 좌표 null은 unknown. 개선: 장애물·실측 신호세기. 같은 좌표라도 다른 표적 ID는 별도 대상. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: (x-cx)^2+(y-cy)^2<=r^2를 세어 sqrt 오차 없이 정수 fixture 검증.

개선: 많은 표적에는 공간 인덱스; 실제 수신 보장은 현장 데이터 필요.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

중심·반경·표적 → 제곱거리 → 포함 ID·개수·미확인 → 담당자가 현장 검증 대상 선정. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"center":[0,0],"radius_m":5,"targets":[["u",3,4],["v",6,0]]}`|`1`|25<=25,36>25|
|boundary|`{"center":[2,2],"radius_m":0,"targets":[["u",2,2],["v",2,3]]}`|`1`|같은 점만 거리0|
|missing|`{"center":[0,0],"radius_m":5,"targets":[["u",null,4]]}`|`"unknown"`|좌표 없음|

## 7. 흔한 오류와 범위 축소

반경 안이라는 이유로 실제 감지 성공률을 주장하지 않는다. 위경도 값에 평면 거리 공식을 바로 쓰지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 포함 결과를 보고 다음에 확인할 표적을 고를 수 있습니까?
- 실제 안 보이는 표적의 장애물 정보가 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 3-4-5 경계값은 어떤 독립 계산으로 확인했습니까?
- 직선거리 결과를 보행거리로 쓸 수 없는 이유는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
