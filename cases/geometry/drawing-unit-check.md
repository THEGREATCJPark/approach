# 도면 좌표와 실측 기준선의 축척 검사

```json
{
  "id": "drawing-unit-check",
  "title": "도면 좌표와 실측 기준선의 축척 검사",
  "family": "GEOMETRY",
  "keywords_ko": [
    "도면",
    "좌표와",
    "실측",
    "기준선의",
    "축척",
    "검사"
  ],
  "keywords_en": [
    "unit-validation",
    "drawing-unit-check"
  ],
  "problem_structure": "unit-validation",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "소형 전시 부스 도면의 좌표가 mm인지 cm인지 불명확해 설치 거리 계산 전에 실측 기준선과 맞는지 검사해 달라.",
  "do_not_use_when": "위경도에 mm 환산을 적용하지 않는다. 단위 없는 숫자에서 자동으로 가장 잘 맞는 단위를 정답으로 확정하지 않는다.",
  "data_required": [
    "최소: drawing_length 양수, unit mm/cm/m, measured_mm 양수, tolerance_mm>=0; 한 행 calibration_id별 같은 기준선. null 필드는 unknown. 개선: 두 번째 축 기준선·원점·회전. 실측 없으면 축척 검증 불가."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rectangle-union"
  ],
  "depth": "standard",
  "path": "cases/geometry/drawing-unit-check.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "unit-validation",
    "input_structure": "최소: drawing_length 양수, unit mm/cm/m, measured_mm 양수, tolerance_mm>=0; 한 행 calibration_id별 같은 기준선. null 필드는 unknown. 개선: 두 번째 축 기준선·원점·회전. 실측 없으면 축척 검증 불가.",
    "hard_constraint": "위경도에 mm 환산을 적용하지 않는다. 단위 없는 숫자에서 자동으로 가장 잘 맞는 단위를 정답으로 확정하지 않는다.",
    "validation": "120과121 차1<=2; 차2는 경계 포함; 단위 없음"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

소형 전시 부스 도면의 좌표가 mm인지 cm인지 불명확해 설치 거리 계산 전에 실측 기준선과 맞는지 검사해 달라.

가능한 설명: 단위 표기가 틀렸다; 좌표 변환에서 축척이 두 번 적용됐다; 실측 기준선 자체가 다른 점 쌍이다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 기준선 양끝이 같은 객체입니까? → 아니면 비교 중단.
2. 단위가 공식 메타데이터입니까? → 미확인 단위는 추측 변환 금지.
3. 허용 오차는 몇 mm입니까? → 확인된 tolerance로만 pass 결정.

## 3. 데이터 계약과 자료 부족 대안

최소: drawing_length 양수, unit mm/cm/m, measured_mm 양수, tolerance_mm>=0; 한 행 calibration_id별 같은 기준선. null 필드는 unknown. 개선: 두 번째 축 기준선·원점·회전. 실측 없으면 축척 검증 불가. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 지정 단위를 mm로 환산한 뒤 절대오차<=tolerance이면 match, 초과 mismatch. 지원하지 않는 단위는 unknown.

개선: 여러 기준선으로 축별 스케일·회전 오차를 분리; 한 선 일치로 전체 도면 정확성을 주장하지 않는다.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

기준선·단위 입력 → mm 변환·오차 → match/mismatch/unknown과 오차 → 담당자가 단위 또는 도면 수정. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"drawing_length":12,"unit":"cm","measured_mm":121,"tolerance_mm":2}`|`"match"`|120과121 차1<=2|
|boundary|`{"drawing_length":1,"unit":"m","measured_mm":1002,"tolerance_mm":2}`|`"match"`|차2는 경계 포함|
|missing|`{"drawing_length":12,"unit":null,"measured_mm":120,"tolerance_mm":2}`|`"unknown"`|단위 없음|

## 7. 흔한 오류와 범위 축소

위경도에 mm 환산을 적용하지 않는다. 단위 없는 숫자에서 자동으로 가장 잘 맞는 단위를 정답으로 확정하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- mismatch일 때 어떤 원본을 고칠 수 있습니까?
- 추가 기준선을 어디에서 측정해야 합니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 허용오차 경계의 기대값을 어떻게 계산했습니까?
- 한 기준선 통과로 보장할 수 없는 공간 오류는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
