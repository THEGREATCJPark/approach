# 역할·과정·산출물의 다중 분류 보류

```json
{
  "id": "taxonomy-ambiguity",
  "title": "역할·과정·산출물의 다중 분류 보류",
  "family": "LEARNING",
  "keywords_ko": [
    "역할·과정·산출물의 다중 분류 보류",
    "학습 카드의 개체 종류를 확정하거나 검토로 보낸다"
  ],
  "keywords_en": [
    "taxonomy-ambiguity",
    "entity id → approved category set"
  ],
  "problem_structure": "entity id → approved category set",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작 요청: 자원봉사 교육 자료에서 누가 하는 일인지, 작업 단계인지, 만들어지는 물건인지 섞여 있어 학습 카드 유형을 정리하려 한다.",
  "do_not_use_when": "역할·과정·산출물을 한 위계의 상하관계로 억지 연결하지 않는다. 단어 출현만으로 분류하는 모델은 기준 방법이 아니다.",
  "data_required": [
    "필수 entity_id 문자열, labels 배열(role/process/product), source_id. 한 객체는 개체 하나의 승인 후보 분류. 중복 라벨은 같은 주장; null labels는 미분류. labels=[]는 검토된 무분류. 실명은 필요 없음."
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
  "path": "cases/LEARNING/taxonomy-ambiguity.md",
  "decision_signature": {
    "decision": "학습 카드의 개체 종류를 확정하거나 검토로 보낸다",
    "input_structure": "entity id → approved category set",
    "hard_constraint": "서로 다른 범주가 여러 개면 임의 단일 분류 금지",
    "validation": "중복 동일 라벨과 상충 라벨 구별"
  }
}
```

## 1. 창작 업무 요청
창작 요청: 자원봉사 교육 자료에서 누가 하는 일인지, 작업 단계인지, 만들어지는 물건인지 섞여 있어 학습 카드 유형을 정리하려 한다.
독립적으로 설계한 합성 연습이다. 공개 자료는 일반 구현 원리의 참고이며 아래 정책·수치는 창작이다.

## 2. 숨은 원인과 다른 목표
- 같은 단어가 역할과 활동 둘 다 쓰인다.
- 서로 다른 문서의 분류가 충돌한다.
- 관계 없는 부서 라벨이 개념 분류에 섞인다.

## 3. 방향을 바꾸는 질문
| 질문 | 답에 따른 변경 |
|---|---|
| 분류 대상은 문장인가 고유 개체인가? | 문장이면 문맥 자료가 먼저; 고유 id면 승인 맵 적용. |
| 복수 범주를 허용하는가? | 허용이면 다중 표시, 본 예제 단일 분류 필요면 needs_review. |
| 충돌 시 누가 정본을 정하는가? | 권한 있는 검토자 결정 전 하나를 자동 선택하지 않음. |

## 4. 데이터와 없을 때의 대안
필수 entity_id 문자열, labels 배열(role/process/product), source_id. 한 객체는 개체 하나의 승인 후보 분류. 중복 라벨은 같은 주장; null labels는 미분류. labels=[]는 검토된 무분류. 실명은 필요 없음.
필수 필드가 없으면 결과를 0으로 채우지 않고 unknown을 표시하고 위 질문의 해당 담당자에게 확인한다. 선택 자료는 기준 방법 통과 후 요청한다.

```json
{
  "entity_id": "tray",
  "labels": [
    "product",
    "product"
  ]
}
```

## 5. 기준 방법과 개선 조건
명시된 라벨을 정규화하고 고유 집합 크기가1이면 해당 범주,2이상이면 검토,0이면 무분류. 자연어 의미를 자동 추측하지 않는다.

문맥별 분류가 필요해지면 개체 id를 문맥 id와 결합하고 담당자 라벨 표본을 만든다.

## 6. 최소 구현과 다음 행동
입력 JSON/표 → 필수 필드·단위 검사 → 학습 카드의 개체 종류를 확정하거나 검토로 보낸다 → 입력·근거·판정 상태를 한 화면에 표시 → 담당자가 결과를 수용하거나 미확인 자료를 보완한다.
외부 모델·자동 전송 없이 로컬 표 또는 Python 표준 라이브러리로 시작한다. 실행 허용이 미확인이면 계산 절차와 Markdown만 읽는다.

## 7. 합성 입력과 기대 결과
각 input은 위 fixture의 최상위 키를 교체한다. 입력 배열은 전체 교체이며, 기대값은 손계산으로 정한 고정 oracle이다.
| 종류 | 입력 변화 | 기대 결과 | 근거 |
|---|---|---|---|
| 정상 | `{}` | `"product"` | 같은 라벨 중복 제거. |
| 경계 | `{"labels": ["role", "process"]}` | `"needs_review"` | 다른 두 라벨 충돌. |
| 정보 부족 | `{"labels": null}` | `"unknown"` | 아직 분류 자료 없음. |
| 새 표본 | `{"labels": []}` | `"unclassified"` | 자료를 확인했지만 허용 범주 없음. |

[실행 검사](../../examples/synthetic/check_expansion_b.py)와 [고정 fixture](../../examples/synthetic/expansion_b.json)는 앱 구현을 가져오지 않는 작은 계산 예제다. 통과는 위 입력과 판정에만 해당하며 생산 시스템 검증이 아니다.

## 8. 오용과 범위 축소
역할·과정·산출물을 한 위계의 상하관계로 억지 연결하지 않는다. 단어 출현만으로 분류하는 모델은 기준 방법이 아니다.
추가 패키지 설치가 불가하면 같은 입력을 표와 손계산으로 검사한다. 시간 부족 시 선택 기능을 줄이고 미확인 상태·필수 규칙·기대값 검사는 유지한다.

## 9. 구현물에 대한 담당자 피드백
- needs_review 카드의 출처를 비교해서 정본을 고를 수 있는가?
- 무분류와 미확인을 구별할 수 있는가?

담당자에게 결과를 보여주고 실제 다음 행동을 선택하게 한다. 완료 건수/관찰 건수, 오류와 우회 행동을 기록한다. 만족도와 업무 효과는 이 합성 검사로 입증되지 않는다.

## 10. 개발자 본인의 설명 사전 연습
PREP에서만 사용한다. 실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
- 복수 라벨을 임의 선택하지 않은 판단 근거는 무엇인가?
- 어떤 추가 문맥이 주어지면 설계를 바꿀 것인가?

## 공개 근거와 연결
- 일반 계산/자료구조 공식 문서: https://docs.python.org/3/library/stdtypes.html (문서 접근 확인; 사례 원문을 가져온 것이 아님)
- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [Python 표준 라이브러리](../../tools/python-stdlib.md)
