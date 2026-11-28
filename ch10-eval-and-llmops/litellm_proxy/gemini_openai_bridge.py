"""gemini_openai_bridge.py — Gemini Antigravity CLI (`agy -p`) OpenAI 호환 HTTP 브리지 (기본 포트: 4010)."""

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
        default_provider="gemini",
        default_port=int(os.getenv("GEMINI_BRIDGE_PORT", "4010")),
    )
