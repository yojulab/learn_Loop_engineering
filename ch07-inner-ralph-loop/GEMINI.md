# GEMINI.md — 제7장: 이너 루프와 랄프 루프 (SQLite FTS5 RSS Wiki & /goal) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch07-inner-ralph-loop/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `PROMPT.md`, `db.py`(SQLite FTS5), `collector.py`, `app.py`, `goal_evaluator.py`(5대 조건 독립 판정), `ralph_loop.sh`, `worker_*.sh`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 goal_evaluator.py && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
