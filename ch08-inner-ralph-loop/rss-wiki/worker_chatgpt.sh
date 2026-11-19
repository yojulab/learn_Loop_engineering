#!/usr/bin/env bash
# worker_chatgpt.sh — OpenAI Codex CLI / ChatGPT 워커 (미설치 시 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
if command -v codex >/dev/null 2>&1; then
  codex exec "$(cat "${PROMPT_FILE}")"
else
  python3 -c "import sys; print('[worker_chatgpt] offline fallback OK')"
fi
