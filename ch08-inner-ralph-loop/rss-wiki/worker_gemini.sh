#!/usr/bin/env bash
# worker_gemini.sh — Google Gemini CLI / Antigravity 워커 (미설치 시 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
if command -v gemini >/dev/null 2>&1; then
  gemini -p "$(cat "${PROMPT_FILE}")"
else
  python3 -c "import sys; print('[worker_gemini] offline fallback OK')"
fi
