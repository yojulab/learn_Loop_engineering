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
    "prologue.html",
    "lecture.html",
    "slides/p_prologue.js",
    "assets/profile_ohsanghun.jpg",
    "assets/qr_linkedin.svg",
    "assets/qr_facebook.svg",
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
        html = (DOCS_DIR / "lecture.html").read_text(encoding="utf-8")
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
        for i in (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12):
            chap = f"ch{i:02d}"
            self.assertRegex(slides_text, rf"id:\s*'{chap}-lab'", f"{chap} 실습+모범답안 슬라이드 누락")
            self.assertIn(f"id: '{chap}',", slides_text, f"{chap} buildLabSlide 호출 누락")
        self.assertNotIn("ch05-theory", slides_text)
        self.assertNotIn("ch05-lab", slides_text)

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
            *sorted((DOCS_DIR / "slides_workshop").glob("*.js")),
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
        self.assertNotIn("'모범답안 (A)'", engine_js)
        self.assertIn("toggleCurrentAnswer()", engine_js)

    def test_lab_steps_linebreak_imperative_and_block_layout(self) -> None:
        css = (DOCS_DIR / "deck.css").read_text(encoding="utf-8")
        self.assertIn(".lab-steps li { position: relative; display: block;", css)
        self.assertIn("white-space: pre-wrap;", css)
        slides_text = "\n".join(
            (DOCS_DIR / f"slides/{name}").read_text(encoding="utf-8")
            for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
        )
        # 모든 실습 스텝 문자열이 <br> 줄바꿈을 포함하고 ~한다./본다. 대신 명령형 종결을 사용
        step_blocks = re.findall(r"steps:\s*\[(.*?)\]", slides_text, re.DOTALL)
        self.assertGreaterEqual(len(step_blocks), 12)
        for block in step_blocks:
            items = re.findall(r"'([^']+)'", block)
            self.assertGreaterEqual(len(items), 3)
            for item in items:
                self.assertIn("<br>", item, f"명령줄과 설명글 사이 <br> 줄바꿈 누락: {item}")
                self.assertFalse(item.endswith("한다.") or item.endswith("본다."), f"명령형 종결 미준수: {item}")

    def test_no_2026_in_webppt_and_timetable_nowrap(self) -> None:
        for rel in ("index.html", "presenter.html", "engine.js", "ui.js", "deck.css"):
            self.assertNotIn("2026", (DOCS_DIR / rel).read_text(encoding="utf-8"), f"Web PPT 내 2026 문구 잔존: {rel}")
        for js in (DOCS_DIR / "slides").glob("*.js"):
            self.assertNotIn("2026", js.read_text(encoding="utf-8"), f"슬라이드 내 2026 문구 잔존: {js.name}")
        css = (DOCS_DIR / "deck.css").read_text(encoding="utf-8")
        self.assertIn("tbl-timetable", css)
        self.assertIn("white-space: nowrap;", css)

    def test_loop_rebranding_and_target_architecture_between_p1_and_p2(self) -> None:
        for rel in ("index.html", "presenter.html", "engine.js", "ui.js", "deck.css", "README.md"):
            txt = (DOCS_DIR / rel).read_text(encoding="utf-8")
            self.assertNotIn("hermes", txt.lower(), f"Hermes 잔존 문구 발견: {rel}")
        for js in (DOCS_DIR / "slides").glob("*.js"):
            txt = js.read_text(encoding="utf-8")
            self.assertNotIn("hermes", txt.lower(), f"슬라이드 내 Hermes 잔존 문구 발견: {js.name}")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# 혼자서 프로젝트 17개 돌리는 개발자의 비밀: 루프 엔지니어링", readme)
        self.assertIn("프롬프트 노가다는 끝났다", readme)
        self.assertIn("https://yojulab.github.io/learn_Loop_engineering/", readme)
        self.assertNotIn("Hermes", readme)

        s0 = (DOCS_DIR / "slides/s0_opening.js").read_text(encoding="utf-8")
        idx_cover = s0.find("id: 'cover'")
        idx_arch = s0.find("id: 'target-architecture'")
        idx_time = s0.find("id: 'timetable'")
        self.assertTrue(0 <= idx_cover < idx_arch < idx_time, "p.1과 p.2 사이 target-architecture 배치 오류")
        self.assertIn("LangGraph", s0[idx_arch:idx_time])
        self.assertIn("Langfuse", s0[idx_arch:idx_time])
        self.assertIn("<svg viewBox=", s0[idx_arch:idx_time])

    @staticmethod
    def _resolve_repo_path(rel_path: str, chap_hint: str = "") -> Path:
        direct = REPO_ROOT / rel_path
        if direct.exists():
            return direct
        if chap_hint and re.match(r"^ch\d{2}$", chap_hint):
            hinted = sorted(REPO_ROOT.glob(f"{chap_hint}*/{rel_path}"))
            if hinted:
                return hinted[0]
        matches = sorted(REPO_ROOT.glob(f"ch*/{rel_path}"))
        if matches:
            return matches[0]
        return direct

    def test_all_slide_referenced_paths_and_runcmds_are_valid(self) -> None:
        import shlex
        slides_text = "\n".join(
            (DOCS_DIR / f"slides/{name}").read_text(encoding="utf-8")
            for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
        )
        # 1) 모든 chXX.../*.py|sh|json|yaml|md|txt 참조 파일 실존 확인
        for m in re.finditer(r"(ch\d{2}[^\s<'\`\"]+\.(?:py|sh|json|yaml|md|txt))", slides_text):
            rel_path = m.group(1)
            self.assertTrue((REPO_ROOT / rel_path).exists(), f"슬라이드에 없는 파일 경로 참조됨: {rel_path}")

        # 2) 모든 runCmd 내 python3 단원 CLI(단위테스트 제외, 단위테스트 디렉터리 실존) 검증
        for m in re.finditer(r"buildLabSlide\(el,\s*A,\s*\{(.*?)\n\s*\}\);", slides_text, re.DOTALL):
            block = m.group(1)
            id_m = re.search(r"id:\s*'([^']+)'", block)
            chap_hint = id_m.group(1) if id_m else ""
            if chap_hint == "capstone":
                chap_hint = "ch12"
            cmd_m = re.search(r"runCmd:\s*'([^']+)'", block)
            if not cmd_m:
                continue
            raw_cmd = cmd_m.group(1).replace("\\n", "\n")
            for line in raw_cmd.splitlines():
                line = line.strip()
                if not line:
                    continue
                if " -m unittest discover -s " in line:
                    tdir = line.split(" -s ", 1)[1].split()[0]
                    resolved_tdir = self._resolve_repo_path(tdir, chap_hint)
                    self.assertTrue(resolved_tdir.is_dir(), f"없는 테스트 디렉터리 참조: {tdir}")
                elif "scripts/verify_chapters.py" in line:
                    self.assertTrue((REPO_ROOT / "scripts/verify_chapters.py").is_file())
                elif line.startswith("python3 "):
                    parts = shlex.split(line)
                    resolved_parts = [
                        str(self._resolve_repo_path(tok, chap_hint))
                        if (i == 1 or (i > 1 and parts[i - 1] == "--root")) and not tok.startswith("-")
                        else tok
                        for i, tok in enumerate(parts)
                    ]
                    proc = subprocess.run(resolved_parts, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
                    self.assertEqual(proc.returncode, 0, f"runCmd 실행 실패 ({line}): {proc.stderr}")

    def test_lab_slides_exclude_chapter_folders_and_symlinks(self) -> None:
        slides_text = "\n".join(
            (DOCS_DIR / f"slides/{name}").read_text(encoding="utf-8")
            for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
        )
        for m in re.finditer(r"buildLabSlide\(el,\s*A,\s*\{(.*?)\n\s*\}\);", slides_text, re.DOTALL):
            body = m.group(1)
            self.assertIsNone(re.search(r"\bch\d{2}(?:-[a-z0-9-]+)?/", body), f"실습 슬라이드에 챕터 폴더 경로 잔존: {body[:120]}")
            self.assertNotIn("심볼릭", body)
            self.assertNotIn("symlink", body.lower())

    def test_home_portal_and_dedicated_prologue_ppt(self) -> None:
        home = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("Let's AX with Cartoons.", home)
        self.assertIn("assets/profile_ohsanghun.jpg", home)
        self.assertIn("assets/qr_linkedin.svg", home)
        self.assertIn("assets/qr_facebook.svg", home)
        self.assertIn("prologue.html", home)
        self.assertIn("lecture.html", home)

        p_js = (DOCS_DIR / "slides/p_prologue.js").read_text(encoding="utf-8")
        self.assertIn("Probability", p_js)
        self.assertIn("이해의 부채", p_js)
        self.assertIn("진정한 검증자", p_js)

        s0_js = (DOCS_DIR / "slides/s0_opening.js").read_text(encoding="utf-8")
        self.assertIn("assets/qr_linkedin.svg", s0_js)
        self.assertIn("assets/qr_facebook.svg", s0_js)

        self.assertIn("https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing", home)
        self.assertIn("https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing", p_js)
        self.assertIn("https://docs.google.com/spreadsheets/d/14zBhkMpG3YPLJtSmYtaeiQcTokBrZbKhKZw8965DnEI/edit?usp=sharing", (DOCS_DIR / "engine.js").read_text(encoding="utf-8"))
        self.assertNotIn("PDF 인쇄", (DOCS_DIR / "engine.js").read_text(encoding="utf-8"))
        self.assertIn("사전 필요 지식", home)
        self.assertIn("DevOps", home)
        self.assertIn("Prompt Engineering", home)
        self.assertIn("home-prereq-row", home)
        self.assertIn('class="home-html"', home)
        self.assertLess(home.find("home-qr-row"), home.find("home-prereq-row"))
        self.assertLess(p_js.find("id: 'prologue-ebook'"), p_js.find("id: 'prologue-goal'"))
        ui_txt = (DOCS_DIR / "ui.js").read_text(encoding="utf-8")
        self.assertIn("btn-copy-prompt", ui_txt)
        self.assertIn("show-prompt", ui_txt)
        self.assertIn("lab-left-col", ui_txt)
        self.assertIn("btn-lab-a-close", ui_txt)
        self.assertIn("[A] 원상태", ui_txt)
        self.assertLess(ui_txt.find("lab-prompt-box"), ui_txt.find("lab-mission"))
        css_txt = (DOCS_DIR / "deck.css").read_text(encoding="utf-8")
        self.assertIn("html.home-html { overflow-x: hidden; overflow-y: auto;", css_txt)
        self.assertIn("position: absolute;\n  inset: 0;\n  width: 100%;\n  height: 100%;", css_txt)
        s5_txt = (DOCS_DIR / "slides/s5_part4_b.js").read_text(encoding="utf-8")
        self.assertLess(s5_txt.find("id: 'ch11-lab'"), s5_txt.find("id: 'ch11-eval-methods'"))
        self.assertLess(s5_txt.find("id: 'ch11-eval-methods'"), s5_txt.find("id: 'ch12-theory'"))
        self.assertLess(s5_txt.find("id: 'closing'"), s5_txt.find("id: 'capstone-agent-first'"))
        self.assertIn("height:250px;display:flex;flex-direction:column", s5_txt)


    def test_cartoon_workshop_deck_without_time_concepts(self) -> None:
        self.assertTrue((DOCS_DIR / "workshop.html").is_file())
        home = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("workshop.html", home)
        workshop_html = (DOCS_DIR / "workshop.html").read_text(encoding="utf-8")
        self.assertIn("slides_workshop/00_manifest.js", workshop_html)

        w_dir = DOCS_DIR / "slides_workshop"
        w_all = "\n".join(f.read_text(encoding="utf-8") for f in sorted(w_dir.glob("*.js")))
        for forbidden in ("5시간", "300분", "75분", "65분", "45분", "40분", "5-HOUR"):
            self.assertNotIn(forbidden, w_all, f"워크숍 덱에 시간 문구 잔존: {forbidden}")
        self.assertFalse((DOCS_DIR / "assets/cartoons/cap_05_in.jpg").exists(), "제5장 카툰 이미지가 삭제되어야 합니다.")
        self.assertNotIn("ch05", w_all, "워크숍 덱에 ch05 문구 잔존")
        for img in (
            "cap_00_in.jpg",
            "cap_01_in.jpg",
            "cap_07_in.jpg",
            "cap_09_in.jpg",
            "cap_11_in.jpg",
            "cap_12_out.jpg",
        ):
            self.assertTrue((DOCS_DIR / "assets/cartoons" / img).is_file(), f"카툰 이미지 누락: {img}")
            self.assertIn(f"assets/cartoons/{img}", w_all, f"카툰 이미지 미배치: {img}")


    def test_lab_slides_have_three_or_more_user_prompt_examples(self) -> None:
        ui_txt = (DOCS_DIR / "ui.js").read_text(encoding="utf-8")
        self.assertIn("사용자 입력 프롬프트 예시", ui_txt)
        self.assertNotIn("컨테이너 실행 명령", ui_txt)
        for deck_sub in ("slides", "slides_workshop"):
            slides_text = "\n".join(
                (DOCS_DIR / f"{deck_sub}/{name}").read_text(encoding="utf-8")
                for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
            )
            blocks = re.findall(r"buildLabSlide\(el,\s*A,\s*\{(.*?)\n\s*\}\);", slides_text, re.DOTALL)
            self.assertEqual(len(blocks), 13, f"{deck_sub} 실습 슬라이드 개수 불일치")
            for block in blocks:
                pe_m = re.search(r"promptExamples:\s*\[(.*?)\]", block, re.DOTALL)
                self.assertIsNotNone(pe_m, f"{deck_sub} promptExamples 누락: {block[:80]}")
                assert pe_m is not None
                items = [line.strip() for line in pe_m.group(1).splitlines() if line.strip().startswith("'")]
                self.assertGreaterEqual(len(items), 3, f"{deck_sub} 사용자 입력 프롬프트 예시 3개 미만: {items}")

    def test_prompt_copy_strips_brackets_and_preserves_clean_prompt(self) -> None:
        ui_txt = (DOCS_DIR / "ui.js").read_text(encoding="utf-8")
        self.assertIn("function stripPromptBrackets(text)", ui_txt)
        self.assertIn("copyTextToClipboard(stripPromptBrackets(promptText), copyBtn)", ui_txt)
        for deck_sub in ("slides", "slides_workshop"):
            slides_text = "\n".join(
                (DOCS_DIR / f"{deck_sub}/{name}").read_text(encoding="utf-8")
                for name in ("s0_opening.js", "s1_part1.js", "s2_part2.js", "s3_part3.js", "s4_part4_a.js", "s5_part4_b.js")
            )
            prompts = re.findall(r"userPrompt:\s*`([^`]+)`", slides_text)
            self.assertEqual(len(prompts), 13, f"{deck_sub} userPrompt 개수 불일치")
            for p in prompts:
                cleaned = re.sub(r"\[[^\]]*\]\s*", "", p).strip()
                self.assertNotIn("[", cleaned, f"{deck_sub} 프롬프트에 대괄호 잔존: {cleaned}")
                self.assertNotIn("]", cleaned, f"{deck_sub} 프롬프트에 대괄호 잔존: {cleaned}")
                self.assertGreater(len(cleaned), 20, f"{deck_sub} 프롬프트 본문 누락 또는 너무 짧음: {cleaned}")

if __name__ == "__main__":
    unittest.main()
