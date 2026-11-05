# CVXPY

- id: `cvxpy`
- 적합: DCP로 표현 가능한 연속 최적화와 지원 solver가 있는 문제
- 부적합: 임의 비볼록 수식, solver 확인 없는 정수 최적화
- 확인: 2026-11-05 / `docs_verified` / Python + CVXPY + 선택 solver; 실행 미검증
- [공식 저장소·홈](https://github.com/cvxpy/cvxpy) · [공식 문서와 예제](https://www.cvxpy.org/tutorial/dcp/index.html) · [라이선스 원문](https://raw.githubusercontent.com/cvxpy/cvxpy/master/LICENSE)

## 먼저 확인할 것

DCP는 Minimize(convex), Maximize(concave), 허용 형태 제약을 확인한다. 부정확 상태·수치 허용오차를 숨기지 않는다.

## 입출력·설치

- 입력: 변수·차원·convex/concave 조건·solver 능력
- 최소 출력: is_dcp 결과·solver 상태·해·잔차
- 설치 조건: 허용된 고정 버전 cvxpy와 목적에 맞는 solver 확인
- 설치 불가 대안: 선형화가 타당하면 작은 LP 또는 열거; 아니면 보류

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 기본 로컬 연산은 외부 호출·자격증명 불필요. 설치/문서 조회만 네트워크를 사용할 수 있고, 별도 I/O 코드 추가 시 다시 확인.
자격증명: 로컬 기본 예제는 불필요.
비용: 변수·제약 수뿐 아니라 canonicalization과 solver 메모리도 필요. solver별 시간 제한과 잔차를 기록한다.

## 확인 범위

라이선스: Apache-2.0; solver별 라이선스 별도. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`PLANNING` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.
