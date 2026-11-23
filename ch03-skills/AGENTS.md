# AGENTS.md — 제3장: 온디맨드 노하우 모듈 — 3단계 확장형 스킬(Skills)

> 본 디렉터리(`ch03-skills/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `git-commit/`, `gh-issue/`, `gh-pr/`, `gh-review/`, `gh-address-review/` (각 `SKILL.md`, `reference.md`, `examples/`, `scripts/validate_*.py`), `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 모든 스킬은 1단계(YAML frontmatter: name, description) -> 2단계(`SKILL.md` 본문 절차) -> 3단계(`reference.md`, `examples/`, `scripts/validate_*.py`)의 점진적 공개(Progressive Disclosure) 구조를 준수한다.
- 산출물 생성 후 반드시 해당 스킬의 `scripts/validate_*.py`로 형식 무결성을 검증한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 git-commit/scripts/validate_commit.py git-commit/examples/sample_commit.txt && python3 -m unittest discover -s tests -p "test_*.py"
```
