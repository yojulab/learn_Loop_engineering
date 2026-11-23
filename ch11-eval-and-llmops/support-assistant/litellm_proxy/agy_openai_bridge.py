"""agy_openai_bridge.py — Antigravity CLI (`agy -p`) OpenAI 호환 HTTP 브리지.

OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY 없이도 LiteLLM Proxy가
`agy -p` (OAuth 로그인된 Antigravity CLI)를 통해 LLM 응답을 생성할 수 있도록
표준 `/v1/chat/completions` 및 `/v1/models` 엔드포인트를 제공합니다.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable


RunnerFn = Callable[[str, str | None, int], tuple[int, str, str]]


def default_agy_runner(prompt: str, model: str | None = None, timeout: int = 120) -> tuple[int, str, str]:
    agy_bin = shutil.which("agy")
    if not agy_bin:
        return 127, "", "agy CLI binary not found on PATH"

    cmd = [agy_bin, "-p", prompt, "--output-format", "text", "--disable-slash-commands"]
    if model and model not in {"agy-cli", "openai/agy-cli", "default"}:
        cmd.extend(["--model", model])

    proc = subprocess.run(
        cmd,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def format_messages_as_prompt(messages: list[dict[str, Any]]) -> str:
    if len(messages) == 1 and str(messages[0].get("role", "user")) == "user":
        return str(messages[0].get("content", ""))
    lines = []
    for msg in messages:
        role = str(msg.get("role", "user")).strip()
        content = str(msg.get("content", "")).strip()
        if content:
            lines.append(f"[{role}] {content}")
    return "\n".join(lines)


def invoke_agy_completion(
    messages: list[dict[str, Any]],
    model: str = "agy-cli",
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> tuple[int, dict[str, Any]]:
    prompt = format_messages_as_prompt(messages)
    run_fn = runner or default_agy_runner
    cli_model = None if model in {"agy-cli", "openai/agy-cli"} else model

    rc, stdout, stderr = run_fn(prompt, cli_model, timeout)
    if rc == 0 and stdout:
        prompt_tokens = max(1, len(prompt.split()))
        completion_tokens = max(1, len(stdout.split()))
        return 200, {
            "id": f"chatcmpl-agy-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": stdout},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }

    detail = stderr or stdout or f"exit={rc}"
    if allow_fallback:
        fallback_text = (
            f"[agy-offline-fallback] 요청을 접수했습니다. "
            f"다음 단계 안내: 입력하신 문의({prompt[:80]})를 담당 부서에서 확인 후 처리하겠습니다."
        )
        prompt_tokens = max(1, len(prompt.split()))
        completion_tokens = max(1, len(fallback_text.split()))
        return 200, {
            "id": f"chatcmpl-agy-fb-{uuid.uuid4().hex[:10]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": fallback_text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
            "bridge_fallback_reason": detail,
        }

    status = 401 if "Authentication required" in detail else 502
    return status, {
        "error": {
            "message": f"agy CLI execution failed (exit={rc}): {detail}",
            "type": "agy_cli_error",
            "code": "authentication_required" if status == 401 else "cli_error",
        }
    }


def make_handler(
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> type[BaseHTTPRequestHandler]:
    class AgyBridgeHandler(BaseHTTPRequestHandler):
        def _send_json(self, code: int, payload: dict[str, Any]) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/health", "/health/liveliness"}:
                self._send_json(200, {"status": "ok", "cli": "agy", "available": bool(shutil.which("agy"))})
                return
            if self.path in {"/v1/models", "/models"}:
                self._send_json(
                    200,
                    {
                        "object": "list",
                        "data": [{"id": "agy-cli", "object": "model", "owned_by": "antigravity"}],
                    },
                )
                return
            self._send_json(404, {"error": {"message": f"Not found: {self.path}"}})

        def do_POST(self) -> None:  # noqa: N802
            if self.path not in {"/v1/chat/completions", "/chat/completions"}:
                self._send_json(404, {"error": {"message": f"Unsupported path: {self.path}"}})
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                body = json.loads(raw_body.decode("utf-8"))
            except json.JSONDecodeError as exc:
                self._send_json(400, {"error": {"message": f"Invalid JSON: {exc}"}})
                return

            messages = body.get("messages") or []
            model = str(body.get("model") or "agy-cli")
            code, resp = invoke_agy_completion(
                messages=messages,
                model=model,
                runner=runner,
                timeout=timeout,
                allow_fallback=allow_fallback,
            )
            self._send_json(code, resp)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

    return AgyBridgeHandler


def start_bridge_server(
    host: str = "0.0.0.0",
    port: int = 4010,
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> ThreadingHTTPServer:
    handler = make_handler(runner=runner, timeout=timeout, allow_fallback=allow_fallback)
    return ThreadingHTTPServer((host, port), handler)


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenAI-compatible HTTP bridge for Antigravity CLI (agy -p)")
    parser.add_argument("--host", default=os.getenv("AGY_BRIDGE_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AGY_BRIDGE_PORT", "4010")))
    parser.add_argument("--timeout", type=int, default=int(os.getenv("AGY_BRIDGE_TIMEOUT", "120")))
    parser.add_argument(
        "--allow-fallback",
        action="store_true",
        default=os.getenv("AGY_BRIDGE_ALLOW_FALLBACK", "0") == "1",
        help="agy 미인증/오류 시 offline-fallback 응답 반환",
    )
    args = parser.parse_args()

    server = start_bridge_server(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        allow_fallback=args.allow_fallback,
    )
    print(f"[agy_openai_bridge] listening on http://{args.host}:{args.port}/v1 (allow_fallback={args.allow_fallback})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
