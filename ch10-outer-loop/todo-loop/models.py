from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Phase(str, Enum):
    DISCOVER = "DISCOVER"
    PLAN = "PLAN"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    ITERATE = "ITERATE"


class StopReason(str, Enum):
    DONE = "DONE"
    HALT_HUMAN_DECISION = "HALT_HUMAN_DECISION"
    HALT_MAX_RETRIES = "HALT_MAX_RETRIES"
    HALT_BUDGET_EXCEEDED = "HALT_BUDGET_EXCEEDED"
    HALT_BLOCKED_DEPENDENCY = "HALT_BLOCKED_DEPENDENCY"


@dataclass
class TaskContract:
    task_id: str
    title: str
    depends_on: list[str] = field(default_factory=list)
    requires_human_decision: bool = False
    status: str = "PENDING"  # PENDING | DONE | HALTED
    retries: int = 0


@dataclass
class LoopBudget:
    max_turns: int = 20
    max_retries_per_task: int = 3
    max_cost_usd: float = 5.0


@dataclass
class LoopResult:
    stop_reason: StopReason
    completed_tasks: list[str]
    halted_tasks: list[str]
    turns_executed: int
    total_cost_usd: float
