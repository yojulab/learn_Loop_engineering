# CLAUDE.md — 제9장: 아우터 루프 엔지니어링 (5단계 루프 & 7대 완료·중단 조건) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch09-outer-loop/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `loop.py`(5단계 아우터 루프), `models.py`, `workers.py`, `cost_logger.py`(JSONL 비용 로거), `sample_tasks/tasks_contract.json`(`CALC-001`~`004`), `sample_tasks/calc_verifier.py`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/outer-loop.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 loop.py --platform claude && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
