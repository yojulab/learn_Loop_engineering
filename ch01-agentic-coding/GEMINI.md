# GEMINI.md — 제1장: 바이브 코딩과 에이전틱 코딩의 탄생 (Quote CLI) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch01-agentic-coding/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `quotes.json`(명언 데이터), `quote_cli.py`(--all/--tag/--seed/--json), `interactive_demo.py`(3단계 루프), `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 quote_cli.py --tag engineering --json && python3 quote_cli.py --seed 42 --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
