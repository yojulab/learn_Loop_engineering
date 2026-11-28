# GEMINI.md — 제9장: 아우터 루프 엔지니어링 (5단계 루프 & 7대 완료·중단 조건) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch09-outer-loop/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `loop.py`(5단계 아우터 루프), `models.py`, `workers.py`, `cost_logger.py`(JSONL 비용 로거), `sample_tasks/tasks_contract.json`(`CALC-001`~`004`), `sample_tasks/calc_verifier.py`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 loop.py --platform claude && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
