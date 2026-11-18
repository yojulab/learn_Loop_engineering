---
name: gh-issue
description: GitHub 이슈 제목·라벨·재현절차·기대결과 표준화 및 검증 스킬
---

# gh-issue

## 절차
1. 문제 유형(`bug`, `feature`, `chore`)에 맞는 라벨을 지정한다.
2. 재현 절차와 기대 결과를 번호 목록으로 명확히 적는다.
3. 제출 전 `scripts/validate_issue.py`로 필수 항목 누락 여부를 점검한다.

## 추가 참조
- 상세 규칙: [reference.md](reference.md)
- 모범 예시: [examples/sample_issue.md](examples/sample_issue.md)
- 검증 스크립트: `scripts/validate_issue.py`
