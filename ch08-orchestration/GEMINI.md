# GEMINI.md — 제8장: 다중 에이전트 오케스트레이션 (3-Agent & 블라인드 합의) (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch08-orchestration/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `run.py`(--mode sim), `src/harness/orchestrator.py`, `src/harness/consensus.py`(첫 줄 블라인드 합의), `src/harness/rubric.py`(0~3점 채점표), `src/harness/permissions.py`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 run.py --mode sim --platform chatgpt && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
