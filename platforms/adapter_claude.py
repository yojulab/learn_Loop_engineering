"""
platforms/adapter_claude.py — Anthropic Claude / Claude Code 플랫폼 어댑터.

동작 우선순위:
1) `ANTHROPIC_API_KEY`가 설정된 경우 Anthropic Messages API (`/v1/messages`) 호출
2) `claude` CLI가 설치된 경우 `claude -p <prompt>` 호출
3) 키 미설정·인증 오류·오프라인 환경에서도 `offline-fallback`으로 무중단 응답 반환
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from typing import Any

from platforms.base import BasePlatformAdapter, PlatformConfig, PlatformResponse


class ClaudePlatformAdapter(BasePlatformAdapter):
    config = PlatformConfig(
        platform="claude",
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"),
        cli_binary="claude",
        api_key_env="ANTHROPIC_API_KEY",
        base_url_env="ANTHROPIC_BASE_URL",
    )

    def invoke(self, prompt: str, **kwargs: Any) -> PlatformResponse:
        api_key = os.getenv(self.config.api_key_env, "")
        base_url = (kwargs.get("base_url") or os.getenv(self.config.base_url_env, "https://api.anthropic.com")).rstrip("/")
        model = str(kwargs.get("model") or self.config.model)
        force_offline = bool(kwargs.get("force_offline", False))
        strict = bool(kwargs.get("strict", False))
        fallback_reason = "ANTHROPIC_API_KEY 및 claude CLI 미설정"

        if api_key and not force_offline:
            try:
                payload = {
                    "model": model,
                    "max_tokens": int(kwargs.get("max_tokens", 512)),
                    "messages": [{"role": "user", "content": prompt}],
                }
                req = urllib.request.Request(
                    f"{base_url}/v1/messages",
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    method="POST",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                blocks = data.get("content", [])
                text = blocks[0].get("text", "") if blocks else data.get("text", "")
                return PlatformResponse(platform="claude", mode="http-api", model=model, text=str(text), metadata=data)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if strict:
                    raise
                fallback_reason = f"http-api fallback ({exc})"

        if self.is_cli_available() and not force_offline:
            proc = subprocess.run([self.config.cli_binary, "-p", prompt], capture_output=True, text=True, check=False)
            if proc.returncode == 0:
                return PlatformResponse(platform="claude", mode="cli", model=model, text=proc.stdout.strip())
            fallback_reason = f"cli fallback (exit={proc.returncode})"

        summary = " ".join(prompt.strip().split())[:120]
        return PlatformResponse(
            platform="claude",
            mode="offline-fallback",
            model=model,
            text=f"[claude-offline-fallback] {summary}",
            metadata={"note": fallback_reason},
        )
