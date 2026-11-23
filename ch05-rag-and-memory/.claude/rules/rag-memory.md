---
paths: ["agentic_rag.py", "memory_manager.py", "TASKS.md", "JOURNAL.md", "corpus/**/*.md"]
---
# 제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory) 조건부 규칙

- 외부 지식 조회 시 전체 문서를 덤프하지 않고 `AgenticRetriever`로 Top-K 핵심 발췌만 컨텍스트에 주입한다.
- 세션 간 작업 상태는 `TASKS.md`에, 의사결정과 검증 증거 요약은 `JOURNAL.md`에 기록한다.
