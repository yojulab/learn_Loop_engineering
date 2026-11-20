"""
ch00-prologue/tests/test_agent_check.py — agent_check.py 단위 테스트.
"""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

PROLOGUE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PROLOGUE_DIR.parent
if str(PROLOGUE_DIR) not in sys.path:
    sys.path.insert(0, str(PROLOGUE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import agent_check  # noqa: E402


class TestAgentCheck(unittest.TestCase):
    def test_inspect_environment_offline(self) -> None:
        info = agent_check.inspect_agent_environment("offline")
        self.assertEqual(info["resolved_platform"], "offline")
        self.assertIn("is_cli_available", info)
        self.assertIn("is_api_configured", info)

    def test_inspect_environment_gemini(self) -> None:
        info = agent_check.inspect_agent_environment("gemini")
        self.assertEqual(info["resolved_platform"], "gemini")

    def test_check_local_ai_offline_response(self) -> None:
        res = agent_check.check_local_ai(prompt="간략 테스트 문장입니다.", platform="offline")
        self.assertEqual(res["status"], "OK")
        self.assertEqual(res["response"]["platform"], "offline")
        self.assertIn("간략 테스트 문장입니다.", res["response"]["reply_text"])

    def test_check_local_ai_gemini_response(self) -> None:
        res = agent_check.check_local_ai(prompt="테스트 질의", platform="gemini")
        self.assertEqual(res["status"], "OK")
        self.assertEqual(res["response"]["platform"], "gemini")
        # 키 미설정 시에도 offline fallback으로 무중단 응답 반환
        self.assertIn("테스트 질의", res["response"]["reply_text"])

    def test_main_cli_text_and_json(self) -> None:
        # 1) 일반 텍스트 모드
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = agent_check.main(["--platform", "offline", "--prompt", "테스트"])
        self.assertEqual(code, 0)
        self.assertIn("로컬 AI 및 Agent Platform 동작 확인", buf.getvalue())

        # 2) JSON 모드
        buf_json = io.StringIO()
        with redirect_stdout(buf_json):
            code = agent_check.main(["--platform", "gemini", "--prompt", "테스트 JSON", "--json"])
        self.assertEqual(code, 0)
        data = json.loads(buf_json.getvalue())
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["response"]["platform"], "gemini")


if __name__ == "__main__":
    unittest.main()
