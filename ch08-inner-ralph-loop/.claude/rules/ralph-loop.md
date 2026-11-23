---
paths: ["db.py", "collector.py", "app.py", "goal_evaluator.py", "ralph_loop.sh"]
---
# 제8장: 이너 루프와 랄프 루프 (SQLite FTS5 RSS Wiki & /goal) 조건부 규칙

- 이너 루프 반복 시 컨텍스트 부패를 막기 위해 파일 상태(`TASKS.md`, `JOURNAL.md`)만 남기고 세션을 초기화한다.
- 동일 작업 3회 연속 실패 시 `[BLOCKED]` 서킷 브레이커를 작동하고 종료 판정은 독립 `goal_evaluator.py`로만 수행한다.
