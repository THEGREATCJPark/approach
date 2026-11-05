# 실습 참여 자격의 만료일 판정

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-eligibility",
  "title": "실습 참여 자격의 만료일 판정",
  "family": "EVENT",
  "problem_structure": "dated eligibility decision",
  "keywords_ko": [
    "실습",
    "참여",
    "자격의",
    "만료일",
    "판정"
  ],
  "keywords_en": [
    "dated",
    "eligibility",
    "decision"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 지역 인쇄 체험실이 참가자가 보유한 안전교육 확인의 유효기간을 행사 날짜와 비교하려 한다.",
  "do_not_use_when": "실명이나 생년월일을 불필요하게 수집하지 않는다. 자격 시스템 연동이 막히면 입력 표 판정까지만 만들고 자동 참가 확정은 제외한다.",
  "data_required": [
    "한 객체는 참가 신청 한 건. application_id가 운영 키; fixture는 ID를 생략한 독립 판정 입력이다. required/certificate는 자격 코드, expires/event는 YYYY-MM-DD 현지 날짜. null은 미확인. 날짜 시간대 변환은 이 날짜 전용 예제 범위 밖."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "deadline-offset"
  ],
  "depth": "standard",
  "path": "cases/event/event-eligibility.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 지역 인쇄 체험실이 참가자가 보유한 안전교육 확인의 유효기간을 행사 날짜와 비교하려 한다.",
    "input_structure": "한 객체는 참가 신청 한 건. application_id가 운영 키; fixture는 ID를 생략한 독립 판정 입력이다. required/certificate는 자격 코드, expires/event는 YYYY-MM-DD 현지 날짜. null은 미확인. 날짜 시간대 변환은 이 날짜 전용 예제 범위 밖.",
    "hard_constraint": "자격 종류 일치와 expires≥event를 모두 만족하면 eligible, 확인된 불일치는 not_eligible, 필수 누락은 unknown.",
    "validation": "만료일 포함"
  }
}
```

## 업무 요청과 다른 원인

창작: 지역 인쇄 체험실이 참가자가 보유한 안전교육 확인의 유효기간을 행사 날짜와 비교하려 한다.

- 접수일에는 유효하지만 행사일에는 만료될 수 있다
- 자격 기록 부재를 미자격으로 오인한다
- 서로 다른 실습의 교육 종류를 혼동한다

## 담당자에게 먼저 물을 질문

1. 유효성 기준이 접수일인가 행사일인가? → 행사일이면 행사 날짜를 기준으로 다시 판정한다.
2. 만료일 당일까지 유효한가? → 이 예제는 포함하며 정책이 다르면 경계 검사를 바꾼다.
3. 요구 자격 종류가 일치하는가? → 종류가 다르면 날짜가 유효해도 not_eligible이다.

## 데이터 계약과 자료 부족 대안

한 객체는 참가 신청 한 건. application_id가 운영 키; fixture는 ID를 생략한 독립 판정 입력이다. required/certificate는 자격 코드, expires/event는 YYYY-MM-DD 현지 날짜. null은 미확인. 날짜 시간대 변환은 이 날짜 전용 예제 범위 밖.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

자격 종류 일치와 expires≥event를 모두 만족하면 eligible, 확인된 불일치는 not_eligible, 필수 누락은 unknown.

여러 자격의 AND/OR 조건이 생길 때만 버전 결정표를 추가한다.

## 최소 구현과 다음 행동

신청·자격 기록 → 종류/날짜 대조 → 판정·사유 → 운영자가 재교육 또는 기록 확인 안내

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"required":"press","certificate":"press","expires":"2030-05-12","event":"2030-05-10"}` | `"eligible"` | 5월12일≥5월10일이고 종류 일치 |
| boundary | `{"required":"press","certificate":"press","expires":"2030-05-10","event":"2030-05-10"}` | `"eligible"` | 만료일 포함 |
| missing | `{"required":"press","certificate":null,"expires":null,"event":"2030-05-10"}` | `"unknown"` | 교육 기록 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

실명이나 생년월일을 불필요하게 수집하지 않는다. 자격 시스템 연동이 막히면 입력 표 판정까지만 만들고 자동 참가 확정은 제외한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 만료 경계의 참가자를 실제로 어떻게 안내하겠는가?
- unknown을 미자격으로 오해하지 않는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 접수일 대신 행사일을 고른 근거는 어디 있는가?
- 이 계산으로 자격 증빙의 진위를 보장할 수 있는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
