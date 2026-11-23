# GEMINI.md — 제4장: 컨텍스트 엔지니어링과 윈도우의 한계 (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch04-context-engineering/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `prompt_template.txt`(7항목), `few_shot_reference.txt`(참조 구현), `context_budget.py`(토큰 예산 진단), `.claude/rules/api.md`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 context_budget.py --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
