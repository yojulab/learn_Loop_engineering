"""ch02-mcp-and-hooks/quote-mcp 단위 테스트."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

QMCP_DIR = Path(__file__).resolve().parent.parent
if str(QMCP_DIR) not in sys.path:
    sys.path.insert(0, str(QMCP_DIR))
if str(QMCP_DIR / "hooks") not in sys.path:
    sys.path.insert(0, str(QMCP_DIR / "hooks"))

import audit_logger  # noqa: E402
import block_dangerous_bash  # noqa: E402
import main as mcp_main  # noqa: E402


class TestQuoteMcpAndHooks(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.temp_quotes = self.tmpdir / "quotes.json"
        shutil.copy(QMCP_DIR / "quotes.json", self.temp_quotes)
        self._prev_env = os.environ.get("QUOTE_DATA_PATH")
        os.environ["QUOTE_DATA_PATH"] = str(self.temp_quotes)

    def tearDown(self) -> None:
        if self._prev_env is None:
            os.environ.pop("QUOTE_DATA_PATH", None)
        else:
            os.environ["QUOTE_DATA_PATH"] = self._prev_env
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_mcp_tools_resource_and_prompt(self) -> None:
        quote = mcp_main.get_random_quote(tag="engineering")
        self.assertIn("text", quote)

        added = mcp_main.add_quote("Verify everything automatically.", "Test Author", ["testing"])
        self.assertEqual(added["status"], "added")
        self.assertEqual(added["quote"]["author"], "Test Author")

        all_json = mcp_main.read_all_quotes()
        all_items = json.loads(all_json)
        self.assertTrue(any(item["author"] == "Test Author" for item in all_items))

        prompt_text = mcp_main.quote_post(topic="engineering", tone="concise")
        self.assertIn("Tone: concise", prompt_text)

    def test_local_fastmcp_adapter_contract(self) -> None:
        adapter = mcp_main.LocalFastMCP("test-mcp")

        @adapter.tool()
        def ping() -> str:
            return "pong"

        @adapter.resource("test://info")
        def info() -> str:
            return "ok"

        @adapter.prompt()
        def greet(who: str) -> str:
            return f"hello {who}"

        self.assertEqual(adapter.call_tool("ping"), "pong")
        self.assertEqual(adapter.read_resource("test://info"), "ok")
        self.assertEqual(adapter.get_prompt("greet", who="world"), "hello world")

    def test_configs_exist_and_valid(self) -> None:
        mcp_cfg = json.loads((QMCP_DIR / ".mcp.json").read_text(encoding="utf-8"))
        env = mcp_cfg["mcpServers"]["quote-mcp"]["env"]
        self.assertIn("${QUOTE_DATA_PATH:-./quotes.json}", env["QUOTE_DATA_PATH"])

        settings = json.loads((QMCP_DIR / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertIn("PreToolUse", settings["hooks"])
        self.assertIn("PostToolUse", settings["hooks"])

    def test_block_dangerous_bash_hook(self) -> None:
        dangerous = [
            "rm -rf /tmp/something",
            "git push origin main --force",
            "git push -f origin develop",
            "git reset --hard HEAD~1",
            "sqlite3 app.db 'DROP TABLE users;'",
            "find . -name '*.log' -delete",
            "mkfs.ext4 /dev/sdb1",
        ]
        for cmd in dangerous:
            with self.subTest(cmd=cmd):
                allowed, _reason = block_dangerous_bash.evaluate_command(cmd)
                self.assertFalse(allowed)
                proc = subprocess.run(
                    [sys.executable, str(QMCP_DIR / "hooks" / "block_dangerous_bash.py")],
                    input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc.returncode, 2)
                out = json.loads(proc.stdout)
                self.assertEqual(out["decision"], "block")

        safe_proc = subprocess.run(
            [sys.executable, str(QMCP_DIR / "hooks" / "block_dangerous_bash.py")],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}}),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(safe_proc.returncode, 0)

    def test_audit_logger_hook(self) -> None:
        log_file = self.tmpdir / "mcp-audit.log"
        entry = audit_logger.record_audit_event(
            {"tool_name": "add_quote", "tool_input": {"author": "A"}, "status": "ok"},
            log_path=log_file,
        )
        self.assertEqual(entry["tool_name"], "add_quote")

        env = dict(os.environ)
        env["QUOTE_AUDIT_LOG"] = str(log_file)
        proc = subprocess.run(
            [sys.executable, str(QMCP_DIR / "hooks" / "audit_logger.py")],
            input=json.dumps({"tool_name": "mcp__quote__add_quote", "tool_input": {"text": "hi"}}),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [json.loads(line) for line in log_file.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[1]["tool_name"], "mcp__quote__add_quote")


if __name__ == "__main__":
    unittest.main()
