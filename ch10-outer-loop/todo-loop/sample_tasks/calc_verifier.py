from __future__ import annotations

from models import TaskContract
from workers import WorkerOutput


def verify_task_independently(task: TaskContract, output: WorkerOutput) -> tuple[bool, str]:
    """워커의 자체 completed 선언과 분리된 독립 검증기."""
    if output.passed_override is False:
        return False, f"{task.task_id}: independent calc check failed"
    return True, f"{task.task_id}: verified"
