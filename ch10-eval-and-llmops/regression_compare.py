from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from evaluator import run_three_evals
from langfuse_ops import LangfuseOpsClient
from models import SupportTicket
from prompting import compile_prompt
from seed_prompts import seed_default_prompts


def compare_prompt_versions(dataset: list[SupportTicket], v1_label: str, v2_label: str, ops: LangfuseOpsClient) -> dict[str, dict[str, float]]:
    report: dict[str, dict[str, float]] = {}
    for label in (v1_label, v2_label):
        prompt = ops.get_prompt("support-answer", label=label)
        scores: list[float] = []
        passes = 0
        for ticket in dataset:
            output = compile_prompt(prompt, ticket)
            ev = run_three_evals(output, ticket.expected_keywords, "환불 계정 정책 안내 다음 단계 회신")
            scores.append(ev.total_score)
            if ev.total_score >= 0.6 and ev.safety_passed:
                passes += 1
            ops.log_trace(f"{ticket.ticket_id}-{label}", prompt.name, prompt.version, output, ev.total_score)
        report[label] = {
            "version": float(prompt.version),
            "avg_score": round(sum(scores) / max(1, len(scores)), 3),
            "pass_rate": round(passes / max(1, len(dataset)), 3),
        }
    return report


def main() -> int:
    raw = json.loads((APP_DIR / "sample_dataset.json").read_text(encoding="utf-8"))
    dataset = [SupportTicket(**item) for item in raw]
    with tempfile.TemporaryDirectory() as tmp:
        ops = LangfuseOpsClient(Path(tmp))
        seed_default_prompts(ops)
        res = compare_prompt_versions(dataset, "production", "candidate", ops)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
