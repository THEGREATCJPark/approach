# 오개념 태그별 승인 피드백 선택

```json
{
  "id": "misconception-feedback",
  "title": "오개념 태그별 승인 피드백 선택",
  "family": "LEARNING",
  "keywords_ko": [
    "오개념 태그별 승인 피드백 선택",
    "관측된 오류 유형에 맞는 교정 행동을 고른다"
  ],
  "keywords_en": [
    "misconception-feedback",
    "attempt → misconception tags → feedback map"
  ],
  "problem_structure": "attempt → misconception tags → feedback map",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 도구 사용 교육에서 같은 오답에도 원인이 달라서 모든 학습자에게 동일한 해설을 반복하는 문제를 줄이려 한다.",
  "do_not_use_when": "오답 문자열에 특정 단어가 있다는 이유로 오개념을 확정하지 않는다. 생성형 튜터는 진단 근거를 대신하지 못한다.",
  "data_required": [
    "필수 attempt_id, tags 배열, feedback_map(tag→승인 피드백 id). 한 객체는 한 시도. null tags는 관측 없음, []는 관측된 오개념 없음. 설명 원문·승인버전은 운영 자료. 점수만으로 태그 생성하지 않는다."
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
  "path": "cases/LEARNING/misconception-feedback.md",
  "decision_signature": {
    "decision": "관측된 오류 유형에 맞는 교정 행동을 고른다",
    "input_structure": "attempt → misconception tags → feedback map",
    "hard_constraint": "상충·미등록 태그는 추측해 답하지 않음",
    "validation": "정답 공개 없이 다음 연습 행동 선택"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 도구 사용 교육에서 같은 오답에도 원인이 달라서 모든 학습자에게 동일한 해설을 반복하는 문제를 줄이려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 단위 변환 오류와 순서 오류를 같은 오답으로 처리한다.
- 관측된 근거 없이 오개념을 추정한다.
- 서로 배타적인 오류 태그가 함께 붙는다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 태그는 누가 어떤 관측으로 확정하는가? | 근거가 없으면 진단 질문부터, 자동 단정 금지. |
| 복수 오류를 동시에 다뤄도 되는가? | 순서가 필요하면 교사가 우선순위를 정함; 본 예제 복수면 review. |
| 피드백은 답인가 다음 시도 행동인가? | 행동 지시만이면 정답 노출 없는 승인 문구 연결. |

## 4. 데이터와 없을 때의 대안
필수 attempt_id, tags 배열, feedback_map(tag→승인 피드백 id). 한 객체는 한 시도. null tags는 관측 없음, []는 관측된 오개념 없음. 설명 원문·승인버전은 운영 자료. 점수만으로 태그 생성하지 않는다.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "tags": [
    "unit-scale"
  ],
  "map": {
    "unit-scale": "compare-units",
    "order-swap": "trace-steps"
  }
}
```

## 5. 기준 방법과 개선 조건
태그 중복 제거 → 단일 승인 매핑 선택. 빈 태그는 표적 피드백 없음, 여러 태그나 미등록 태그는 검토. 학습자에게 재시도 행동과 그 이유를 보여준다.

복수 오류의 실제 수정 순서 자료가 생기면 교사 승인된 우선순위를 추가한다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 관측된 오류 유형에 맞는 교정 행동을 고른다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `"compare-units"` | 등록된 단일 오류. |
| 경계 | `{"tags": []}` | `"no_targeted_feedback"` | 오류 근거 없으면 교정문 강제 제공하지 않음. |
| 정보 부족 | `{"tags": null}` | `"unknown"` | 시도 관측 없음. |
| 충돌 | `{"tags": ["unit-scale", "order-swap"]}` | `"needs_review"` | 복수 교정 순서는 담당자 확인. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
오답 문자열에 특정 단어가 있다는 이유로 오개념을 확정하지 않는다. 생성형 튜터는 진단 근거를 대신하지 못한다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- 이 행동 지시로 다시 시도할 수 있는가?
- 틀리지 않은 개념까지 고치라고 느껴지는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 피드백 선택 근거와 오개념 진단 근거를 어떻게 구분했는가?
- 관측 누락을 표시한 반례를 설명할 수 있는가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/stdtypes.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
