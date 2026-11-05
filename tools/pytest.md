# pytest

- id: `pytest`
- 적합: 계산·상태·오류·매개변수 기반 회귀 검사
- 부적합: 자기 구현으로 만든 기대값만 대조하고 독립 검증 주장
- 확인: 2026-11-05 / `docs_verified` / Python + pytest; 실행 미검증
- [공식 저장소·홈](https://github.com/pytest-dev/pytest) · [공식 문서와 예제](https://docs.pytest.org/en/stable/getting-started.html) · [라이선스 원문](https://raw.githubusercontent.com/pytest-dev/pytest/main/LICENSE)

## 먼저 확인할 것

공식 첫 예제는 의도적으로 실패한다. 실행 성공과 요구 충족은 별도다. 플러그인 자동 로딩·네트워크 fixture를 점검한다.

## 입출력·설치

- 입력: 수동 기대값·fixtures·검사 함수
- 최소 출력: pass/fail/skip와 실패 입력
- 설치 조건: 허용된 고정 버전 pytest. 기존 버전 확인 후 선택
- 설치 불가 대안: unittest 또는 assert를 쓰는 독립 스크립트

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 테스트 엔진의 기본 로컬 검사에는 외부 서비스 불필요. 사용자 테스트·fixture·플러그인은 네트워크를 호출할 수 있어 별도 점검. 패키지 설치는 네트워크 사용 가능.
자격증명: 로컬 기본 예제는 불필요.
비용: fixture 설정 비용×테스트 수를 측정. 외부 DB·파일 fixture를 분리하고 단위 테스트 실패부터 재현한다.

## 확인 범위

라이선스: MIT. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

패키지 설치와 공식 예제 실행은 이번 기록에서 **미실행**. 기능 설명 확인을 실행 성공으로 취급하지 않는다.

## 관련 문제 구조

`EVENT`, `TRANSACTION` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.
