# 필수 증빙 누락과 수동 검토 경로

```json
{
  "id": "evidence-manual-review",
  "title": "필수 증빙 누락과 수동 검토 경로",
  "family": "TRANSACTION",
  "keywords_ko": [
    "필수",
    "증빙",
    "누락과",
    "수동",
    "검토",
    "경로"
  ],
  "keywords_en": [
    "evidence-gate",
    "evidence-manual-review"
  ],
  "problem_structure": "evidence-gate",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "공동 창작공간의 보증 물품 반환 요청에서 파손 확인 자료가 없으면 자동 승인·자동 거절 모두 하지 말고 담당자에게 넘겨 달라.",
  "do_not_use_when": "증빙 완비를 무결함 또는 반환완료로 표시하지 않는다. 자료 부족 요청에 0점 자동 거절 금지.",
  "data_required": [
    "최소: required 증빙 ID 목록, present 증빙 ID 목록, age_days int/null, max_age_days int, defect bool/null. 한 행 return_id. null 상태는 미확인, []present는 없음 확인. 개선: 증빙출처·촬영시각."
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
  "path": "cases/TRANSACTION/evidence-manual-review.md",
  "test_count": 3,
  "fixture_path": "examples/synthetic/expansion_e.json",
  "decision_signature": {
    "decision": "evidence-gate",
    "input_structure": "최소: required 증빙 ID 목록, present 증빙 ID 목록, age_days int/null, max_age_days int, defect bool/null. 한 행 return_id. null 상태는 미확인, []present는 없음 확인. 개선: 증빙출처·촬영시각.",
    "hard_constraint": "증빙 완비를 무결함 또는 반환완료로 표시하지 않는다. 자료 부족 요청에 0점 자동 거절 금지.",
    "validation": "photo 누락; 시효3 경계 허용; 촬영 나이 미확인"
  }
}
```

## 1. 창작 업무 요청과 숨은 가설

공동 창작공간의 보증 물품 반환 요청에서 파손 확인 자료가 없으면 자동 승인·자동 거절 모두 하지 말고 담당자에게 넘겨 달라.

가능한 설명: 자료 없음과 이상 없음이 혼동된다; 최소 증빙 목록이 없다; 오래된 사진을 최신 상태로 본다. 이 배경·수치·정책은 독립 창작이다. 실제 업무 조건으로 자동 적용하지 않는다.

## 2. 방향을 가르는 담당자 질문

1. 어떤 증빙이 필수입니까? → required 목록 확정.
2. 최대 자료 나이는 며칠입니까? → age 기준 확인.
3. 결함 확인 시 자동 거절입니까? → 이번 범위는 review_defect로 사람이 결정.

## 3. 데이터 계약과 자료 부족 대안

최소: required 증빙 ID 목록, present 증빙 ID 목록, age_days int/null, max_age_days int, defect bool/null. 한 행 return_id. null 상태는 미확인, []present는 없음 확인. 개선: 증빙출처·촬영시각. 자료를 받을 수 없으면 합성 예제로 형식만 확인하고 실제 판정은 보류한다. 최소 자료를 먼저 요청하고 불필요한 개인정보를 요청하지 않는다.

## 4. 기준 방법과 개선 조건

기준: 필드 미확인 unknown; required 미충족 manual_missing; 자료 오래됨 manual_stale; defect=True manual_defect; 모두 충족이면 ready_for_decision.

개선: 담당자 큐와 누락 요청 안내; 자연어 사진판독 모델은 성능·권한 확인 전 제외.

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 설치 불가 또는 실행 미허용이면 아래 소형 예제를 손계산한다. 새 도구를 설치하기 전에 기존 실행 환경과 규정을 확인한다.

## 5. 최소 구현과 다음 행동

요청·증빙 메타데이터 → 누락/시효 검사 → 검토큐 사유 → 사람이 최종 결정. 처음에는 한 건 입력과 결과·사유·미확인 상태를 표시하는 표로 충분하다. 자동 승인·외부 실행 기능은 이 연습의 기본 범위가 아니다.

## 6. 합성 입력과 기대값

[fixture](../../examples/synthetic/expansion_e.json)에서 이 카드 ID를 찾는다. 아래 기대값은 직접 규칙과 산술로 계산했다. [독립 계산 검사](../../examples/synthetic/check_expansion_e.py)는 실제 앱이나 외부 서비스에 연결하지 않는다.

|종류|입력|기대|계산·근거|
|---|---|---|---|
|normal|`{"required":["photo","tag"],"present":["tag"],"age_days":1,"max_age_days":3,"defect":false}`|`"manual_missing"`|photo 누락|
|boundary|`{"required":["photo"],"present":["photo"],"age_days":3,"max_age_days":3,"defect":false}`|`"ready_for_decision"`|시효3 경계 허용|
|missing|`{"required":["photo"],"present":["photo"],"age_days":null,"max_age_days":3,"defect":false}`|`"unknown"`|촬영 나이 미확인|

## 7. 흔한 오류와 범위 축소

증빙 완비를 무결함 또는 반환완료로 표시하지 않는다. 자료 부족 요청에 0점 자동 거절 금지. 연습 시간이 부족하면 개선 알고리즘·시각 장식을 줄이고 정상·경계·자료부족 세 상태는 유지한다. 입력 계약 밖의 값은 검증 오류로 분리하며 합성 계산기의 지원 범위를 확대 해석하지 않는다.

## 8. 구현물 사용자 피드백

- 누락 사유가 추가로 받아야 할 자료를 알려줍니까?
- ready_for_decision과 최종 승인이 구분됩니까?

사용자에게 실제 과제를 수행하게 하고 관찰한 오류·우회·다음 행동을 기록한다. “좋나요?”만 묻지 않는다.

## 9. 개발자 설명 연습 — PREP 전용

AI 금지 실제 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다. 아래는 사전 창작 연습에서 본인이 근거 파일로 설명할 질문이다.

- 자료 없음과 결함 없음의 반례를 제시하십시오.
- 모델 판독 없이도 해결한 업무 부분은 무엇입니까?

## 10. 검증 범위·공개 근거

측정 가능: 명시한 합성 입력의 기대 일치 여부, 보류·충돌 상태 누락 수. 실제 사용자 오류 감소·처리시간 절감·현장 효과는 아직 측정하지 않았다. 이 소형 oracle은 입력 계약 안의 예제 검사용이며 배포용 완성 구현이 아니다.

[Python 공식 문서](https://docs.python.org/3/library/decimal.html), [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)을 참고한다. 공식 문서는 계산 도구의 공개 근거이며 이 창작 업무의 정책 출처는 아니다.
