# CLAUDE.md — 제6장: 모델을 감싸는 안전장치 — 하네스 엔지니어링 (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch06-harness-engineering/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `AGENTS.md`(100줄 이하 목차형), `arch_linter.py`(6계층 의존성 린터), `guardrails.py`(5줄 파괴 명령 차단), `doc_gardening.py`(문서 정원 가꾸기), `samples/`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/harness.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 arch_linter.py --root samples/valid_app --json && python3 guardrails.py --cmd "ls -la" --json && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
