# CLAUDE.md — 제4장: 컨텍스트 엔지니어링과 윈도우의 한계 (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch04-context-engineering/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `prompt_template.txt`(7항목), `few_shot_reference.txt`(참조 구현), `context_budget.py`(토큰 예산 진단), `.claude/rules/api.md`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/api.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 context_budget.py --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
