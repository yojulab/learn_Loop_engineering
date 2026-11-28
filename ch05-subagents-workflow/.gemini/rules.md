# .gemini/rules.md — 제5장: 서브에이전트와 동적 병렬 워크플로

- 감사·리뷰 역할(`api-reviewer`, `security-scanner`, `code-quality`)은 읽기 전용 도구(`Read`, `Grep`, `Glob`)만 허용한다.
- 각 서브에이전트는 격리된 컨텍스트에서 병렬 실행된 뒤 단일 요약 리포트로 병합되어야 한다.
