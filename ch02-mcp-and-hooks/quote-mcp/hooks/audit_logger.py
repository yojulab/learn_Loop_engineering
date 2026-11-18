"""제2장 PostToolUse 훅: add_quote 등 MCP 도구 호출을 mcp-audit.log JSONL로 기록."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOG_PATH = Path(__file__).resolve().parent.parent / "mcp-audit.log"


def record_audit_event(
    payload: dict[str, Any],
    log_path: Path | str | None = None,
) -> dict[str, Any]:
    """도구 호출 감사 이벤트를 JSONL 파일에 한 줄로 기록한다."""
    target = Path(
        log_path
        or os.environ.get("QUOTE_AUDIT_LOG", "").strip()
        or DEFAULT_LOG_PATH
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_name": payload.get("tool_name", "unknown"),
        "tool_input": payload.get("tool_input", {}),
        "status": payload.get("status", "ok"),
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        return 0
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            payload = {"tool_name": "raw", "tool_input": {"raw": raw}}
    except json.JSONDecodeError:
        payload = {"tool_name": "raw", "tool_input": {"raw": raw}}
    record_audit_event(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
