> **최신 상태: 120개 완료.** [120개 확장 검증 보고](expansion-quality-report.md)와 [현재 커버리지](coverage-report.md)를 우선한다. 아래는 첫30개 작성 당시의 검증 기록이며 이후 실행 횟수·링크 수와 다를 수 있다.

# 검증 결과와 제한

기준일 2026-11-05. 아래 실제 실행 로그와 정적 검토를 구분한다. 성능·출제·실제 업무 효과를 보장하지 않는다.

## 실행한 검증

| 검사 | 결과·범위 | 증거 |
|---|---|---|
| 합성 계산 A | 10사례, 65개 통과 | [결과](synthetic-a-results.json), [실행](../examples/synthetic/check_a.py) |
| 합성 계산 B | 10사례, 60개 통과 | [결과](synthetic-b-results.json), [실행](../examples/synthetic/check_b.py) |
| 합성 계산 C | 10사례, 60개 통과 | [결과](synthetic-c-results.json), [실행](../examples/synthetic/check_c.py) |
| 카탈로그·스키마·내부 링크 | 최종 실제 결과는 로그 참조 | [결과](integrity-results.json) |
| 라우터18요청+3변경 시나리오 | 최초19/21→수정21/21 | [최초](routing-results-before-fix.json), [후속](routing-results-after-negation.json) |
| 추가 요청3건 | 최초 정분류1/3, 수정2/3; 1건 분류 보류 | [기록](routing-followup.json) |
| AI 금지 모드·부정 표현 | 각3개 실행 확인 | [기록](routing-followup.json) |
| 도구 작은 smoke | Python Decimal·SQLite FTS5 2개 통과 | [출처·실행](source-checks.json) |
| 공개 파일 패턴 | 자동 결과와 수동 검토 분리 | [파일 목록·결과](publication-results.json) |

라우터 검사는 작성자 설계 및 수정에 사용한 회귀 집합이다. 독립 미관측 정확도나 전체 성공확률이 아니다.
새 요청3건도 검토자가 문서를 본 뒤 작성했으며 외부 블라인드 벤치마크가 아니다.
명시적 부정 절만 처리하므로 복잡한 부정·일상어 표현은 오분류할 수 있다. 항상 [수동 라우터](../ROUTER.md)와 담당자 답을 우선한다.

## 출처와 링크

도구·방법론·선택적 워크플로는 공식 문서와 라이선스 원문을 확인했다. [source-checks](source-checks.json)에 실패 경로·대체 경로·검증 수준을 보존했다.
[추가 기술 문서](additional-source-checks.json)와 [진입 문서 출처](entry-source-checks.json)도 별도로 열어 확인했다.
로컬 일괄 링크 검사는 DNS 해석 제한으로 완료하지 못했다. [수정 전](link-results-first-attempt.json), [수정 후](link-results.json)를 구분한다.
이는 링크가 없다는 뜻이 아니다. 별도 웹/연결 도구로 활성 링크64개 중63개의 기반 URL 접근 근거를 확보했다. fragment 앵커는 별도 전수 확인하지 않았다.
JSON Schema 메타스키마 URL은 웹 도구의 content-type 제한 및 직접 요청403으로 본문 미확인이다. 로컬 스키마 파일 검증은 원격 조회 없이 실행한다.
Walking Skeleton 상세 원전은 접근 실패했고 저자 소개의 짧은 정의만 확인했다. 해당 카드는 partial_reference_verified다.
URL·stable 문서는 변경될 수 있고 전부 commit SHA로 고정하지 않았다. 도구8개와 외부 워크플로4개는 실행하지 않았다.

## 내용·사용성·공개 적합성

[별도 검토](independent-review.md)는 실제 별도 에이전트가 15영역20카드와 진입 경로를 읽고 대표 기대값15건을 다른 계산으로 대조한 기록이다.
통합 담당자는 나머지10카드의 메타데이터·데이터 계약·fixture·기대값을 대조했다. 작성자와의 수정 검토에서 필드 별칭·축약 입력의 한계·잘못 붙은 테스트 이름·같아도 되는 기대값 쌍을 수정했다.
전체 게시 파일 목록과 diff를 확인하고 일반 비밀정보·연락처 패턴을 검사했다. 원문 공지·대화·실제 과제 자료·작업 지시서는 게시 대상에 넣지 않았다.
사례 작성자는 비공개 과제 원문을 사례 작성 재료로 읽지 않았고, 일반 방법과 독립 합성 수치로 작성했다. 자동 검사가 독립 창작·무누출을 증명하는 것은 아니다.

Markdown만 읽는 초기 경로와 스크립트 경로를 점검했다. 오프라인 대안은 문서·표·손계산 경로를 정적으로 검토했으며 실제 무인터넷 장치를 재현한 시험은 아니다.
실제 사용자 조사, UI 동작, DB 경합, 통계 구간 추정, 설치 환경 행렬, 성능/토큰 측정은 수행하지 않았다.

## 재현

```sh
python scripts/validate_repo.py
python scripts/scan_publication.py
python scripts/test_routing.py
python examples/synthetic/check_a.py
python examples/synthetic/check_b.py
python examples/synthetic/check_c.py
```

외부 링크 검사는 허용된 PREP 환경에서만 `python scripts/check_links.py --online`으로 실행한다.
실제 TASK 데이터는 별도 허용 작업 폴더에 두고 공개 저장소에 push하지 않는다.
NO_AI_REVIEW는 질문 생성·답변 작성·실시간 코칭을 중단한다.
