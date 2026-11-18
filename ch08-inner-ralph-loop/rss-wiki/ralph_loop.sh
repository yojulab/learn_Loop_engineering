#!/usr/bin/env bash
set -euo pipefail

TASKS_FILE="${TASKS_FILE:-TASKS.md}"
JOURNAL_FILE="${JOURNAL_FILE:-JOURNAL.md}"
MAX_ITERATIONS="${MAX_ITERATIONS:-10}"
CONSECUTIVE_FAIL_LIMIT="${CONSECUTIVE_FAIL_LIMIT:-3}"
WORKER_CMD="${WORKER_CMD:-true}"

iter=0
fail_streak=0

while [ "${iter}" -lt "${MAX_ITERATIONS}" ]; do
  if ! grep -q "^- \[ \]" "${TASKS_FILE}" 2>/dev/null; then
    echo "ALL_DONE" >> "${JOURNAL_FILE}"
    echo "[ralph_loop] ALL_DONE (iterations=${iter})"
    exit 0
  fi

  iter=$((iter + 1))
  if eval "${WORKER_CMD}"; then
    fail_streak=0
    echo "- [iter ${iter}] WORKER_OK" >> "${JOURNAL_FILE}"
  else
    fail_streak=$((fail_streak + 1))
    echo "- [iter ${iter}] WORKER_FAIL (streak=${fail_streak}/${CONSECUTIVE_FAIL_LIMIT})" >> "${JOURNAL_FILE}"
    if [ "${fail_streak}" -ge "${CONSECUTIVE_FAIL_LIMIT}" ]; then
      python3 - "${TASKS_FILE}" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").splitlines()
replaced = False
out = []
for line in lines:
    if not replaced and line.startswith("- [ ]"):
        out.append(line.replace("- [ ]", "- [BLOCKED]", 1))
        replaced = True
    else:
        out.append(line)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
      echo "- [iter ${iter}] CIRCUIT_BREAKER_TRIGGERED: marked BLOCKED" >> "${JOURNAL_FILE}"
      echo "[ralph_loop] BLOCKED after ${fail_streak} consecutive failures"
      exit 2
    fi
  fi
done

echo "[ralph_loop] MAX_ITERATIONS=${MAX_ITERATIONS} reached"
exit 1
