# 처리 상태와 역할별 다음 행동

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "policy-next-action",
  "title": "처리 상태와 역할별 다음 행동",
  "family": "POLICY",
  "problem_structure": "role state affordance table",
  "keywords_ko": [
    "처리",
    "상태와",
    "역할별",
    "다음",
    "행동"
  ],
  "keywords_en": [
    "role",
    "state",
    "affordance",
    "table"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 공동 도구 자료실의 신청 화면에 모든 버튼이 보여 사용자가 할 수 없는 행동을 누른다.",
  "do_not_use_when": "화면에서 버튼을 숨기는 것만으로 서버 보안을 검증했다고 하지 않는다. 시간 부족이면 읽기 전용 행동 안내만 제공한다.",
  "data_required": [
    "role는 applicant/reviewer, state는 draft/submitted/approved. 한 객체는 현재 사용자 역할×신청 상태. null은 unknown. 합성 정책표는 버전 고정; 운영 request_id와 actor_id는 별도 키."
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
  "depth": "standard",
  "path": "cases/POLICY/policy-next-action.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 공동 도구 자료실의 신청 화면에 모든 버튼이 보여 사용자가 할 수 없는 행동을 누른다.",
    "input_structure": "role는 applicant/reviewer, state는 draft/submitted/approved. 한 객체는 현재 사용자 역할×신청 상태. null은 unknown. 합성 정책표는 버전 고정; 운영 request_id와 actor_id는 별도 키.",
    "hard_constraint": "applicant+draft→edit,submit; applicant+submitted→withdraw; reviewer+submitted→approve,reject; 그 외 빈 목록. unknown 역할/상태는 invalid.",
    "validation": "승인 후 직접 행동 없음"
  }
}
```

## 업무 요청과 다른 원인

창작: 공동 도구 자료실의 신청 화면에 모든 버튼이 보여 사용자가 할 수 없는 행동을 누른다.

- 상태를 무시한 공통 버튼
- 사용자 역할 갱신 누락
- 가능한 다음 행동과 실행 권한 혼동

## 담당자에게 먼저 물을 질문

1. 상태별 행동 권한은 누가 정하는가? → 정책표를 먼저 합의한다.
2. 화면 숨김만 필요한가 서버 거절도 필요한가? → 실제 실행 API는 별도 권한 검사가 필요하다.
3. 한 사람이 여러 역할을 가지는가? → 합집합 정책 또는 우선 역할을 확인한다.

## 데이터 계약과 자료 부족 대안

role는 applicant/reviewer, state는 draft/submitted/approved. 한 객체는 현재 사용자 역할×신청 상태. null은 unknown. 합성 정책표는 버전 고정; 운영 request_id와 actor_id는 별도 키.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

applicant+draft→edit,submit; applicant+submitted→withdraw; reviewer+submitted→approve,reject; 그 외 빈 목록. unknown 역할/상태는 invalid.

다중 역할과 제한된 철회 시간은 결정표의 추가 열로 관리한다.

## 최소 구현과 다음 행동

현재 역할·상태 → 허용 행동표 → 버튼과 설명 → 사용자가 다음 행동 선택

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"role":"applicant","state":"draft"}` | `["edit", "submit"]` | 신청자는 초안 편집/제출 |
| boundary | `{"role":"applicant","state":"approved"}` | `[]` | 승인 후 직접 행동 없음 |
| missing | `{"role":null,"state":"submitted"}` | `"unknown"` | 역할 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

화면에서 버튼을 숨기는 것만으로 서버 보안을 검증했다고 하지 않는다. 시간 부족이면 읽기 전용 행동 안내만 제공한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 다음 버튼이 없는 이유를 이해하는가?
- 이미 승인된 건을 바꾸려면 누구에게 연락할지 보이는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 빈 행동 목록과 unknown을 어떻게 구별했는가?
- UI 권한 안내와 서버 권한 검사는 무엇이 다른가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
