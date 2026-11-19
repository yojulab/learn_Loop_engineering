from __future__ import annotations

import base64
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
PROXY_DIR = APP_DIR / "litellm_proxy"
if str(PROXY_DIR) not in sys.path:
    sys.path.insert(0, str(PROXY_DIR))

from fetch_prompt import fetch_and_compile_prompt
from langfuse_ops import LangfuseOpsClient
from models import PromptRecord, SupportTicket
from prompting import compile_prompt
from regression_compare import compare_prompt_versions
from seed_prompts import seed_default_prompts
from trace_to_prompt import promote_trace_as_prompt
from zero_code_proxy_demo import existing_app_call_llm, start_mock_litellm_proxy


class _MockLangfuseServer:
    """HTTP Basic Auth 기반 Langfuse v2 Prompts/Traces/Ingestion Mock 서버."""

    def __init__(self, public_key: str, secret_key: str) -> None:
        self.expected_auth = "Basic " + base64.b64encode(f"{public_key}:{secret_key}".encode()).decode("ascii")
        self.prompts: list[dict] = []
        self.traces: dict[str, dict] = {
            "trace-live-001": {
                "id": "trace-live-001",
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": "[티켓 T-900] 제품(ProPlan) '환불': 결제 취소 요청합니다.",
                        }
                    ]
                },
                "output": "다음 단계: 주문 번호를 남겨주세요.",
            }
        }
        parent = self

        class Handler(BaseHTTPRequestHandler):
            def _auth_ok(self) -> bool:
                return self.headers.get("Authorization") == parent.expected_auth

            def _send(self, code: int, body: dict) -> None:
                raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_GET(self) -> None:
                if not self._auth_ok():
                    self._send(401, {"error": "unauthorized"})
                    return
                parsed = urlparse(self.path)
                if parsed.path.startswith("/api/public/v2/prompts/"):
                    name = unquote(parsed.path.split("/api/public/v2/prompts/", 1)[1])
                    qs = parse_qs(parsed.query)
                    label = qs.get("label", [None])[0]
                    ver = qs.get("version", [None])[0]
                    for p in reversed(parent.prompts):
                        if p["name"] != name:
                            continue
                        if ver and str(p["version"]) == str(ver):
                            self._send(200, p)
                            return
                        if label and label in p["labels"]:
                            self._send(200, p)
                            return
                    self._send(404, {"error": "prompt not found"})
                    return
                if parsed.path.startswith("/api/public/traces/"):
                    tid = unquote(parsed.path.split("/api/public/traces/", 1)[1])
                    if tid in parent.traces:
                        self._send(200, parent.traces[tid])
                        return
                    self._send(404, {"error": "trace not found"})
                    return
                if parsed.path == "/api/public/traces":
                    self._send(200, {"data": list(parent.traces.values())})
                    return
                self._send(404, {"error": "not found"})

            def do_POST(self) -> None:
                if not self._auth_ok():
                    self._send(401, {"error": "unauthorized"})
                    return
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if self.path == "/api/public/v2/prompts":
                    name = payload["name"]
                    existing = [p for p in parent.prompts if p["name"] == name]
                    ver = max((p["version"] for p in existing), default=0) + 1
                    labels = list(payload.get("labels", []))
                    for p in existing:
                        p["labels"] = [lb for lb in p["labels"] if lb not in labels]
                    rec = {"name": name, "version": ver, "prompt": payload["prompt"], "labels": labels}
                    parent.prompts.append(rec)
                    self._send(200, rec)
                    return
                if self.path == "/api/public/ingestion":
                    for evt in payload.get("batch", []):
                        body = evt.get("body", {})
                        if body.get("id"):
                            parent.traces[body["id"]] = body
                    self._send(200, {"successes": len(payload.get("batch", []))})
                    return
                self._send(404, {"error": "not found"})

            def log_message(self, format: str, *args: object) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> "_MockLangfuseServer":
        self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.server.shutdown()
        self.server.server_close()


class TestSupportAssistant(unittest.TestCase):
    def test_offline_jsonl_seed_compile_and_compare(self) -> None:
        raw = json.loads((APP_DIR / "sample_dataset.json").read_text(encoding="utf-8"))
        dataset = [SupportTicket(**item) for item in raw]
        with tempfile.TemporaryDirectory() as tmp:
            ops = LangfuseOpsClient(Path(tmp), host="", public_key="", secret_key="")
            self.assertTrue(ops.offline_mode)
            seed_default_prompts(ops)
            p1 = ops.get_prompt("support-answer", label="production")
            compiled = compile_prompt(p1, dataset[0])
            self.assertIn("T-101", compiled)

            cmp_res = compare_prompt_versions(dataset, "production", "candidate", ops)
            self.assertGreater(cmp_res["candidate"]["avg_score"], cmp_res["production"]["avg_score"])
            self.assertTrue((Path(tmp) / "traces.jsonl").is_file())

            ops.promote_label("support-answer", version=2, label="production")
            promoted = ops.get_prompt("support-answer", label="production")
            self.assertEqual(promoted.version, 2)

    def test_mustache_and_python_format_compile(self) -> None:
        ticket = SupportTicket(ticket_id="T-777", product="Enterprise", subject="SSO", message="SAML 설정 문의")
        mustache_prompt = PromptRecord(name="m", version=1, template="[{{ ticket_id }}] {{product}} - {{subject}}: {{message}}")
        self.assertEqual(compile_prompt(mustache_prompt, ticket), "[T-777] Enterprise - SSO: SAML 설정 문의")

    def test_zero_code_litellm_proxy_save_as_prompt_and_remote_fetch(self) -> None:
        pk, sk = "pk-lf-test", "sk-lf-test"
        with _MockLangfuseServer(pk, sk) as lf_srv, tempfile.TemporaryDirectory() as tmp:
            ops = LangfuseOpsClient(Path(tmp), host=lf_srv.url, public_key=pk, secret_key=sk)
            self.assertFalse(ops.offline_mode)

            # 1) 무코드 LiteLLM 프록시로 기존 앱 코드 수정 없이 Trace 자동 적재
            proxy_srv, proxy_url = start_mock_litellm_proxy(ops)
            try:
                existing_app_call_llm("[티켓 T-201] 제품(ProPlan) '환불': 결제 후 2일 내 환불 되나요?", base_url=proxy_url)
            finally:
                proxy_srv.shutdown()
                proxy_srv.server_close()

            traces = ops.list_traces()
            self.assertTrue(any(t["id"] == "litellm-trace-001" for t in traces))

            # 2) 기존 Trace Input에서 프롬프트 추출 등록 (Save as Prompt)
            promoted = promote_trace_as_prompt(
                ops,
                trace_id="litellm-trace-001",
                prompt_name="support-from-trace",
                labels=["production"],
                variable_mapping={
                    "T-201": "ticket_id",
                    "ProPlan": "product",
                    "환불": "subject",
                    "결제 후 2일 내 환불 되나요?": "message",
                },
            )
            self.assertIn("{{ticket_id}}", promoted.template)

            # 3) Langfuse 서버에서 확인된 production 프롬프트를 가져와 앱 티켓에 적용
            new_ticket = SupportTicket(ticket_id="T-888", product="TeamPlan", subject="청구서", message="PDF 발송 요청")
            fetched = fetch_and_compile_prompt(ops, "support-from-trace", new_ticket, label="production")
            self.assertEqual(fetched["source"], "langfuse-remote")
            self.assertIn("T-888", fetched["compiled_text"])
            self.assertIn("TeamPlan", fetched["compiled_text"])


if __name__ == "__main__":
    unittest.main()
