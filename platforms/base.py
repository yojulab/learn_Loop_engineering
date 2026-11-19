"""
platforms/base.py — Claude · ChatGPT(OpenAI/Codex) · Gemini(Antigravity) 공용 추상화 계층.

- 우선순위: 명시 인자(platform) -> 환경변수 AGENT_PLATFORM -> 설치된 API Key / CLI 자동 탐지 -> offline 폴백
- 어느 플랫폼에서 실행하더라도 동일한 PlatformResponse 계약으로 응답을 반환합니다.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from typing import Any

SUPPORTED_PLATFORMS: tuple[str, ...] = ("claude", "chatgpt", "gemini", "offline")


@dataclass(frozen=True)
class PlatformConfig:
    platform: str
    model: str
    cli_binary: str
    api_key_env: str
    base_url_env: str = ""


@dataclass
class PlatformResponse:
    platform: str
    mode: str  # "cli" | "http-api" | "offline-fallback"
    model: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BasePlatformAdapter:
    """3대 플랫폼 어댑터가 구현해야 하는 공통 실행 계약."""

    config: PlatformConfig

    def is_cli_available(self) -> bool:
        return bool(self.config.cli_binary and shutil.which(self.config.cli_binary))

    def is_api_configured(self) -> bool:
        return bool(self.config.api_key_env and os.getenv(self.config.api_key_env))

    def invoke(self, prompt: str, **kwargs: Any) -> PlatformResponse:
        raise NotImplementedError


class OfflineFallbackAdapter(BasePlatformAdapter):
    """API 키나 CLI가 없는 컨테이너/CI 환경에서도 결정론적으로 동작하는 폴백 어댑터."""

    config = PlatformConfig(
        platform="offline",
        model="deterministic-offline",
        cli_binary="",
        api_key_env="",
    )

    def invoke(self, prompt: str, **kwargs: Any) -> PlatformResponse:
        summary = " ".join(prompt.strip().split())[:120]
        return PlatformResponse(
            platform="offline",
            mode="offline-fallback",
            model=self.config.model,
            text=f"[offline-fallback] {summary}",
            metadata={"requested_platform": kwargs.get("requested_platform", "offline")},
        )


def resolve_platform(platform: str = "auto") -> str:
    """현재 실행 환경에서 사용 가능한 플랫폼을 결정한다 (claude | chatgpt | gemini | offline)."""
    req = (platform or "auto").strip().lower()
    if req != "auto":
        if req not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform '{platform}'. Allowed: {SUPPORTED_PLATFORMS + ('auto',)}")
        return req

    env_plat = os.getenv("AGENT_PLATFORM", "").strip().lower()
    if env_plat in SUPPORTED_PLATFORMS:
        return env_plat

    # 1) API 키 자동 감지
    if os.getenv("ANTHROPIC_API_KEY"):
        return "claude"
    if os.getenv("OPENAI_API_KEY"):
        return "chatgpt"
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return "gemini"

    # 2) 로컬 CLI 바이너리 자동 감지
    if shutil.which("claude"):
        return "claude"
    if shutil.which("codex"):
        return "chatgpt"
    if shutil.which("gemini"):
        return "gemini"

    # 3) 무중단 오프라인 폴백
    return "offline"


def get_adapter(platform: str = "auto") -> BasePlatformAdapter:
    """해석된 플랫폼 이름에 대응하는 어댑터 인스턴스를 반환한다."""
    resolved = resolve_platform(platform)
    if resolved == "claude":
        from platforms.adapter_claude import ClaudePlatformAdapter
        return ClaudePlatformAdapter()
    if resolved == "chatgpt":
        from platforms.adapter_chatgpt import ChatGPTPlatformAdapter
        return ChatGPTPlatformAdapter()
    if resolved == "gemini":
        from platforms.adapter_gemini import GeminiPlatformAdapter
        return GeminiPlatformAdapter()
    return OfflineFallbackAdapter()


def run_with_any_platform(prompt: str, platform: str = "auto", **kwargs: Any) -> PlatformResponse:
    """단일 진입점: 어떤 플랫폼(claude/chatgpt/gemini/auto/offline)에서도 안전하게 실행한다."""
    adapter = get_adapter(platform)
    return adapter.invoke(prompt, requested_platform=platform, **kwargs)
