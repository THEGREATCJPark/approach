# 운영 리허설의 동시 체류 인원

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "event-rehearsal-capacity",
  "title": "운영 리허설의 동시 체류 인원",
  "family": "EVENT",
  "problem_structure": "event interval sweep",
  "keywords_ko": [
    "운영",
    "리허설의",
    "동시",
    "체류",
    "인원"
  ],
  "keywords_en": [
    "event",
    "interval",
    "sweep"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 실내 설명회에서 도착·퇴장 리허설 기록으로 어느 시각에 실내 정원이 넘는지 확인하려 한다.",
  "do_not_use_when": "총 신청 수를 최대 체류로 쓰지 않는다. 시간 부족이면 애니메이션 대신 시간별 인원 표를 유지한다.",
  "data_required": [
    "intervals는 [enter,exit] 배열, 각 행은 포함 대상 한 명의 계획 체류구간. 분 단위, enter≤exit, 반열린 [enter,exit). null exit는 unknown. cap는 정수 명."
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
  "path": "cases/event/event-rehearsal-capacity.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 실내 설명회에서 도착·퇴장 리허설 기록으로 어느 시각에 실내 정원이 넘는지 확인하려 한다.",
    "input_structure": "intervals는 [enter,exit] 배열, 각 행은 포함 대상 한 명의 계획 체류구간. 분 단위, enter≤exit, 반열린 [enter,exit). null exit는 unknown. cap는 정수 명.",
    "hard_constraint": "시각별 +1/-1 사건을 합쳐 누적 최대 인원을 구하고 peak>cap인지 표시한다. 길이0 구간은 체류0.",
    "validation": "반열린 구간은 서로 겹치지 않음"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 실내 설명회에서 도착·퇴장 리허설 기록으로 어느 시각에 실내 정원이 넘는지 확인하려 한다.

- 하루 총 방문과 동시 체류 혼동
- 같은 시각 입퇴장 처리순 미정
- 퇴장 기록 누락

## 담당자에게 먼저 물을 질문

1. 같은 시각 퇴장과 입장은 어떻게 처리하는가? → 이 사례는 퇴장 먼저다.
2. 기록은 계획인가 관측인가? → 계획이면 실제 혼잡 검증이라 부르지 않는다.
3. 정원 초과 판단에 운영자도 포함하는가? → 포함 대상 정의에 따라 사건을 바꾼다.

## 데이터 계약과 자료 부족 대안

intervals는 [enter,exit] 배열, 각 행은 포함 대상 한 명의 계획 체류구간. 분 단위, enter≤exit, 반열린 [enter,exit). null exit는 unknown. cap는 정수 명.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

시각별 +1/-1 사건을 합쳐 누적 최대 인원을 구하고 peak>cap인지 표시한다. 길이0 구간은 체류0.

실제 도착 변동을 알면 지연 시나리오별 peak를 비교한다.

## 최소 구현과 다음 행동

체류구간 → 시각 정렬·누적 → 최대 체류/초과 여부 → 운영자가 입장 간격 조정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"intervals":[[0,10],[5,15],[10,20]],"cap":2}` | `{"peak": 2, "over": false}` | 10분에 한 명 퇴장과 한 명 입장; 최대2 |
| boundary | `{"intervals":[[0,5],[5,10]],"cap":1}` | `{"peak": 1, "over": false}` | 반열린 구간은 서로 겹치지 않음 |
| missing | `{"intervals":[[0,null]],"cap":2}` | `"unknown"` | 퇴장 시각 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

총 신청 수를 최대 체류로 쓰지 않는다. 시간 부족이면 애니메이션 대신 시간별 인원 표를 유지한다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 최대 체류 시각에 입장 지연 안내가 가능한가?
- 운영 인력 누락으로 인원이 과소 계산되지 않는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 같은 시각 퇴장 먼저라는 정책은 어떻게 테스트했는가?
- 계획 구간 검증과 실제 혼잡 측정은 무엇이 다른가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
