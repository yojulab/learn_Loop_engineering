from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspect_stages(repo_root: str | Path) -> dict[str, object]:
    root = Path(repo_root)
    s1 = (root / "AGENTS.md").is_file() and (root / "CLAUDE.md").is_file() and (root / "scripts" / "verify_chapters.py").is_file()
    s2 = (root / "ch08-orchestration" / "src" / "harness" / "permissions.py").is_file() and (root / "ch08-orchestration" / "src" / "harness" / "rubric.py").is_file()
    s3 = (root / "ch09-outer-loop" / "loop.py").is_file() and (root / "ch09-outer-loop" / "cost_logger.py").is_file()
    s4 = (root / "ch10-eval-and-llmops" / "evaluator.py").is_file() and (root / "ch10-eval-and-llmops" / "langfuse_ops.py").is_file()

    stages = {
        "stage_1_foundation": s1,
        "stage_2_role_separation": s2,
        "stage_3_outer_loop": s3,
        "stage_4_llmops": s4,
    }
    return {
        "repo_root": str(root),
        "stages": stages,
        "completed_stages": sum(1 for v in stages.values() if v),
        "total_stages": 4,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Epilogue Stage 1~4 Readiness Checker")
    default_root = "." if Path("scripts/verify_chapters.py").is_file() else str(Path(__file__).resolve().parent.parent)
    parser.add_argument("--path", default=default_root)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    report = inspect_stages(args.path)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Readiness: {report['completed_stages']}/{report['total_stages']}")
        for k, v in report["stages"].items():
            print(f"  - {k}: {'OK' if v else 'MISSING'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
