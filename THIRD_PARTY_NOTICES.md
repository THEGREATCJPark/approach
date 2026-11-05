# 외부 자료와 라이선스

이 저장소는 외부 코드를 vendoring하지 않고 공식 문서와 라이선스로 연결한다. 카드의 연습 절차와 합성 자료는 독립 작성했다. 링크 대상의 라이선스를 이 저장소 전체에 적용하지 않는다. 새로 복사할 때는 해당 파일·버전·의존성의 조건을 다시 확인한다. 저장소 자체의 사용 허락은 별도 LICENSE 유무를 따른다.

| 도구 | 확인한 라이선스 | 원문 |
|---|---|---|
| python-stdlib | PSF-2.0; 포함 구성요소별 조건 별도 | [원문](https://docs.python.org/3/license.html) |
| sqlite | Public domain dedication; SQLite 원문 확인 | [원문](https://www.sqlite.org/copyright.html) |
| or-tools | Apache-2.0 | [원문](https://raw.githubusercontent.com/google/or-tools/stable/LICENSE) |
| scipy | BSD-3-Clause; 번들 의존성 별도 | [원문](https://raw.githubusercontent.com/scipy/scipy/main/LICENSE.txt) |
| cvxpy | Apache-2.0; solver별 라이선스 별도 | [원문](https://raw.githubusercontent.com/cvxpy/cvxpy/master/LICENSE) |
| shapely | BSD-3-Clause; GEOS 등 별도 | [원문](https://raw.githubusercontent.com/shapely/shapely/main/LICENSE.txt) |
| networkx | BSD-3-Clause | [원문](https://raw.githubusercontent.com/networkx/networkx/main/LICENSE.txt) |
| pytest | MIT | [원문](https://raw.githubusercontent.com/pytest-dev/pytest/main/LICENSE) |
| hypothesis | MPL-2.0; 명시된 예외는 별도 | [원문](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/LICENSE.txt) |
| playwright | Apache-2.0; 브라우저 배포물 조건 별도 | [원문](https://raw.githubusercontent.com/microsoft/playwright/main/LICENSE) |

방법론은 각 카드의 공개 1차 출처를 참고한다. 웹사이트 공개 접근은 내용 전체 재배포 허락을 뜻하지 않는다. 직접 인용·도표·외부 테스트 코드를 가져오지 않았다. Domain Storytelling 사이트의 CC-BY-4.0 등 개별 조건과 저자 귀속은 원문에서 확인한다.

확인일: 2026-11-05. 원문 접근 기록과 오류는 [source-checks](validation/source-checks.json)에 남겼다. 일부 실패한 이전 경로는 감사 기록에만 남기며 추천 경로에는 사용하지 않는다.

선택적 워크플로 참고의 LICENSE 원문도 확인했다: Symposium MIT, Ouroboros MIT, AI-DLC Workflows MIT-0, gstack MIT. [비교 문서](tools/workflow-references.md)의 원문 링크와 source-checks의 blob SHA를 참고한다. 실행 또는 코드 복사 기록은 없다.
