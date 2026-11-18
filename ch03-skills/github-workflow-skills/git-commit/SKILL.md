---
name: git-commit
description: Conventional Commits 규격 커밋 메시지 작성 및 검증 스킬
---

# git-commit

## 절차
1. 변경 성격을 `feat|fix|docs|refactor|test|chore` 중 하나로 분류한다.
2. 선택적 scope를 괄호에 넣고 50자 내외 명령조 제목을 작성한다.
3. 커밋 전 `scripts/validate_commit.py`로 제목 포맷을 검증한다.

## 추가 참조
- 상세 규칙: [reference.md](reference.md)
- 모범 예시: [examples/sample_commit.txt](examples/sample_commit.txt)
- 검증 스크립트: `scripts/validate_commit.py`
