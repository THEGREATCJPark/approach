# 정책 실패 사유 코드의 우선순위

```json
{
  "id": "policy-reason-priority",
  "title": "정책 실패 사유 코드의 우선순위",
  "family": "TRANSACTION",
  "keywords_ko": [
    "정책",
    "실패",
    "사유",
    "코드의",
    "우선순위"
  ],
  "keywords_en": [
    "reason-code-table",
    "policy-reason-priority"
  ],
  "problem_structure": "reason-code-table",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 수리 부품 교환 신청에서 여러 규칙에 동시에 걸릴 때 운영자가 먼저 해결할 사유 코드를 일관되게 보여 달라.",
  "do_not_use_when": "검사 순서를 우연한 dict 순서에 맡기지 않는다. PASS를 실제 지급 완료로 쓰지 않는다.",
  "data_required": [
    "최소: authorized bool, age_days 정수>=0, limit_days 정수>=0, quantity 정수, max_quantity 정수. 한 행 claim_id. null은 unknown. 개선: 정책버전·모든 사유 목록. 기한은 동일 기준일에서 계산."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "transaction-reservation"
  ],
  "depth": "standard",
  "path": "cases/TRANSACTION/policy-reason-priority.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "reason-code-table",
    "input_structure": "최소: authorized bool, age_days 정수>=0, limit_days 정수>=0, quantity 정수, max_quantity 정수. 한 행 claim_id. null은 unknown. 개선: 정책버전·모든 사유 목록. 기한은 동일 기준일에서 계산.",
    "hard_constraint": "검사 순서를 우연한 dict 순서에 맡기지 않는다. PASS를 실제 지급 완료로 쓰지 않는다.",
    "validation": "최우선 권한실패; 두 상한과같음 허용; 권한 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

창작 수리 부품 교환 신청에서 여러 규칙에 동시에 걸릴 때 운영자가 먼저 해결할 사유 코드를 일관되게 보여 달라.

가능한 설명: 검사 순서가 구현마다 다르다; 필수 조건을 가중점수로 상쇄한다; 누락된 정책을 통과로 처리한다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 한 사유만 표시합니까 전체입니까? → 이번 예제 대표1개, 전체 요구면 목록도 유지.
2. 권한·기한·한도 순서에 동의합니까? → 정책 소유자 답으로 순서 수정.
3. 필드 미확인은 거절입니까? → 본 예제 unknown, 불이익 자동 확정 금지.

## 3. 데이터 계약과 자료 부족 대안

최소: authorized bool, age_days 정수>=0, limit_days 정수>=0, quantity 정수, max_quantity 정수. 한 행 claim_id. null은 unknown. 개선: 정책버전·모든 사유 목록. 기한은 동일 기준일에서 계산. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 누락이면 unknown; unauthorized면 AUTH; age>limit면 EXPIRED; quantity>max면 LIMIT; 나머지 PASS.

개선: 버전 있는 decision table로 사유와 조치 연결; 품질·권한 필수조건을 점수로 상쇄 금지.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

신청·정책 입력 → 순서 규칙 → 코드·근거·다음 행동 → 담당자가 보완/거절 검토. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"authorized":false,"age_days":15,"limit_days":10,"quantity":4,"max_quantity":2}`|`"AUTH"`|최우선 권한실패|
|boundary|`{"authorized":true,"age_days":10,"limit_days":10,"quantity":2,"max_quantity":2}`|`"PASS"`|두 상한과같음 허용|
|missing|`{"authorized":null,"age_days":1,"limit_days":10,"quantity":1,"max_quantity":2}`|`"unknown"`|권한 미확인|

## 7. 흔한 오류와 범위 축소

검사 순서를 우연한 dict 순서에 맡기지 않는다. PASS를 실제 지급 완료로 쓰지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 대표 사유가 가장 먼저 해결할 항목과 맞습니까?
- 사유코드만으로 보완 방법을 찾을 수 있습니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 동시에 두 규칙이 실패하는 기대값을 설명하십시오.
- PASS와실행완료의 차이는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
