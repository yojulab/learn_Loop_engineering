# CLAUDE.md — 제10장: 프로덕션의 눈과 저울 — 평가(Eval)와 LLMOps (Claude Code 1층위 지침)

- 본 챕터 폴더(`ch10-eval-and-llmops/`)에서 `claude` CLI 접속 시 자동 적용되는 상시 지침입니다.
- 핵심 파일: `litellm_proxy/`(무코드 관측 & CLI 브리지), `langfuse_ops.py`, `trace_to_prompt.py`(Save as Prompt), `fetch_prompt.py`, `evaluator.py`(3종 Eval), `regression_compare.py`, `seed_langfuse_dashboard.py`, `tests/`
- 세부 경로 조건부 규칙은 `.claude/rules/eval-llmops.md`를 따르며, 공통 구조는 `AGENTS.md`를 참조합니다.
- 작업 완료 후 반드시 현재 폴더에서 `python3 trace_to_prompt.py --demo --json && python3 fetch_prompt.py --demo --json && python3 regression_compare.py && python3 -m unittest discover -s tests -p "test_*.py"` 명령으로 검증 결과를 출력하세요.
