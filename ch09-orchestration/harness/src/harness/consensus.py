from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CHOICE_RE = re.compile(r"^선택\s*:\s*([A-Z])\b")


@dataclass
class ConsensusOutcome:
    status: str  # AGREED | RETRY | HALTED
    adopted: str | None = None
    reason: str = ""
    halt_file: Path | None = None


def parse_choice_line(text: str) -> str | None:
    first_line = (text.strip().splitlines() or [""])[0].strip()
    m = CHOICE_RE.match(first_line)
    return m.group(1) if m else None


def evaluate_consensus(
    docs_dir: Path,
    topic: str,
    attempt: int,
    max_attempts: int = 3,
    irreversible: bool = False,
) -> ConsensusOutcome:
    decisions_dir = docs_dir / "decisions"
    if irreversible:
        halt_path = docs_dir / "HALT"
        halt_path.write_text(f"HALT: topic '{topic}' is irreversible and requires human approval.\n", encoding="utf-8")
        return ConsensusOutcome(status="HALTED", reason="irreversible decision", halt_file=halt_path)

    p_file = decisions_dir / f"{topic}.planner.md"
    e_file = decisions_dir / f"{topic}.evaluator.md"
    p_choice = parse_choice_line(p_file.read_text(encoding="utf-8")) if p_file.exists() else None
    e_choice = parse_choice_line(e_file.read_text(encoding="utf-8")) if e_file.exists() else None

    if p_choice and e_choice and p_choice == e_choice:
        return ConsensusOutcome(status="AGREED", adopted=p_choice, reason=f"agreed on {p_choice}")

    if attempt >= max_attempts:
        halt_path = docs_dir / "HALT"
        halt_path.write_text(
            f"HALT: blind consensus failed after {attempt} attempts for '{topic}' (planner={p_choice}, evaluator={e_choice}).\n",
            encoding="utf-8",
        )
        return ConsensusOutcome(status="HALTED", reason="max attempts disagreed", halt_file=halt_path)

    return ConsensusOutcome(status="RETRY", reason=f"disagreed: planner={p_choice}, evaluator={e_choice}")
