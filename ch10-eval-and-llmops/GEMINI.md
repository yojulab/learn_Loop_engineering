# GEMINI.md — 제10장: 프로덕션의 눈과 저울 — 평가(Eval)와 LLMOps (Gemini / Antigravity `agy` 지침)

- 본 챕터 폴더(`ch10-eval-and-llmops/`)에서 `agy` 또는 Gemini CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `litellm_proxy/`(무코드 관측 & CLI 브리지), `langfuse_ops.py`, `trace_to_prompt.py`(Save as Prompt), `fetch_prompt.py`, `evaluator.py`(3종 Eval), `regression_compare.py`, `seed_langfuse_dashboard.py`, `tests/`
- 플랫폼 세부 설정은 `.gemini/settings.json` 및 `.gemini/rules.md`를 참조하며, 공통 규칙은 `AGENTS.md`와 동기화됩니다.
- 사용자 프롬프트 실행 시 `python3 trace_to_prompt.py --demo --json && python3 fetch_prompt.py --demo --json && python3 regression_compare.py && python3 -m unittest discover -s tests -p "test_*.py"` 검증 결과를 함께 보고하세요.
