# 선택적 워크플로 참고

이 문서는 도구 카드 수에 포함하지 않는 비교 자료다. 2026-11-05 공식 저장소의 README와 LICENSE를 직접 읽었다. 네 도구 모두 **docs_verified, 설치·실행 미검증**이다. 호스트별 동작과 이름은 확인 당시 문서 기준이며 현재 환경에서 제공된다고 단정하지 않는다.

기본 경로는 이 저장소의 Markdown을 읽는 것이다. 외부 워크플로 전체를 설치하거나 여러 프레임워크를 겹쳐 실행할 필요는 없다. 규정이 unknown이면 별도 모델 호출·설치·전역 설정 변경·자동 브라우저·외부 게시 기능은 비활성화한다. 원격 설치 스크립트를 검토 없이 실행하지 않는다.

| 참고 | 문서에서 확인한 범위 | 검토할 상황 | 도입 전 확인·대안 | 라이선스 |
|---|---|---|---|---|
| [Symposium](https://github.com/Q00/Symposium) | 요청의 의미를 질문으로 좁혀 목표·제약·수용 기준을 작성하는 Markdown skill pack | 표현이 모호하여 구현 범위를 정하지 못함 | 프로젝트/전역 skill 설치와 scratch 기록 위치가 있음. 설치 없이 [Example Mapping](../methods/example-mapping.md)으로 결정 질문 3개부터 | [MIT](https://github.com/Q00/Symposium/blob/main/LICENSE) |
| [Ouroboros](https://github.com/Q00/ouroboros) | 인터뷰·명세·실행·평가를 연결하는 runtime/MCP workflow | 여러 반복의 상태·근거를 추적할 준비 시간과 자원이 있음 | 모델 제공자·MCP·세션·설치 권한·기록 경로 확인. 짧은 작업은 [Timeboxing](../methods/timeboxing.md)과 결정 로그 | [MIT](https://github.com/Q00/ouroboros/blob/main/LICENSE) |
| [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) | 요구·구현·검토·운영의 단계와 승인 기록, harness별 연동 | 긴 개발 수명주기의 책임과 기록 연결이 필요함 | provider·hooks·로컬 runtime·외부 모델 비용 확인. 고정 환경 변경 금지 시 [Traceability](../methods/traceability.md) 표만 사용 | [MIT-0](https://github.com/awslabs/aidlc-workflows/blob/main/LICENSE) |
| [gstack](https://github.com/garrytan/gstack) | 역할별 검토·브라우저 QA·배포 관련 skill과 host별 지원 표 | 허용된 개발 환경에서 좁은 리뷰 항목을 참고함 | 자동 업데이트·브라우저·외부 리뷰·게시 기능을 각각 확인. 문서의 속도·생산성 주장을 검증된 효과로 인용하지 않음. [독립 검증](../methods/verification.md)과 수동 UI가 대안 | [MIT](https://github.com/garrytan/gstack/blob/main/LICENSE) |

## Symposium 사고방식을 설치 없이 쓰는 창작 연습

요청: “공유 공구 대여 현황이 헷갈린다.”

1. 먼저 대여 기록의 행 단위와 상태값을 본다. 현재 재고가 틀린 것인지, 반납 예정일을 찾기 어려운 것인지 아직 확정하지 않는다.
2. 담당자에게 “이번 출력으로 무엇을 결정하나요?”, “예약된 공구를 가용 재고에서 빼나요?”, “기록이 없는 것은 미대여인가요, 확인 불가인가요?”를 묻는다.
3. 답이 ‘가용량 판단’이면 총량·대여·예약의 관계와 중복 처리 방지를 최소 경로로 삼는다. 답이 ‘독촉 대상’이면 시간 기준·반납 예외·조회 정렬로 방향을 바꾼다.
4. 목표, 필수조건, 제외 범위, 정상·보류 기대값 한 건을 적고 담당자에게 확인한다. 질문 횟수나 유사도 점수만으로 요구 완성을 선언하지 않는다.

이는 이 저장소가 독립 작성한 연습이며 외부 skill을 실제 실행한 결과가 아니다. 실제 후속 평가에서 AI가 금지되면 이 질문 생성·답변 작성·실시간 코칭을 모두 중단한다.
