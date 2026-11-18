from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from models import PromptRecord


class LangfuseOpsClient:
    """Langfuse 연동 및 오프라인 로컬 JSONL 폴백 클라이언트."""

    def __init__(self, store_dir: str | Path) -> None:
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.offline_mode = not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
        self.prompts_file = self.store_dir / "prompts.json"
        self.traces_file = self.store_dir / "traces.jsonl"
        self._prompts: list[dict[str, Any]] = (
            json.loads(self.prompts_file.read_text(encoding="utf-8")) if self.prompts_file.exists() else []
        )

    def _save_prompts(self) -> None:
        self.prompts_file.write_text(json.dumps(self._prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def create_prompt(self, name: str, prompt: str, labels: list[str] | None = None) -> PromptRecord:
        labels = labels or []
        existing = [p for p in self._prompts if p["name"] == name]
        version = max((int(p["version"]) for p in existing), default=0) + 1
        for p in existing:
            p["labels"] = [lb for lb in p["labels"] if lb not in labels]
        rec = {"name": name, "version": version, "template": prompt, "labels": list(labels)}
        self._prompts.append(rec)
        self._save_prompts()
        return PromptRecord(**rec)

    def get_prompt(self, name: str, label: str = "production") -> PromptRecord:
        for p in reversed(self._prompts):
            if p["name"] == name and label in p["labels"]:
                return PromptRecord(**p)
        raise KeyError(f"Prompt '{name}' with label '{label}' not found")

    def promote_label(self, name: str, version: int, label: str = "production") -> PromptRecord:
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

    def log_trace(self, trace_id: str, prompt_name: str, prompt_version: int, output: str, score: float, latency_ms: int = 120) -> None:
        entry = {
            "trace_id": trace_id,
            "prompt_name": prompt_name,
            "prompt_version": prompt_version,
            "output": output,
            "score": score,
            "latency_ms": latency_ms,
        }
        with self.traces_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
