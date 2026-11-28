from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from langfuse_ops import LangfuseOpsClient

V1_TEMPLATE = (
    "[티켓 {ticket_id}] 제품({product}) 문의 '{subject}' 확인했습니다.\n"
    "요청 내용: {message}\n"
    "안내: 정책을 확인해 주세요."
)

V2_TEMPLATE = (
    "[티켓 {ticket_id}] 제품({product}) 문의 '{subject}'에 대한 안내입니다.\n"
    "핵심 확인: {message} 관련 환불/계정 정책을 점검했습니다.\n"
    "다음 단계: 주문 번호와 함께 고객센터로 회신해 주시면 즉시 처리해 드리겠습니다."
)


def seed_default_prompts(ops: LangfuseOpsClient) -> None:
    ops.create_prompt(name="support-answer", prompt=V1_TEMPLATE, labels=["production"])
    ops.create_prompt(name="support-answer", prompt=V2_TEMPLATE, labels=["candidate"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ch10 기본 프롬프트(support-answer) Langfuse 시더")
    parser.add_argument("--store-dir", default="", help="오프라인 폴백 저장 경로")
    parser.add_argument("--if-missing", action="store_true", help="이미 production/candidate 라벨이 있으면 건너뜀")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 결과 출력")
    args = parser.parse_args(argv)

    tmp_ctx = tempfile.TemporaryDirectory() if not args.store_dir else None
    store_path = Path(tmp_ctx.name) if tmp_ctx else Path(args.store_dir)
    try:
        ops = LangfuseOpsClient(store_path)
        skipped = False
        if args.if_missing:
            try:
                ops.get_prompt("support-answer", label="production")
                ops.get_prompt("support-answer", label="candidate")
                skipped = True
            except Exception:
                skipped = False

        if not skipped:
            seed_default_prompts(ops)

        p_prod = ops.get_prompt("support-answer", label="production")
        p_cand = ops.get_prompt("support-answer", label="candidate")
        out = {
            "mode": "offline-fallback" if ops.offline_mode else "langfuse-remote",
            "host": ops.host or None,
            "skipped": skipped,
            "production_version": p_prod.version,
            "candidate_version": p_cand.version,
        }
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(
                f"[seed_prompts] mode={out['mode']} | skipped={skipped} | "
                f"production=v{p_prod.version} | candidate=v{p_cand.version}"
            )
        return 0
    finally:
        if tmp_ctx:
            tmp_ctx.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
