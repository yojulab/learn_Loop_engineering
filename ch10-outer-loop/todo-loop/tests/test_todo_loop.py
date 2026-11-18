from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from cost_logger import CostLogger
from loop import OuterLoopController, load_sample_tasks
from models import LoopBudget, StopReason
from workers import DeterministicTestWorker, LLMWorker


class TestTodoLoop(unittest.TestCase):
    def test_calc_001_to_004_with_human_halt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "cost.jsonl"
            ctrl = OuterLoopController(load_sample_tasks(), DeterministicTestWorker(), LoopBudget(), CostLogger(log_file))
            res = ctrl.run(halt_on_human=True)
            self.assertEqual(res.stop_reason, StopReason.HALT_HUMAN_DECISION)
            self.assertEqual(res.completed_tasks, ["CALC-001", "CALC-002"])
            self.assertEqual(res.halted_tasks, ["CALC-003"])
            self.assertTrue(log_file.is_file())

    def test_dependency_order_calc_004_after_skipping_human_halt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "cost.jsonl"
            ctrl = OuterLoopController(load_sample_tasks(), LLMWorker(), LoopBudget(), CostLogger(log_file))
            res = ctrl.run(halt_on_human=False)
            self.assertEqual(res.completed_tasks, ["CALC-001", "CALC-002", "CALC-004"])
            self.assertEqual(res.halted_tasks, ["CALC-003"])
            self.assertGreater(res.total_cost_usd, 0.0)


if __name__ == "__main__":
    unittest.main()
