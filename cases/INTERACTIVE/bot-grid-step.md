# 단순 봇의 한 칸 이동과 막힌 경로

```json
{
  "id": "bot-grid-step",
  "title": "단순 봇의 한 칸 이동과 막힌 경로",
  "family": "INTERACTIVE",
  "keywords_ko": [
    "단순",
    "봇의",
    "한",
    "칸",
    "이동과",
    "막힌",
    "경로"
  ],
  "keywords_en": [
    "grid-policy",
    "bot-grid-step"
  ],
  "problem_structure": "grid-policy",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 보드 시뮬레이션에서 봇이 목표 쪽으로 한 칸 움직이되 벽에 막히면 대기하도록 구현해 달라.",
  "do_not_use_when": "루프를 무한 반복해 목표 도달을 보장하지 않는다. 전체 경로 탐색 요구가 없으면 새 엔진 설치 제외.",
  "data_required": [
    "최소: pos,target=[정수 x,y] cell, blocked 좌표배열, 한 행 bot_id의 tick. null blocked는 unknown, []는 없음. 유효 범위는 작은 무한 정수 격자 예제; 개선: 유한 지도 경계."
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
  "path": "cases/INTERACTIVE/bot-grid-step.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "grid-policy",
    "input_structure": "최소: pos,target=[정수 x,y] cell, blocked 좌표배열, 한 행 bot_id의 tick. null blocked는 unknown, []는 없음. 유효 범위는 작은 무한 정수 격자 예제; 개선: 유한 지도 경계.",
    "hard_constraint": "루프를 무한 반복해 목표 도달을 보장하지 않는다. 전체 경로 탐색 요구가 없으면 새 엔진 설치 제외.",
    "validation": "오른쪽으로 거리3→2; 거리 감소 유일 칸 막힘; 벽 정보 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 보드 시뮬레이션에서 봇이 목표 쪽으로 한 칸 움직이되 벽에 막히면 대기하도록 구현해 달라.

가능한 설명: 최단경로와 단순 탐욕 이동의 기대가 다르다; 동률 방향이 불명확하다; 장애물을 통과한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 우회가 필수입니까? → 예이면 BFS/A*로 변경.
2. 동률 우선순위가 있습니까? → 본 예제 오른쪽,위,왼쪽,아래 순.
3. 다른 봇은 장애물입니까? → 동시 이동이면 충돌 정책 추가.

## 3. 데이터 계약과 자료 부족 대안

최소: pos,target=[정수 x,y] cell, blocked 좌표배열, 한 행 bot_id의 tick. null blocked는 unknown, []는 없음. 유효 범위는 작은 무한 정수 격자 예제; 개선: 유한 지도 경계. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 맨해튼 거리를 엄격히 줄이는 인접 칸 중 비장애물 첫 칸을 선택, 없으면 stay. 도착하면 stay.

개선: 막혀도 도달 가능한 우회를 요구하면 BFS; 탐욕법의 막힘을 도달 불가능 증명으로 쓰지 않음.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

위치·목표·벽 → 한 칸 후보 → next/stay와 이유 → 사용자가 동작 확인. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"pos":[0,0],"target":[2,1],"blocked":[]}`|`[1, 0]`|오른쪽으로 거리3→2|
|boundary|`{"pos":[0,0],"target":[1,0],"blocked":[[1,0]]}`|`[0, 0]`|거리 감소 유일 칸 막힘|
|missing|`{"pos":[0,0],"target":[1,0],"blocked":null}`|`"unknown"`|벽 정보 미확인|

## 7. 흔한 오류와 범위 축소

루프를 무한 반복해 목표 도달을 보장하지 않는다. 전체 경로 탐색 요구가 없으면 새 엔진 설치 제외. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 막힌 경우 대기와 우회 중 무엇이 필요합니까?
- 동률 이동 방향이 일관되어 이해됩니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 이 탐욕 봇이 실패하는 벽 배치를 제시하십시오.
- 한 칸 결정 검증과 목표 도달 검증의 차이는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
