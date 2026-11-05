# Hypothesis

- id: `hypothesis`
- 적합: 입력 공간·불변식·변형 관계의 반례 탐색
- 부적합: 증명되지 않은 속성, 확률적 테스트 통과를 전체 증명으로 주장
- 확인: 2026-11-05 / `docs_verified` / Python + Hypothesis; 문서 6.170.14, 실행 미검증
- [공식 저장소·홈](https://github.com/HypothesisWorks/hypothesis) · [공식 문서와 예제](https://hypothesis.readthedocs.io/en/latest/quickstart.html) · [라이선스 원문](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/LICENSE.txt)

## 먼저 확인할 것

행 순서 불변은 순서 비의존 집계에서만 주장한다. 상태 저장·데이터 생성 비용과 시간 제한을 설정한다.

## 입출력·설치

- 입력: 입력 전략·유효 범위·도메인상 성립하는 속성
- 최소 출력: 축소된 실패 예·재현 정보
- 설치 조건: 허용된 고정 버전 hypothesis; 예제 DB 저장 위치 확인
- 설치 불가 대안: 고정 seed 표준 random + 명시 경계값 열거

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 테스트 엔진의 기본 로컬 검사에는 외부 서비스 불필요. 사용자 테스트·fixture·플러그인은 네트워크를 호출할 수 있어 별도 점검. 패키지 설치는 네트워크 사용 가능.
자격증명: 로컬 기본 예제는 불필요.
비용: 생성 예 수·deadline·shrinking 시간이 실행 비용을 좌우. example database 경로와 제한을 명시한다.

## 확인 범위

라이선스: MPL-2.0; 명시된 예외는 별도. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`ANALYTICS`, `INTERACTIVE` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.
