# 정책 개정 중 접수된 신청의 경과조치

독립 창작 합성 사례. 실제 기관·과제·정책을 재게시한 것이 아니다.

```json
{
  "id": "policy-effective-version",
  "title": "정책 개정 중 접수된 신청의 경과조치",
  "family": "POLICY",
  "problem_structure": "grandfathered pending application transition",
  "keywords_ko": [
    "정책 개정",
    "경과조치",
    "소급",
    "접수일",
    "기존 신청"
  ],
  "keywords_en": [
    "grandfathering",
    "retroactivity",
    "pending application"
  ],
  "deliverable_types": [
    "analysis",
    "prototype"
  ],
  "provenance": "synthetic",
  "applicable_when": "창작: 작은 교육 자료실이 처리 대기 중인 대여 신청에 새 정책을 적용할지, 접수 당시 확정한 규칙을 유지할지 구별하려 한다.",
  "do_not_use_when": "현재 날짜에 유효한 정책 하나를 찾아 과거 접수 건에 일괄 적용하지 않는다. 소급 여부가 미확정이면 자동 재판정을 멈춘다. 이 예제는 창작 운영 정책이며 법률 해석이 아니다.",
  "data_required": [
    "한 객체는 개정일을 사이에 둔 대기 신청 한 건. filed는 접수일, decided는 판정일, cutoff는 새 규칙 시행일이며 동일 기준 정수 일이다. locked_version은 접수 때 기록한 v1, retroactive는 명시된 소급 적용 정책 true/false/null. 운영 request_id는 별도 키. null은 미확인이다. 예제는 decided≥cutoff인 개정 후 처리만 다루고 filed>decided는 invalid이다."
  ],
  "method_ids": [
    "baseline-first",
    "verification"
  ],
  "tool_ids": [
    "python-stdlib"
  ],
  "related_cases": [
    "evidence-approval"
  ],
  "depth": "standard",
  "path": "cases/POLICY/policy-effective-version.md",
  "test_count": 4,
  "decision_signature": {
    "decision": "창작: 작은 교육 자료실이 처리 대기 중인 대여 신청에 새 정책을 적용할지, 접수 당시 확정한 규칙을 유지할지 구별하려 한다.",
    "input_structure": "한 객체는 개정일을 사이에 둔 대기 신청 한 건. filed는 접수일, decided는 판정일, cutoff는 새 규칙 시행일이며 동일 기준 정수 일이다. locked_version은 접수 때 기록한 v1, retroactive는 명시된 소급 적용 정책 true/false/null. 운영 request_id는 별도 키. null은 미확인이다. 예제는 decided≥cutoff인 개정 후 처리만 다루고 filed>decided는 invalid이다.",
    "hard_constraint": "개정일 전에 접수된 건(filed<cutoff)은 locked_version=v1이 확인되고 retroactive=False이면 v1을 유지한다. retroactive=True이면 v2로 재판정한다. 개정일 당일 이후 접수는 v2이다. 오래된 건의 소급 여부가 null이면 unknown이다. 출력에 kept_at_filing / explicit_retroactive / filed_under_new 이유를 함께 남긴다.",
    "validation": "같은 접수일8·판정일12에도 retroactive false→v1,true→v2;시행일 접수는v2"
  }
}
```

## 업무 요청과 다른 원인

작은 교육 자료실이 처리 대기 중인 대여 신청에 새 정책을 적용할지, 접수 당시 규칙을 유지할지 구별하려 한다.

- 처리일의 최신 규칙을 모든 대기 건에 적용하고 있다.
- 접수 당시 확정된 버전 기록이 누락되었다.
- 소급 적용에 관한 경과조치가 아직 확인되지 않았다.

## 담당자에게 먼저 물을 질문

1. 개정 전 접수 건을 보호하는가? → 비소급이면 잠근 v1 유지, 명시적 소급이면 v2로 재판정한다.
2. 접수 완료는 초안 작성인가 최종 제출인가? → 정책이 정한 완료 시점을 filed로 사용한다.
3. 기존 버전 잠금 기록이 없는 건은 어떻게 하는가? → 접수일만으로 v1을 추측하지 않고 unknown으로 보류한다.

## 데이터 계약과 자료 부족 대안

한 객체는 개정일을 사이에 둔 대기 신청 한 건. filed는 접수일, decided는 판정일, cutoff는 새 규칙 시행일이며 동일 기준 정수 일이다. locked_version은 접수 때 기록한 v1, retroactive는 명시된 소급 적용 정책 true/false/null. 운영 request_id는 별도 키. null은 미확인이다. 예제는 decided≥cutoff인 개정 후 처리만 다루고 filed>decided는 invalid이다.

