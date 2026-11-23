"""
hooks/platform_hook_bridge.py — Claude / ChatGPT(Codex) / Gemini 훅 페이로드 정규화 브릿지.

- Claude (`PreToolUse` / `PostToolUse`): {"tool_name": "Bash", "tool_input": {"command": "..."}}
- ChatGPT (`tool_call` / `tool_result`): {"function": {"name": "shell", "arguments": {"command": "..."}}}
- Gemini (`BeforeTool` / `AfterTool`): {"tool": "run_shell_command", "args": {"command": "..."}}
모든 플랫폼 페이로드를 단일 포맷으로 정규화해 block_dangerous_bash / audit_logger를 실행합니다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HOOKS_DIR = Path(__file__).resolve().parent
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

import audit_logger
import block_dangerous_bash


def normalize_hook_payload(platform: str, payload: dict[str, Any]) -> dict[str, Any]:
    plat = platform.lower()
    if plat == "chatgpt":
        fn = payload.get("function", {})
        args = fn.get("arguments", payload.get("arguments", {}))
        if isinstance(args, str):
            args = json.loads(args)
        return {"tool_name": fn.get("name", payload.get("tool_name", "shell")), "tool_input": args}
    if plat == "gemini":
        return {
            "tool_name": payload.get("tool", payload.get("tool_name", "run_shell_command")),
            "tool_input": payload.get("args", payload.get("tool_input", {})),
        }
    return {
        "tool_name": payload.get("tool_name", "Bash"),
        "tool_input": payload.get("tool_input", {}),
    }


def dispatch_hook(platform: str, phase: str, payload: dict[str, Any], log_path: Path | None = None) -> tuple[int, dict[str, Any]]:
    norm = normalize_hook_payload(platform, payload)
    if phase == "pre":
        cmd = str(norm["tool_input"].get("command", ""))
        allowed, reason = block_dangerous_bash.evaluate_command(cmd)
        if not allowed:
            return 2, {"decision": "block", "platform": platform, "reason": reason}
        return 0, {"decision": "allow", "platform": platform}
    entry = audit_logger.record_audit_event(norm, log_path=log_path)
    return 0, {"status": "logged", "platform": platform, "entry": entry}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Multi-platform Hook Bridge (claude/chatgpt/gemini)")
    parser.add_argument("--platform", choices=["claude", "chatgpt", "gemini"], default="claude")
    parser.add_argument("--phase", choices=["pre", "post"], default="pre")
    args = parser.parse_args(argv)
    raw = sys.stdin.read().strip() or "{}"
    payload = json.loads(raw)
    code, out = dispatch_hook(args.platform, args.phase, payload)
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
