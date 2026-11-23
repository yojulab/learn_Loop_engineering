# CLAUDE.md — 제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch05-rag-and-memory/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `agentic_rag.py`(Query Rewrite + Hybrid RRF), `memory_manager.py`(--status --json), `TASKS.md`, `JOURNAL.md`, `corpus/*.md`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/rag-memory.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 agentic_rag.py && python3 memory_manager.py --status --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
