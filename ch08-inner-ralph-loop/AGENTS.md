# AGENTS.md — 제8장: 이너 루프와 랄프 루프 (SQLite FTS5 RSS Wiki & /goal)

> 본 디렉터리(`ch08-inner-ralph-loop/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `PROMPT.md`, `db.py`(SQLite FTS5), `collector.py`, `app.py`, `goal_evaluator.py`(5대 조건 독립 판정), `ralph_loop.sh`, `worker_*.sh`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 이너 루프 반복 시 컨텍스트 부패를 막기 위해 파일 상태(`TASKS.md`, `JOURNAL.md`)만 남기고 세션을 초기화한다.
- 동일 작업 3회 연속 실패 시 `[BLOCKED]` 서킷 브레이커를 작동하고 종료 판정은 독립 `goal_evaluator.py`로만 수행한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 goal_evaluator.py && python3 -m unittest discover -s tests -p "test_*.py"
```
