from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from langfuse_ops import LangfuseOpsClient
from models import SupportTicket
from prompting import compile_prompt


def fetch_and_compile_prompt(
    ops: LangfuseOpsClient,
    prompt_name: str,
    ticket: SupportTicket,
    label: str = "production",
) -> dict[str, Any]:
    """Langfuse(또는 오프라인 폴백)에서 확인된 프롬프트를 가져와 앱 티켓 변수로 컴파일합니다."""
    prompt = ops.fetch_prompt_from_langfuse(name=prompt_name, label=label)
    compiled = compile_prompt(prompt, ticket)
    return {
        "prompt_name": prompt.name,
        "version": prompt.version,
        "labels": prompt.labels,
        "source": "langfuse-remote" if ops.remote_enabled else "offline-fallback",
        "compiled_text": compiled,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Langfuse 프롬프트 조회 및 앱 변수 컴파일 CLI")
    parser.add_argument("--name", default="support-answer")
    parser.add_argument("--label", default="production")
    parser.add_argument("--store-dir", default="")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    tmp_ctx = tempfile.TemporaryDirectory() if not args.store_dir else None
    store_path = Path(tmp_ctx.name) if tmp_ctx else Path(args.store_dir)
    try:
        ops = LangfuseOpsClient(store_path, host="" if args.demo else None)
        if args.demo and ops.offline_mode:
            ops.create_prompt(
                name=args.name,
                prompt="[티켓 {{ticket_id}}] 제품({{product}}) '{{subject}}' 안내: {{message}}\n다음 단계: 주문번호를 회신해 주세요.",
                labels=[args.label],
            )
        sample_ticket = SupportTicket(
            ticket_id="T-301",
            product="TeamPlan",
            subject="결제 영수증",
            message="법인카드 영수증 재발급 요청합니다.",
        )
        res = fetch_and_compile_prompt(ops, args.name, sample_ticket, label=args.label)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else res["compiled_text"])
        return 0
    finally:
        if tmp_ctx:
            tmp_ctx.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
