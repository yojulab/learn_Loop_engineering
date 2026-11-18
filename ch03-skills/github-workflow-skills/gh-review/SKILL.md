---
name: gh-review
description: 심각도 태그와 파일/라인 근거를 강제하는 코드 리뷰 스킬
---

# gh-review

## 절차
1. 각 코멘트에 심각도 태그(`[BLOCKER|MAJOR|MINOR|NIT]`)를 부여한다.
2. 반드시 파일 경로와 라인 번호(`file.py:42` 또는 `L42`)를 근거로 제시한다.
3. 리뷰 작성 후 `scripts/validate_review.py`로 포맷을 검증한다.

## 추가 참조
- 상세 규칙: [reference.md](reference.md)
- 모범 예시: [examples/sample_review.md](examples/sample_review.md)
- 검증 스크립트: `scripts/validate_review.py`
