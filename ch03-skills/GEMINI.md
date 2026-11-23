# GEMINI.md — 제3장: 온디맨드 노하우 모듈 — 3단계 확장형 스킬(Skills) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch03-skills/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `git-commit/`, `gh-issue/`, `gh-pr/`, `gh-review/`, `gh-address-review/` (각 `SKILL.md`, `reference.md`, `examples/`, `scripts/validate_*.py`), `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 git-commit/scripts/validate_commit.py git-commit/examples/sample_commit.txt && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
