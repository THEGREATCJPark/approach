# 전시 설치 작업의 선행관계와 최소 완료시간

> 독립 창작 합성 사례. 실제 조직·과제·인물을 재현하지 않는다. 공개 알고리즘 자료는 방법의 참고이며 아래 업무 정책·수치는 이 연습에서 새로 정했다.

```json
{
  "id": "dependency-critical-path",
  "title": "전시 설치 작업의 선행관계와 최소 완료시간",
  "family": "DEPENDENCY",
  "keywords_ko": [
    "선행",
    "병목",
    "완료시간",
    "의존"
  ],
  "keywords_en": [
    "directed",
    "acyclic",
    "graph",
    "critical",
    "path"
  ],
  "problem_structure": "directed acyclic graph critical path",
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "선행관계와 작업시간이 만드는 critical path 문제다.",
  "do_not_use_when": "작업 간 인력 공유가 큰 일정에 DAG 완료시간을 실행 가능한 계획으로 제시하지 않는다.",
  "data_required": "작업 한 행. id 기본키, duration 정수 시간, predecessors 완료 후 시작해야 하는 id 배열. 자원 무제한, lag0, 시간0 시작을 이 합성 모델의 가정으로 고정한다.",
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": ["dependency-reachability"],
  "depth": "deep",
  "path": "cases/DEPENDENCY/dependency-critical-path.md"
}
```

## 요청과 다른 해석

“소규모 전시 설치에서 어떤 작업 지연이 전체 개장을 늦추는지 알고 싶다.”

- 선행관계와 작업시간이 만드는 critical path 문제다.
- 인원 공유가 있다면 자원 제약 일정 문제다.
- 작업시간이 불확실하면 단일 날짜는 과신일 수 있다.

## 우선 질문과 방향 변화

1. 서로 다른 작업을 동시에 할 인력이 충분한가? → 아니면 아래 DAG 하한을 실제 일정으로 부르지 않는다.
2. 선행조건은 종료 후 시작인가? → 다른 lag나 겹침이면 별도 모델이 필요하다.
3. 시간은 확정인가 범위인가? → 범위이면 시나리오별 완료시간을 제시한다.

파일에서 이미 확인되는 답은 다시 묻지 않는다. 정책을 결정할 권한자와 기준 시점을 함께 기록한다.

## 데이터 계약과 합성 입력

작업 한 행. id 기본키, duration 정수 시간, predecessors 완료 후 시작해야 하는 id 배열. 자원 무제한, lag0, 시간0 시작을 이 합성 모델의 가정으로 고정한다.

최소 필수는 아래 판정 필드와 키다. 대표 샘플·스키마로 시작하며 개인 식별 정보는 필요하지 않다. 개선용 데이터는 실제 작업 시간과 오류 기록이다. 전체 이력이나 외부 API는 첫 검증에 없어도 된다. null은 미확인이며 0·false와 다르다. 필수 필드가 없으면 해당 판정을 보류하고 담당자 확인 목록에 남긴다.

```json
[
  {
    "id": "A",
    "duration": 2,
    "predecessors": []
  },
  {
    "id": "B",
    "duration": 4,
    "predecessors": [
      "A"
    ]
  },
  {
    "id": "C",
    "duration": 3,
    "predecessors": [
      "A"
    ]
  },
  {
    "id": "D",
    "duration": 2,
    "predecessors": [
      "B",
      "C"
    ]
  },
  {
    "id": "E",
    "duration": 1,
    "predecessors": [
      "C"
    ]
  }
]
```

## 기준 방법, 제약과 최소 경로

위상 정렬로 cycle을 먼저 찾고, earliest_start=max(선행 earliest_finish), finish=start+duration을 계산한다. 후방 계산으로 slack을 구하면 병목 후보와 여유를 구분할 수 있다.

필수: 선행키 존재, duration≥0, DAG. 목적은 가정하 최소 완료시간과 critical path. 실제 인원 제약을 최적화한 결과가 아니다.

