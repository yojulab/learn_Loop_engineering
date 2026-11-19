"""Any-Platform (Claude, ChatGPT/Codex, Gemini/Antigravity) 공용 실행 어댑터 패키지."""

from platforms.base import (
    SUPPORTED_PLATFORMS,
    BasePlatformAdapter,
    PlatformConfig,
    PlatformResponse,
    get_adapter,
    resolve_platform,
    run_with_any_platform,
)

__all__ = [
    "SUPPORTED_PLATFORMS",
    "BasePlatformAdapter",
    "PlatformConfig",
    "PlatformResponse",
    "get_adapter",
    "resolve_platform",
    "run_with_any_platform",
]
