from __future__ import annotations

ROLE_TOOL_PERMISSIONS: dict[str, dict[str, object]] = {
    "planner": {
        "allowed_tools": {"Read", "Glob", "Grep", "WriteDocs"},
        "can_modify_code": False,
        "can_run_bash": False,
    },
    "generator": {
        "allowed_tools": {"Read", "Glob", "Grep", "Write", "Edit", "Bash"},
        "can_modify_code": True,
        "can_run_bash": True,
    },
    "evaluator": {
        "allowed_tools": {"Read", "Glob", "Grep", "WriteReview", "BashVerify"},
        "can_modify_code": False,
        "can_run_bash": True,
    },
}


class PermissionViolationError(PermissionError):
    pass


def assert_role_action(role: str, action: str) -> None:
    cfg = ROLE_TOOL_PERMISSIONS.get(role)
    if cfg is None:
        raise PermissionViolationError(f"Unknown role: {role}")
    if action == "modify_code" and not cfg["can_modify_code"]:
        raise PermissionViolationError(f"Role '{role}' cannot modify target code")
    if action == "run_bash" and not cfg["can_run_bash"]:
        raise PermissionViolationError(f"Role '{role}' cannot execute Bash")
