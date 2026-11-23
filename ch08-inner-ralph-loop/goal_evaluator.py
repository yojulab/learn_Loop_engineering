from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GoalCondition:
    name: str
    passed: bool
    detail: str


def evaluate_goal(target_dir: str | Path) -> dict:
    root = Path(target_dir)
    checks = [
        GoalCondition("db_module", (root / "db.py").exists(), "db.py 존재 확인"),
        GoalCondition("collector_module", (root / "collector.py").exists(), "collector.py 존재 확인"),
        GoalCondition("app_module", (root / "app.py").exists(), "app.py 존재 확인"),
        GoalCondition("ralph_loop_script", (root / "ralph_loop.sh").exists(), "ralph_loop.sh 존재 확인"),
        GoalCondition("tests_present", any((root / "tests").glob("test_*.py")), "단위 테스트 존재 확인"),
    ]
    all_met = all(c.passed for c in checks)
    return {
        "status": "MET" if all_met else "CONTINUE",
        "passed_count": sum(1 for c in checks if c.passed),
        "total_count": len(checks),
        "checks": [c.__dict__ for c in checks],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="/goal 독립 완료 판정 시뮬레이터")
    parser.add_argument("--target", default=str(Path(__file__).resolve().parent))
    args = parser.parse_args(argv)
    report = evaluate_goal(args.target)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
