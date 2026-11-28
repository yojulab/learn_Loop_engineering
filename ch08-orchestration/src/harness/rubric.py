from __future__ import annotations

BASE_CRITERIA = ("spec_fit", "module_boundary", "test_rigor", "ops_readiness")


def score_evaluation(scores: dict[str, int], has_ui: bool = False) -> dict[str, object]:
    keys = list(BASE_CRITERIA) + (["ui_polish"] if has_ui else [])
    total = 0
    for k in keys:
        val = int(scores.get(k, 0))
        if val < 0 or val > 3:
            raise ValueError(f"Score for {k} must be between 0 and 3, got {val}")
        total += val

    max_score = 15 if has_ui else 12
    if has_ui:
        verdict = "PASS" if total >= 12 else ("CONDITIONAL_PASS" if total >= 8 else "FAIL")
    else:
        verdict = "PASS" if total >= 9 else ("CONDITIONAL_PASS" if total >= 6 else "FAIL")

    return {"total": total, "max_score": max_score, "verdict": verdict, "has_ui": has_ui}
