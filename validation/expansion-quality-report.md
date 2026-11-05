# 120개 확장 검증 결과

2026-11-05. 사례120개(심화30·표준90)를 작성했다. 숫자만 채우는 미완성 카드는 포함하지 않았다.
기존30개 파일은 SHA-256으로 비교해 원래 내용과 동일함을 확인했다. 공개 상태·이력은 유지하며 강제 갱신하지 않는다.

## 실제 실행

| 검사 묶음 | 사례 | 통과/실행 |
|---|---:|---:|
| [check_a](../examples/synthetic/check_a.py) | 10 | 65/65 |
| [check_b](../examples/synthetic/check_b.py) | 10 | 60/60 |
| [check_c](../examples/synthetic/check_c.py) | 10 | 60/60 |
| [check_expansion_a](../examples/synthetic/check_expansion_a.py) | 18 | 66/66 |
| [check_expansion_b](../examples/synthetic/check_expansion_b.py) | 18 | 64/64 |
| [check_expansion_c](../examples/synthetic/check_expansion_c.py) | 18 | 61/61 |
| [check_expansion_d](../examples/synthetic/check_expansion_d.py) | 18 | 55/55 |
| [check_expansion_e](../examples/synthetic/check_expansion_e.py) | 18 | 56/56 |

합계 **487/487 통과**. [전체 실행 기록](all-examples-results.json), `check_*-results.json`에 입력·기대·실제·상태를 기록했다.
표준 사례의 입력은 단독 입력 또는 카드의 공통 fixture에 대한 변경값이다. B 묶음의 빈 입력 {}는 공통 fixture를 그대로 사용하는 시험이다.
기대값은 손계산·독립 소형 규칙 계산과 대조했다. 생산 앱이나 외부 서비스를 시험한 것이 아니며 실제 DB 동시성·UI·사용자 효과를 보장하지 않는다.

## 무결성·중복·내용 검토

- [최종 무결성 결과](integrity-results.json): JSON 스키마, 필수 필드, ID·경로 중복, 카드와 카탈로그 일치,120개 카드와15영역×8개, 고아 파일, 내부 링크.
- 표준90개에 최소3개 입력/기대/근거와 fixture를 요구한다. 기존 심화 일부는 기대 근거가 카드의 손계산 절에 있어 경고로 기록하며 실행 실패와 구별한다.
- [구조 중복 점검](distinctness-results.json)은 동일 서명·동일 테스트·유사 표현을 검토 후보로 찾는다. 독립 창작이나 의미상 차이를 자동 증명하는 도구는 아니다.
- [별도 사례 검토](expansion-content-review.md), [A 검토](expansion-a-review.md), [C 검토](expansion-c-review.md)에서 실제 발견·수정·미검증 범위를 구분한다.
- 공개본에 원래 과제·인물·비공개 원문·지시서·실제 결과물을 넣지 않았다. [공개 파일 목록과 패턴 검사](publication-results.json)에 게시 파일을 명시하고 수동으로 변경 내용을 검토했다.

## 라우터

어휘 기반 검색을120개 카탈로그의 제목·키워드·구조 단서로 확장했다. 원래의 규정 확인과 NO_AI_REVIEW 중단은 유지한다.
[새18요청 수정 전](routing-expansion-before.json) / [수정 후](routing-expansion-after.json),
[표준15요청 수정 전](routing-standard-before.json) / [수정 후](routing-standard-after.json)에 영역과 카드 선택 결과를 구분했다.
[기존21회귀](routing-original21-after-expansion.json), [AI 금지 모드](routing-no-ai-after-expansion.json)를 별도로 재검사했다.
영역을 맞혀도 적합한 카드가 첫 후보에 없을 수 있다. 새 사례에 대한 업무 적합성과 카탈로그 회귀 결과를 혼동하지 않으며 정확도·속도·출제 확률을 주장하지 않는다.
필요하면 [영역 표](../ROUTER.md)와 [전체 색인](../catalog/INDEX.md)에서 직접 골라 질문으로 반증한다.

## 출처와 남은 한계

공식 문서·라이선스 확인은 [기존 기록](source-checks.json)을 유지한다. 이번에 새로 사용한 Python library/unittest·NIST CUSUM 문서는 [추가 기록](expansion-source-checks.json)에 실제 열람을 남겼다.
기존 로컬 DNS 제한으로 일괄 HTTP 검사를 성공했다고 하지 않는다. 링크 존재와 본문 확인, 설치·실행, 실사용 검증은 별개다.
외부 도구8개·외부 워크플로4개의 설치/전체 실행, 실제 업무 데이터, 실제 사용자 평가, UI·동시성·성능·교육 효과·통계 검출력은 미검증이다.
합성 정책값은 실제 조직 승인 기준이 아니다. CUSUM의 기준·임계값도 연습용이며 오탐률을 보정한 기준이 아니다.
TASK의 실제 작업 결과는 공개 참고 저장소 밖에 보관하고 외부 전송하지 않는다. AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.

## 재현

```sh
python scripts/validate_repo.py --expected-cases 120 --expected-per-family 8 --expected-family-count 15
python scripts/run_examples.py
python scripts/test_routing.py
python scripts/check_catalog_distinctness.py
python scripts/scan_publication.py
```
