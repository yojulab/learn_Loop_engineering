# GEMINI.md — 제7장: 모델을 감싸는 안전장치 — 하네스 엔지니어링 (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch07-harness-engineering/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `AGENTS.md`(100줄 이하 목차형), `arch_linter.py`(6계층 의존성 린터), `guardrails.py`(5줄 파괴 명령 차단), `doc_gardening.py`(문서 정원 가꾸기), `samples/`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 arch_linter.py --root samples/valid_app --json && python3 guardrails.py --cmd "ls -la" --json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
