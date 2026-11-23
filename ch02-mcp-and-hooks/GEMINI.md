# GEMINI.md — 제2장: 도구를 쥐여주는 표준 — MCP와 훅(Hooks) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch02-mcp-and-hooks/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `main.py`(FastMCP 서버: Tools/Resources/Prompts), `.mcp.json`, `.claude/settings.json`, `hooks/block_dangerous_bash.py`, `hooks/audit_logger.py`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 main.py && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
