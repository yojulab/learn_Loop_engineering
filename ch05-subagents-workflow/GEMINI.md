# GEMINI.md — 제5장: 서브에이전트와 동적 병렬 워크플로 (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch05-subagents-workflow/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `.claude/agents/*.md`(5종 전문 서브에이전트), `dynamic_workflow.py`(동적 선택·병렬 실행), `quote_cli.py`(--search/--author 확장), `agents_chatgpt.json`, `agents_gemini.json`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 dynamic_workflow.py --task-type api_change --json && python3 quote_cli.py --search "harness" --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
