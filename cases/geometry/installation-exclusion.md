# 설치 금지 사각형과 후보점 경계 판정

```json
{
  "id": "installation-exclusion",
  "title": "설치 금지 사각형과 후보점 경계 판정",
  "family": "GEOMETRY",
  "keywords_ko": [
    "설치",
    "금지",
    "사각형과",
    "후보점",
    "경계",
    "판정"
  ],
  "keywords_en": [
    "geometry-filter",
    "installation-exclusion"
  ],
  "problem_structure": "geometry-filter",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "지역 기록실에서 이동식 안내 장치 후보점을 정했는데 통행 확보 구역 안이나 경계에 있는 점을 제외해 달라.",
  "do_not_use_when": "금지구역은 비용점수로 상쇄하지 않는다. 위치가 안전하다는 법적·현장 보증으로 확대하지 않는다.",
  "data_required": [
    "최소: point=[x,y] m, forbidden=[xmin,ymin,xmax,ymax] m 또는 null; 한 레코드 한 후보점 candidate_id. 좌표계 동일. null은 금지정보 미확인. 개선: 장치 footprint·여유거리. 도면 누락이면 설치 승인 불가."
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
  "path": "cases/geometry/installation-exclusion.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "geometry-filter",
    "input_structure": "최소: point=[x,y] m, forbidden=[xmin,ymin,xmax,ymax] m 또는 null; 한 레코드 한 후보점 candidate_id. 좌표계 동일. null은 금지정보 미확인. 개선: 장치 footprint·여유거리. 도면 누락이면 설치 승인 불가.",
    "hard_constraint": "금지구역은 비용점수로 상쇄하지 않는다. 위치가 안전하다는 법적·현장 보증으로 확대하지 않는다.",
    "validation": "0<=3,4<=5; x=5 경계 포함; 영역 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

지역 기록실에서 이동식 안내 장치 후보점을 정했는데 통행 확보 구역 안이나 경계에 있는 점을 제외해 달라.

가능한 설명: 금지구역 경계 포함 규칙이 다르다; 좌표 단위가 다르다; 점만 검사하고 장치 폭을 빠뜨렸다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 장치는 점으로 근사해도 됩니까? → 폭 필요 시 금지구역을 장치 여유만큼 확장.
2. 경계도 금지입니까? → 현 예제는 포함, 아니면 strict 비교.
3. 금지구역이 최신 도면과 같습니까? → 버전 미확인 시 보류.

## 3. 데이터 계약과 자료 부족 대안

최소: point=[x,y] m, forbidden=[xmin,ymin,xmax,ymax] m 또는 null; 한 레코드 한 후보점 candidate_id. 좌표계 동일. null은 금지정보 미확인. 개선: 장치 footprint·여유거리. 도면 누락이면 설치 승인 불가. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 닫힌 사각형 포함이면 forbidden, 바깥이면 allowed. 부등호 경계 포함을 명시한다.

개선: 비정형 도형이면 polygon containment; footprint의 실제 충돌과 점 포함을 구별.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

후보점·금지구역 → 포함 판정 → 사유와 허용/금지/보류 → 담당자가 후보 위치 조정. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"point":[3,4],"forbidden":[0,0,5,5]}`|`"forbidden"`|0<=3,4<=5|
|boundary|`{"point":[5,2],"forbidden":[0,0,5,5]}`|`"forbidden"`|x=5 경계 포함|
|missing|`{"point":[8,2],"forbidden":null}`|`"unknown"`|영역 미확인|

## 7. 흔한 오류와 범위 축소

금지구역은 비용점수로 상쇄하지 않는다. 위치가 안전하다는 법적·현장 보증으로 확대하지 않는다. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 경계 후보를 제외하는 규칙이 운영 기준과 맞습니까?
- 장치의 실제 크기를 반영해야 할 후보는 무엇입니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 경계값 테스트에서 <=를 쓴 근거는 무엇입니까?
- 점 판정에서 면적 충돌로 바뀌는 추가 데이터는 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
