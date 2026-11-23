"""LiteLLM CustomLogger for Langfuse v2 (/api/public/ingestion).

Langfuse v2 공식 Ingestion API 스펙에 맞춰 다음 항목을 모두 전송합니다:
- `trace-create`: `userId`, `sessionId`, `tags`, `metadata`
- `generation-create`: 실제 `startTime`/`endTime` (Latency 계산), `promptName`/`promptVersion`,
  `usage` (`input`, `output`, `total`, `unit="TOKENS"`), 결정론적 `observationId` (`uuid5`)
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import urllib.request
import uuid
from typing import Any

from litellm.integrations.custom_logger import CustomLogger


def _to_iso_utc(value: Any, fallback: str) -> str:
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    if isinstance(value, dt.datetime):
        d = value if value.tzinfo is not None else value.replace(tzinfo=dt.timezone.utc)
        return d.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return fallback


def _normalize_model(raw_model: Any, meta: dict[str, Any]) -> str:
    alias = meta.get("model_group") or meta.get("model_alias")
    if alias:
        return str(alias)
    m = str(raw_model or "unknown")
    if m.startswith("openai/") and m.endswith("-cli"):
        return m.split("/", 1)[1]
    return m


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

        now_iso = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        start_iso = _to_iso_utc(start_time, now_iso)
        end_iso = _to_iso_utc(end_time, now_iso)

        litellm_params = kwargs.get("litellm_params") or {}
        meta_a = litellm_params.get("metadata") if isinstance(litellm_params, dict) else None
        meta_b = kwargs.get("metadata")
        meta: dict[str, Any] = {}
        if isinstance(meta_b, dict):
            meta.update(meta_b)
        if isinstance(meta_a, dict):
            meta.update(meta_a)

        trace_id = str(meta.get("trace_id") or kwargs.get("litellm_call_id") or uuid.uuid4())
        gen_id = str(meta.get("observation_id") or uuid.uuid5(uuid.NAMESPACE_DNS, f"gen-{trace_id}"))
        model = _normalize_model(kwargs.get("model"), meta)
        messages = kwargs.get("messages") or []
        user_id = meta.get("user_id")
        session_id = meta.get("session_id")
        prompt_name = meta.get("prompt_name")
        prompt_version = meta.get("prompt_version")

        output_text: Any = None
        usage: dict[str, Any] = {}
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
                    in_t = int(raw_usage.get("prompt_tokens") or 0)
                    out_t = int(raw_usage.get("completion_tokens") or 0)
                    tot_t = int(raw_usage.get("total_tokens") or (in_t + out_t))
                    usage = {"input": in_t, "output": out_t, "total": tot_t, "unit": "TOKENS"}
            except Exception:
                output_text = str(response_obj)
        elif status_message:
            output_text = {"error": status_message}

        tags = ["litellm-proxy", model, "ok" if level == "DEFAULT" else level.lower()]
        trace_body: dict[str, Any] = {
            "id": trace_id,
            "name": str(meta.get("trace_name") or f"litellm:{model}"),
            "timestamp": start_iso,
            "input": messages,
            "output": output_text,
            "tags": tags,
            "metadata": {"model": model, "status": status_message or "ok"},
        }
        if user_id:
            trace_body["userId"] = str(user_id)
        if session_id:
            trace_body["sessionId"] = str(session_id)

        gen_body: dict[str, Any] = {
            "id": gen_id,
            "traceId": trace_id,
            "name": model,
            "model": model,
            "startTime": start_iso,
            "endTime": end_iso,
            "input": messages,
            "output": output_text,
            "level": level,
            "statusMessage": status_message,
        }
        if usage:
            gen_body["usage"] = usage
        if prompt_name:
            gen_body["promptName"] = str(prompt_name)
        if prompt_version is not None:
            gen_body["promptVersion"] = int(prompt_version)

        events: list[dict[str, Any]] = [
            {"id": f"evt-trace-{trace_id}", "type": "trace-create", "timestamp": start_iso, "body": trace_body},
            {"id": f"evt-gen-{gen_id}", "type": "generation-create", "timestamp": end_iso, "body": gen_body},
        ]

        auth = base64.b64encode(f"{pk}:{sk}".encode("utf-8")).decode("ascii")
        req = urllib.request.Request(
            f"{host}/api/public/ingestion",
            data=json.dumps({"batch": events}, ensure_ascii=False, default=str).encode("utf-8"),
            method="POST",
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
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
