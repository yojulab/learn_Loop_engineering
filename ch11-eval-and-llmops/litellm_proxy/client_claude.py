"""
client_claude.py — Anthropic Claude 모델을 LiteLLM 프록시로 무코드 관측하는 클라이언트.

- 앱 코드는 표준 OpenAI 호환 `/chat/completions` 포맷과 `model="claude-sonnet"`만 지정합니다.
- 실제 실행 시 `OPENAI_BASE_URL=http://localhost:4000/v1`로 LiteLLM 프록시를 가리키면 Langfuse에 자동 기록됩니다.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

PROXY_DIR = Path(__file__).resolve().parent
if str(PROXY_DIR) not in sys.path:
    sys.path.insert(0, str(PROXY_DIR))


def call_claude_via_proxy(prompt: str, base_url: str | None = None, api_key: str | None = None) -> dict[str, Any]:
    resolved_base = (base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:4000/v1")).rstrip("/")
    resolved_key = api_key or os.getenv("LITELLM_MASTER_KEY", "sk-litellm-local")
    body = json.dumps({"model": "claude-sonnet", "messages": [{"role": "user", "content": prompt}]}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{resolved_base}/chat/completions",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {resolved_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))
