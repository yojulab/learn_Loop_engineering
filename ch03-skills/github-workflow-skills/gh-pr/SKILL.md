---
name: gh-pr
description: 이슈 연결(Closes #N), 변경 요약, 테스트 체크리스트 포함 PR 작성 및 검증 스킬
---

# gh-pr

## 절차
1. `## 요약` 섹션에 핵심 변경점을 3줄 이내로 정리한다.
2. 관련 이슈 번호(`Closes #N`)를 본문에 명시한다.
3. 테스트 실행 체크리스트를 작성하고 `scripts/validate_pr.py`로 검증한다.

## 추가 참조
- 상세 규칙: [reference.md](reference.md)
- 모범 예시: [examples/sample_pr.md](examples/sample_pr.md)
- 검증 스크립트: `scripts/validate_pr.py`
