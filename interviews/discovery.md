# 개발 전 결정 질문

[시작](../START_HERE.md) · [규정 확인](../RULES_GATE.md)

적용: PREP 또는 허용된 TASK. NO_AI_REVIEW에서는 질문 생성·답변 작성·실시간 코칭을 중단한다. 실제 기록은 별도 허용 작업 공간에 남긴다.

파일에서 이미 확인한 내용은 다시 묻지 않는다. 아래에서 설계를 바꾸는 질문 최대 3개부터 선택한다. 질문 수를 채우기 위한 면담은 하지 않는다.

## 사용자

- ask_when: 결정 주체가 모호함
- target: 최종 사용자
- question: 결과를 읽고 누가 어떤 동작을 해야 합니까?
- why: 화면보다 업무 완료를 정의
- expected_evidence: 작업 전후 사례
- changes_plan: 조회만 필요하면 실행 기능 제외
- stop_condition: 사용자와 다음 행동 확인

## 최근 사례

- ask_when: 추상 요청뿐임
- target: 처리 담당자
- question: 최근 한 건을 입력부터 전달까지 보여주시겠습니까?
- why: 실제 흐름과 예외 관찰
- expected_evidence: 허용된 대표 샘플
- changes_plan: 병목이 전달이면 계산보다 인계 개선
- stop_condition: 한 건의 입력과 완료 확인

## 업무 흐름

- ask_when: 인계점이 불명확함
- target: 송신·수신 담당자
- question: 어느 시점에 누구에게 무엇을 넘깁니까?
- why: 상태와 책임 구분
- expected_evidence: 상태별 산출물
- changes_plan: 공유 파일이면 서버 구축 보류
- stop_condition: 인계 조건 일치

## 병목

- ask_when: 속도가 느리다는 요청
- target: 운영 담당자
- question: 기다림과 직접 처리 중 어느 시간이 큽니까?
- why: 잘못된 자동화 방지
- expected_evidence: 단계별 시간 표본
- changes_plan: 대기가 크면 승인·대기열 분석
- stop_condition: 가장 큰 지연 근거 확보

## 실패 비용

- ask_when: 오류 우선순위 미정
- target: 책임자
- question: 잘못 허용한 경우와 잘못 막은 경우 각각 어떤 손실이 있습니까?
- why: 오류 비용 비대칭 파악
- expected_evidence: 실패 사례·복구 절차
- changes_plan: 고위험 판정은 수동 검토 추가
- stop_condition: 오류 유형별 행동 합의

## 데이터

- ask_when: 누락 의미 불명확
- target: 데이터 관리자
- question: 빈 칸은 없음입니까, 미수집입니까?
- why: 0과 unknown 구분
- expected_evidence: 필드 정의·누락 사례
- changes_plan: 미수집이면 자동 승인 보류
- stop_condition: 결측 처리 규칙 확인

## 정책

- ask_when: 필수와 선호 혼합
- target: 정책 권한자
- question: 반드시 지킬 조건과 양보 가능한 조건은 각각 무엇입니까?
- why: 가중 점수로 위반 상쇄 방지
- expected_evidence: 정책 버전·경계 예
- changes_plan: 필수면 제약, 선호면 정렬 기준
- stop_condition: 필수·선호 구분 완료

## 예외

- ask_when: 일반 규칙만 있음
- target: 예외 승인자
- question: 겉보기에는 같지만 결과가 다른 두 건을 보여주시겠습니까?
- why: 숨은 분기 발견
- expected_evidence: 서로 다른 판정 두 건
- changes_plan: 새 필드 또는 보류 상태 추가
- stop_condition: 차이를 설명하는 근거 확보

## 시간

- ask_when: 기준 시점 불명확
- target: 운영 담당자
- question: 접수·처리·현지 시각 중 무엇으로 마감을 판정합니까?
- why: 시차·지연 경계 오류 방지
- expected_evidence: 시간대·정확한 경계 규칙
- changes_plan: 시각 정규화와 포함 경계 변경
- stop_condition: 동일 시각의 기대 판정 확인

## 성공 조건

- ask_when: 좋아져야 한다는 표현
- target: 결과 사용자
- question: 입력 한 건을 이렇게 처리하면 완료로 볼 수 있습니까?
- why: 검증 가능한 합의
- expected_evidence: 기대 출력·다음 행동
- changes_plan: 출력 형식·필수 항목 수정
- stop_condition: 대표 결과 수용 또는 수정

## 권한

- ask_when: 자료·실행 범위 불명확
- target: 운영자
- question: 이 자료를 어느 도구와 공간에서 처리할 수 있습니까?
- why: 외부 전송·실행 범위 확인
- expected_evidence: 현재 안내의 허용 근거
- changes_plan: unknown 기능 비활성화
- stop_condition: allowed/forbidden/unknown 기록

## 운영

- ask_when: 반복 사용 요구
- target: 운영 책임자
- question: 오류나 정책 변경 때 누가 수정하고 되돌립니까?
- why: 운영 지속성 확인
- expected_evidence: 복구 담당·변경 절차
- changes_plan: 일회성 분석이면 운영 서버 제외
- stop_condition: 책임·복구 경로 확인

## 범위

- ask_when: 여러 목표 충돌
- target: 요청 책임자
- question: 시간 안에 한 가지만 된다면 어떤 판단을 먼저 가능하게 해야 합니까?
- why: 최소 경로 선택
- expected_evidence: 필수 완료 기준
- changes_plan: 나머지를 선택 개선으로 이동
- stop_condition: 우선순위와 제외 범위 확인

## 데이터 요청의 최소화

| 등급 | 요청 예 | 필요한 범위 | 없을 때 |
|---|---|---|---|
| 최소 필수 | 행의 의미·키·판정 필드·단위 | 스키마와 대표 샘플 우선 | 판정 보류 또는 범위 축소 |
| 있으면 개선 | 과거 처리 시간·오류 유형 | 집계 또는 비식별 표본 | 기준 방법으로 진행 |
| 없어도 가능 | 장식용 사진·사용자 프로필 | 요청하지 않음 | 기능 생략 |

개인정보는 목적에 필요한 최소한만 요청한다. 상충 답변은 적용 기간과 권한자를 표시하고 해결 전까지 둘을 임의 합치지 않는다.
