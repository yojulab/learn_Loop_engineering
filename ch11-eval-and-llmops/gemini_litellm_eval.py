"""gemini_litellm_eval.py — Gemini CLI (`agy -p`) -> LiteLLM Proxy -> Langfuse(Trace + Eval Scores) 실행기."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from cli_litellm_eval import run_eval_cli  # noqa: E402


if __name__ == "__main__":
    run_eval_cli(
        default_model="gemini-cli",
        description="Gemini CLI (agy -p) -> LiteLLM -> Langfuse Trace & Eval 실행기",
    )
