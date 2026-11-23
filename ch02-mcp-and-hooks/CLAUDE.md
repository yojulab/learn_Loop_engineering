# CLAUDE.md — 제2장: 도구를 쥐여주는 표준 — MCP와 훅(Hooks) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch02-mcp-and-hooks/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `main.py`(FastMCP 서버: Tools/Resources/Prompts), `.mcp.json`, `.claude/settings.json`, `hooks/block_dangerous_bash.py`, `hooks/audit_logger.py`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/mcp-hooks.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 main.py && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
