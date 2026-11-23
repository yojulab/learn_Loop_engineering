# CLAUDE.md — 제1장: 바이브 코딩과 에이전틱 코딩의 탄생 (Quote CLI) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch01-agentic-coding/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `quotes.json`(명언 데이터), `quote_cli.py`(--all/--tag/--seed/--json), `interactive_demo.py`(3단계 루프), `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/agent-loop.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 quote_cli.py --tag engineering --json && python3 quote_cli.py --seed 42 --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
