"""제2장 PreToolUse 훅: 파괴적 Bash 명령 탐지 및 차단(exit 2)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

DANGEROUS_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"(^|\s|;|&&|\|\|)rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r|--recursive\s+--force)", "Blocked destructive 'rm -rf' command"),
    (r"\bgit\s+push\b[^\n]*(--force-with-lease|--force|\s-f(\s|$))", "Blocked destructive 'git push --force/-f' command"),
    (r"\bgit\s+reset\s+--hard\b", "Blocked destructive 'git reset --hard' command"),
    (r"\bdrop\s+table\b", "Blocked destructive SQL 'DROP TABLE' statement"),
    (r"\bfind\b[^\n]*\s-delete\b", "Blocked destructive 'find ... -delete' command"),
    (r"(^|\s|;|&&|\|\|)mkfs(\.[a-z0-9]+)?\b", "Blocked filesystem format 'mkfs' command"),
)


def evaluate_command(command: str) -> tuple[bool, str]:
    """명령어 안전 여부를 판별한다. (True, 'allowed') 또는 (False, reason)."""
    text = command.strip()
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return False, reason
    return True, "allowed"


def _extract_command(payload: dict[str, Any]) -> str:
    if "tool_input" in payload and isinstance(payload["tool_input"], dict):
        return str(payload["tool_input"].get("command", ""))
    return str(payload.get("command", ""))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PreToolUse dangerous Bash blocker")
    parser.add_argument("--command", default=None, help="직접 검사할 Bash 명령 문자열")
    args = parser.parse_args(argv)

    if args.command is not None:
        command = args.command
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            return 0
        try:
            payload = json.loads(raw)
            command = _extract_command(payload) if isinstance(payload, dict) else raw
        except json.JSONDecodeError:
            command = raw

    allowed, reason = evaluate_command(command)
    if not allowed:
        print(json.dumps({"decision": "block", "reason": reason, "command": command}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
