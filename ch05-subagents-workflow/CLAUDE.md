# CLAUDE.md — 제5장: 서브에이전트와 동적 병렬 워크플로 (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch05-subagents-workflow/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `.claude/agents/*.md`(5종 전문 서브에이전트), `dynamic_workflow.py`(동적 선택·병렬 실행), `quote_cli.py`(--search/--author 확장), `agents_chatgpt.json`, `agents_gemini.json`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/subagents.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 dynamic_workflow.py --task-type api_change --json && python3 quote_cli.py --search "harness" --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
