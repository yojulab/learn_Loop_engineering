"""ch03-skills/github-workflow-skills 5종 스킬 구조 및 검증 스크립트 단위 테스트."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent.parent

SKILL_VALIDATORS = (
    ("gh-issue", "sample_issue.md", "validate_issue.py", "validate_issue", "invalid text"),
    ("git-commit", "sample_commit.txt", "validate_commit.py", "validate_commit", "bad commit message"),
    ("gh-pr", "sample_pr.md", "validate_pr.py", "validate_pr", "no issue link here"),
    ("gh-review", "sample_review.md", "validate_review.py", "validate_review", "looks good"),
    ("gh-address-review", "sample_address_review.md", "validate_address_review.py", "validate_address_review", "done"),
)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TestGithubWorkflowSkills(unittest.TestCase):
    def test_all_five_skills_structure_and_frontmatter(self) -> None:
        for skill_name, example_name, validator_name, _, _ in SKILL_VALIDATORS:
            with self.subTest(skill=skill_name):
                sdir = SKILLS_ROOT / skill_name
                skill_md = (sdir / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(skill_md.startswith("---"))
                self.assertIn(f"name: {skill_name}", skill_md)
                self.assertTrue((sdir / "reference.md").is_file())
                self.assertTrue((sdir / "examples" / example_name).is_file())
                self.assertTrue((sdir / "scripts" / validator_name).is_file())

    def test_validators_positive_and_negative(self) -> None:
        for skill_name, example_name, validator_name, fn_name, bad_input in SKILL_VALIDATORS:
            with self.subTest(skill=skill_name):
                sdir = SKILLS_ROOT / skill_name
                script_path = sdir / "scripts" / validator_name
                example_path = sdir / "examples" / example_name
                mod = _load_module(script_path, f"mod_{skill_name.replace('-', '_')}")
                fn = getattr(mod, fn_name)

                ok, errors = fn(example_path.read_text(encoding="utf-8"))
                self.assertTrue(ok, f"{skill_name} sample failed: {errors}")

                bad_ok, bad_errors = fn(bad_input)
                self.assertFalse(bad_ok)
                self.assertGreater(len(bad_errors), 0)

                proc = subprocess.run(
                    [sys.executable, str(script_path), str(example_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)

                proc_bad = subprocess.run(
                    [sys.executable, str(script_path), "--text", bad_input],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc_bad.returncode, 1)


if __name__ == "__main__":
    unittest.main()
