# 증빙 누락과 승인 권한을 분리한 비용 안내

```json
{
  "id": "evidence-approval",
  "title": "증빙 누락과 승인 권한을 분리한 비용 안내",
  "family": "POLICY",
  "keywords_ko": [
    "증빙",
    "승인",
    "금액"
  ],
  "keywords_en": [
    "decision table",
    "policy"
  ],
  "problem_structure": "decision table",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 작은 자료 보존실의 운영자가 구매 비용의 다음 승인 담당자를 안내하되 증빙 미제출을 자동 반려로 처리하지 말아 달라고 한다.",
  "do_not_use_when": "법률·회계 판단이 아니라 창작 운영 규칙 예제다. 챗봇이 정책을 추측하게 하지 않는다. 버전 불명 시 자동 경로를 멈추고 확인 담당자만 안내.",
  "data_required": [
    "최소 필수: request_id, amount(정수 비용단위), evidence(true/false/null), policy_version. 한 행은 신청 한 건. null 증빙은 미확인. 승인자표는 필수, 신청자 이름은 없어도 가능. 정책이 없으면 자료 요청 상태만 제공."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "resubmission-state"
  ],
  "depth": "deep",
  "path": "cases/POLICY/evidence-approval.md",
  "test_count": 6,
  "tests": [
    {
      "kind": "정상",
      "input": {
        "amount": 80,
        "evidence": true
      },
      "expected": "staff",
      "basis": "100 이하."
    },
    {
      "kind": "경계",
      "input": {
        "amount": 100,
        "evidence": true
      },
      "expected": "staff",
      "basis": "100 포함."
    },
    {
      "kind": "정보 부족",
      "input": {
        "amount": 50,
        "evidence": null
      },
      "expected": "unknown",
      "basis": "증빙 확인 대기."
    },
    {
      "kind": "충돌",
      "input": {
        "amount": -1,
        "evidence": true
      },
      "expected": "invalid",
      "basis": "음수 신청은 예제 정책 범위 밖."
    },
    {
      "kind": "재시도",
      "input": {
        "amount": 101,
        "evidence": true,
        "repeat": true
      },
      "expected": "manager",
      "basis": "재계산으로 승인 완료를 만들지 않는다."
    },
    {
      "kind": "새 표본",
      "input": {
        "amount": 50,
        "evidence": false
      },
      "expected": "need_evidence",
      "basis": "증빙 없음은 보완 요청."
    }
  ],
  "fixture": [
    {
      "request_id": "q1",
      "amount": 80,
      "evidence": true,
      "policy_version": "v1"
    },
    {
      "request_id": "q2",
      "amount": 100,
      "evidence": true,
      "policy_version": "v1"
    },
    {
      "request_id": "q3",
      "amount": 101,
      "evidence": true,
      "policy_version": "v1"
    },
    {
      "request_id": "q4",
      "amount": 50,
      "evidence": false,
      "policy_version": "v1"
    },
    {
      "request_id": "q5",
      "amount": 50,
      "evidence": null,
      "policy_version": "v1"
    }
  ]
}
```

## 창작 요청과 가능한 원인
창작 요청: 작은 자료 보존실의 운영자가 구매 비용의 다음 승인 담당자를 안내하되 증빙 미제출을 자동 반려로 처리하지 말아 달라고 한다.

- 승인 금액 구간이 화면 문구와 다르다.
- 증빙 미확인을 부적격으로 단정한다.
- 정책 버전이 바뀌었지만 과거 건도 새 규칙으로 재판정한다.

## 먼저 가를 질문
| 질문 | 답에 따른 방향 |
|---|---|
| 금액 경계에서 어느 승인자가 맡는가? | 본 예제 100까지 담당,100초과 관리자; 포함 관계를 명시. |
| 증빙 없다는 것과 아직 확인 안 됐다는 것이 같은가? | False는 보완 요청, null은 확인 대기. |
| 어느 정책 버전을 적용하는가? | 신청시점 버전인지 처리시점 버전인지 확인 후 고정. |

## 데이터 계약과 합성 입력
최소 필수: request_id, amount(정수 비용단위), evidence(true/false/null), policy_version. 한 행은 신청 한 건. null 증빙은 미확인. 승인자표는 필수, 신청자 이름은 없어도 가능. 정책이 없으면 자료 요청 상태만 제공.

```json
[
  {
    "request_id": "q1",
    "amount": 80,
    "evidence": true,
    "policy_version": "v1"
  },
  {
    "request_id": "q2",
    "amount": 100,
    "evidence": true,
    "policy_version": "v1"
  },
  {
    "request_id": "q3",
    "amount": 101,
    "evidence": true,
    "policy_version": "v1"
  },
  {
    "request_id": "q4",
    "amount": 50,
    "evidence": false,
    "policy_version": "v1"
  },
  {
    "request_id": "q5",
    "amount": 50,
    "evidence": null,
    "policy_version": "v1"
  }
]
```

