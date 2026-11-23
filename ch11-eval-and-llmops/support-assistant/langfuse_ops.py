from __future__ import annotations

import base64
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from models import PromptRecord


class LangfuseOpsClient:
    """Langfuse Public API 연동(HTTP Basic Auth) 및 오프라인 로컬 JSONL 폴백 클라이언트."""

    def __init__(
        self,
        store_dir: str | Path,
        host: str | None = None,
        public_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.host = (host if host is not None else os.getenv("LANGFUSE_HOST", "")).rstrip("/")
        self.public_key = public_key if public_key is not None else os.getenv("LANGFUSE_PUBLIC_KEY", "")
        self.secret_key = secret_key if secret_key is not None else os.getenv("LANGFUSE_SECRET_KEY", "")
        self.remote_enabled = bool(self.host and self.public_key and self.secret_key)
        self.offline_mode = not self.remote_enabled

        self.prompts_file = self.store_dir / "prompts.json"
        self.traces_file = self.store_dir / "traces.jsonl"
        self._prompts: list[dict[str, Any]] = (
            json.loads(self.prompts_file.read_text(encoding="utf-8")) if self.prompts_file.exists() else []
        )

    def _auth_header(self) -> str:
        token = base64.b64encode(f"{self.public_key}:{self.secret_key}".encode("utf-8")).decode("ascii")
        return f"Basic {token}"

    def _http_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.host}{path}"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": self._auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {}

    def _save_prompts(self) -> None:
        self.prompts_file.write_text(json.dumps(self._prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def create_prompt(
        self,
        name: str,
        prompt: str,
        labels: list[str] | None = None,
        prompt_type: str = "text",
    ) -> PromptRecord:
        labels = list(labels or [])
        if self.remote_enabled:
            res = self._http_json(
                "POST",
                "/api/public/v2/prompts",
                {"name": name, "prompt": prompt, "labels": labels, "type": prompt_type},
            )
            return PromptRecord(
                name=str(res.get("name", name)),
                version=int(res.get("version", 1)),
                template=str(res.get("prompt", prompt)),
                labels=list(res.get("labels", labels)),
            )

        existing = [p for p in self._prompts if p["name"] == name]
        version = max((int(p["version"]) for p in existing), default=0) + 1
        for p in existing:
            p["labels"] = [lb for lb in p["labels"] if lb not in labels]
        rec = {"name": name, "version": version, "template": prompt, "labels": labels}
        self._prompts.append(rec)
        self._save_prompts()
        return PromptRecord(**rec)

    def get_prompt(self, name: str, label: str = "production", version: int | None = None) -> PromptRecord:
        if self.remote_enabled:
            q_name = urllib.parse.quote(name, safe="")
            params = f"version={version}" if version is not None else f"label={urllib.parse.quote(label, safe='')}"
            res = self._http_json("GET", f"/api/public/v2/prompts/{q_name}?{params}")
            return PromptRecord(
                name=str(res.get("name", name)),
                version=int(res.get("version", version or 1)),
                template=str(res.get("prompt", "")),
                labels=list(res.get("labels", [label])),
            )

        for p in reversed(self._prompts):
            if p["name"] != name:
                continue
            if version is not None and int(p["version"]) == version:
                return PromptRecord(**p)
            if version is None and label in p["labels"]:
                return PromptRecord(**p)
        raise KeyError(f"Prompt '{name}' (label={label}, version={version}) not found")

    def fetch_prompt_from_langfuse(self, name: str, label: str = "production") -> PromptRecord:
        """Langfuse 서버 또는 오프라인 저장소에서 확인된 프롬프트를 가져오는 명시적 헬퍼."""
        return self.get_prompt(name=name, label=label)

    def promote_label(self, name: str, version: int, label: str = "production") -> PromptRecord:
        if self.remote_enabled:
            cur = self.get_prompt(name=name, version=version)
            merged_labels = sorted(set(cur.labels) | {label})
            return self.create_prompt(name=name, prompt=cur.template, labels=merged_labels)

        target = None
        for p in self._prompts:
            if p["name"] == name:
                p["labels"] = [lb for lb in p["labels"] if lb != label]
                if int(p["version"]) == version:
                    p["labels"].append(label)
                    target = p
        if target is None:
            raise KeyError(f"Prompt '{name}' v{version} not found")
        self._save_prompts()
        return PromptRecord(**target)

    def log_trace(
        self,
        trace_id: str,
        prompt_name: str,
        prompt_version: int,
        output: str,
        score: float,
        latency_ms: int = 120,
        input_payload: Any = None,
    ) -> None:
        entry = {
            "id": trace_id,
            "trace_id": trace_id,
            "prompt_name": prompt_name,
            "prompt_version": prompt_version,
            "input": input_payload,
            "output": output,
            "score": score,
            "latency_ms": latency_ms,
        }
        if self.remote_enabled:
            ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
            res = self._http_json(
                "POST",
                "/api/public/ingestion",
                {
                    "batch": [
                        {
                            "id": f"evt-{trace_id}",
                            "type": "trace-create",
                            "timestamp": ts,
                            "body": {
                                "id": trace_id,
                                "name": prompt_name,
                                "timestamp": ts,
                                "input": input_payload,
                                "output": output,
                                "metadata": {"prompt_version": prompt_version, "score": score, "latency_ms": latency_ms},
                            },
                        }
                    ]
                },
            )
            if res.get("errors"):
                raise RuntimeError(f"Langfuse ingestion failed: {res['errors']}")
            return

        with self.traces_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_score(
        self,
        trace_id: str,
        name: str,
        value: float,
        data_type: str = "NUMERIC",
        comment: str = "",
        observation_id: str | None = None,
    ) -> None:
        if self.remote_enabled:
            payload: dict[str, Any] = {
                "traceId": trace_id,
                "name": name,
                "value": float(value),
                "dataType": data_type,
            }
            if observation_id:
                payload["observationId"] = observation_id
            if comment:
                payload["comment"] = comment
            self._http_json("POST", "/api/public/scores", payload)
            return

        scores_file = self.store_dir / "scores.jsonl"
        entry = {
            "trace_id": trace_id,
            "observation_id": observation_id,
            "name": name,
            "value": float(value),
            "data_type": data_type,
            "comment": comment,
        }
        with scores_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def ensure_custom_model(
        self,
        model_name: str,
        match_pattern: str,
        input_price: float = 0.0000001,
        output_price: float = 0.0000004,
        unit: str = "TOKENS",
    ) -> dict[str, Any]:
        """Langfuse /api/public/models 에 커스텀 모델 가격/패턴을 멱등 등록합니다."""
        if not self.remote_enabled:
            return {"modelName": model_name, "mode": "offline-fallback"}
        try:
            existing = self._http_json("GET", "/api/public/models?limit=100").get("data", [])
            for item in existing:
                if item.get("modelName") == model_name:
                    return item
            return self._http_json(
                "POST",
                "/api/public/models",
                {
                    "modelName": model_name,
                    "matchPattern": match_pattern,
                    "unit": unit,
                    "inputPrice": input_price,
                    "outputPrice": output_price,
                },
            )
        except Exception as exc:
            return {"modelName": model_name, "error": str(exc)}

    def list_traces(self, limit: int = 20) -> list[dict[str, Any]]:
        if self.remote_enabled:
            res = self._http_json("GET", f"/api/public/traces?limit={limit}")
            return list(res.get("data", []))
        if not self.traces_file.exists():
            return []
        lines = [ln for ln in self.traces_file.read_text(encoding="utf-8").splitlines() if ln.strip()]
        return [json.loads(ln) for ln in lines[-limit:]]

    def get_trace(self, trace_id: str) -> dict[str, Any]:
        if self.remote_enabled:
            return self._http_json("GET", f"/api/public/traces/{urllib.parse.quote(trace_id, safe='')}")
        for tr in reversed(self.list_traces(limit=500)):
            if tr.get("id") == trace_id or tr.get("trace_id") == trace_id:
                return tr
        raise KeyError(f"Trace '{trace_id}' not found")
