from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
REPO_ROOT = Path(__file__).resolve().parent.parent
for p in (SRC_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from harness.orchestrator import run_cycle
from platforms.base import resolve_platform, run_with_any_platform


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chapter 9 Any-Platform 3-Agent Orchestration Runner")
    parser.add_argument("--mode", choices=["sim", "dry-run"], default="sim")
    parser.add_argument("--platform", choices=["auto", "claude", "chatgpt", "gemini", "offline"], default="auto")
    args = parser.parse_args(argv)

    resolved_platform = resolve_platform(args.platform)
    platform_probe = run_with_any_platform("Planner-Generator-Evaluator cycle check", platform=args.platform, force_offline=(args.mode == "sim"))

    with tempfile.TemporaryDirectory() as tmp:
        res = run_cycle(
            Path(tmp) / "docs",
            "RSS-Wiki-Search",
            {"spec_fit": 3, "module_boundary": 3, "test_rigor": 2, "ops_readiness": 2},
            has_ui=False,
        )
        print(json.dumps({
            "mode": args.mode,
            "platform": resolved_platform,
            "adapter_mode": platform_probe.mode,
            **res,
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