검사 입력은 축약형으로 정책 버전 `v1`을 테스트 컨텍스트에 고정한다. `v1`은 증빙 우선, 금액100 이하 staff인 위 합성 정책이다. 테스트는 버전 선택·정책 조회를 구현하거나 검증하지 않는다. 실제 버전이 없거나 알 수 없으면 이 결정표를 적용하지 않고 unknown으로 보류해야 한다.

## 기준 방법과 최소 구현
입력 유효성→정책 버전 확인→증빙 상태→금액 구간 순으로 결정표 적용. 경로 안내는 실제 승인 완료와 다르다.

정책 분기가 커지면 결정표를 버전 관리하고 승인 상태기계와 연결하되 자유문 생성으로 규칙을 대체하지 않는다.

신청 행 → 사유코드·다음 담당자 → 신청자가 보완하거나 승인 담당자에게 전달

목적함수 없음. 필수: 정책 버전과 증빙 상태 우선. 선호: 짧은 다음 행동 문구. 관리자 경로를 자동 승인으로 표현 금지.

## 반례와 기대값
| 종류 | 입력 변화 | 기대 출력 | 계산·판정 근거 |
|---|---|---|---|
| 정상 | `{"amount": 80, "evidence": true}` | `"staff"` | 100 이하. |
| 경계 | `{"amount": 100, "evidence": true}` | `"staff"` | 100 포함. |
| 정보 부족 | `{"amount": 50, "evidence": null}` | `"unknown"` | 증빙 확인 대기. |
| 충돌 | `{"amount": -1, "evidence": true}` | `"invalid"` | 음수 신청은 예제 정책 범위 밖. |
| 재시도 | `{"amount": 101, "evidence": true, "repeat": true}` | `"manager"` | 재계산으로 승인 완료를 만들지 않는다. |
| 새 표본 | `{"amount": 50, "evidence": false}` | `"need_evidence"` | 증빙 없음은 보완 요청. |

입력 변화는 위 합성 입력에 적용한다. `only`, `events`, `values`는 전체 입력 교체, 그 외는 해당 항목 변경이다. 테스트 실행 코드가 변형의 정확한 의미를 정의한다.

독립 기대값 근거: 80≤100 및100≤100은 staff,101>100은 manager. 증빙 False/None은 금액 구간보다 먼저 분기한다.

서로 비슷하지만 달라야 하는 두 건: 같은50에서 evidence=False는 need_evidence, null은 unknown이다.

## 답변 변화와 범위 통제
- 100도 관리자 승인이라는 답변 → 경계 포함을 수정하고100 테스트를 변경.
- 정책 v2를 신청일 기준으로 적용한다는 답변 → 날짜와 버전 맵핑을 선행.

법률·회계 판단이 아니라 창작 운영 규칙 예제다. 챗봇이 정책을 추측하게 하지 않는다. 버전 불명 시 자동 경로를 멈추고 확인 담당자만 안내.

## 시간과 도구
연습용 권장 예산이며 실제 실행시간 보장이 아니다.
- 30분: 위 합성 입력 한 건과 반례를 손으로 계산하고 필수 정책 1개를 확인한다.
- 90분: 데이터 입력 → 판정/계산 → 근거와 다음 행동까지 연결하고 아래 6개 검사를 실행한다.
- 180분: 담당자 피드백으로 오해가 있는 표현을 수정하고 실제로 추가된 조건만 반영한다.
- 1순위: Python 표준 라이브러리. 설치 없이 소형 계산·집계·완전탐색을 재현한다. 설치/실행 불가 시 표 계산 또는 종이 결정표로 동일 기대값을 대조한다.
- 실행 허용이 unknown이면 자동 실행하지 않고 Markdown과 합성 표를 읽는 경로를 사용한다.

## 구현물에 대한 담당자 피드백
- 이 사유만 보고 어떤 자료를 보완해야 하는지 알 수 있는가?
- 승인 요청 경로를 승인 완료로 오해하지 않는가?

## 개발자 설명 사전 연습
시험 전 PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.
- null과 False를 구분한 자료 계약은 어디 있는가?
- 정책 변경을 테스트에 반영한 근거는 무엇인가?

## 검증 범위와 효과
[독립 계산 검사](../../examples/synthetic/check_b.py)는 작은 합성 입력의 기대값만 검사한다. 생산 앱·실사용자 검증은 수행하지 않았다. 측정 가능 항목은 6개 기대값 일치 여부와 담당자가 다음 행동을 정확히 선택한 건수/관찰 건수이다. 실제 시간 절감·학습 향상·비용 절감·안전성은 별도 전후 관찰 없이는 주장할 수 없다.

## 연결과 공개 근거
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
- 공개 1차 기술 참고: https://docs.python.org/3/library/stdtypes.html (일반 계산/구조 참고이며 사례·정책·수치는 독립 창작)
