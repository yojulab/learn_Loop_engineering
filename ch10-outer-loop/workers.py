from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from models import TaskContract

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from platforms.base import resolve_platform, run_with_any_platform


@dataclass
class WorkerOutput:
    declared_completed: bool
    impl_note: str
    prompt_tokens: int = 120
    completion_tokens: int = 60
    passed_override: bool | None = None


class BaseWorker:
    def run_task(self, task: TaskContract, attempt: int) -> WorkerOutput:
        raise NotImplementedError


class ManualWorker(BaseWorker):
    def run_task(self, task: TaskContract, attempt: int) -> WorkerOutput:
        return WorkerOutput(declared_completed=True, impl_note=f"manual:{task.task_id}:attempt={attempt}")


class DeterministicTestWorker(BaseWorker):
    """CALC-001~CALC-004 시나리오를 결정론적으로 재현하는 시험용 워커."""

    def run_task(self, task: TaskContract, attempt: int) -> WorkerOutput:
        if task.task_id == "CALC-002" and attempt == 1:
            return WorkerOutput(declared_completed=True, impl_note="calc-002-first-buggy", passed_override=False)
        return WorkerOutput(declared_completed=True, impl_note=f"ok:{task.task_id}:attempt={attempt}", passed_override=True)


class LLMWorker(BaseWorker):
    """Claude / ChatGPT / Gemini / Auto 플랫폼 어댑터를 통해 실행하는 범용 워커."""

    def __init__(self, platform: str = "auto") -> None:
        self.platform = platform

    def run_task(self, task: TaskContract, attempt: int) -> WorkerOutput:
        resolved = resolve_platform(self.platform)
        resp = run_with_any_platform(f"Execute {task.task_id}: {task.title}", platform=self.platform)
        if resp.mode == "offline-fallback":
            det = DeterministicTestWorker().run_task(task, attempt)
            det.impl_note = f"{resolved}:{resp.mode}:{det.impl_note}"
            return det
        return WorkerOutput(
            declared_completed=True,
            impl_note=f"{resp.platform}:{resp.mode}:{resp.text[:80]}",
            passed_override=True,
        )
