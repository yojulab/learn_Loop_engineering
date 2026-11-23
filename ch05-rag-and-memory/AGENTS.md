# AGENTS.md — 제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory)

> 본 디렉터리(`ch05-rag-and-memory/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `agentic_rag.py`(Query Rewrite + Hybrid RRF), `memory_manager.py`(--status --json), `TASKS.md`, `JOURNAL.md`, `corpus/*.md`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 외부 지식 조회 시 전체 문서를 덤프하지 않고 `AgenticRetriever`로 Top-K 핵심 발췌만 컨텍스트에 주입한다.
- 세션 간 작업 상태는 `TASKS.md`에, 의사결정과 검증 증거 요약은 `JOURNAL.md`에 기록한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 agentic_rag.py && python3 memory_manager.py --status --json && python3 -m unittest discover -s tests -p "test_*.py"
```
