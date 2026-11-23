from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
SAMPLE_DIR = ROOT_DIR / "sample_tasks"
if str(SAMPLE_DIR) not in sys.path:
    sys.path.insert(0, str(SAMPLE_DIR))

from calc_verifier import verify_task_independently
from cost_logger import CostLogger
from models import LoopBudget, LoopResult, StopReason, TaskContract
from workers import BaseWorker, DeterministicTestWorker


class OuterLoopController:
    def __init__(self, tasks: list[TaskContract], worker: BaseWorker, budget: LoopBudget, cost_logger: CostLogger) -> None:
        self.tasks = tasks
        self.worker = worker
        self.budget = budget
        self.cost_logger = cost_logger

    def _dependencies_done(self, task: TaskContract) -> bool:
        done_ids = {t.task_id for t in self.tasks if t.status == "DONE"}
        return all(dep in done_ids for dep in task.depends_on)

    def run(self, halt_on_human: bool = True) -> LoopResult:
        turns = 0
        halted: list[str] = []
        stop_reason = StopReason.DONE

        while turns < self.budget.max_turns:
            pending = [t for t in self.tasks if t.status == "PENDING" and self._dependencies_done(t)]
            if not pending:
                break

            task = pending[0]
            if task.requires_human_decision:
                task.status = "HALTED"
                halted.append(task.task_id)
                if halt_on_human:
                    stop_reason = StopReason.HALT_HUMAN_DECISION
                    break
                continue

            while task.retries < self.budget.max_retries_per_task and turns < self.budget.max_turns:
                turns += 1
                attempt = task.retries + 1
                out = self.worker.run_task(task, attempt)
                ok, _ = verify_task_independently(task, out)
                self.cost_logger.record(task.task_id, attempt, out.prompt_tokens, out.completion_tokens, ok)
                if self.cost_logger.total_cost_usd > self.budget.max_cost_usd:
                    stop_reason = StopReason.HALT_BUDGET_EXCEEDED
                    return LoopResult(stop_reason, [t.task_id for t in self.tasks if t.status == "DONE"], halted, turns, self.cost_logger.total_cost_usd)
                if ok:
                    task.status = "DONE"
                    break
                task.retries += 1

            if task.status != "DONE":
                task.status = "HALTED"
                halted.append(task.task_id)
                stop_reason = StopReason.HALT_MAX_RETRIES
                break

        return LoopResult(
            stop_reason=stop_reason,
            completed_tasks=[t.task_id for t in self.tasks if t.status == "DONE"],
            halted_tasks=halted,
            turns_executed=turns,
            total_cost_usd=self.cost_logger.total_cost_usd,
        )


def load_sample_tasks() -> list[TaskContract]:
    raw = json.loads((SAMPLE_DIR / "tasks_contract.json").read_text(encoding="utf-8"))
    return [TaskContract(**item) for item in raw]


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Chapter 10 Any-Platform Outer Loop Controller")
    parser.add_argument("--platform", choices=["auto", "claude", "chatgpt", "gemini", "offline"], default="offline")
    args = parser.parse_args(argv)
    from workers import LLMWorker
    worker = DeterministicTestWorker() if args.platform == "offline" else LLMWorker(platform=args.platform)
    with tempfile.TemporaryDirectory() as tmp:
        logger = CostLogger(Path(tmp) / "cost.jsonl")
        ctrl = OuterLoopController(load_sample_tasks(), worker, LoopBudget(), logger)
        res = ctrl.run(halt_on_human=True)
        print(json.dumps({
            "stop_reason": res.stop_reason.value,
            "completed_tasks": res.completed_tasks,
            "halted_tasks": res.halted_tasks,
            "turns_executed": res.turns_executed,
            "total_cost_usd": res.total_cost_usd,
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
