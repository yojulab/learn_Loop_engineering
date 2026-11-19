"""
platforms/adapter_chatgpt.py — OpenAI ChatGPT / Codex CLI 플랫폼 어댑터.

동작 우선순위:
1) `OPENAI_API_KEY`가 설정된 경우 OpenAI Chat Completions API (`/chat/completions`) 호출
   - `OPENAI_BASE_URL`을 LiteLLM 프록시(`http://localhost:4000/v1`)로 두면 무코드 관측이 즉시 적용됩니다.
2) `codex` CLI가 설치된 경우 `codex exec <prompt>` 호출
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


class ChatGPTPlatformAdapter(BasePlatformAdapter):
    config = PlatformConfig(
        platform="chatgpt",
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        cli_binary="codex",
        api_key_env="OPENAI_API_KEY",
        base_url_env="OPENAI_BASE_URL",
    )

    def invoke(self, prompt: str, **kwargs: Any) -> PlatformResponse:
        api_key = os.getenv(self.config.api_key_env, "")
        base_url = (kwargs.get("base_url") or os.getenv(self.config.base_url_env, "https://api.openai.com/v1")).rstrip("/")
        model = str(kwargs.get("model") or self.config.model)
        force_offline = bool(kwargs.get("force_offline", False))
        strict = bool(kwargs.get("strict", False))
        fallback_reason = "OPENAI_API_KEY 및 codex CLI 미설정"

        if api_key and not force_offline:
            try:
                payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
                req = urllib.request.Request(
                    f"{base_url}/chat/completions",
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    method="POST",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                text = choices[0]["message"]["content"] if choices else ""
                return PlatformResponse(platform="chatgpt", mode="http-api", model=model, text=str(text), metadata=data)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if strict:
                    raise
                fallback_reason = f"http-api fallback ({exc})"

        if self.is_cli_available() and not force_offline:
            proc = subprocess.run([self.config.cli_binary, "exec", prompt], capture_output=True, text=True, check=False)
            if proc.returncode == 0:
                return PlatformResponse(platform="chatgpt", mode="cli", model=model, text=proc.stdout.strip())
            fallback_reason = f"cli fallback (exit={proc.returncode})"

        summary = " ".join(prompt.strip().split())[:120]
        return PlatformResponse(
            platform="chatgpt",
            mode="offline-fallback",
            model=model,
            text=f"[chatgpt-offline-fallback] {summary}",
            metadata={"note": fallback_reason},
        )
