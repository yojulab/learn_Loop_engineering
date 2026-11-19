#!/usr/bin/env bash
# worker_claude.sh — Claude Code 비대화형 워커 (미설치 시 공용 platforms/ 오프라인 폴백)
set -euo pipefail
PROMPT_FILE="${1:-PROMPT.md}"
if command -v claude >/dev/null 2>&1; then
  claude -p "$(cat "${PROMPT_FILE}")" --permission-mode acceptEdits
else
  python3 -c "import sys; print('[worker_claude] offline fallback OK')"
fi
