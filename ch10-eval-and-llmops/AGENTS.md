# AGENTS.md — 제10장: 프로덕션의 눈과 저울 — 평가(Eval)와 LLMOps

> 본 디렉터리(`ch10-eval-and-llmops/`)에서 AI CLI(`codex`, `claude`, `agy`)로 실습할 때 자동 로드되는 100줄 이하 목차형 에이전트 지침입니다.

## 1. 핵심 파일 구조
- 주요 자산: `litellm_proxy/`(무코드 관측 & CLI 브리지), `langfuse_ops.py`, `trace_to_prompt.py`(Save as Prompt), `fetch_prompt.py`, `evaluator.py`(3종 Eval), `regression_compare.py`, `seed_langfuse_dashboard.py`, `tests/`
- 플랫폼별 지침: `CLAUDE.md` (`.claude/`), `GEMINI.md` (`.gemini/`), `AGENTS.md`

## 2. 실습 및 운영 원칙
- 기존 앱 코드 수정 없이 `OPENAI_BASE_URL` LiteLLM 프록시 전환만으로 Langfuse Trace/Generation을 수집한다.
- Trace에서 추출한 프롬프트(`Save as Prompt`)는 `fetch_prompt.py`로 로드하고 3종 Eval(`accuracy`, `helpfulness`, `safety`) 회귀 비교를 통과해야 승격한다.
- 파괴적 셸 명령(`rm -rf`, `git push --force`, `git reset --hard`) 실행을 금지한다.

## 3. 표준 검증 명령 (현재 챕터 루트 기준)
```bash
python3 trace_to_prompt.py --demo --json && python3 fetch_prompt.py --demo --json && python3 regression_compare.py && python3 -m unittest discover -s tests -p "test_*.py"
```
