---
paths: ["main.py", "hooks/**/*.py", ".mcp.json", "tests/**/*.py"]
---
# 제2장: 도구를 쥐여주는 표준 — MCP와 훅(Hooks) 조건부 규칙

- `PreToolUse` 훅(`hooks/block_dangerous_bash.py`)은 위험 명령(`rm -rf`, `git push --force` 등) 감지 시 즉시 종료 코드 2와 차단 JSON을 반환한다.
- `PostToolUse` 훅(`hooks/audit_logger.py`)은 `add_quote` 실행 이력을 감사 로그에 기록한다.
