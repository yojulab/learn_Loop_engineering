"""ch01-agentic-coding/quote-cli 단위 테스트."""

from __future__ import annotations

import json
import random
import subprocess
import sys
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

import interactive_demo  # noqa: E402
import quote_cli  # noqa: E402


class TestQuoteCli(unittest.TestCase):
    def test_load_and_filter_by_tag(self) -> None:
        quotes = quote_cli.load_quotes()
        self.assertGreaterEqual(len(quotes), 5)
        eng = quote_cli.filter_by_tag(quotes, "engineering")
        self.assertGreaterEqual(len(eng), 2)
        self.assertTrue(all("engineering" in q["tags"] for q in eng))

    def test_get_random_quote_deterministic_seed(self) -> None:
        quotes = quote_cli.load_quotes()
        q1 = quote_cli.get_random_quote(quotes, rng=random.Random(42))
        q2 = quote_cli.get_random_quote(quotes, rng=random.Random(42))
        self.assertEqual(q1, q2)

    def test_format_quotes_json_and_text(self) -> None:
        quotes = quote_cli.load_quotes()[:1]
        as_json = quote_cli.format_quotes(quotes, as_json=True)
        parsed = json.loads(as_json)
        self.assertEqual(len(parsed), 1)
        as_text = quote_cli.format_quotes(quotes, as_json=False)
        self.assertIn(quotes[0]["author"], as_text)

    def test_cli_all_and_tag(self) -> None:
        proc_all = subprocess.run(
            [sys.executable, str(CLI_DIR / "quote_cli.py"), "--all", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc_all.returncode, 0, proc_all.stderr)
        self.assertGreaterEqual(len(json.loads(proc_all.stdout)), 5)

        proc_tag = subprocess.run(
            [sys.executable, str(CLI_DIR / "quote_cli.py"), "--tag", "engineering", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc_tag.returncode, 0, proc_tag.stderr)
        tagged = json.loads(proc_tag.stdout)
        self.assertGreaterEqual(len(tagged), 2)

    def test_interactive_demo_loop_and_pipe(self) -> None:
        res = interactive_demo.run_agent_loop("verify engineering quotes", tag="engineering")
        self.assertTrue(res["step_3_verification"]["verified"])
        proc = subprocess.run(
            [sys.executable, str(CLI_DIR / "interactive_demo.py"), "--stdin", "--json"],
            input="piped task from stdin\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["step_1_context"]["task"], "piped task from stdin")
        self.assertTrue(payload["step_3_verification"]["verified"])


if __name__ == "__main__":
    unittest.main()
