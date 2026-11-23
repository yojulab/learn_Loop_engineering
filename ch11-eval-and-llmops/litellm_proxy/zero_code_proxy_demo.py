from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from langfuse_ops import LangfuseOpsClient


def existing_app_call_llm(user_prompt: str, base_url: str | None = None, api_key: str | None = None) -> dict[str, Any]:
    """기존 앱 코드: Langfuse SDK 의존성이 전혀 없는 표준 OpenAI 호환 HTTP 호출."""
    resolved_base = (base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:4000/v1")).rstrip("/")
    resolved_key = api_key or os.getenv("OPENAI_API_KEY", "sk-litellm-local")
    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": user_prompt}],
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{resolved_base}/chat/completions",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {resolved_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def start_mock_litellm_proxy(ops: LangfuseOpsClient) -> tuple[ThreadingHTTPServer, str]:
    """실제 LiteLLM 프록시의 `success_callback: ['langfuse']` 동작을 오프라인으로 재현하는 Mock 프록시."""
    counter = {"n": 0}

    class ProxyHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            req_data = json.loads(self.rfile.read(length).decode("utf-8"))
            messages = req_data.get("messages", [])
            user_text = messages[-1].get("content", "") if messages else ""
            counter["n"] += 1
            trace_id = f"litellm-trace-{counter['n']:03d}"
            answer = f"[티켓 T-201] 제품(ProPlan) 문의 확인: {user_text[:40]} -> 다음 단계: 주문번호 회신 부탁드립니다."
            # 무코드 관측 콜백: 프록시가 자동으로 Langfuse Trace에 input/output 적재
            ops.log_trace(
                trace_id=trace_id,
                prompt_name="litellm-auto-trace",
                prompt_version=0,
                output=answer,
                score=0.9,
                input_payload={"messages": messages, "model": req_data.get("model", "gpt-4o-mini")},
            )
            resp_body = json.dumps({
                "id": trace_id,
                "choices": [{"index": 0, "message": {"role": "assistant", "content": answer}}],
            }, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), ProxyHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{port}/v1"


def run_zero_code_demo(store_dir: str | Path | None = None) -> dict[str, Any]:
    tmp_ctx = tempfile.TemporaryDirectory() if store_dir is None else None
    target_dir = Path(tmp_ctx.name) if tmp_ctx else Path(store_dir)
    try:
        ops = LangfuseOpsClient(target_dir)
        server, proxy_url = start_mock_litellm_proxy(ops)
        try:
            resp = existing_app_call_llm(
                "[티켓 T-201] 제품(ProPlan) 환불 문의: 결제 후 2일 이내 환불 요청합니다.",
                base_url=proxy_url,
            )
            traces = ops.list_traces()
            matched = [t for t in traces if t.get("id") == "litellm-trace-001"]
            latest_id = matched[0]["id"] if matched else (traces[0]["id"] if ops.remote_enabled and traces else (traces[-1]["id"] if traces else None))
            return {
                "proxy_url": proxy_url,
                "assistant_reply": resp["choices"][0]["message"]["content"],
                "captured_trace_count": len(traces),
                "latest_trace_id": latest_id,
            }
        finally:
            server.shutdown()
            server.server_close()
    finally:
        if tmp_ctx:
            tmp_ctx.cleanup()


if __name__ == "__main__":
    print(json.dumps(run_zero_code_demo(), ensure_ascii=False, indent=2))
