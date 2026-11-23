# AGENTS.md — 제10장: 아우터 루프 엔지니어링 (5단계 루프 & 7대 완료·중단 조건)

> 본 디렉터리(`ch10-outer-loop/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `loop.py`(5단계 아우터 루프), `models.py`, `workers.py`, `cost_logger.py`(JSONL 비용 로거), `sample_tasks/tasks_contract.json`(`CALC-001`~`004`), `sample_tasks/calc_verifier.py`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- `Discover -> Plan -> Execute -> Verify -> Iterate` 5단계 루프와 7대 완료·중단 조건(예산, 반복, 연속 실패, 인간 이관 HALT)을 준수한다.
- 워커의 자체 완료 선언과 무관하게 `calc_verifier.py` 독립 검증기가 통과해야만 `DONE`으로 전이한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 loop.py --platform claude && python3 -m unittest discover -s tests -p "test_*.py"
```
