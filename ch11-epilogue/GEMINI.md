# GEMINI.md — 제11장 에필로그: 4계층 아키텍처 치트시트 & Stage 1~4 도입 진단 (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch11-epilogue/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `stage_readiness_check.py`(--format json|text), `README.md`(4계층 치트시트), `tests/test_stage_readiness.py`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 stage_readiness_check.py --format json && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
