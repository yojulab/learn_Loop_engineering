from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

EPILOGUE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = EPILOGUE_DIR.parent


class TestStageReadiness(unittest.TestCase):
    def test_cli_json_reports_all_stages(self) -> None:
        res = subprocess.run(
            [sys.executable, str(EPILOGUE_DIR / "stage_readiness_check.py"), "--path", str(REPO_ROOT), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        data = json.loads(res.stdout)
        self.assertEqual(data["completed_stages"], 4)


if __name__ == "__main__":
    unittest.main()
