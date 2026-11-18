from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = HARNESS_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from harness.consensus import evaluate_consensus, parse_choice_line
from harness.orchestrator import run_cycle
from harness.permissions import PermissionViolationError, assert_role_action
from harness.rubric import score_evaluation


class TestOrchestrationHarness(unittest.TestCase):
    def test_prompts_exist(self) -> None:
        prompts_dir = SRC_DIR / "harness" / "prompts"
        for name in ["planner.md", "generator.md", "evaluator.md", "planner_bootstrap.md"]:
            self.assertTrue((prompts_dir / name).is_file(), f"Missing {name}")

    def test_permissions_enforced(self) -> None:
        with self.assertRaises(PermissionViolationError):
            assert_role_action("planner", "modify_code")
        with self.assertRaises(PermissionViolationError):
            assert_role_action("evaluator", "modify_code")
        assert_role_action("generator", "modify_code")

    def test_blind_consensus_agree_and_halt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            dec = docs / "decisions"
            dec.mkdir(parents=True)
            (dec / "001.planner.md").write_text("선택: A\nreason p\n", encoding="utf-8")
            (dec / "001.evaluator.md").write_text("선택: A\nreason e\n", encoding="utf-8")
            self.assertEqual(parse_choice_line("선택: A\n"), "A")
            ok = evaluate_consensus(docs, "001", attempt=1)
            self.assertEqual(ok.status, "AGREED")
            self.assertEqual(ok.adopted, "A")

            (dec / "002.planner.md").write_text("선택: A\n", encoding="utf-8")
            (dec / "002.evaluator.md").write_text("선택: B\n", encoding="utf-8")
            halt = evaluate_consensus(docs, "002", attempt=3, max_attempts=3)
            self.assertEqual(halt.status, "HALTED")
            self.assertTrue((docs / "HALT").is_file())

    def test_rubric_15_and_12_scales(self) -> None:
        r12 = score_evaluation({"spec_fit": 3, "module_boundary": 2, "test_rigor": 2, "ops_readiness": 2}, has_ui=False)
        self.assertEqual(r12["max_score"], 12)
        self.assertEqual(r12["verdict"], "PASS")
        r15 = score_evaluation({"spec_fit": 2, "module_boundary": 2, "test_rigor": 1, "ops_readiness": 1, "ui_polish": 1}, has_ui=True)
        self.assertEqual(r15["max_score"], 15)
        self.assertEqual(r15["verdict"], "FAIL")

    def test_file_mediated_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            res = run_cycle(docs, "TASK-DEMO", {"spec_fit": 3, "module_boundary": 3, "test_rigor": 3, "ops_readiness": 3})
            self.assertEqual(res["verdict"], "PASS")
            for f in ["PRD.md", "PLAN.md", "TASKS.md", "IMPL.md", "REVIEW.md", "JOURNAL.md"]:
                self.assertTrue((docs / f).is_file())


if __name__ == "__main__":
    unittest.main()
