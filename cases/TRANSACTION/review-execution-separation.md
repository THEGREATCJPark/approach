# 승인 결과와 실제 실행 상태 분리

```json
{
  "id": "review-execution-separation",
  "title": "승인 결과와 실제 실행 상태 분리",
  "family": "TRANSACTION",
  "keywords_ko": [
    "승인",
    "결과와",
    "실제",
    "실행",
    "상태",
    "분리"
  ],
  "keywords_en": [
    "two-phase-state",
    "review-execution-separation"
  ],
  "problem_structure": "two-phase-state",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "공유 장비 교환권 처리 화면에서 승인되었다는 이유만으로 실물 인도가 완료됐다고 표시하지 않게 해 달라.",
  "do_not_use_when": "승인 성공을 실제 이전 완료로 표기하지 않는다. 합성 예제로 실물 인도 시스템 신뢰도를 입증하지 않는다.",
  "data_required": [
    "최소: decision approved/rejected/pending, receipt bool/null; 한 행 request_id. receipt null은 확인불가, false는 미인도 확인. 개선: receipt_id·인도시각·담당자. decision 누락이면 unknown."
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
  "path": "cases/TRANSACTION/review-execution-separation.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "two-phase-state",
    "input_structure": "최소: decision approved/rejected/pending, receipt bool/null; 한 행 request_id. receipt null은 확인불가, false는 미인도 확인. 개선: receipt_id·인도시각·담당자. decision 누락이면 unknown.",
    "hard_constraint": "승인 성공을 실제 이전 완료로 표기하지 않는다. 합성 예제로 실물 인도 시스템 신뢰도를 입증하지 않는다.",
    "validation": "허가됐으나 미인도; 거절과 인도 상충; 실행 증거 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

공유 장비 교환권 처리 화면에서 승인되었다는 이유만으로 실물 인도가 완료됐다고 표시하지 않게 해 달라.

가능한 설명: 심사와 실행 상태를 같은 필드에 저장한다; 실행 확인서가 늦게 온다; 거절된 요청에 잘못된 실행 사건이 붙었다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 승인은 실행 권한만 부여합니까? → 예이면 approved와 completed 분리.
2. 인도 확인 근거는 무엇입니까? → receipt 없으면 완료 불가.
3. 거절 뒤 receipt가 오면 어떻게 합니까? → 본 예제 conflict 수동 검토.

## 3. 데이터 계약과 자료 부족 대안

최소: decision approved/rejected/pending, receipt bool/null; 한 행 request_id. receipt null은 확인불가, false는 미인도 확인. 개선: receipt_id·인도시각·담당자. decision 누락이면 unknown. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: approved+true=completed, approved+false=ready, approved+null=unknown. rejected+true=conflict. pending은 pending.

개선: 승인·실행 별도 상태기계와 원자적 전이 로그; 외부 실제 실행은 이번 합성 범위 제외.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

심사·receipt 입력 → 상태 조합검사 → ready/completed/pending/conflict/unknown → 담당자가 인도 또는 조사. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"decision":"approved","receipt":false}`|`"ready"`|허가됐으나 미인도|
|boundary|`{"decision":"rejected","receipt":true}`|`"conflict"`|거절과 인도 상충|
|missing|`{"decision":"approved","receipt":null}`|`"unknown"`|실행 증거 미확인|

## 7. 흔한 오류와 범위 축소

승인 성공을 실제 이전 완료로 표기하지 않는다. 합성 예제로 실물 인도 시스템 신뢰도를 입증하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- ready와completed를 보고 다음 조치가 구분됩니까?
- receipt 미확인일 때 어느 담당자가 확인합니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 승인과 실행을 분리한 반례는 무엇입니까?
- 실제 완료의 근거 필드를 어디에 연결했습니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
