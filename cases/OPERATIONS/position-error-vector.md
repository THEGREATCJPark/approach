# 방향을 보존한 위치 오차 판정

```json
{
  "id": "position-error-vector",
  "title": "방향을 보존한 위치 오차 판정",
  "family": "OPERATIONS",
  "keywords_ko": [
    "방향을 보존한 위치 오차 판정",
    "측정 위치가 허용 반경 안인지 확인"
  ],
  "keywords_en": [
    "position-error-vector",
    "target/measured xy vectors"
  ],
  "problem_structure": "target/measured xy vectors",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 소형 조립 지그 담당자가 위치 오차를 숫자 하나로만 받아 어느 방향을 조정해야 하는지 모른다.",
  "do_not_use_when": "위경도를 mm처럼 빼지 않는다. 원형 기준을 각 축≤반경으로 대체하면 모서리가 잘못 합격한다. 좌표계 없으면 그림 대신 원자료 요청.",
  "data_required": [
    "필수 target_xy/measured_xy 길이2 배열(mm), radius_mm 비음수 수치. 한 객체는 기준점 한 개의 관측. point_id로 도면과 결합. null 좌표는 미측정. 회전 변환은 실제 데이터에 있을 때 별도 필요."
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
  "path": "cases/OPERATIONS/position-error-vector.md",
  "decision_signature": {
    "decision": "측정 위치가 허용 반경 안인지 확인",
    "input_structure": "target/measured xy vectors",
    "hard_constraint": "동일 평면 좌표와 거리 단위",
    "validation": "방향·거리·허용경계 각각 확인"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 소형 조립 지그 담당자가 위치 오차를 숫자 하나로만 받아 어느 방향을 조정해야 하는지 모른다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 거리만 있고 방향이 사라진다.
- 축 단위나 원점이 섞였다.
- 각 축 허용값과 원형 반경 기준을 혼동한다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 허용구역은 원인가 축별 사각형인가? | 원은 유클리드 거리, 사각형은 축별 검사로 변경. |
| 두 좌표의 원점과 단위가 같은가? | 다르면 변환 검증 전 판정 보류. |
| 오차는 measured−target 방향인가 반대인가? | 조정 방향과 오차 벡터를 구분해 라벨 확정. |

## 4. 데이터와 없을 때의 대안
필수 target_xy/measured_xy 길이2 배열(mm), radius_mm 비음수 수치. 한 객체는 기준점 한 개의 관측. point_id로 도면과 결합. null 좌표는 미측정. 회전 변환은 실제 데이터에 있을 때 별도 필요.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "target": [
    0,
    0
  ],
  "measured": [
    3,
    4
  ],
  "radius": 4
}
```

## 5. 기준 방법과 개선 조건
측정−기준 벡터와 거리의 제곱을 계산해 반경제곱과 비교한다. 결과 화면에 좌표계·단위·오차 방향을 표시한다.

여러 점의 일관된 회전·평행이동이 확인되면 좌표 정합 모델을 별도 적합한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 측정 위치가 허용 반경 안인지 확인 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `{"dx": 3, "dy": 4, "distance": 5.0, "status": "outside"}` | 3²+4²=25,거리5>4. |
| 경계 | `{"radius": 5}` | `{"dx": 3, "dy": 4, "distance": 5.0, "status": "within"}` | 반경 경계 포함. |
| 정보 부족 | `{"measured": null}` | `"unknown"` | 미측정은 원점이 아님. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
위경도를 mm처럼 빼지 않는다. 원형 기준을 각 축≤반경으로 대체하면 모서리가 잘못 합격한다. 좌표계 없으면 그림 대신 원자료 요청.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 오차 방향과 실제 조정 방향을 혼동하지 않는가?
- 경계에 걸린 점의 처리 근거가 보이는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 거리5의 독립 계산을 설명할 수 있는가?
- 원형과 사각형 기준이 다른 반례는 무엇인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/decimal.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
