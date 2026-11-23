# AGENTS.md — 제2장: 도구를 쥐여주는 표준 — MCP와 훅(Hooks)

> 본 디렉터리(`ch02-mcp-and-hooks/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `main.py`(FastMCP 서버: Tools/Resources/Prompts), `.mcp.json`, `.claude/settings.json`, `hooks/block_dangerous_bash.py`, `hooks/audit_logger.py`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- `PreToolUse` 훅(`hooks/block_dangerous_bash.py`)은 위험 명령(`rm -rf`, `git push --force` 등) 감지 시 즉시 종료 코드 2와 차단 JSON을 반환한다.
- `PostToolUse` 훅(`hooks/audit_logger.py`)은 `add_quote` 실행 이력을 감사 로그에 기록한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 main.py && python3 -m unittest discover -s tests -p "test_*.py"
```
