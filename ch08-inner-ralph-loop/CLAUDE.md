# CLAUDE.md — 제8장: 이너 루프와 랄프 루프 (SQLite FTS5 RSS Wiki & /goal) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch08-inner-ralph-loop/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `PROMPT.md`, `db.py`(SQLite FTS5), `collector.py`, `app.py`, `goal_evaluator.py`(5대 조건 독립 판정), `ralph_loop.sh`, `worker_*.sh`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/ralph-loop.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 goal_evaluator.py && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
