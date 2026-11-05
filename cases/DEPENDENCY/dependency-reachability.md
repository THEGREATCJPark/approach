# 수리 부품 중단의 영향 경로 추적

> 독립 창작 합성 사례. 실제 조직·과제·인물을 재현하지 않는다. 공개 알고리즘 자료는 방법의 참고이며 아래 업무 정책·수치는 이 연습에서 새로 정했다.

```json
{
  "id": "dependency-reachability",
  "title": "수리 부품 중단의 영향 경로 추적",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "의존",
    "영향",
    "경로",
    "공급"
  ],
  "keywords_en": [
    "directed",
    "graph",
    "reachability"
  ],
  "problem_structure": "directed graph reachability",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "확인된 필수 의존 관계의 도달 가능성이 필요하다.",
  "do_not_use_when": "금액 손실·확률 예측이 필요한 과제에 단순 도달 수를 답으로 쓰지 않는다.",
  "data_required": "방향 간선 한 행. source 공급 노드, target 의존 노드, type required/optional, verified 불리언. 아래는 source 중단이 target 검토 대상으로 전파되는 방향. 관계키(source,target,type).",
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": ["dependency-critical-path"],
  "depth": "deep",
  "path": "cases/DEPENDENCY/dependency-reachability.md"
}
```

## 요청과 다른 해석

“지역 수리망의 공용 부품이 중단되면 어떤 키트와 서비스가 영향을 받을지 근거 경로를 보고 싶다.”

- 확인된 필수 의존 관계의 도달 가능성이 필요하다.
- 대체재가 있으면 도달 가능과 실제 중단은 다르다.
- 관계 출처가 오래되어 그래프 자체가 틀릴 수 있다.

## 우선 질문과 방향 변화

1. 간선은 필수 공급인가 참고 관계인가? → 필수 확인 관계만 주 영향 경로에 쓴다.
2. 대체 경로가 있는가? → 있으면 단순 도달을 중단 확정으로 표시하지 않는다.
3. 간선 기준 시점·출처가 있는가? → 없으면 미확인 관계로 분리한다.

파일에서 이미 확인되는 답은 다시 묻지 않는다. 정책을 결정할 권한자와 기준 시점을 함께 기록한다.

## 데이터 계약과 합성 입력

방향 간선 한 행. source 공급 노드, target 의존 노드, type required/optional, verified 불리언. 아래는 source 중단이 target 검토 대상으로 전파되는 방향. 관계키(source,target,type).

최소 필수는 아래 판정 필드와 키다. 대표 샘플·스키마로 시작하며 개인 식별 정보는 필요하지 않다. 개선용 데이터는 실제 작업 시간과 오류 기록이다. 전체 이력이나 외부 API는 첫 검증에 없어도 된다. null은 미확인이며 0·false와 다르다. 필수 필드가 없으면 해당 판정을 보류하고 담당자 확인 목록에 남긴다.

```json
[
  {
    "source": "P",
    "target": "K",
    "type": "required",
    "verified": true
  },
  {
    "source": "K",
    "target": "S",
    "type": "required",
    "verified": true
  },
  {
    "source": "P",
    "target": "T",
    "type": "optional",
    "verified": true
  },
  {
    "source": "X",
    "target": "S",
    "type": "required",
    "verified": true
  },
  {
    "source": "S",
    "target": "Z",
    "type": "required",
    "verified": null
  }
]
```

## 기준 방법, 제약과 최소 경로

확인된 required 간선에서 BFS/DFS로 방문 집합과 첫 근거 경로를 구한다. 미확인·선택 간선은 별도 표시한다. 개선은 대체 공급의 논리식과 상태를 명시한 후 전파한다.

필수: 방향·관계 종류·출처 확인 상태 보존, 순환에서는 방문 집합으로 종료. 목적은 검토 후보 추적이며 매출 손실 예측이 아니다.

간선표 → P에서 K,S 도달 → P→K→S 경로 표시 → 담당자가 K/S 대체 가능 여부를 점검한다.

## 기대 결과와 반례

| 유형 | 입력 또는 변경 | 기대 결과 |
|---|---|---|
| 정상 | P에서 확인 required 탐색 | K,S |
| 경계 | 없는 노드 Q 조회 | 노드 없음 오류; 영향0과 구별 |
| 정보 부족 | S→Z verified=null | Z 미확인 후보,확정 집합 제외 |
| 충돌 | K→P required 추가 | 순환 경고,탐색 종료 |
| 중복 | P→K 같은 간선 반복 | K를 한 번만 집계 |
| 새 샘플 | P→T를required로 변경 | K,S,T |

손계산 근거: P의 확인 필수 이웃은 K, K의 이웃은 S. P→T는 optional, S→Z는 미확인이라 확정 집합 크기2. X는 S의 다른 공급원이지 P의 하류가 아니다.

비슷하지만 다른 두 건: P→K와 K→P는 영향 방향이 반대다. 선만 연결된 그림으로 동일하게 처리하면 안 된다.

작은 계산 예제는 [check_c.py](../../examples/synthetic/check_c.py)에서 별도 표준 라이브러리 계산으로 확인한다. 각 수용 테스트 행의 기대값은 소형 오라클 계산으로 확인한다. 전체 앱·화면·DB 동시성은 구현하거나 검증하지 않았으며, 기대값 검증과 구현물 테스트 통과는 다르다. 실행 범위는 해당 스크립트 출력과 검증 보고서를 따른다.

## 답변이 바뀌면 수정할 계획

- 대체 공급 X가 S를 완전히 유지한다면 S는 검토 후보이되 중단 확정에서는 제외한다.
- 정량 손실을 요구하면 노드별 수요·재고·대체 용량·기간을 추가받고 별도 모델을 만든다.

## 피할 구현과 축소 기준

- 금액 손실·확률 예측이 필요한 과제에 단순 도달 수를 답으로 쓰지 않는다.
- 관계 계수를 근거 없이 곱하거나 모든 관계를 무방향 처리하지 않는다.
- 시간 부족이면 복잡한 그래프 UI보다 경로·관계 출처 표를 유지한다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 이 작은 합성 입력에는 패키지 설치·외부 호출이 필요 없다. Python도 실행할 수 없으면 표에 후보를 전부 적고 손계산한다. 대규모 개선 도구는 설치·규정·입력 적합성이 확인된 이후 별도 선택한다.

## 연습 시간 예산과 효과 측정

30분: 세 관계 경로 손그림. 90분: 입력과 경로 표. 180분: 대체 관계·출처 만료 표시. 권장 연습 예산이다.

도달 노드 수와 근거 누락 관계 수를 측정한다. 이 합성 예제만으로 실제 조직의 시간 절감·만족도·수익 향상을 주장할 수 없다.

## 구현물에 대한 담당자 피드백

1. 결과 한 건의 근거와 보류 사유를 보고 다음 행동을 선택할 수 있는가? 실제로 선택하는 모습을 관찰한다.
2. 간선은 필수 공급인가 참고 관계인가?에 대한 합의와 화면 결과가 어긋나는 사례가 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

1. 이 기준 방법을 선택한 이유를 입력 크기·정책·반례 파일을 근거로 설명할 수 있는가?
2. 수리 부품 중단의 영향 경로 추적에서 계산 검증이 보장하지 못하는 부분은 무엇이며 어떤 추가 관찰이 필요한가?

## 공개 근거

- [공식 기술 문서](https://docs.python.org/3/library/collections.html#collections.deque) — 일반 계산 구조를 참고했다. 창작 업무 조건의 외부 검증이나 적용 허가를 뜻하지 않는다.
- [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)
