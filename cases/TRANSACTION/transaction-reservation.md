# 대여 재고의 예약 잠금과 실행 분리

> 독립 창작 합성 사례. 실제 조직·과제·인물을 재현하지 않는다. 공개 알고리즘 자료는 방법의 참고이며 아래 업무 정책·수치는 이 연습에서 새로 정했다.

```json
{
  "id": "transaction-reservation",
  "title": "대여 재고의 예약 잠금과 실행 분리",
  "family": "TRANSACTION",
  "keywords_ko": [
    "재고",
    "가용",
    "잠금",
    "멱등",
    "예약"
  ],
  "keywords_en": [
    "state",
    "machine",
    "idempotency",
    "inventory"
  ],
  "problem_structure": "state machine idempotency inventory",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "승인·잠금·인도의 상태 의미가 섞였다.",
  "do_not_use_when": "분산 환경에서 이 메모리 ledger를 운영용 멱등 저장소로 쓰지 않는다.",
  "data_required": "품목 stock total/locked 정수 개수, available=total-locked. 요청 id가 멱등 키이며 qty 양의 정수. 인도 시 total과 locked 모두 감소. 예약 시 locked만 증가.",
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": ["transaction-rounding"],
  "depth": "deep",
  "path": "cases/TRANSACTION/transaction-reservation.md"
}
```

## 요청과 다른 해석

“공동 작업실에서 예약 승인 표시가 실제 물품 인도 완료로 오해되고 재시도로 수량이 두 번 빠진다.”

- 승인·잠금·인도의 상태 의미가 섞였다.
- 동일 요청 재처리에 멱등 키가 없다.
- 동시 요청이 가용량을 같은 시점에 읽는다.

## 우선 질문과 방향 변화

1. 승인이 곧 인도인가? → 아니면 approved/reserved/fulfilled를 분리한다.
2. 예약 만료는 언제 누구 권한으로 푸는가? → 명시된 만료 정책 없이는 자동 해제하지 않는다.
3. 동일 요청 키에 수량이 바뀌면 어떻게 하는가? → 원 결과 반환 대신 payload 충돌로 거절한다.

파일에서 이미 확인되는 답은 다시 묻지 않는다. 정책을 결정할 권한자와 기준 시점을 함께 기록한다.

## 데이터 계약과 합성 입력

품목 stock total/locked 정수 개수, available=total-locked. 요청 id가 멱등 키이며 qty 양의 정수. 인도 시 total과 locked 모두 감소. 예약 시 locked만 증가.

최소 필수는 아래 판정 필드와 키다. 대표 샘플·스키마로 시작하며 개인 식별 정보는 필요하지 않다. 개선용 데이터는 실제 작업 시간과 오류 기록이다. 전체 이력이나 외부 API는 첫 검증에 없어도 된다. null은 미확인이며 0·false와 다르다. 필수 필드가 없으면 해당 판정을 보류하고 담당자 확인 목록에 남긴다.

```json
{
  "stock": {
    "total": 7,
    "locked": 2
  },
  "requests": [
    {
      "id": "r1",
      "qty": 3
    },
    {
      "id": "r1",
      "qty": 3
    },
    {
      "id": "r2",
      "qty": 3
    }
  ],
  "initial_reservations": [
    {
      "id": "prior",
      "qty": 2,
      "status": "reserved"
    }
  ]
}
```

## 기준 방법, 제약과 최소 경로

단일 실행 예제는 요청 ledger와 재고 전이를 원자적 작업으로 모델링한다. 실제 구현은 DB 트랜잭션과 조건부 갱신/잠금이 필요하다. UI 버튼 비활성만으로 중복 처리를 막지 않는다.

필수: 0≤locked≤total, 가용량 음수 금지, 같은 id 같은 payload는 같은 결과. 요청은 accepted/rejected/needs_review 구분. 승인 자체가 재고를 움직이지 않는다.

요청 → 가용량 검증·ledger → r1 예약, 재시도 원 결과, r2 재고부족 → 담당자가 인도 시 별도 fulfill을 실행한다.

## 기대 결과와 반례

| 유형 | 입력 또는 변경 | 기대 결과 |
|---|---|---|
| 정상 | 7/2에서 r1 qty3 | total7 locked5 available2 |
| 경계 | 초기가용5에 qty5 | 수락,available0 |
| 정보 부족 | qty=null | needs_review,재고 불변 |
| 충돌 | 가용2에 qty3 | rejected,재고 불변 |
| 재시도 | r1 qty3 반복 | 추가 잠금0 |
| 새 샘플 | r1 예약3 인도 완료 | total4 locked2 available2 |

손계산 근거: 초기가용7-2=5. 예약3 후 locked=2+3=5,available=2. 인도 시 total7-3=4,locked5-3=2, 가용2 유지.

비슷하지만 다른 두 건: 같은 id·같은 qty는 원 결과, 같은 id·다른 qty는 충돌이다. 새 id·같은 qty는 별도 요청이다.

작은 계산 예제는 [check_c.py](../../examples/synthetic/check_c.py)에서 별도 표준 라이브러리 계산으로 확인한다. 각 수용 테스트 행의 기대값은 소형 오라클 계산으로 확인한다. 전체 앱·화면·DB 동시성은 구현하거나 검증하지 않았으며, 기대값 검증과 구현물 테스트 통과는 다르다. 실행 범위는 해당 스크립트 출력과 검증 보고서를 따른다.

## 답변이 바뀌면 수정할 계획

- 예약이 단순 의향이면 locked를 쓰지 않고 확정 예약 단계에만 재고를 묶는다.
- 병렬 입력이 있다면 DB 수준 충돌 테스트를 완료하기 전 동시성 보장을 표시하지 않는다.

## 피할 구현과 축소 기준

- 분산 환경에서 이 메모리 ledger를 운영용 멱등 저장소로 쓰지 않는다.
- 총량·잠금량·평가 금액을 같은 필드로 취급하지 않는다.
- 시간 부족이면 실제 인도 연동을 빼고 상태별 수량과 거절 이유를 검증한다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 이 작은 합성 입력에는 패키지 설치·외부 호출이 필요 없다. Python도 실행할 수 없으면 표에 후보를 전부 적고 손계산한다. 대규모 개선 도구는 설치·규정·입력 적합성이 확인된 이후 별도 선택한다.

## 연습 시간 예산과 효과 측정

30분: 상태별 수량 손계산. 90분: ledger와 재고표. 180분: 허용 환경에서 원자적 저장과 동시성 검증. 권장 연습 예산이다.

불변식 위반 수, 중복 차감 수, 미해결 수동검토 건수를 측정한다. 이 합성 예제만으로 실제 조직의 시간 절감·만족도·수익 향상을 주장할 수 없다.

## 구현물에 대한 담당자 피드백

1. 결과 한 건의 근거와 보류 사유를 보고 다음 행동을 선택할 수 있는가? 실제로 선택하는 모습을 관찰한다.
2. 승인이 곧 인도인가?에 대한 합의와 화면 결과가 어긋나는 사례가 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

1. 이 기준 방법을 선택한 이유를 입력 크기·정책·반례 파일을 근거로 설명할 수 있는가?
2. 대여 재고의 예약 잠금과 실행 분리에서 계산 검증이 보장하지 못하는 부분은 무엇이며 어떤 추가 관찰이 필요한가?

## 공개 근거

- [공식 기술 문서](https://docs.python.org/3/library/sqlite3.html) — 일반 계산 구조를 참고했다. 창작 업무 조건의 외부 검증이나 적용 허가를 뜻하지 않는다.
- [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)
