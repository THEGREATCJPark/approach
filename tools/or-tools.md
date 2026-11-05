# OR-Tools

- id: `or-tools`
- 적합: 기간 배정 CP-SAT, 방문 순서 Routing, 선형/정수 모델별 선택
- 부적합: 단순 필터, 정의되지 않은 목적함수, 연속 제약의 무검토 CP-SAT 투입
- 확인: 2026-11-05 / `docs_verified` / Python와 대응 wheel; 현재 문서 stable, 실행 미검증
- [공식 저장소·홈](https://github.com/google/or-tools) · [공식 문서와 예제](https://developers.google.com/optimization/cp/cp_solver) · [라이선스 원문](https://raw.githubusercontent.com/google/or-tools/stable/LICENSE)

## 먼저 확인할 것

OPTIMAL/FEASIBLE/INFEASIBLE/MODEL_INVALID/UNKNOWN을 보존. 시간 만료 미발견은 불가능 증명이 아니다. Routing을 기간 편성의 대용으로 쓰지 않는다.

## 입출력·설치

- 입력: 정수 변수 범위·필수 제약·목적·시간 제한
- 최소 출력: 상태·목적값·배정·미배정·위반 목록
- 설치 조건: 허용된 환경에서 고정 버전 ortools wheel 설치. CP-SAT 정수 스케일 설계 필요
- 설치 불가 대안: 작은 입력 완전탐색 또는 greedy와 명시적 위반 검사

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 기본 로컬 연산은 외부 호출·자격증명 불필요. 설치/문서 조회만 네트워크를 사용할 수 있고, 별도 I/O 코드 추가 시 다시 확인.
자격증명: 로컬 기본 예제는 불필요.
비용: 조합 탐색 시간이 입력에 민감. time limit·worker 수·메모리 예산을 명시하고 incumbent와 bound를 따로 기록한다.

## 확인 범위

라이선스: Apache-2.0. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`PLANNING`, `MOBILITY` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.

[설치 안내](https://developers.google.com/optimization/install/python)를 확인했다. 환경별 세부 설치는 선택한 고정 버전 문서와 wheel 지원 여부를 확인해야 한다.
