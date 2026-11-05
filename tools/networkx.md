# NetworkX

- id: `networkx`
- 적합: 방향 관계 경로·연결성·의존 전파 후보
- 부적합: 관계만으로 인과 효과나 매출 손실 수치 확정
- 확인: 2026-11-05 / `docs_verified` / Python + NetworkX; stable 문서, 실행 미검증
- [공식 저장소·홈](https://github.com/networkx/networkx) · [공식 문서와 예제](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html) · [라이선스 원문](https://raw.githubusercontent.com/networkx/networkx/main/LICENSE.txt)

## 먼저 확인할 것

weight=None이면 간선 수 경로다. 가중치·음수 여부·방향을 확인한다. 순환 그래프를 DAG로 가정하지 않는다.

## 입출력·설치

- 입력: 노드 ID·방향 edge·의미·출처·weight 단위
- 최소 출력: 경로·도달 집합·끊긴 대상과 가정
- 설치 조건: 허용된 고정 버전 networkx 설치
- 설치 불가 대안: dict adjacency + BFS/DFS 표준 라이브러리

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 기본 로컬 연산은 외부 호출·자격증명 불필요. 설치/문서 조회만 네트워크를 사용할 수 있고, 별도 I/O 코드 추가 시 다시 확인.
자격증명: 로컬 기본 예제는 불필요.
비용: Python 그래프 객체는 대규모 edge에서 메모리 부담. 무가중 BFS는 O(V+E), 모든 쌍 경로는 별도 비용; 필요한 출발점만 계산한다.

## 확인 범위

라이선스: BSD-3-Clause. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`DEPENDENCY`, `LEARNING` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.
