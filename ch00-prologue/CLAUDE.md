# CLAUDE.md — 프롤로그: 4계층 12대 스택 & Any-Platform 환경 진단 (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch00-prologue/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `stack_check.py`(4계층 12대 스택 진단), `agent_check.py`(플랫폼 어댑터 점검), `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/prologue.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 stack_check.py --json && AGENT_PLATFORM=offline python3 agent_check.py --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
