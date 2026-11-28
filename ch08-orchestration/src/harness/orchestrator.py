from __future__ import annotations

from pathlib import Path

from harness.permissions import assert_role_action
from harness.rubric import score_evaluation


def run_cycle(docs_dir: Path, task_name: str, scores: dict[str, int], has_ui: bool = False) -> dict[str, object]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    assert_role_action("planner", "read_docs")
    (docs_dir / "PRD.md").write_text(f"# PRD\n- Target: {task_name}\n", encoding="utf-8")
    (docs_dir / "PLAN.md").write_text(f"# PLAN\n1. Implement {task_name}\n", encoding="utf-8")
    (docs_dir / "TASKS.md").write_text(f"- [ ] {task_name}\n", encoding="utf-8")

    assert_role_action("generator", "modify_code")
    (docs_dir / "IMPL.md").write_text(f"# IMPL\n- Implemented: {task_name}\n", encoding="utf-8")

    assert_role_action("evaluator", "run_bash")
    eval_res = score_evaluation(scores, has_ui=has_ui)
    (docs_dir / "REVIEW.md").write_text(
        f"# REVIEW\n- Verdict: {eval_res['verdict']} ({eval_res['total']}/{eval_res['max_score']})\n",
        encoding="utf-8",
    )
    with (docs_dir / "JOURNAL.md").open("a", encoding="utf-8") as f:
        f.write(f"- {task_name}: {eval_res['verdict']} ({eval_res['total']}/{eval_res['max_score']})\n")
    return eval_res
