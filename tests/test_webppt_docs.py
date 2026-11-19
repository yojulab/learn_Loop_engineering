"""GitHub Pages 5시간 웹 PPT(docs/) 구조, 접근성, 토글 모범답안, JS 문법 검증 테스트."""

from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

REQUIRED_WEBPPT_FILES = (
    "README.md",
    "ARCHITECTURE.md",
    ".nojekyll",
    "index.html",
    "presenter.html",
    "deck.css",
    "engine.js",
    "ui.js",
    "slides/00_manifest.js",
    "slides/s0_opening.js",
    "slides/s1_part1.js",
    "slides/s2_part2.js",
    "slides/s3_part3.js",
    "slides/s4_part4_a.js",
    "slides/s5_part4_b.js",
)


class WebPptDocsTests(unittest.TestCase):
    def test_required_files_and_existing_architecture_preserved(self) -> None:
        for rel in REQUIRED_WEBPPT_FILES:
            path = DOCS_DIR / rel
            self.assertTrue(path.is_file(), f"필수 Web PPT 파일 누락: {path}")
        arch = (DOCS_DIR / "ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertGreater(len(arch.strip()), 200)

    def test_index_html_uses_relative_local_assets_and_semantic_landmarks(self) -> None:
        html = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="ko">', html)
        self.assertIn('<main id="deck"', html)
        for asset in (
            "deck.css",
            "engine.js",
            "ui.js",
            "slides/00_manifest.js",
            "slides/s0_opening.js",
            "slides/s5_part4_b.js",
        ):
            self.assertIn(f'"{asset}"', html)
            self.assertNotIn(f'"/{asset}"', html, "GitHub Pages 서브패스 호환을 위해 루트 절대경로('/') 금지")

    def test_all_chapters_have_lab_and_clickable_answer_without_summary_headings(self) -> None:
        slides_text = "\n".join(
            (DOCS_DIR / f"slides/{name}").read_text(encoding="utf-8")
            for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
        )
        for i in range(13):
            chap = f"ch{i:02d}"
            self.assertRegex(slides_text, rf"id:\s*'{chap}-lab'", f"{chap} 실습+모범답안 슬라이드 누락")
            self.assertIn(f"id: '{chap}',", slides_text, f"{chap} buildLabSlide 호출 누락")

        ui_js = (DOCS_DIR / "ui.js").read_text(encoding="utf-8")
        self.assertIn("h('details', 'answer-toggle'", ui_js)
        self.assertIn("h('summary', '', det)", ui_js)
        self.assertIn("setAttribute('tabindex', '0')", ui_js)
        self.assertIn("setAttribute('role', 'region')", ui_js)
        # modern-web-guidance: summary 내부에 h1~h6 배치 금지
        self.assertIsNone(re.search(r"<summary[^>]*>.*?<h[1-6]\b", ui_js + slides_text, re.DOTALL))

    def test_css_prefers_reduced_motion_and_focus_visible(self) -> None:
        css = (DOCS_DIR / "deck.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: no-preference", css)
        self.assertIn("::details-content", css)
        self.assertIn(":focus-visible", css)

    def test_javascript_files_pass_node_syntax_check(self) -> None:
        node_bin = shutil.which("node")
        if node_bin is None:
            self.skipTest("node 바이너리가 없어 JS 문법 검사를 건너뜁니다.")
        js_files = [
            DOCS_DIR / "engine.js",
            DOCS_DIR / "ui.js",
            *sorted((DOCS_DIR / "slides").glob("*.js")),
        ]
        for js in js_files:
            proc = subprocess.run([node_bin, "--check", str(js)], capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, f"JS 문법 오류 ({js}): {proc.stderr}")


    def test_keyboard_shortcuts_use_physical_codes_and_exclude_n(self) -> None:
        engine_js = (DOCS_DIR / "engine.js").read_text(encoding="utf-8")
        for code_name in ("KeyA", "KeyO", "KeyF", "KeyB", "KeyH", "KeyP", "Space", "NumpadEnter"):
            self.assertIn(code_name, engine_js, f"한글 IME/다양한 키보드 대응용 e.code 누락: {code_name}")
        self.assertNotIn("KeyN", engine_js)
        self.assertNotIn("메모 (N)", engine_js)
        self.assertNotIn("k === 'n'", engine_js)

if __name__ == "__main__":
    unittest.main()
