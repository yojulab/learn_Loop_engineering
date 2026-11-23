"""저장소 루트 5종 문서, platforms/ 어댑터, AGENTS.md 100줄 제한, 레거시 완전 삭제 및 README 5단 구성 검증."""

from __future__ import annotations

import os
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY_MARKER = "ecare" + "24"
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}


class TestRepoRoot(unittest.TestCase):
    def test_root_docs_and_platforms_exist(self) -> None:
        required = [
            "README.md",
            "AGENTS.md",
            "CLAUDE.md",
            "CHATGPT.md",
            "GEMINI.md",
            "docs/ARCHITECTURE.md",
            "platforms/base.py",
            "platforms/adapter_claude.py",
            "platforms/adapter_chatgpt.py",
            "platforms/adapter_gemini.py",
        ]
        for rel in required:
            with self.subTest(path=rel):
                self.assertTrue((REPO_ROOT / rel).is_file(), f"Missing {rel}")

    def test_agents_md_within_100_lines(self) -> None:
        lines = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8").splitlines()
        self.assertGreater(len(lines), 0)
        self.assertLessEqual(len(lines), 100, f"AGENTS.md has {len(lines)} lines (>100)")

    def test_readme_five_section_template(self) -> None:
        content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        for idx in range(1, 6):
            self.assertRegex(content, rf"(?m)^##\s+{idx}\.")
        self.assertIn("```mermaid", content)

    def test_legacy_agents_dir_and_files_removed(self) -> None:
        self.assertFalse((REPO_ROOT / ".agents").exists(), ".agents directory must not exist")
        legacy_docs = [
            "docs/agent",
            "docs/USER_PROMPTS.md",
            "docs/PRD_TEMPLATE.md",
            "docs/user_prompt_history.md",
        ]
        for rel in legacy_docs:
            self.assertFalse((REPO_ROOT / rel).exists(), f"Legacy path must not exist: {rel}")

    def test_zero_legacy_marker_in_repository(self) -> None:
        hits: list[str] = []
        for current_root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fpath = Path(current_root) / fname
                if fpath.is_symlink():
                    continue
                text = fpath.read_text(encoding="utf-8", errors="ignore")
                if LEGACY_MARKER in text.lower():
                    hits.append(str(fpath.relative_to(REPO_ROOT)))
        self.assertEqual(hits, [], f"Legacy marker found in: {hits}")

    def test_existing_symlinks_are_valid(self) -> None:
        for ch_idx in range(1, 12):
            compat_dir = REPO_ROOT / f"ch{ch_idx:02d}"
            if not compat_dir.exists():
                continue
            for entry in compat_dir.rglob("*"):
                if entry.is_symlink():
                    self.assertTrue(entry.exists(), f"Broken symlink: {entry}")



    def test_all_chapters_have_ai_docs_folders_and_prompt_examples(self) -> None:
        chapters = sorted(p for p in REPO_ROOT.glob("ch*-*") if p.is_dir())
        self.assertEqual(len(chapters), 13)
        for cdir in chapters:
            with self.subTest(chapter=cdir.name):
                for doc in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md"):
                    self.assertTrue((cdir / doc).is_file(), f"{cdir.name}/{doc} 누락")
                self.assertLessEqual(len((cdir / "AGENTS.md").read_text(encoding="utf-8").splitlines()), 100)
                self.assertTrue((cdir / ".claude").is_dir(), f"{cdir.name}/.claude 폴더 누락")
                self.assertTrue((cdir / ".gemini").is_dir(), f"{cdir.name}/.gemini 폴더 누락")
                readme_txt = (cdir / "README.md").read_text(encoding="utf-8")
                for idx in (1, 2, 3):
                    self.assertIn(f"프롬프트 예시 {idx}", readme_txt, f"{cdir.name}/README.md 프롬프트 예시 {idx} 누락")


if __name__ == "__main__":
    unittest.main()
