"""제1장: 에이전트 3단계 루프(컨텍스트 수집 -> 작업 수행 -> 검증) 및 비대화형 파이프 데모."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

CLI_PATH = Path(__file__).resolve().parent / "quote_cli.py"


def run_agent_loop(task: str, tag: str = "engineering") -> dict[str, Any]:
    """컨텍스트 수집 -> 비대화형 CLI 실행 -> 결과 검증 3단계 루프를 시연한다."""
    # 1. 컨텍스트 수집
    context = {
        "task": task,
        "cli_path": str(CLI_PATH),
        "target_tag": tag,
        "mode": "non-interactive-pipe",
    }

    # 2. 작업 수행 (표준출력 파이프 캡처)
    proc = subprocess.run(
        [sys.executable, str(CLI_PATH), "--tag", tag, "--json"],
        capture_output=True,
        text=True,
        check=False,
    )

    # 3. 결과 검증
    parsed_items: list[dict[str, Any]] = []
    verified = False
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            if isinstance(data, list) and len(data) > 0:
                parsed_items = data
                verified = True
        except json.JSONDecodeError:
            verified = False

    return {
        "step_1_context": context,
        "step_2_execution": {
            "returncode": proc.returncode,
            "stdout_bytes": len(proc.stdout.encode("utf-8")),
        },
        "step_3_verification": {
            "verified": verified,
            "matched_count": len(parsed_items),
            "sample": parsed_items[0] if parsed_items else None,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="에이전틱 코딩 3단계 루프 & 파이프 데모")
    parser.add_argument("--task", default="engineering 태그 명언 조회", help="실행할 작업 설명")
    parser.add_argument("--tag", default="engineering", help="조회할 태그")
    parser.add_argument("--stdin", action="store_true", help="표준입력에서 작업 문자열 읽기")
    parser.add_argument("--json", action="store_true", help="JSON 결과 출력")
    args = parser.parse_args(argv)

    task_text = args.task
    if args.stdin and not sys.stdin.isatty():
        piped = sys.stdin.read().strip()
        if piped:
            task_text = piped

    result = run_agent_loop(task=task_text, tag=args.tag)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        v = result["step_3_verification"]
        print(f"[1. Gather] task={result['step_1_context']['task']} tag={args.tag}")
        print(f"[2. Act] returncode={result['step_2_execution']['returncode']}")
        print(f"[3. Verify] verified={v['verified']} matched_count={v['matched_count']}")
    return 0 if result["step_3_verification"]["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
