# CHATGPT.md — OpenAI ChatGPT / Codex CLI 전용 상시 규칙

> 본 프로젝트는 Claude(`CLAUDE.md`), ChatGPT/Codex(`AGENTS.md`, `CHATGPT.md`), Gemini/Antigravity(`GEMINI.md`) **어느 플랫폼에서도 동일하게 실행**되도록 설계되었습니다.

## 1. 플랫폼 연동 포인터
- 공용 실행 어댑터: `platforms/adapter_chatgpt.py` (`OPENAI_API_KEY` 또는 `codex exec` 자동 감지)
- 무코드 관측 프록시: `OPENAI_BASE_URL=http://localhost:4000/v1` 지정 시 LiteLLM 프록시를 통해 Langfuse 트레이스가 자동 적재됩니다(`ch10-eval-and-llmops/litellm_proxy/`).
- 지속 지침: 루트 `AGENTS.md`(100줄 이하 목차형) 및 `ch04-context-engineering/guidelines_chatgpt.md` 참조.

## 2. 필수 검증 명령
```bash
python3 -m unittest discover -s platforms/tests -p "test_*.py"
python3 scripts/verify_chapters.py --all
```
