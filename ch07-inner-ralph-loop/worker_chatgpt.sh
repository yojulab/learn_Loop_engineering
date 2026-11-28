#!/usr/bin/env bash
# worker_chatgpt.sh — OpenAI Codex CLI / ChatGPT 워커 (미설치·미인증 시 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
if command -v codex >/dev/null 2>&1 && [[ -n "${OPENAI_API_KEY:-}" ]]; then
  codex exec "$(cat "${PROMPT_FILE}")" < /dev/null
else
  python3 -c "print('[worker_chatgpt] offline fallback OK')"
fi
