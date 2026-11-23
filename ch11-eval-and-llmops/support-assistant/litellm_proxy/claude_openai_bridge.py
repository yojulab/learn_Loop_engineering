"""claude_openai_bridge.py — Claude Code CLI (`claude -p`) OpenAI 호환 HTTP 브리지 (기본 포트: 4011)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from cli_openai_bridge import run_bridge_cli  # noqa: E402


if __name__ == "__main__":
    run_bridge_cli(
        default_provider="claude",
        default_port=int(os.getenv("CLAUDE_BRIDGE_PORT", "4011")),
    )
