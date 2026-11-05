# 작은 양의 변화의 누적 경보

```json
{
  "id": "one-sided-cusum",
  "title": "작은 양의 변화의 누적 경보",
  "family": "OPERATIONS",
  "keywords_ko": [
    "작은 양의 변화의 누적 경보",
    "작은 상승이 누적되었을 때 점검 후보 표시"
  ],
  "keywords_en": [
    "one-sided-cusum",
    "ordered samples × fixed reference"
  ],
  "problem_structure": "ordered samples × fixed reference",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 작업장 공기 흐름 측정 담당자가 한 번에 큰 변화는 없지만 조금씩 성능이 나빠지는 상황을 놓친다고 한다.",
  "do_not_use_when": "입력을 값의 크기순으로 정렬하지 않는다. 관리한계를 제품 규격으로 표시하지 않는다. 기준 근거가 없으면 누적 곡선만 연습 출력한다.",
  "data_required": [
    "필수 시간순 values 배열(지표단위), baseline,k,h 수치 같은 단위. 한 값 한 관측, 인덱스는 순서. null은 미수신으로 unknown. 본 합성 baseline10,k0.5,h1은 연습 값이며 보편 관리한계 아님."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [],
  "depth": "standard",
  "path": "cases/OPERATIONS/one-sided-cusum.md",
  "decision_signature": {
    "decision": "작은 상승이 누적되었을 때 점검 후보 표시",
    "input_structure": "ordered samples × fixed reference",
    "hard_constraint": "순서 유지·사전 기준값·미확인 데이터 보류",
    "validation": "단일 상한 미초과여도 누적 초과 검출"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 작업장 공기 흐름 측정 담당자가 한 번에 큰 변화는 없지만 조금씩 성능이 나빠지는 상황을 놓친다고 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 작은 지속 변화가 단일 한계 안에 숨어 있다.
- 기준 평균이 현재 조건과 다르다.
- 누락 또는 순서 변경이 누적값을 왜곡한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 기준 평균은 안정된 어느 기간에서 얻었는가? | 기준 근거 없으면 경보 승인 없이 관측 그래프만. |
| 어느 방향 변화가 문제인가? | 상승만이면 단측, 양방향이면 별도 두 누적통계. |
| 경보 이후 누적값을 어떻게 초기화하는가? | 본 예제 최초 초과만;운영 재설정은 승인 정책 필요. |

## 4. 데이터와 없을 때의 대안
필수 시간순 values 배열(지표단위), baseline,k,h 수치 같은 단위. 한 값 한 관측, 인덱스는 순서. null은 미수신으로 unknown. 본 합성 baseline10,k0.5,h1은 연습 값이며 보편 관리한계 아님.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "values": [
    10,
    11,
    11,
    11
  ],
  "baseline": 10,
  "k": 0.5,
  "h": 1
}
```

## 5. 기준 방법과 개선 조건
S0=0, St=max(0,S이전+x−baseline−k)를 시간순으로 계산하고 최초 St>h 인덱스를 표시한다. 경보는 점검 신호이지 불량 판정이 아니다.

오경보·탐지 지연 목표와 기준 구간이 확인되면 k,h 설계를 통계 담당자와 검증한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 작은 상승이 누적되었을 때 점검 후보 표시 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"first_alarm_index": 3, "max_cusum": 1.5}` | 누적0,0.5,1,1.5;엄격h초과는 index3. |
| 경계 | `{"values": [10, 11, 11]}` | `{"first_alarm_index": null, "max_cusum": 1.0}` | h와같으면경보아님. |
| 정보 부족 | `{"values": [10, null, 11]}` | `"unknown"` | 누락을 정상값으로 보간하지 않음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
입력을 값의 크기순으로 정렬하지 않는다. 관리한계를 제품 규격으로 표시하지 않는다. 기준 근거가 없으면 누적 곡선만 연습 출력한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 최초 경보 시점에서 확인할 운영 기록을 찾을 수 있는가?
- 단일 관측 정상과 누적 경보를 구별할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 행 순서 불변 테스트를 여기 적용하면 안 되는 이유는 무엇인가?
- k와 h를 실제 기준으로 확정하지 않은 한계는 어디에 적었는가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/statistics.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)

- 누적합 방법의 공개 1차 참고: https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm (NIST CUSUM 설명). 본 예제의 baseline, k, h는 독립 창작 연습값이며 실제 공정에서 보정된 관리 기준이 아니다.
