from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from harness.orchestrator import run_cycle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chapter 9 3-Agent Orchestration Runner")
    parser.add_argument("--mode", choices=["sim", "dry-run"], default="sim")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        res = run_cycle(
            Path(tmp) / "docs",
            "RSS-Wiki-Search",
            {"spec_fit": 3, "module_boundary": 3, "test_rigor": 2, "ops_readiness": 2},
            has_ui=False,
        )
        print(json.dumps({"mode": args.mode, **res}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