최소 필드만 대표 표본으로 확인한다. 개선용 개정 이력은 정책이 확정된 뒤 연결한다. 소급 허용 여부가 없으면 담당자 결정까지 보류한다.

## 단순 기준 방법과 개선 조건

개정일 전에 접수된 건(filed<cutoff)은 locked_version=v1이 확인되고 retroactive=False이면 v1을 유지한다. retroactive=True이면 v2로 재판정한다. 개정일 당일 이후 접수는 v2이다. 오래된 건의 소급 여부가 null이면 unknown이다. 출력에 kept_at_filing / explicit_retroactive / filed_under_new 이유를 함께 남긴다.

취소·재신청 또는 완료된 건의 재심사가 필요하면 신청 이력과 추가 상태를 받아 별도 분기를 만든다. 현재 유효구간 검색만으로 이 경과조치를 해결할 수 없다.

## 최소 구현과 다음 행동

접수·판정일과 잠근 버전·소급 정책 → 경과조치 결정표 → 적용 버전과 이유 → 담당자가 기존안 유지 또는 재판정 목록을 확인한다.

## 합성 예제와 기대값

| 유형 | 입력 | 기대 결과 | 독립 판정 근거 |
|---|---|---|---|
| normal | `{"filed": 8, "decided": 12, "cutoff": 10, "locked_version": "v1", "retroactive": false}` | `{"version": "v1", "reason": "kept_at_filing"}` | 개정 후12일 처리라도8일 접수와 비소급 정책으로v1 유지 |
| boundary | `{"filed": 10, "decided": 12, "cutoff": 10, "locked_version": null, "retroactive": false}` | `{"version": "v2", "reason": "filed_under_new"}` | 접수일10은 개정일 포함; 구 버전 잠금 불필요 |
| missing | `{"filed": 8, "decided": 12, "cutoff": 10, "locked_version": "v1", "retroactive": null}` | `"unknown"` | 개정 전 접수 건의 소급 정책이 확인되지 않음 |
| retroactive_override | `{"filed": 8, "decided": 12, "cutoff": 10, "locked_version": "v1", "retroactive": true}` | `{"version": "v2", "reason": "explicit_retroactive"}` | normal과 날짜는 같지만 명시적 소급 정책이 결과를 바꿈 |

[fixture](../../examples/synthetic/expansion_d.json)와 [독립 계산](../../examples/synthetic/check_expansion_d.py)의 네 기대값을 대조한다. 정상과 소급 허용의 날짜는 완전히 같고 정책 응답만 다르다. 생산 앱이나 실제 규정 판단을 검증한 것은 아니다.

## 피할 구현과 범위 축소

최신 규칙으로 과거 접수 건을 일괄 덮지 않는다. 처리가 늦었다는 이유만으로 구 정책을 유지한다고 추측하지도 않는다. 경과조치가 미확정이면 버전별 후보와 unknown만 표시한다. 실제 법률·회계 판단은 본 예제의 범위 밖이다.

## 핵심 도구와 설치 불가 대안

1순위는 [Python 표준 라이브러리](../../tools/python-stdlib.md)의 결정표 계산이다. 실행이 불가하면 네 행을 손으로 대조한다. 외부 모델·API·브라우저 자동화는 기본 경로가 아니다.

## 구현물 사용자 피드백

- 같은 판정일인데 적용 버전이 다른 이유를 확인할 수 있는가?
- 소급 여부 미확인 건을 누가 결정해야 하는지 보이는가?

## 개발자 설명 연습 — PREP 전용

실제 AI 금지 후속 평가에서는 질문 생성·답변 작성·실시간 코칭을 중단한다.

- 같은 두 날짜에서도 답이 달라지는 정책 필드와 테스트를 보여줄 수 있는가?
- 이 판정과 날짜별 유효 문서 검색의 차이는 무엇인가?

## 검증 범위와 공개 참고

측정 가능 항목은 네 합성 기대값 일치와 잘못된 버전 선택 수이다. 실제 정책 해석의 정당성이나 현장 효율은 확인하지 않았다.

- [기준 방법](../../methods/baseline-first.md)
- [독립 검증](../../methods/verification.md)
- [공식 Python 표준 라이브러리](https://docs.python.org/3/library/index.html): 일반 계산 구조 참고이며 창작 경과조치의 외부 승인 근거가 아니다.
