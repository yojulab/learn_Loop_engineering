"""
platforms/adapter_gemini.py — Google Gemini / Antigravity CLI 플랫폼 어댑터.

동작 우선순위:
1) `GEMINI_API_KEY` 또는 `GOOGLE_API_KEY` 설정 시 Gemini `generateContent` REST API 호출
2) `gemini` CLI가 설치된 경우 `gemini -p <prompt>` 호출
3) 키 미설정·인증 오류·오프라인 환경에서도 `offline-fallback`으로 무중단 응답 반환
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from platforms.base import BasePlatformAdapter, PlatformConfig, PlatformResponse


class GeminiPlatformAdapter(BasePlatformAdapter):
    config = PlatformConfig(
        platform="gemini",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        cli_binary="gemini",
        api_key_env="GEMINI_API_KEY",
        base_url_env="GEMINI_BASE_URL",
    )

    def is_api_configured(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

    def invoke(self, prompt: str, **kwargs: Any) -> PlatformResponse:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        base_url = (
            kwargs.get("base_url")
            or os.getenv(self.config.base_url_env, "https://generativelanguage.googleapis.com")
        ).rstrip("/")
        model = str(kwargs.get("model") or self.config.model)
        force_offline = bool(kwargs.get("force_offline", False))
        strict = bool(kwargs.get("strict", False))
        fallback_reason = "GEMINI_API_KEY 및 gemini CLI 미설정"

        if api_key and not force_offline:
            try:
                q_key = urllib.parse.quote(api_key, safe="")
                url = f"{base_url}/v1beta/models/{model}:generateContent?key={q_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    method="POST",
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                cands = data.get("candidates", [])
                text = ""
                if cands:
                    parts = cands[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                return PlatformResponse(platform="gemini", mode="http-api", model=model, text=str(text), metadata=data)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if strict:
                    raise
                fallback_reason = f"http-api fallback ({exc})"

        if self.is_cli_available() and not force_offline:
            cli_env = {**os.environ, "GEMINI_CLI_TRUST_WORKSPACE": "true"}
            proc = subprocess.run([self.config.cli_binary, "-p", prompt], capture_output=True, text=True, env=cli_env, check=False)
            if proc.returncode == 0:
                return PlatformResponse(platform="gemini", mode="cli", model=model, text=proc.stdout.strip())
            fallback_reason = f"cli fallback (exit={proc.returncode})"

        summary = " ".join(prompt.strip().split())[:120]
        return PlatformResponse(
            platform="gemini",
            mode="offline-fallback",
            model=model,
            text=f"[gemini-offline-fallback] {summary}",
            metadata={"note": fallback_reason},
        )
