from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from app import create_app, get_test_client
from collector import collect_from_source
from db import WikiDatabase
from goal_evaluator import evaluate_goal


class TestRssWikiAndRalphLoop(unittest.TestCase):
    def test_fts5_and_collector(self) -> None:
        db = WikiDatabase(":memory:")
        items = collect_from_source(APP_DIR / "sample_feed.xml", db=db)
        self.assertEqual(len(items), 3)
        hits = db.search_fts("FTS5")
        self.assertEqual(len(hits), 1)
        self.assertIn("SQLite FTS5", hits[0]["title"])
        db.close()

    def test_web_app_routes_http_200(self) -> None:
        app = create_app(":memory:")
        db = getattr(app, "state", None).db if hasattr(app, "state") else app.db
        collect_from_source(APP_DIR / "sample_feed.xml", db=db)
        client = get_test_client(app)
        for path in ["/", "/articles", "/articles/1", "/search?q=Ralph", "/wiki", "/health"]:
            resp = client.get(path)
            self.assertEqual(resp.status_code, 200, f"Failed on {path}")

    def test_ralph_loop_normal_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "TASKS.md"
            jpath = Path(tmp) / "JOURNAL.md"
            tpath.write_text("- [ ] TASK-1: demo\n", encoding="utf-8")
            jpath.write_text("", encoding="utf-8")
            worker_cmd = f"python3 -c \"from pathlib import Path; p=Path('{tpath}'); p.write_text(p.read_text().replace('- [ ]', '- [x]', 1))\""
            env = {**os.environ, "TASKS_FILE": str(tpath), "JOURNAL_FILE": str(jpath), "WORKER_CMD": worker_cmd}
            res = subprocess.run(["bash", str(APP_DIR / "ralph_loop.sh")], env=env, capture_output=True, text=True, check=False)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertIn("ALL_DONE", jpath.read_text(encoding="utf-8"))

    def test_ralph_loop_three_failures_blocked_circuit_breaker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tpath = Path(tmp) / "TASKS.md"
            jpath = Path(tmp) / "JOURNAL.md"
            tpath.write_text("- [ ] TASK-FAIL: always fail\n", encoding="utf-8")
            jpath.write_text("", encoding="utf-8")
            env = {
                **os.environ,
                "TASKS_FILE": str(tpath),
                "JOURNAL_FILE": str(jpath),
                "CONSECUTIVE_FAIL_LIMIT": "3",
                "WORKER_CMD": "false",
            }
            res = subprocess.run(["bash", str(APP_DIR / "ralph_loop.sh")], env=env, capture_output=True, text=True, check=False)
            self.assertEqual(res.returncode, 2)
            self.assertIn("- [BLOCKED] TASK-FAIL", tpath.read_text(encoding="utf-8"))
            self.assertIn("CIRCUIT_BREAKER_TRIGGERED", jpath.read_text(encoding="utf-8"))

    def test_goal_evaluator_met(self) -> None:
        report = evaluate_goal(APP_DIR)
        self.assertEqual(report["status"], "MET")


    def test_multi_platform_worker_scripts_and_ralph_dispatch(self) -> None:
        for script in ("worker_claude.sh", "worker_chatgpt.sh", "worker_gemini.sh"):
            res = subprocess.run(["bash", str(APP_DIR / script), str(APP_DIR / "PROMPT.md")], capture_output=True, text=True, check=False)
            self.assertEqual(res.returncode, 0, res.stderr)


if __name__ == "__main__":
    unittest.main()
