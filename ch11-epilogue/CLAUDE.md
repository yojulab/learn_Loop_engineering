# CLAUDE.md — 제11장 에필로그: 4계층 아키텍처 치트시트 & Stage 1~4 도입 진단 (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch11-epilogue/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `stage_readiness_check.py`(--format json|text), `README.md`(4계층 치트시트), `tests/test_stage_readiness.py`
- 세부 경로 조건부 규칙은 `.claude/rules/readiness.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 stage_readiness_check.py --format json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
