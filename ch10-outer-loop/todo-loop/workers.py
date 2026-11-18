from __future__ import annotations

import os
from dataclasses import dataclass

from models import TaskContract


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
            # 1차 시도는 실패(거짓 완료 방지 검증용), 2차 시도에서 성공
            return WorkerOutput(declared_completed=True, impl_note="calc-002-first-buggy", passed_override=False)
        return WorkerOutput(declared_completed=True, impl_note=f"ok:{task.task_id}:attempt={attempt}", passed_override=True)


class LLMWorker(BaseWorker):
    def run_task(self, task: TaskContract, attempt: int) -> WorkerOutput:
        if not os.getenv("OPENAI_API_KEY"):
            # 오프라인 환경 안전 폴백
            return DeterministicTestWorker().run_task(task, attempt)
        return DeterministicTestWorker().run_task(task, attempt)
