# CLAUDE.md — 제3장: 온디맨드 노하우 모듈 — 3단계 확장형 스킬(Skills) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch03-skills/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `git-commit/`, `gh-issue/`, `gh-pr/`, `gh-review/`, `gh-address-review/` (각 `SKILL.md`, `reference.md`, `examples/`, `scripts/validate_*.py`), `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/skills.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 git-commit/scripts/validate_commit.py git-commit/examples/sample_commit.txt && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
