# 동시 참여 요구에 따른 서버 범위 결정

```json
{
  "id": "multiplayer-scope-gate",
  "title": "동시 참여 요구에 따른 서버 범위 결정",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "동시",
    "참여",
    "요구에",
    "따른",
    "서버",
    "범위",
    "결정"
  ],
  "keywords_en": [
    "scope-decision-table",
    "multiplayer-scope-gate"
  ],
  "problem_structure": "scope-decision-table",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 공동 전시 게임을 여러 사람이 한다는 요청이 들어왔다. 같은 장치 교대인지 독립 장치 실시간인지 먼저 구분해 달라.",
  "do_not_use_when": "같은 화면 2인 플레이에 서버를 기본 설치하지 않는다. server_needed를 서버 구현 완료로 표시하지 않는다.",
  "data_required": [
    "최소: devices 정수>=1, shared_state bool, server_permission allowed/forbidden/unknown. 한 행 session_plan_id. null은 unknown. 개선: 지연·동시성·인증. 실측 사용자 수 없으면 규모 성능 주장 금지."
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
  "path": "cases/INTERACTIVE/multiplayer-scope-gate.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "scope-decision-table",
    "input_structure": "최소: devices 정수>=1, shared_state bool, server_permission allowed/forbidden/unknown. 한 행 session_plan_id. null은 unknown. 개선: 지연·동시성·인증. 실측 사용자 수 없으면 규모 성능 주장 금지.",
    "hard_constraint": "같은 화면 2인 플레이에 서버를 기본 설치하지 않는다. server_needed를 서버 구현 완료로 표시하지 않는다.",
    "validation": "다중 장치 공유; 단일 장치 통신 불필요; 통신 허용 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 공동 전시 게임을 여러 사람이 한다는 요청이 들어왔다. 같은 장치 교대인지 독립 장치 실시간인지 먼저 구분해 달라.

가능한 설명: 참여 인원과 동시 연결 수를 혼동한다; 공유 상태가 필요 없는데 서버를 만든다; 서버 승인 없이 동기화를 약속한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 같은 라운드 상태를 실시간 공유합니까? → 아니면 로컬 진행 가능.
2. 독립 장치 몇 대가 동시에 접속합니까? → 2대 이상 공유이면 서버 후보.
3. 서버 실행·통신이 허용됩니까? → 금지이면 범위불가, unknown이면 확인.

## 3. 데이터 계약과 자료 부족 대안

최소: devices 정수>=1, shared_state bool, server_permission allowed/forbidden/unknown. 한 행 session_plan_id. null은 unknown. 개선: 지연·동시성·인증. 실측 사용자 수 없으면 규모 성능 주장 금지. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: devices=1 또는 shared_state=False는 local. 그 외 권한 allowed이면 server_needed, forbidden이면 out_of_scope, unknown이면 unknown.

개선: 서버 필요가 확인된 후에만 authoritative state, event ordering, latency 실험.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

참여 조건 입력 → 범위 게이트 → local/server_needed/out_of_scope/unknown → 담당자가 범위 결정. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"devices":3,"shared_state":true,"server_permission":"allowed"}`|`"server_needed"`|다중 장치 공유|
|boundary|`{"devices":1,"shared_state":true,"server_permission":"forbidden"}`|`"local"`|단일 장치 통신 불필요|
|missing|`{"devices":3,"shared_state":true,"server_permission":"unknown"}`|`"unknown"`|통신 허용 미확인|

## 7. 흔한 오류와 범위 축소

같은 화면 2인 플레이에 서버를 기본 설치하지 않는다. server_needed를 서버 구현 완료로 표시하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 교대와 실시간 동시 참여 중 어느 흐름이 맞습니까?
- 통신 불가일 때 로컬 시연을 수용할 수 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 장치 수와 공유 상태 중 어느 답이 설계를 바꿨습니까?
- 범위 판단 테스트가 부하 성능을 보장하지 않는 이유는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
