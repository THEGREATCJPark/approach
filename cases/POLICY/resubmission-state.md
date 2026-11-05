# 반려 후 재제출과 중복 이벤트 제어

```json
{
  "id": "resubmission-state",
  "title": "반려 후 재제출과 중복 이벤트 제어",
  "family": "POLICY",
  "keywords_ko": [
    "반려",
    "재제출",
    "상태전이"
  ],
  "keywords_en": [
    "state machine",
    "idempotency"
  ],
  "problem_structure": "state machine",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 시설 대여 신청 담당자가 반려 건을 수정해 다시 제출할 수 있게 하되 승인 건의 중복 제출로 상태가 바뀌지 않도록 해 달라고 한다.",
  "do_not_use_when": "버튼 비활성화만으로 멱등성을 보장하지 않는다. 외부 자동화 도구 없이도 전이표와 단위 검사로 시작 가능. 시간 부족이면 단일 사용자와 명확한 비동시성 한계를 제공.",
  "data_required": [
    "최소 필수: object_id, event_id, action, current_state, expected_version. 한 행은 명령 이벤트. id는 멱등키, 버전은 동시 변경 감지 키. null action은 미확인. 실제 실행에는 트랜잭션과 원자적 저장이 필요하며 이 예제는 단일 프로세스 전이 검증만 한다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "evidence-approval"
  ],
  "depth": "deep",
  "path": "cases/POLICY/resubmission-state.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {},
      "expected": {
        "state": "approved",
        "applied": 5
      },
      "basis": "5개 허용 전이."
    },
    {
      "kind": "경계",
      "input": {
        "events": []
      },
      "expected": {
        "state": "draft",
        "applied": 0
      },
      "basis": "빈 명령은 상태 유지."
    },
    {
      "kind": "정보 부족",
      "input": {
        "events": [
          {
            "event_id": "x",
            "action": null
          }
        ]
      },
      "expected": "unknown",
      "basis": "명령 누락."
    },
    {
      "kind": "충돌",
      "input": {
        "events": [
          {
            "event_id": "x",
            "action": "approve"
          }
        ]
      },
      "expected": "invalid_transition",
      "basis": "draft에서 직접 approve 불가."
    },
    {
      "kind": "재전송",
      "input": {
        "duplicate": true
      },
      "expected": {
        "state": "approved",
        "applied": 5
      },
      "basis": "e1 같은 내용은 중복 적용하지 않는다."
    },
    {
      "kind": "새 표본",
      "input": {
        "events": [
          {
            "event_id": "x",
            "action": "submit"
          },
          {
            "event_id": "x",
            "action": "reject"
          }
        ]
      },
      "expected": "conflict",
      "basis": "동일 id 다른 payload 거부."
    }
  ],
  "fixture": [
    {
      "event_id": "e1",
      "action": "submit"
    },
    {
      "event_id": "e2",
      "action": "reject"
    },
    {
      "event_id": "e3",
      "action": "edit"
    },
    {
      "event_id": "e4",
      "action": "submit"
    },
    {
      "event_id": "e5",
      "action": "approve"
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 시설 대여 신청 담당자가 반려 건을 수정해 다시 제출할 수 있게 하되 승인 건의 중복 제출로 상태가 바뀌지 않도록 해 달라고 한다.

- 화면 버튼만 숨겨 서버에서 잘못된 전이를 허용한다.
- 재전송 이벤트가 중복 이력을 만든다.
- 같은 이벤트 id에 다른 내용이 들어와 충돌한다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 승인 후 수정은 가능한가? | 불가면 전이 거부, 가능하면 별도 변경 요청 상태로 모델링. |
| 같은 이벤트 id의 재전송은 어떻게 처리하는가? | 같은 내용이면 기존 결과, 다른 내용이면 conflict. |
| 반려 사유가 없으면 반려할 수 있는가? | 필수이면 reject 이벤트의 증빙 조건에 추가. |

## 데이터 계약과 합성 입력
최소 필수: object_id, event_id, action, current_state, expected_version. 한 행은 명령 이벤트. id는 멱등키, 버전은 동시 변경 감지 키. null action은 미확인. 실제 실행에는 트랜잭션과 원자적 저장이 필요하며 이 예제는 단일 프로세스 전이 검증만 한다.

```json
[
  {
    "event_id": "e1",
    "action": "submit"
  },
  {
    "event_id": "e2",
    "action": "reject"
  },
  {
    "event_id": "e3",
    "action": "edit"
  },
  {
    "event_id": "e4",
    "action": "submit"
  },
  {
    "event_id": "e5",
    "action": "approve"
  }
]
```

축약 fixture는 한 object_id의 draft 상태를 시작점으로 한다. expected_version은 이 단일 프로세스 계산에서 사용하지 않는다. 버전 비교·트랜잭션·다중 프로세스 동시성은 모두 미검증이며 운영 구현에 추가해야 한다.

## 기준 방법과 최소 구현
허용 전이표 draft→submitted(submit),submitted→rejected(reject),rejected→draft(edit),submitted→approved(approve)를 적용한다. 이벤트 id/content를 기억한다.

다중 사용자가 실제로 필요하면 저장소 트랜잭션·조건부 버전 갱신을 추가하고 동시성 테스트를 별도로 실행한다.

현재 상태+이벤트 → 전이 검증 → 새 상태/거부 사유+이력 → 사용자가 편집·제출·확인 중 다음 행동 선택

목적함수 없음. 필수: 전이표·id 불변·기록 일치. 선호: 다음 가능한 행동 표시. 상태 변경과 처리 이력은 실제 시스템에서 원자적이어야 한다.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"state": "approved", "applied": 5}` | 5개 허용 전이. |
| 경계 | `{"events": []}` | `{"state": "draft", "applied": 0}` | 빈 명령은 상태 유지. |
| 정보 부족 | `{"events": [{"event_id": "x", "action": null}]}` | `"unknown"` | 명령 누락. |
| 충돌 | `{"events": [{"event_id": "x", "action": "approve"}]}` | `"invalid_transition"` | draft에서 직접 approve 불가. |
| 재전송 | `{"duplicate": true}` | `{"state": "approved", "applied": 5}` | e1 같은 내용은 중복 적용하지 않는다. |
| 새 표본 | `{"events": [{"event_id": "x", "action": "submit"}, {"event_id": "x", "action": "reject"}]}` | `"conflict"` | 동일 id 다른 payload 거부. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: draft→submitted→rejected→draft→submitted→approved로 적용5번. e1 submit을 곧바로 재전송해도 적용수는 증가하지 않는다.

서로 비슷하지만 달라야 하는 두 건: 새 id로 draft에서 approve는 invalid_transition, 같은 id로 다른 action은 conflict이다.

## 답변 변화와 범위 통제
- 반려 후 바로 재제출 가능이라는 답변 → edit 단계를 제거할지 정책 책임자와 확정.
- 동시 편집자가 있다는 답변 → 단일 프로세스 데모를 중단하고 버전 충돌 설계 우선.

버튼 비활성화만으로 멱등성을 보장하지 않는다. 외부 자동화 도구 없이도 전이표와 단위 검사로 시작 가능. 시간 부족이면 단일 사용자와 명확한 비동시성 한계를 제공.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 반려 후 화면에서 수정→제출 경로를 찾을 수 있는가?
- 중복 메시지와 실제 두 번 처리된 사건을 구별할 수 있는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- 단위 테스트가 동시성 안전을 보장하지 않는 부분은 어디인가?
- id와 payload 충돌을 분리한 실패 사례를 보여줄 수 있는가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/sqlite3.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
