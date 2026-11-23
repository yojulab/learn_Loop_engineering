"""cli_openai_bridge.py — Gemini(`agy -p`) / Claude(`claude -p`) OpenAI 호환 HTTP 브리지 공통 코어.

OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY 없이도 LiteLLM Proxy가
로그인된 CLI(`agy -p` 또는 `claude -p`)를 통해 응답을 생성할 수 있도록
표준 `/v1/chat/completions`, `/v1/models`, `/health` 엔드포인트를 제공합니다.
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

CLI_SPECS: dict[str, dict[str, Any]] = {
    "gemini": {
        "binary": "agy",
        "model_id": "gemini-cli",
        "owned_by": "antigravity-gemini",
        "extra_args": ["--output-format", "text", "--disable-slash-commands"],
    },
    "claude": {
        "binary": "claude",
        "model_id": "claude-cli",
        "owned_by": "anthropic-claude-code",
        "extra_args": ["--output-format", "text"],
    },
}


def make_cli_runner(provider: str) -> RunnerFn:
    spec = CLI_SPECS[provider]
    binary = str(spec["binary"])
    extra_args = list(spec["extra_args"])

    def _run(prompt: str, model: str | None = None, timeout: int = 120) -> tuple[int, str, str]:
        bin_path = shutil.which(binary)
        if not bin_path:
            return 127, "", f"{binary} CLI binary not found on PATH"

        cmd = [bin_path, "-p", prompt, *extra_args]
        if model and model not in {spec["model_id"], f"openai/{spec['model_id']}", "default"}:
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

    return _run


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


def invoke_cli_completion(
    provider: str,
    messages: list[dict[str, Any]],
    model: str | None = None,
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> tuple[int, dict[str, Any]]:
    spec = CLI_SPECS[provider]
    default_model_id = str(spec["model_id"])
    resolved_model = model or default_model_id
    prompt = format_messages_as_prompt(messages)
    run_fn = runner or make_cli_runner(provider)
    cli_model = None if resolved_model in {default_model_id, f"openai/{default_model_id}"} else resolved_model

    rc, stdout, stderr = run_fn(prompt, cli_model, timeout)
    if rc == 0 and stdout:
        prompt_tokens = max(1, len(prompt.split()))
        completion_tokens = max(1, len(stdout.split()))
        return 200, {
            "id": f"chatcmpl-{provider}-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": resolved_model,
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
            f"[{provider}-cli-fallback] 결제 오류 확인을 도와드리겠습니다. "
            f"다음 단계 안내: 영수증 번호와 결제 시각을 회신해 주시면 영업일 기준 3일 이내 환불 처리됩니다."
        )
        prompt_tokens = max(1, len(prompt.split()))
        completion_tokens = max(1, len(fallback_text.split()))
        return 200, {
            "id": f"chatcmpl-{provider}-fb-{uuid.uuid4().hex[:10]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": resolved_model,
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

    low = detail.lower()
    is_auth = "authentication required" in low or "login" in low or "not logged in" in low or "unauthorized" in low
    status = 401 if is_auth else 502
    return status, {
        "error": {
            "message": f"{spec['binary']} CLI execution failed (exit={rc}): {detail}",
            "type": f"{provider}_cli_error",
            "code": "authentication_required" if status == 401 else "cli_error",
        }
    }


def make_handler(
    provider: str,
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> type[BaseHTTPRequestHandler]:
    spec = CLI_SPECS[provider]
    binary = str(spec["binary"])
    model_id = str(spec["model_id"])
    owned_by = str(spec["owned_by"])

    class CliBridgeHandler(BaseHTTPRequestHandler):
        def _send_json(self, code: int, payload: dict[str, Any]) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/health", "/health/liveliness"}:
                self._send_json(200, {"status": "ok", "provider": provider, "cli": binary, "available": bool(shutil.which(binary))})
                return
            if self.path in {"/v1/models", "/models"}:
                self._send_json(
                    200,
                    {
                        "object": "list",
                        "data": [{"id": model_id, "object": "model", "owned_by": owned_by}],
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
            model = str(body.get("model") or model_id)
            code, resp = invoke_cli_completion(
                provider=provider,
                messages=messages,
                model=model,
                runner=runner,
                timeout=timeout,
                allow_fallback=allow_fallback,
            )
            self._send_json(code, resp)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

    return CliBridgeHandler


def start_bridge_server(
    provider: str = "gemini",
    host: str = "0.0.0.0",
    port: int = 4010,
    *,
    runner: RunnerFn | None = None,
    timeout: int = 120,
    allow_fallback: bool = False,
) -> ThreadingHTTPServer:
    handler = make_handler(provider, runner=runner, timeout=timeout, allow_fallback=allow_fallback)
    return ThreadingHTTPServer((host, port), handler)


def run_bridge_cli(default_provider: str, default_port: int) -> None:
    parser = argparse.ArgumentParser(description=f"OpenAI-compatible HTTP bridge for {default_provider} CLI")
    parser.add_argument("--provider", choices=sorted(CLI_SPECS), default=default_provider)
    parser.add_argument("--host", default=os.getenv("CLI_BRIDGE_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=default_port)
    parser.add_argument("--timeout", type=int, default=int(os.getenv("CLI_BRIDGE_TIMEOUT", "120")))
    parser.add_argument(
        "--allow-fallback",
        action="store_true",
        default=os.getenv("CLI_BRIDGE_ALLOW_FALLBACK", "0") == "1",
        help="CLI 미인증/오류 시 offline-fallback 응답 반환",
    )
    args = parser.parse_args()

    server = start_bridge_server(
        provider=args.provider,
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        allow_fallback=args.allow_fallback,
    )
    print(
        f"[{args.provider}_openai_bridge] listening on http://{args.host}:{args.port}/v1 (allow_fallback={args.allow_fallback})",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
