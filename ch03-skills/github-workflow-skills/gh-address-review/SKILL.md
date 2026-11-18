---
name: gh-address-review
description: 리뷰 코멘트 ID별 수정 내역과 회신 코멘트를 추적하는 리뷰 대응 스킬
---

# gh-address-review

## 절차
1. 대상 리뷰 코멘트 ID(`#comment-N` 또는 `R-N`)를 매핑한다.
2. 실제 코드 수정 내역과 테스트 결과를 기록한다.
3. `scripts/validate_address_review.py`로 3요소(코멘트 ID, 수정 내역, 회신) 완결성을 검사한다.

## 추가 참조
- 상세 규칙: [reference.md](reference.md)
- 모범 예시: [examples/sample_address_review.md](examples/sample_address_review.md)
- 검증 스크립트: `scripts/validate_address_review.py`
