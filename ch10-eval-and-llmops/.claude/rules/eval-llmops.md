---
paths: ["*.py", "litellm_proxy/**/*", "tests/**/*.py"]
---
# 제10장: 프로덕션의 눈과 저울 — 평가(Eval)와 LLMOps 조건부 규칙

- 기존 앱 코드 수정 없이 `OPENAI_BASE_URL` LiteLLM 프록시 전환만으로 Langfuse Trace/Generation을 수집한다.
- Trace에서 추출한 프롬프트(`Save as Prompt`)는 `fetch_prompt.py`로 로드하고 3종 Eval(`accuracy`, `helpfulness`, `safety`) 회귀 비교를 통과해야 승격한다.
