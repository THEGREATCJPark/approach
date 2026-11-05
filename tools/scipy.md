# SciPy linear_sum_assignment

- id: `scipy`
- 적합: 비용 행렬의 단일 일대일 최소비용 배정
- 부적합: 기간 반복, 다중 자원 용량, 시간창을 행렬 비용만으로 표현
- 확인: 2026-11-05 / `docs_verified` / Python + NumPy + SciPy; 문서 v1.18.0, 실행 미검증
- [공식 저장소·홈](https://github.com/scipy/scipy) · [공식 문서와 예제](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html) · [라이선스 원문](https://raw.githubusercontent.com/scipy/scipy/main/LICENSE.txt)

## 먼저 확인할 것

직사각 행렬은 일부 대상을 남길 수 있다. 비용 0과 배정 금지는 다르다. 금지 쌍 처리와 미배정 정책을 먼저 정한다.

## 입출력·설치

- 입력: 행/열 대상 ID, 단위가 같은 비용 행렬
- 최소 출력: 선택 행/열 쌍과 총비용, 남은 대상
- 설치 조건: 허용된 고정 버전 scipy/NumPy wheel 필요
- 설치 불가 대안: 작은 정방 행렬 permutation 완전탐색

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 기본 로컬 연산은 외부 호출·자격증명 불필요. 설치/문서 조회만 네트워크를 사용할 수 있고, 별도 I/O 코드 추가 시 다시 확인.
자격증명: 로컬 기본 예제는 불필요.
비용: 밀집 비용 행렬은 행×열 메모리가 필요. 큰 희소 문제를 dense로 바꾸기 전 크기를 계산한다.

## 확인 범위

라이선스: BSD-3-Clause; 번들 의존성 별도. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`MOBILITY`, `PLANNING` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.

[설치 안내](https://scipy.org/install/)를 확인했다. 환경별 세부 설치는 선택한 고정 버전 문서와 wheel 지원 여부를 확인해야 한다.
