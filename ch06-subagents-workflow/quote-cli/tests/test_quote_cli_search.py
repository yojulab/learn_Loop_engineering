"""ch06-subagents-workflow/quote-cli 검색 확장 단위 테스트."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

QCLI6_DIR = Path(__file__).resolve().parent.parent
if str(QCLI6_DIR) not in sys.path:
    sys.path.insert(0, str(QCLI6_DIR))

import quote_cli  # noqa: E402


class TestQuoteCliSearch(unittest.TestCase):
    def test_search_author_and_tag(self) -> None:
        quotes = quote_cli.load_quotes()
        self.assertGreaterEqual(len(quote_cli.search_quotes(quotes, "guardrails")), 1)
        self.assertGreaterEqual(len(quote_cli.filter_by_author(quotes, "Hermes")), 2)
        self.assertGreaterEqual(len(quote_cli.filter_by_tag(quotes, "subagents")), 1)

    def test_cli_search_and_dot_claude_symlink(self) -> None:
        agents_link = QCLI6_DIR / ".claude" / "agents"
        self.assertTrue(agents_link.is_dir())
        self.assertEqual(len(list(agents_link.glob("*.md"))), 5)

        proc = subprocess.run(
            [sys.executable, str(QCLI6_DIR / "quote_cli.py"), "--search", "Hermes", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertGreaterEqual(len(data), 2)


if __name__ == "__main__":
    unittest.main()
