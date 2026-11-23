# GEMINI.md — 제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch05-rag-and-memory/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `agentic_rag.py`(Query Rewrite + Hybrid RRF), `memory_manager.py`(--status --json), `TASKS.md`, `JOURNAL.md`, `corpus/*.md`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 agentic_rag.py && python3 memory_manager.py --status --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
