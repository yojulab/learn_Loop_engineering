"""ch07-harness-engineering/harness-templates 단위 테스트."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

HT_DIR = Path(__file__).resolve().parent.parent
if str(HT_DIR) not in sys.path:
    sys.path.insert(0, str(HT_DIR))

import arch_linter  # noqa: E402
import doc_gardening  # noqa: E402
import guardrails  # noqa: E402


class TestHarnessTemplates(unittest.TestCase):
    def test_agents_md_under_100_lines_and_four_questions(self) -> None:
        text = (HT_DIR / "AGENTS.md").read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertLessEqual(len(lines), 100)
        for keyword in ("무엇을 막을 것인가", "무엇을 보여줄 것인가", "어떤 도구를 줄 것인가", "어떻게 갈아 끼울 것인가"):
            self.assertIn(keyword, text)

    def test_arch_linter_valid_and_invalid_apps(self) -> None:
        valid_dir = HT_DIR / "samples" / "valid_app"
        invalid_dir = HT_DIR / "samples" / "invalid_app"

        self.assertEqual(arch_linter.check_architecture(valid_dir), [])
        violations = arch_linter.check_architecture(invalid_dir)
        self.assertGreaterEqual(len(violations), 2)
        v_types = {v.violation_type for v in violations}
        self.assertIn("reverse_dependency", v_types)
        self.assertIn("layer_skip", v_types)
        self.assertTrue(all("여기가 틀렸으니 이렇게 고쳐라" in v.fix_guide for v in violations))

        proc_bad = subprocess.run(
            [sys.executable, str(HT_DIR / "arch_linter.py"), "--root", str(invalid_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(proc_bad.returncode, 0)
        self.assertIn("여기가 틀렸으니 이렇게 고쳐라", proc_bad.stdout)

    def test_guardrails_blocks_dangerous_and_allows_safe(self) -> None:
        self.assertEqual(len(guardrails.CORE_GUARDRAIL_RULES), 5)
        ok_safe, _ = guardrails.check_command_safety("python3 -m unittest discover")
        self.assertTrue(ok_safe)

        for bad_cmd in ("rm -rf /", "git push --force", "git reset --hard", "DROP TABLE t;", "mkfs.ext4 /dev/sda"):
            ok_bad, msgs = guardrails.check_command_safety(bad_cmd)
            self.assertFalse(ok_bad, f"Should block {bad_cmd}")
            self.assertGreaterEqual(len(msgs), 1)

    def test_doc_gardening_valid_and_invalid_apps(self) -> None:
        self.assertEqual(doc_gardening.audit_docs(HT_DIR / "samples" / "valid_app"), [])
        issues = doc_gardening.audit_docs(HT_DIR / "samples" / "invalid_app")
        issue_types = {i.issue_type for i in issues}
        self.assertIn("orphan_doc", issue_types)
        self.assertTrue("stale_index" in issue_types or "broken_link" in issue_types)


if __name__ == "__main__":
    unittest.main()
