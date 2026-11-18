"""제4장: 컨텍스트 윈도우 토큰 예산 계산 및 임계치 경고 시뮬레이터 CLI."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BudgetAllocation:
    system: int
    instructions: int
    tools: int
    history: int
    output: int
    max_window: int
    total_tokens: int
    utilization: float
    status: str
    lost_in_the_middle_risk: bool
    recommendations: list[str]


def estimate_tokens(text: str) -> int:
    """텍스트 길이 기반 결정론적 근사 토큰 수를 계산한다."""
    stripped = text.strip()
    if not stripped:
        return 0
    return max(1, (len(stripped) + 3) // 4)


def _to_tokens(value: str | int) -> int:
    if isinstance(value, int):
        return max(0, value)
    return estimate_tokens(value)


def evaluate_budget(
    system: str | int,
    instructions: str | int,
    tools: str | int,
    history: str | int,
    output: str | int,
    max_window: int = 200_000,
    warn_ratio: float = 0.75,
) -> BudgetAllocation:
    """5개 구획의 토큰 점유율을 계산하고 /compact·/clear·Lost-in-the-Middle 경고를 생성한다."""
    if max_window <= 0:
        raise ValueError("max_window must be positive")

    sys_t = _to_tokens(system)
    inst_t = _to_tokens(instructions)
    tools_t = _to_tokens(tools)
    hist_t = _to_tokens(history)
    out_t = _to_tokens(output)

    total = sys_t + inst_t + tools_t + hist_t + out_t
    utilization = round(total / max_window, 4)

    recommendations: list[str] = []
    lost_in_the_middle_risk = utilization >= 0.65 or (hist_t / max_window) >= 0.50

    if utilization >= 0.90:
        status = "CRITICAL"
        recommendations.append("Run /clear before switching tasks or isolate sub-work into a subagent.")
    elif utilization >= warn_ratio:
        status = "WARN"
        recommendations.append("Run /compact to summarize stale turns and preserve key decisions in TASKS.md.")
    else:
        status = "OK"

    if lost_in_the_middle_risk:
        recommendations.append(
            "Lost-in-the-Middle risk detected: place critical instructions at the top/bottom and trim middle history."
        )
    if tools_t / max_window >= 0.30:
        recommendations.append(
            "Tool output exceeds 30% of window: apply Top-K and excerpt filtering."
        )

    return BudgetAllocation(
        system=sys_t,
        instructions=inst_t,
        tools=tools_t,
        history=hist_t,
        output=out_t,
        max_window=max_window,
        total_tokens=total,
        utilization=utilization,
        status=status,
        lost_in_the_middle_risk=lost_in_the_middle_risk,
        recommendations=recommendations,
    )


def format_budget_report(alloc: BudgetAllocation, as_json: bool = False) -> str:
    """BudgetAllocation 결과를 JSON 또는 텍스트 테이블로 포맷한다."""
    if as_json:
        return json.dumps(asdict(alloc), ensure_ascii=False, indent=2)

    lines = [
        "=== Context Window Budget Report ===",
        f"Status: {alloc.status} | Total: {alloc.total_tokens:,} / {alloc.max_window:,} "
        f"({alloc.utilization * 100:.1f}%) | Lost-in-the-Middle Risk: {alloc.lost_in_the_middle_risk}",
        f"  - system       : {alloc.system:,} tokens",
        f"  - instructions : {alloc.instructions:,} tokens",
        f"  - tools        : {alloc.tools:,} tokens",
        f"  - history      : {alloc.history:,} tokens",
        f"  - output       : {alloc.output:,} tokens",
    ]
    if alloc.recommendations:
        lines.append("[Recommendations]")
        for rec in alloc.recommendations:
            lines.append(f"  * {rec}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="제4장 컨텍스트 예산 시뮬레이터")
    parser.add_argument("--system-tokens", type=int, default=4_000)
    parser.add_argument("--instructions-tokens", type=int, default=3_000)
    parser.add_argument("--tools-tokens", type=int, default=18_000)
    parser.add_argument("--history-tokens", type=int, default=65_000)
    parser.add_argument("--output-tokens", type=int, default=8_000)
    parser.add_argument("--max-window", type=int, default=200_000)
    parser.add_argument("--warn-ratio", type=float, default=0.75)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    alloc = evaluate_budget(
        system=args.system_tokens,
        instructions=args.instructions_tokens,
        tools=args.tools_tokens,
        history=args.history_tokens,
        output=args.output_tokens,
        max_window=args.max_window,
        warn_ratio=args.warn_ratio,
    )
    print(format_budget_report(alloc, as_json=args.json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
