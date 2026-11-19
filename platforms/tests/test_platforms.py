from __future__ import annotations

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from platforms.base import resolve_platform, run_with_any_platform


class _MockMultiPlatformHTTP:
    def __init__(self) -> None:
        class Handler(BaseHTTPRequestHandler):
            def _send(self, payload: dict) -> None:
                raw = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_POST(self) -> None:
                if self.path == "/v1/messages":
                    self._send({"content": [{"type": "text", "text": "claude-ok"}]})
                    return
                if self.path == "/chat/completions":
                    self._send({"choices": [{"message": {"content": "chatgpt-ok"}}]})
                    return
                if ":generateContent" in self.path:
                    self._send({"candidates": [{"content": {"parts": [{"text": "gemini-ok"}]}}]})
                    return
                self.send_response(404)
                self.end_headers()

            def log_message(self, format: str, *args: object) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> "_MockMultiPlatformHTTP":
        self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.server.shutdown()
        self.server.server_close()


class TestPlatforms(unittest.TestCase):
    def test_auto_resolve_and_offline_fallback_all_platforms(self) -> None:
        clean_env = {
            k: v
            for k, v in os.environ.items()
            if k not in {"AGENT_PLATFORM", "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"}
        }
        with patch.dict(os.environ, clean_env, clear=True):
            with patch("shutil.which", return_value=None):
                self.assertEqual(resolve_platform("auto"), "offline")
                for plat in ("claude", "chatgpt", "gemini", "offline"):
                    resp = run_with_any_platform("hello world", platform=plat)
                    self.assertEqual(resp.platform, plat)
                    self.assertEqual(resp.mode, "offline-fallback")

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "k1"}, clear=True):
            self.assertEqual(resolve_platform("auto"), "claude")
        with patch.dict(os.environ, {"OPENAI_API_KEY": "k2"}, clear=True):
            self.assertEqual(resolve_platform("auto"), "chatgpt")
        with patch.dict(os.environ, {"GEMINI_API_KEY": "k3"}, clear=True):
            self.assertEqual(resolve_platform("auto"), "gemini")

    def test_http_api_invocation_all_three_platforms(self) -> None:
        with _MockMultiPlatformHTTP() as srv:
            with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "k1", "ANTHROPIC_BASE_URL": srv.url}, clear=False):
                r = run_with_any_platform("ping", platform="claude")
                self.assertEqual((r.platform, r.mode, r.text), ("claude", "http-api", "claude-ok"))

            with patch.dict(os.environ, {"OPENAI_API_KEY": "k2", "OPENAI_BASE_URL": srv.url}, clear=False):
                r = run_with_any_platform("ping", platform="chatgpt")
                self.assertEqual((r.platform, r.mode, r.text), ("chatgpt", "http-api", "chatgpt-ok"))

            with patch.dict(os.environ, {"GEMINI_API_KEY": "k3", "GEMINI_BASE_URL": srv.url}, clear=False):
                r = run_with_any_platform("ping", platform="gemini")
                self.assertEqual((r.platform, r.mode, r.text), ("gemini", "http-api", "gemini-ok"))


if __name__ == "__main__":
    unittest.main()
