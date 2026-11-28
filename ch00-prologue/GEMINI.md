# GEMINI.md — 프롤로그: 4계층 11대 스택 & Any-Platform 환경 진단 (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch00-prologue/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `stack_check.py`(4계층 11대 스택 진단), `agent_check.py`(플랫폼 어댑터 점검), `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 stack_check.py --json && AGENT_PLATFORM=offline python3 agent_check.py --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
