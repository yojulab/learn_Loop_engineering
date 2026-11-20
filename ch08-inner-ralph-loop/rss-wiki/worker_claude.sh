#!/usr/bin/env bash
# worker_claude.sh — Claude Code 비대화형 워커 (미설치·미인증 시 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
CRED_FILE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.credentials.json"
if command -v claude >/dev/null 2>&1 && { [[ -n "${ANTHROPIC_API_KEY:-}" ]] || [[ -f "${CRED_FILE}" ]]; }; then
  claude -p "$(cat "${PROMPT_FILE}")" --permission-mode acceptEdits < /dev/null
else
  python3 -c "print('[worker_claude] offline fallback OK')"
fi
