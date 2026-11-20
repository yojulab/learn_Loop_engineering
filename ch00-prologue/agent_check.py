"""
ch00-prologue/agent_check.py — 로컬 AI 및 Agent Platform 동작 확인 도구.

- 3대 플랫폼(Claude · ChatGPT · Gemini) 및 오프라인 폴백 동작 상태를 점검합니다.
- API 키 유무와 무관하게 간략 문장에 대한 응답(대변)을 생성하여 로컬 환경을 검증합니다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# 저장소 루트를 sys.path에 추가하여 platforms 패키지 로드 보장
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from platforms.base import (
        SUPPORTED_PLATFORMS,
        get_adapter,
        resolve_platform,
        run_with_any_platform,
    )
except ImportError:
    # platforms 모듈 로드 실패 시 자체 인라인 폴백
    SUPPORTED_PLATFORMS = ("claude", "chatgpt", "gemini", "offline")

    def resolve_platform(platform: str = "auto") -> str:
        req = (platform or "auto").strip().lower()
        if req != "auto" and req in SUPPORTED_PLATFORMS:
            return req
        env = os.getenv("AGENT_PLATFORM", "").strip().lower()
        return env if env in SUPPORTED_PLATFORMS else "offline"

    def run_with_any_platform(prompt: str, platform: str = "auto", **kwargs: Any):
        class DummyResponse:
            def __init__(self, plat: str, text: str):
                self.platform = plat
                self.mode = "offline-fallback"
                self.model = "deterministic-offline"
                self.text = text
                self.metadata = {}
        plat = resolve_platform(platform)
        return DummyResponse(plat, f"[{plat}-offline-fallback] {prompt[:100]}")

    def get_adapter(platform: str = "auto"):
        return None


DEFAULT_PROMPT = "2026 모던 AI 에이전트 스택 환경 점검: 런타임 및 플랫폼 동작을 확인합니다."


def inspect_agent_environment(platform: str = "auto") -> dict[str, Any]:
    """현재 플랫폼 환경 설정 상태(API 키, CLI 가용 여부, 플랫폼 해석 결과)를 진단한다."""
    resolved = resolve_platform(platform)

    adapter = None
    cli_available = False
    api_configured = False
    model_name = "auto"

    try:
        adapter = get_adapter(resolved)
        if adapter:
            cli_available = adapter.is_cli_available()
            api_configured = adapter.is_api_configured()
            model_name = adapter.config.model
    except Exception:
        pass

    return {
        "requested_platform": platform,
        "resolved_platform": resolved,
        "model": model_name,
        "is_cli_available": cli_available,
        "is_api_configured": api_configured,
        "env_agent_platform": os.getenv("AGENT_PLATFORM", ""),
    }


def check_local_ai(prompt: str = DEFAULT_PROMPT, platform: str = "auto") -> dict[str, Any]:
    """로컬 AI 플랫폼 동작을 확인하고 간략 문장에 대한 응답(대변)을 생성한다."""
    env_info = inspect_agent_environment(platform)
    response = run_with_any_platform(prompt=prompt, platform=platform)

    return {
        "status": "OK",
        "environment": env_info,
        "prompt": prompt,
        "response": {
            "platform": response.platform,
            "mode": response.mode,
            "model": response.model,
            "reply_text": response.text,
            "metadata": response.metadata,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="프롤로그: 로컬 AI 동작 및 Agent Platform 확인 도구")
    parser.add_argument(
        "-p",
        "--platform",
        default="auto",
        choices=["auto", "claude", "chatgpt", "gemini", "offline"],
        help="대상 에이전트 플랫폼 (기본값: auto 또는 AGENT_PLATFORM 환경변수)",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="테스트 문장 (기본값: 환경 점검 기본 문구)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 형식으로 출력",
    )
    args = parser.parse_args(argv)

    result = check_local_ai(prompt=args.prompt, platform=args.platform)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        env = result["environment"]
        resp = result["response"]
        print("=== 로컬 AI 및 Agent Platform 동작 확인 ===")
        print(f"• 요청 플랫폼: {env['requested_platform']} (해석: {env['resolved_platform']})")
        print(f"• 모델/동작 모드: {resp['model']} ({resp['mode']})")
        print(f"• CLI 사용 가능: {env['is_cli_available']} | API 키 설정: {env['is_api_configured']}")
        print(f"• 입력 문장: {result['prompt']}")
        print(f"• 응답(대변): {resp['reply_text']}")
        print("===========================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