작업표 → A2 B6 C5 D8 E6 완료 → 경로 A-B-D 8시간 → 담당자가 B 지연을 우선 점검한다.

## 기대 결과와 반례

| 유형 | 입력 또는 변경 | 기대 결과 |
|---|---|---|
| 정상 | 기본 다섯 작업 | 최소 완료8,critical A-B-D |
| 경계 | E duration0 | 완료8 유지 |
| 정보 부족 | B duration=null | 완료시간 판정 보류 |
| 충돌 | A 선행에D 추가 | cycle,일정 불가능 |
| 순서변경 | 행 순서 역전 | 완료8 유지 |
| 새 샘플 | C duration5 | 완료9,critical A-C-D |

손계산 근거: A 종료2. B=2+4=6, C=2+3=5. D=max(6,5)+2=8, E=5+1=6. C가5시간이면 종료7,D9라 경로가 바뀐다.

비슷하지만 다른 두 건: C가1시간 지연되면 D 시작6으로 전체8 유지,2시간 지연되면 D 시작7로 전체9가 된다.

작은 계산 예제는 [check_c.py](../../examples/synthetic/check_c.py)에서 별도 표준 라이브러리 계산으로 확인한다. 각 수용 테스트 행의 기대값은 소형 오라클 계산으로 확인한다. 전체 앱·화면·DB 동시성은 구현하거나 검증하지 않았으며, 기대값 검증과 구현물 테스트 통과는 다르다. 실행 범위는 해당 스크립트 출력과 검증 보고서를 따른다.

## 답변이 바뀌면 수정할 계획

- 인력 한 팀뿐이라면 병렬 가정을 제거하고 자원 배정 일정으로 전환한다.
- 선행관계가 잠정이면 확정·잠정 시나리오를 따로 계산한다.

## 피할 구현과 축소 기준

- 작업 간 인력 공유가 큰 일정에 DAG 완료시간을 실행 가능한 계획으로 제시하지 않는다.
- cycle을 임의 제거하거나 누락 작업 시간을0으로 채우지 않는다.
- 시간 부족이면 Gantt 장식 대신 시작/종료/선행 표와 cycle 오류를 유지한다.

1순위 도구는 [Python 표준 라이브러리](../../tools/python-stdlib.md)다. 이 작은 합성 입력에는 패키지 설치·외부 호출이 필요 없다. Python도 실행할 수 없으면 표에 후보를 전부 적고 손계산한다. 대규모 개선 도구는 설치·규정·입력 적합성이 확인된 이후 별도 선택한다.

## 연습 시간 예산과 효과 측정

30분: 다섯 종료시간 손계산. 90분: 선행키·cycle 검증과 표. 180분: slack과 기간 범위 시나리오. 권장 연습 예산이다.

모델 완료시간, cycle 수, 미확인 duration 수를 측정한다. 이 합성 예제만으로 실제 조직의 시간 절감·만족도·수익 향상을 주장할 수 없다.

## 구현물에 대한 담당자 피드백

1. 결과 한 건의 근거와 보류 사유를 보고 다음 행동을 선택할 수 있는가? 실제로 선택하는 모습을 관찰한다.
2. 서로 다른 작업을 동시에 할 인력이 충분한가?에 대한 합의와 화면 결과가 어긋나는 사례가 있는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

1. 이 기준 방법을 선택한 이유를 입력 크기·정책·반례 파일을 근거로 설명할 수 있는가?
2. 전시 설치 작업의 선행관계와 최소 완료시간에서 계산 검증이 보장하지 못하는 부분은 무엇이며 어떤 추가 관찰이 필요한가?

## 공개 근거

- [공식 기술 문서](https://docs.python.org/3/library/graphlib.html) — 일반 계산 구조를 참고했다. 창작 업무 조건의 외부 검증이나 적용 허가를 뜻하지 않는다.
- [기준 방법](../../methods/baseline-first.md), [독립 검증](../../methods/verification.md)
