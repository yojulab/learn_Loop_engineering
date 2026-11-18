from __future__ import annotations

import json
from pathlib import Path


class CostLogger:
    def __init__(self, log_path: str | Path) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.total_cost_usd = 0.0
        self.turns = 0

    def record(self, task_id: str, attempt: int, prompt_tokens: int, completion_tokens: int, verified: bool) -> float:
        cost = round((prompt_tokens * 0.000001) + (completion_tokens * 0.000002), 6)
        self.total_cost_usd = round(self.total_cost_usd + cost, 6)
        self.turns += 1
        entry = {
            "turn": self.turns,
            "task_id": task_id,
            "attempt": attempt,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": cost,
            "verified": verified,
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return cost
