# CLAUDE.md — 제8장: 다중 에이전트 오케스트레이션 (3-Agent & 블라인드 합의) (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch08-orchestration/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `run.py`(--mode sim), `src/harness/orchestrator.py`, `src/harness/consensus.py`(첫 줄 블라인드 합의), `src/harness/rubric.py`(0~3점 채점표), `src/harness/permissions.py`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/orchestration.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 run.py --mode sim --platform chatgpt && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
