# Agentic RAG & Excerpt Filtering

전통적인 덤프 방식 RAG와 달리 Agentic RAG는 검색 사서가 필요한 문서만 고른다.
Top-K 상한(예: 3개)과 발췌 길이 상한(max_chars_per_excerpt)을 강제해야 도구 출력 오염을 막을 수 있다.
불필요한 서론을 제외하고 쿼리 토큰과 일치하는 핵심 문장만 반환한다.
