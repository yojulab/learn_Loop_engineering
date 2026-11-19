# Google Gemini / Antigravity 컨텍스트 엔지니어링 지침 (`guidelines_gemini.md`)
<!-- Antigravity / Gemini CLI: GEMINI.md 계층 + JIT 컨텍스트 로드 + /compact -->
- 상시 규칙: 워크스페이스 `GEMINI.md` + 전역 `~/.gemini/GEMINI.md`
- 오염 초기화: `/compact` 또는 새 대화 시작 후 `context_budget.py --json`으로 토큰 점유 점검
