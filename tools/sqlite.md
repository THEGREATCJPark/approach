# SQLite / FTS5

- id: `sqlite`
- 적합: SQL 집계, 로컬 근거 문서 검색, UNIQUE 키·트랜잭션
- 부적합: 의미 이해를 보장하는 검색, 토크나이저 확인 없는 한국어 품질 보장
- 확인: 2026-11-05 / `smoke_tested` / SQLite FTS5 확장; 실행 확인 SQLite 3.53.1 via Python
- [공식 저장소·홈](https://www.sqlite.org/index.html) · [공식 문서와 예제](https://www.sqlite.org/fts5.html) · [라이선스 원문](https://www.sqlite.org/copyright.html)

## 먼저 확인할 것

FTS5 검색 결과의 명령을 실행하지 않는다. 한국어 띄어쓰기·형태 변화는 별도 테스트한다. 중복 실행 방지는 DB 제약과 원자적 처리로 검증한다.

## 입출력·설치

- 입력: 문서 ID·본문·버전·출처, 매개변수화한 질의
- 최소 출력: 문서 ID와 일치 구간; 없으면 no_evidence
- 설치 조건: Python sqlite3 제공 여부와 FTS5 빌드를 확인. 없으면 설치부터 하지 않는다
- 설치 불가 대안: 표준 라이브러리 키워드 검색과 수동 근거 확인

## 실행 조건

unknown; 현재 과제 규정 확인 전 설치/외부 통신/자동 조작 비활성. 버전 변경을 기본 동작으로 삼지 않는다.
외부 호출: 기본 로컬 연산은 외부 호출·자격증명 불필요. 설치/문서 조회만 네트워크를 사용할 수 있고, 별도 I/O 코드 추가 시 다시 확인.
자격증명: 로컬 기본 예제는 불필요.
비용: DB 파일 크기·FTS 인덱스 저장 공간·갱신 비용 측정. 검색 결과 건수 제한과 query plan을 확인; 전체 문서 scan을 숨기지 않는다.

## 확인 범위

라이선스: Public domain dedication; SQLite 원문 확인. 종속 패키지·복사하는 코드의 개별 조건은 별도 확인한다.
문서와 예제 경로를 실제 열어 해당 API·설명 존재를 확인했다. mutable URL을 확인한 기록이며 릴리스 전체나 설치 성공을 인증하지 않는다.

로컬 smoke: SQLite 3.53.1 메모리 FTS5 테이블에 `repair gasket`, `inspect cable` 삽입 후 `gasket` MATCH 결과 기대·실제 rowid `[1]`. 한국어 검색·동시성 검증은 미실행.

## 관련 문제 구조

`SUPPORT`, `POLICY` 영역에서 조건을 확인한 후 선택한다. [라우터](../ROUTER.md)로 돌아가 데이터와 반증 질문을 먼저 비교한다.
