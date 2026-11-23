# AGENTS.md — 제9장: 다중 에이전트 오케스트레이션 (3-Agent & 블라인드 합의)

> 본 디렉터리(`ch09-orchestration/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `run.py`(--mode sim), `src/harness/orchestrator.py`, `src/harness/consensus.py`(첫 줄 블라인드 합의), `src/harness/rubric.py`(0~3점 채점표), `src/harness/permissions.py`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 작성자(Planner/Generator)와 평가자(Evaluator)의 도구 권한을 `permissions.py`로 엄격히 분리한다.
- 의사결정은 첫 줄(`선택: A`) 블라인드 합의로 비교하며 3회 불일치 또는 비가역 결정 시 `docs/HALT`를 생성한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 run.py --mode sim --platform chatgpt && python3 -m unittest discover -s tests -p "test_*.py"
```
