# 고정 근무 구간의 서비스 공백 찾기

독립 창작 합성 사례. 아래 수치·정책은 연습용이며 실제 기관·과제에서 가져오지 않았다.

```json
{
  "id": "planning-service-coverage",
  "title": "고정 근무 구간의 서비스 공백 찾기",
  "family": "PLANNING",
  "problem_structure": "interval union gap detection",
  "keywords_ko": [
    "고정",
    "근무",
    "구간의",
    "서비스",
    "공백",
    "찾기"
  ],
  "keywords_en": [
    "interval",
    "union",
    "gap",
    "detection"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 장비 대여 창구가 직원 근무시간은 충분한데 접수 가능한 시간에 공백이 생긴다는 문의를 받았다.",
  "do_not_use_when": "겹친 근무시간을 합쳐 공백을 상쇄하지 않는다. 자동 편성을 요청받지 않았다면 검출 보고만 만든다.",
  "data_required": [
    "window=[open,close], shifts는 [start,end] 정수 분 구간 배열. 한 행은 직원 한 명의 확정 서비스 가능 구간; 동일 분 기준. null 끝점은 unknown. 사람 신원은 필요 없다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "rotation-budget"
  ],
  "depth": "standard",
  "path": "cases/PLANNING/planning-service-coverage.md",
  "test_count": 3,
  "decision_signature": {
    "decision": "창작: 작은 장비 대여 창구가 직원 근무시간은 충분한데 접수 가능한 시간에 공백이 생긴다는 문의를 받았다.",
    "input_structure": "window=[open,close], shifts는 [start,end] 정수 분 구간 배열. 한 행은 직원 한 명의 확정 서비스 가능 구간; 동일 분 기준. null 끝점은 unknown. 사람 신원은 필요 없다.",
    "hard_constraint": "근무 구간을 영업 창에 잘라 정렬·합집합 병합 후 미덮인 구간을 출력한다. 맞닿은 구간은 공백이 없다.",
    "validation": "30분 경계 맞닿음"
  }
}
```

## 업무 요청과 다른 원인

창작: 작은 장비 대여 창구가 직원 근무시간은 충분한데 접수 가능한 시간에 공백이 생긴다는 문의를 받았다.

- 총근무시간과 연속 서비스 혼동
- 점심시간 중복 이탈
- 영업범위 밖 시간을 포함해 합계 과대

## 담당자에게 먼저 물을 질문

1. 한 명만 있으면 서비스 가능한가? → 이 예제는 그렇고 최소2명이면 중첩 개수 모델이 필요하다.
2. 시작·끝 경계는 어떻게 세는가? → [start,end)로 합의한다.
3. 구간은 고정인가 재배치 가능한가? → 고정이면 공백 검출,가능하면 편성 문제로 바뀐다.

## 데이터 계약과 자료 부족 대안

window=[open,close], shifts는 [start,end] 정수 분 구간 배열. 한 행은 직원 한 명의 확정 서비스 가능 구간; 동일 분 기준. null 끝점은 unknown. 사람 신원은 필요 없다.

최소 필수 필드만 대표 표본으로 먼저 확인한다. 개선용 이력은 기본 판정이 맞은 뒤 요청한다. 필요한 자료가 없으면 아래 합성 입력으로 흐름만 확인하고 실제 판정은 보류한다.

## 단순 기준 방법과 개선 조건

근무 구간을 영업 창에 잘라 정렬·합집합 병합 후 미덮인 구간을 출력한다. 맞닿은 구간은 공백이 없다.

최소 서비스 인원·휴게 규정·업무 종류를 받으면 시간대 인원 제약을 검사한다.

## 최소 구현과 다음 행동

영업창·근무표 → 구간 병합 → 공백 분과 구간 → 담당자가 교대 조정

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 계산·판정 근거 |
|---|---|---|---|
| normal | `{"window":[0,60],"shifts":[[0,20],[30,60]]}` | `{"gaps": [[20, 30]], "minutes": 10}` | 20~30분만 미덮임 |
| boundary | `{"window":[0,60],"shifts":[[0,30],[30,60]]}` | `{"gaps": [], "minutes": 0}` | 30분 경계 맞닿음 |
| missing | `{"window":[0,60],"shifts":[[0,null]]}` | `"unknown"` | 퇴근 시각 미확인 |

[fixture 묶음](../../examples/synthetic/expansion_d.json)과 [작은 독립 계산](../../examples/synthetic/check_expansion_d.py)을 연결한다. 이것은 생산 구현·동시성·UI 검증이 아니며 입력 전부를 처리하는 완성 앱도 아니다. 정상·경계·정보 부족 세 기대값의 실행 결과만 검증 기록에 센다.

## 피할 구현과 범위 축소

겹친 근무시간을 합쳐 공백을 상쇄하지 않는다. 자동 편성을 요청받지 않았다면 검출 보고만 만든다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md). 작은 입력의 표 계산·집합·정수 계산이면 충분하다. 실행이 허용되지 않거나 Python이 없으면 표와 손계산으로 기대값을 대조한다. 별도 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 표시된 공백에 접수 중단 안내가 필요한가?
- 실제 휴게·준비 시간이 구간에서 빠져 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 아래는 허용된 사전 창작 연습에서 본인이 답한 뒤 실제 파일 근거를 확인할 질문이다.

- 총합 시간이 충분해도 공백이 생기는 이유는 무엇인가?
- 맞닿은 끝점을 공백으로 잘못 세지 않았는가?

## 검증 범위와 공개 참고

측정 가능 항목은 합성 기대값 일치 수, 잘못된 판정 수, unknown 표시 누락 수이다. 실제 시간 절감·사용자 만족·운영 안정성은 현장 관찰 없이는 주장하지 않는다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 계산 자료구조의 기술 참고. 창작 정책에 대한 외부 승인이나 정확성 보증은 아니다.
