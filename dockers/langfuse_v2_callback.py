"""LiteLLM CustomLogger for Langfuse v2 (/api/public/ingestion).

최신 LiteLLM 이미지의 기본 `langfuse` 콜백은 Langfuse v3+ OTLP(/api/public/otel/v1/traces)만
지원하므로, Langfuse v2 서버와 호환되도록 `/api/public/ingestion` 배치 API를 직접 호출합니다.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import urllib.error
import urllib.request
import uuid
from typing import Any

from litellm.integrations.custom_logger import CustomLogger


class LangfuseV2Logger(CustomLogger):
    def _post_ingestion(
        self,
        *,
        kwargs: dict[str, Any],
        response_obj: Any,
        start_time: Any,
        end_time: Any,
        level: str = "DEFAULT",
        status_message: str | None = None,
    ) -> None:
        host = os.getenv("LANGFUSE_HOST", "").strip().rstrip("/")
        pk = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()
        sk = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
        if not (host and pk and sk):
            return

        now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
        trace_id = str(kwargs.get("litellm_call_id") or uuid.uuid4())
        gen_id = str(uuid.uuid4())
        model = str(kwargs.get("model") or "unknown")
        messages = kwargs.get("messages") or []

        output_text: Any = None
        usage: dict[str, int] = {}
        if response_obj is not None:
            try:
                if hasattr(response_obj, "model_dump"):
                    resp_dict = response_obj.model_dump()
                elif isinstance(response_obj, dict):
                    resp_dict = response_obj
                else:
                    resp_dict = {}
                choices = resp_dict.get("choices") or []
                if choices:
                    output_text = choices[0].get("message", {}).get("content")
                raw_usage = resp_dict.get("usage") or {}
                if raw_usage:
                    usage = {
                        "input": int(raw_usage.get("prompt_tokens") or 0),
                        "output": int(raw_usage.get("completion_tokens") or 0),
                        "total": int(raw_usage.get("total_tokens") or 0),
                    }
            except Exception:
                output_text = str(response_obj)
        elif status_message:
            output_text = {"error": status_message}

        events: list[dict[str, Any]] = [
            {
                "id": f"evt-trace-{trace_id}",
                "type": "trace-create",
                "timestamp": now,
                "body": {
                    "id": trace_id,
                    "name": f"litellm:{model}",
                    "timestamp": now,
                    "input": messages,
                    "output": output_text,
                    "tags": ["litellm-proxy", level.lower()],
                    "metadata": {"model": model, "status": status_message or "ok"},
                },
            },
            {
                "id": f"evt-gen-{gen_id}",
                "type": "generation-create",
                "timestamp": now,
                "body": {
                    "id": gen_id,
                    "traceId": trace_id,
                    "name": model,
                    "model": model,
                    "startTime": now,
                    "endTime": now,
                    "input": messages,
                    "output": output_text,
                    "level": level,
                    "statusMessage": status_message,
                    **({"usage": usage} if usage else {}),
                },
            },
        ]

        auth = base64.b64encode(f"{pk}:{sk}".encode("utf-8")).decode("ascii")
        req = urllib.request.Request(
            f"{host}/api/public/ingestion",
            data=json.dumps({"batch": events}, ensure_ascii=False, default=str).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
        except Exception as exc:
            print(f"[langfuse_v2_callback] WARN: ingestion failed: {exc}", flush=True)

    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._post_ingestion(kwargs=kwargs, response_obj=response_obj, start_time=start_time, end_time=end_time)

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._post_ingestion(kwargs=kwargs, response_obj=response_obj, start_time=start_time, end_time=end_time)

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        exc = kwargs.get("exception")
        self._post_ingestion(
            kwargs=kwargs,
            response_obj=None,
            start_time=start_time,
            end_time=end_time,
            level="ERROR",
            status_message=str(exc) if exc else "failure",
        )

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        exc = kwargs.get("exception")
        self._post_ingestion(
            kwargs=kwargs,
            response_obj=None,
            start_time=start_time,
            end_time=end_time,
            level="ERROR",
            status_message=str(exc) if exc else "failure",
        )


proxy_handler_instance = LangfuseV2Logger()
