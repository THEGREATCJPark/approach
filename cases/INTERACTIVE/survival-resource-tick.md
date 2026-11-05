# 경과 시간에 따른 산소 자원 소모

```json
{
  "id": "survival-resource-tick",
  "title": "경과 시간에 따른 산소 자원 소모",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "경과",
    "시간에",
    "따른",
    "산소",
    "자원",
    "소모"
  ],
  "keywords_en": [
    "time-step",
    "survival-resource-tick"
  ],
  "problem_structure": "time-step",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 잠수 연습 게임에서 프레임 수가 달라도 같은 실제 경과시간이면 산소 잔량이 같도록 만들어 달라.",
  "do_not_use_when": "프레임 수를 초로 취급하지 않는다. 생존 밸런스를 단위 테스트만으로 검증했다고 말하지 않는다.",
  "data_required": [
    "최소: oxygen 정수 단위, rate 초당 단위, elapsed_s>=0, paused bool; 행은 한 tick, tick_id. null elapsed는 unknown. 개선: 프레임 누락·서버 권위. 단위 불명확하면 실제 게임 밸런스 보류."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "interactive-reset"
  ],
  "depth": "standard",
  "path": "cases/INTERACTIVE/survival-resource-tick.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "time-step",
    "input_structure": "최소: oxygen 정수 단위, rate 초당 단위, elapsed_s>=0, paused bool; 행은 한 tick, tick_id. null elapsed는 unknown. 개선: 프레임 누락·서버 권위. 단위 불명확하면 실제 게임 밸런스 보류.",
    "hard_constraint": "프레임 수를 초로 취급하지 않는다. 생존 밸런스를 단위 테스트만으로 검증했다고 말하지 않는다.",
    "validation": "10-2*3=4; 정확히0; 시간 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 잠수 연습 게임에서 프레임 수가 달라도 같은 실제 경과시간이면 산소 잔량이 같도록 만들어 달라.

가능한 설명: 프레임마다 고정량을 빼고 있다; 일시정지 시간을 소모로 센다; 0 아래 값을 허용해 종료가 늦는다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 일시정지는 시간이 흐릅니까? → 아니면 paused tick 소모0.
2. 산소0은 즉시 종료입니까? → 예이면 clamp 뒤 ended.
3. 벽시계입니까 시뮬레이션 시간입니까? → 서버 시간 요구면 동기화 설계.

## 3. 데이터 계약과 자료 부족 대안

최소: oxygen 정수 단위, rate 초당 단위, elapsed_s>=0, paused bool; 행은 한 tick, tick_id. null elapsed는 unknown. 개선: 프레임 누락·서버 권위. 단위 불명확하면 실제 게임 밸런스 보류. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 남은 산소=max(0,oxygen-rate*elapsed_s), paused이면 원래 값. 출력에는 상태를 함께 표시.

개선: 고정 timestep 누적과 render 분리; 긴 delta 상한 정책은 별도 합의.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

tick 입력 → 시간 기반 소모 → 잔량과 종료 → 사용자가 재시작 또는 계속 선택. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"oxygen":10,"rate":2,"elapsed_s":3,"paused":false}`|`4`|10-2*3=4|
|boundary|`{"oxygen":10,"rate":2,"elapsed_s":5,"paused":false}`|`0`|정확히0|
|missing|`{"oxygen":10,"rate":2,"elapsed_s":null,"paused":false}`|`"unknown"`|시간 미확인|

## 7. 흔한 오류와 범위 축소

프레임 수를 초로 취급하지 않는다. 생존 밸런스를 단위 테스트만으로 검증했다고 말하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 정지 중 산소가 줄지 않는 것이 기대와 맞습니까?
- 긴 지연 뒤 즉시 종료가 이해됩니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 60fps와30fps 같은 시간이 같은 결과라는 근거는 무엇입니까?
- clamp가 게임 종료 조건에 주는 영향은 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
