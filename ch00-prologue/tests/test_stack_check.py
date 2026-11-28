"""ch00-prologue/stack_check.py 단위 테스트."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

PROLOGUE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PROLOGUE_DIR.parent
if str(PROLOGUE_DIR) not in sys.path:
    sys.path.insert(0, str(PROLOGUE_DIR))

import stack_check  # noqa: E402


class TestStackCheck(unittest.TestCase):
    def test_four_layers_eleven_elements_structure(self) -> None:
        elements = stack_check.FOUR_LAYERS_ELEMENTS
        self.assertEqual(len(elements), 11)
        layers = {e["layer_index"] for e in elements}
        self.assertEqual(layers, {1, 2, 3, 4})
        indices = [e["element_index"] for e in elements]
        self.assertEqual(indices, list(range(1, 12)))
        self.assertTrue(all(e["chapter"] != "ch05" for e in elements))

    def test_check_python_runtime(self) -> None:
        rt = stack_check.check_python_runtime()
        self.assertTrue(rt["python_supported"])
        self.assertIsInstance(rt["sqlite_fts5_enabled"], bool)
        self.assertTrue(rt["sqlite_fts5_enabled"])

    def test_check_installed_packages(self) -> None:
        pkg = stack_check.check_installed_packages()
        self.assertIn("packages", pkg)
        self.assertIn("pydantic", pkg["packages"])
        self.assertIn("PyYAML", pkg["packages"])

    def test_check_repo_layers(self) -> None:
        repo = stack_check.check_repo_layers(REPO_ROOT)
        self.assertTrue(repo["prologue_present"])
        self.assertEqual(len(repo["elements"]), 11)
        self.assertTrue(repo["root_docs"]["README.md"])

    def test_format_report_text_and_json(self) -> None:
        text = stack_check.format_report(as_json=False, root=REPO_ROOT)
        self.assertIn("4계층 11대 요소", text)
        raw_json = stack_check.format_report(as_json=True, root=REPO_ROOT)
        parsed = json.loads(raw_json)
        self.assertEqual(parsed["elements_count"], 11)
        self.assertEqual(parsed["layers_count"], 4)

    def test_cli_execution_exit_zero(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(PROLOGUE_DIR / "stack_check.py"), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["elements_count"], 11)


if __name__ == "__main__":
    unittest.main()
