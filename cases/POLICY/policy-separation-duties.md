# 작성자와 최종 승인자의 분리

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "policy-separation-duties",
  "title": "작성자와 최종 승인자의 분리",
  "family": "POLICY",
  "problem_structure": "separation of duties constraint",
  "keywords_ko": [
    "작성자와",
    "최종",
    "승인자의",
    "분리"
  ],
  "keywords_en": [
    "separation",
    "of",
    "duties",
    "constraint"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 자료 복원 팀에서 작업비 신청자가 자기 신청을 최종 승인하는 실수를 막으려 한다.",
  "do_not_use_when": "다른 표시 이름을 다른 사람으로 취급하지 않는다. 실제 인증 자료가 없으면 합성 판정만 보여준다.",
  "data_required": [
    "creator/approver는 실제 행위 주체 내부 ID, authorized는 최종 승인권자 집합. 한 객체는 요청의 승인 시도. null 주체는 unknown. 실제 계정 인증은 범위 밖."
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
  "depth": "standard",
  "path": "cases/POLICY/policy-separation-duties.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 자료 복원 팀에서 작업비 신청자가 자기 신청을 최종 승인하는 실수를 막으려 한다.",
    "input_structure": "creator/approver는 실제 행위 주체 내부 ID, authorized는 최종 승인권자 집합. 한 객체는 요청의 승인 시도. null 주체는 unknown. 실제 계정 인증은 범위 밖.",
    "hard_constraint": "creator==approver이면 manual_escalation, 다르나 권한 없으면 denied, 다르고 권한 있으면 eligible. eligible은 승인 완료가 아니다.",
    "validation": "권한이 있어도 자기 승인 금지"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 자료 복원 팀에서 작업비 신청자가 자기 신청을 최종 승인하는 실수를 막으려 한다.

- 한 사람이 복수 역할 보유
- 대리 계정과 실제 주체 불일치
- 검토와 최종 승인 단계 혼동

## 담당자에게 먼저 물을 질문

1. 분리 대상은 검토자인가 최종 승인자인가? → 이 사례는 최종 승인자이다.
2. 실제 주체 ID를 확인할 수 있는가? → 표시 이름 비교를 쓰지 않는다.
3. 대체 승인자가 없으면 어떻게 하는가? → 자동 예외 대신 manual_escalation이다.

## 데이터 계약과 자료 부족 대안

creator/approver는 실제 행위 주체 내부 ID, authorized는 최종 승인권자 집합. 한 객체는 요청의 승인 시도. null 주체는 unknown. 실제 계정 인증은 범위 밖.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

creator==approver이면 manual_escalation, 다르나 권한 없으면 denied, 다르고 권한 있으면 eligible. eligible은 승인 완료가 아니다.

다단계 승인이라면 단계별 금지 조합과 대체 경로를 별도 표로 만든다.

## 최소 구현과 다음 행동

작성/승인 주체 → 동일인·권한 대조 → 실행 가능성/이관 사유 → 책임자가 대체 승인자 지정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"creator":"a","approver":"b","authorized":["b"]}` | `"eligible"` | 주체 다르고 b 권한 있음 |
| boundary | `{"creator":"a","approver":"a","authorized":["a"]}` | `"manual_escalation"` | 권한이 있어도 자기 승인 금지 |
| missing | `{"creator":"a","approver":null,"authorized":["b"]}` | `"unknown"` | 승인 주체 없음 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

다른 표시 이름을 다른 사람으로 취급하지 않는다. 실제 인증 자료가 없으면 합성 판정만 보여준다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 자기 승인 거절 후 대체 담당자를 찾을 수 있는가?
- eligible을 이미 승인된 것으로 오해하지 않는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 주체와 계정의 구별이 이 규칙에 왜 필요한가?
- 권한은 있으나 승인할 수 없는 반례는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
