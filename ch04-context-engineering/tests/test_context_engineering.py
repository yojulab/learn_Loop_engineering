"""ch04-context-engineering 단위 테스트."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

CH04_DIR = Path(__file__).resolve().parent.parent
if str(CH04_DIR) not in sys.path:
    sys.path.insert(0, str(CH04_DIR))

import context_budget  # noqa: E402


class TestContextEngineering(unittest.TestCase):
    def test_required_templates_and_layered_instructions(self) -> None:
        required_files = [
            "prompt_template.txt",
            "few_shot_reference.txt",
            "claude_working_guidelines.md",
            "CLAUDE.md",
            ".claude/rules/api.md",
            "AGENTS.md",
            "GEMINI.md",
        ]
        for rel in required_files:
            self.assertTrue((CH04_DIR / rel).is_file(), f"Missing {rel}")

        prompt_text = (CH04_DIR / "prompt_template.txt").read_text(encoding="utf-8")
        for section in ("[목표]", "[맥락]", "[참고 패턴]", "[제약과 범위]", "[도구/절차]", "[완료 기준]", "[보고 형식]"):
            self.assertIn(section, prompt_text)

        api_rule = (CH04_DIR / ".claude" / "rules" / "api.md").read_text(encoding="utf-8")
        self.assertTrue(api_rule.startswith("---"))
        self.assertIn("paths:", api_rule)

    def test_estimate_tokens_and_evaluate_budget_thresholds(self) -> None:
        self.assertEqual(context_budget.estimate_tokens(""), 0)
        self.assertGreater(context_budget.estimate_tokens("hello world!"), 0)

        ok_alloc = context_budget.evaluate_budget("sys", "inst", "tools", "hist", "out", max_window=10_000)
        self.assertEqual(ok_alloc.status, "OK")
        self.assertFalse(ok_alloc.lost_in_the_middle_risk)

        warn_alloc = context_budget.evaluate_budget(10_000, 10_000, 70_000, 70_000, 5_000, max_window=200_000)
        self.assertEqual(warn_alloc.status, "WARN")
        self.assertTrue(warn_alloc.lost_in_the_middle_risk)
        self.assertTrue(any("/compact" in rec for rec in warn_alloc.recommendations))

        crit_alloc = context_budget.evaluate_budget(10_000, 10_000, 50_000, 115_000, 5_000, max_window=200_000)
        self.assertEqual(crit_alloc.status, "CRITICAL")
        self.assertTrue(any("/clear" in rec for rec in crit_alloc.recommendations))

    def test_cli_json_and_text_exit_zero(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CH04_DIR / "context_budget.py"), "--json", "--history-tokens", "140000"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "WARN")


if __name__ == "__main__":
    unittest.main()
