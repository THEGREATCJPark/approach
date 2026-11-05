# approach

낯선 업무 요청에서 **자료 확인 → 질문 → 최소 구현 → 검증 → 사용자 피드백**으로 이동하는 한국어 참고자료.
모든 업무 사례는 공개 일반 방법에 근거한 독립 창작이다. 실제 문제의 익명화·기출 복원이 아니다.

**주 사용법:** 제작 요구사항 README 전체를 채팅에 붙여넣고 “이 저장소를 확인해서 가이드에 따라 진행 방법을 알려줘”라고 요청한다.
[붙여넣기 시작 문장](START_HERE.md)과 [응답 예시](examples/synthetic/readme-intake.md)를 제공한다. 이미 적힌 조건은 재질문하지 않고 원문 요구를 구현·검증 계획으로 연결한다.

- 사람용 한 페이지: [QUICK_REFERENCE](QUICK_REFERENCE.md)
- AI 첫 경로: [AGENTS](AGENTS.md) → [START_HERE](START_HERE.md) → [ROUTER](ROUTER.md)
- 사용 경계: [RULES_GATE](RULES_GATE.md)
- 실제 작성·검증 현황: [coverage](validation/coverage-report.md), [quality](validation/quality-report.md)
- 도구 출처·확인 수준: [tools catalog](catalog/tools.json), [third-party notices](THIRD_PARTY_NOTICES.md)

독립 창작 사례 **120건을 완성**했다: 15영역 × (심화2건 + 표준6건). [전체 색인](catalog/INDEX.md)에서 찾을 수 있다.
표준 사례도 데이터 계약·분기 질문·정상/경계/정보 부족 기대값·실행 검사·피드백 질문을 포함한다.
완성 앱 모음이 아니라 데이터 계약·판정 예·작은 계산·검증 근거다.
실제 사용자 효과나 출제 적중을 보장하지 않는다.

```sh
python scripts/route.py '제한된 정원에 신청 순서대로 배정하고 중복을 막기'
python scripts/validate_repo.py
python scripts/scan_publication.py
```

일반 Markdown만으로도 탐색할 수 있다. 패키지·모델·외부 서비스는 기본 설치하지 않는다.
실제 과제에서는 최신 규정이 우선하며 작업 결과를 이 공개 참고 저장소에 쓰지 않는다.
AI 금지 후속 평가에는 질문 생성·답변 작성·코칭 기능을 사용하지 않는다.

이 저장소 자체의 재배포 라이선스는 아직 지정하지 않았다. 공개 열람 가능과 재배포 허락은 구별한다.
외부 자료는 원문을 복사하지 않고 요약·링크로 참조하며 원 저작물의 라이선스를 별도로 확인한다.

로컬 일괄 링크 검사는 DNS 제한으로 완료하지 못했습니다. 별도 공식 문서 확인과 미확인 항목은 [검증 기록](validation/quality-report.md)에 구분했습니다.
