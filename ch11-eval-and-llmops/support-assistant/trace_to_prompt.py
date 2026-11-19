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
from models import PromptRecord


def _flatten_input_payload(input_payload: Any) -> str:
    if isinstance(input_payload, str):
        return input_payload
    if isinstance(input_payload, dict):
        msgs = input_payload.get("messages")
        if isinstance(msgs, list):
            return "\n".join(str(m.get("content", "")) for m in msgs if isinstance(m, dict) and m.get("content"))
        return json.dumps(input_payload, ensure_ascii=False)
    if isinstance(input_payload, list):
        return "\n".join(str(m.get("content", m)) if isinstance(m, dict) else str(m) for m in input_payload)
    return str(input_payload or "")


def extract_prompt_template_from_trace(
    trace_entry: dict[str, Any],
    variable_mapping: dict[str, str] | None = None,
) -> str:
    """기존 Trace의 Input 페이로드에서 텍스트를 추출하고 샘플 값을 `{{var}}` 변수로 승격합니다."""
    raw_text = _flatten_input_payload(trace_entry.get("input"))
    if not raw_text.strip():
        raise ValueError("Trace에 승격할 input 페이로드가 없습니다.")
    template = raw_text
    if variable_mapping:
        for literal, var_name in sorted(variable_mapping.items(), key=lambda kv: len(kv[0]), reverse=True):
            placeholder = f"{{{{{var_name}}}}}"
            template = template.replace(literal, placeholder)
    return template


def promote_trace_as_prompt(
    ops: LangfuseOpsClient,
    trace_id: str,
    prompt_name: str,
    labels: list[str] | None = None,
    variable_mapping: dict[str, str] | None = None,
) -> PromptRecord:
    """Langfuse Trace(또는 로컬 traces.jsonl)를 조회해 버전 관리되는 Prompt 자산으로 등록합니다."""
    trace_entry = ops.get_trace(trace_id)
    template = extract_prompt_template_from_trace(trace_entry, variable_mapping=variable_mapping)
    return ops.create_prompt(name=prompt_name, prompt=template, labels=labels or ["production"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Trace Input -> Langfuse Save as Prompt 승격 CLI")
    parser.add_argument("--trace-id", default="")
    parser.add_argument("--name", default="support-answer")
    parser.add_argument("--label", default="production")
    parser.add_argument("--store-dir", default="")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    tmp_ctx = tempfile.TemporaryDirectory() if not args.store_dir else None
    store_path = Path(tmp_ctx.name) if tmp_ctx else Path(args.store_dir)
    try:
        ops = LangfuseOpsClient(store_path)
        trace_id = args.trace_id
        var_map: dict[str, str] | None = None
        if args.demo or not trace_id:
            trace_id = "litellm-trace-demo"
            ops.log_trace(
                trace_id=trace_id,
                prompt_name="litellm-auto-trace",
                prompt_version=0,
                output="환불 정책 안내 및 다음 단계: 주문번호 회신",
                score=0.9,
                input_payload={
                    "messages": [
                        {
                            "role": "user",
                            "content": "[티켓 T-201] 제품(ProPlan) 문의 '환불 요청': 결제 후 2일 이내 환불 가능한가요?",
                        }
                    ]
                },
            )
            var_map = {
                "T-201": "ticket_id",
                "ProPlan": "product",
                "환불 요청": "subject",
                "결제 후 2일 이내 환불 가능한가요?": "message",
            }
        rec = promote_trace_as_prompt(ops, trace_id, args.name, labels=[args.label], variable_mapping=var_map)
        out = {"name": rec.name, "version": rec.version, "labels": rec.labels, "template": rec.template, "offline_mode": ops.offline_mode}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else f"[Save as Prompt] {rec.name} v{rec.version} ({rec.labels}): {rec.template}")
        return 0
    finally:
        if tmp_ctx:
            tmp_ctx.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
