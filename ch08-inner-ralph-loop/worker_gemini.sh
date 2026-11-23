#!/usr/bin/env bash
# worker_gemini.sh — Antigravity CLI(agy) 워커 (미설치·미인증 시 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
if command -v agy >/dev/null 2>&1 && [[ -n "${GEMINI_API_KEY:-}${GOOGLE_API_KEY:-}" ]]; then
  agy -p "$(cat "${PROMPT_FILE}")" < /dev/null
else
  python3 -c "print('[worker_gemini] offline fallback OK')"
fi
