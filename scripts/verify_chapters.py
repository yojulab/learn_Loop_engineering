"""전 단원(ch00~ch12) 구조, 심볼릭 링크, 레거시 부재, CLI, 단위 테스트 통합 검증 러너."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

LEGACY_MARKER = "ecare" + "24"
LEGACY_DOCS_PATHS: tuple[str, ...] = (
    "docs/agent",
    "docs/USER_PROMPTS.md",
    "docs/PRD_TEMPLATE.md",
    "docs/user_prompt_history.md",
)
ROOT_DOCS: tuple[str, ...] = ("README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md")
TEXT_SCAN_SKIP_DIRS: frozenset[str] = frozenset({".git", "__pycache__", ".pytest_cache"})


@dataclass(frozen=True)
class ChapterSpec:
    chapter_id: str
    phase: int
    canonical_dir: str
    title: str
    required_files: tuple[str, ...] = ()
    test_dirs: tuple[str, ...] = ()
    cli_commands: tuple[tuple[str, ...], ...] = ()
    symlinks: tuple[tuple[str, str], ...] = ()


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)


CHAPTER_SPECS: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        chapter_id="ch00",
        phase=1,
        canonical_dir="ch00-prologue",
        title="프롤로그: 4계층 12대 스택 환경 진단",
        required_files=("README.md", "stack_check.py", "tests/test_stack_check.py"),
        test_dirs=("ch00-prologue/tests",),
        cli_commands=(
            ("ch00-prologue/stack_check.py",),
            ("ch00-prologue/stack_check.py", "--json"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch01",
        phase=2,
        canonical_dir="ch01-agentic-coding",
        title="제1장: 바이브 코딩과 에이전틱 코딩의 탄생",
        required_files=(
            "README.md",
            "quote-cli/quotes.json",
            "quote-cli/quote_cli.py",
            "quote-cli/interactive_demo.py",
            "quote-cli/tests/test_quote_cli.py",
        ),
        test_dirs=("ch01-agentic-coding/quote-cli/tests",),
        cli_commands=(
            ("ch01-agentic-coding/quote-cli/quote_cli.py", "--all"),
            ("ch01-agentic-coding/quote-cli/quote_cli.py", "--tag", "engineering"),
        ),
        symlinks=(("ch01/quote-cli", "ch01-agentic-coding/quote-cli"),),
    ),
    ChapterSpec(
        chapter_id="ch02",
        phase=2,
        canonical_dir="ch02-mcp-and-hooks",
        title="제2장: MCP와 훅(Hooks)",
        required_files=(
            "README.md",
            "quote-mcp/main.py",
            "quote-mcp/quotes.json",
            "quote-mcp/.mcp.json",
            "quote-mcp/.claude/settings.json",
            "quote-mcp/hooks/block_dangerous_bash.py",
            "quote-mcp/hooks/audit_logger.py",
            "quote-mcp/tests/test_quote_mcp_and_hooks.py",
        ),
        test_dirs=("ch02-mcp-and-hooks/quote-mcp/tests",),
        symlinks=(
            ("ch02/quote-mcp", "ch02-mcp-and-hooks/quote-mcp"),
            ("ch04/quote-cli/main.py", "ch02-mcp-and-hooks/quote-mcp/main.py"),
            ("ch04/quote-cli/quotes.json", "ch02-mcp-and-hooks/quote-mcp/quotes.json"),
            ("ch04/quote-cli/.mcp.json", "ch02-mcp-and-hooks/quote-mcp/.mcp.json"),
            ("ch04/quote-cli/.claude", "ch02-mcp-and-hooks/quote-mcp/.claude"),
            ("ch04/quote-cli/cli", "ch01-agentic-coding/quote-cli"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch03",
        phase=2,
        canonical_dir="ch03-skills",
        title="제3장: 온디맨드 노하우 모듈: 스킬(Skills)",
        required_files=(
            "README.md",
            "github-workflow-skills/tests/test_github_workflow_skills.py",
        ),
        test_dirs=("ch03-skills/github-workflow-skills/tests",),
        symlinks=(("ch03/github-workflow-skills", "ch03-skills/github-workflow-skills"),),
    ),
    ChapterSpec(
        chapter_id="ch04",
        phase=3,
        canonical_dir="ch04-context-engineering",
        title="제4장: 컨텍스트 엔지니어링과 윈도우의 한계",
        required_files=(
            "README.md",
            "prompt_template.txt",
            "few_shot_reference.txt",
            "claude_working_guidelines.md",
            "CLAUDE.md",
            ".claude/rules/api.md",
            "AGENTS.md",
            "GEMINI.md",
            "context_budget.py",
            "tests/test_context_engineering.py",
        ),
        test_dirs=("ch04-context-engineering/tests",),
        cli_commands=(("ch04-context-engineering/context_budget.py",),),
        symlinks=(
            ("ch04/prompt_template.txt", "ch04-context-engineering/prompt_template.txt"),
            ("ch04/few_shot_reference.txt", "ch04-context-engineering/few_shot_reference.txt"),
            ("ch04/claude_working_guidelines.md", "ch04-context-engineering/claude_working_guidelines.md"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch05",
        phase=3,
        canonical_dir="ch05-rag-and-memory",
        title="제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory)",
        required_files=(
            "README.md",
            "memory_pattern/memory_manager.py",
            "memory_pattern/agentic_rag.py",
            "memory_pattern/TASKS.md",
            "memory_pattern/JOURNAL.md",
            "memory_pattern/tests/test_memory_pattern.py",
        ),
        test_dirs=("ch05-rag-and-memory/memory_pattern/tests",),
        symlinks=(("ch05/memory_pattern", "ch05-rag-and-memory/memory_pattern"),),
    ),
    ChapterSpec(
        chapter_id="ch06",
        phase=4,
        canonical_dir="ch06-subagents-workflow",
        title="제6장: 서브에이전트와 워크플로",
        required_files=(
            "README.md",
            "quote-cli/quote_cli.py",
            "dynamic_workflow.py",
            "tests/test_dynamic_workflow.py",
        ),
        test_dirs=(
            "ch06-subagents-workflow/quote-cli/tests",
            "ch06-subagents-workflow/tests",
        ),
        symlinks=(
            ("ch06/quote-cli", "ch06-subagents-workflow/quote-cli"),
            ("ch06-subagents-workflow/quote-cli/.claude", "ch06-subagents-workflow/.claude"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch07",
        phase=4,
        canonical_dir="ch07-harness-engineering",
        title="제7장: 하네스 엔지니어링",
        required_files=(
            "README.md",
            "harness-templates/AGENTS.md",
            "harness-templates/arch_linter.py",
            "harness-templates/guardrails.py",
            "harness-templates/doc_gardening.py",
            "harness-templates/tests/test_harness_templates.py",
        ),
        test_dirs=("ch07-harness-engineering/harness-templates/tests",),
        symlinks=(("ch07/harness-templates", "ch07-harness-engineering/harness-templates"),),
    ),
    ChapterSpec(
        chapter_id="ch08",
        phase=4,
        canonical_dir="ch08-inner-ralph-loop",
        title="제8장: 이너 루프와 랄프 루프",
        required_files=(
            "README.md",
            "rss-wiki/db.py",
            "rss-wiki/collector.py",
            "rss-wiki/app.py",
            "rss-wiki/ralph_loop.sh",
            "rss-wiki/goal_evaluator.py",
            "rss-wiki/tests/test_rss_wiki.py",
        ),
        test_dirs=("ch08-inner-ralph-loop/rss-wiki/tests",),
        symlinks=(("ch08/rss-wiki", "ch08-inner-ralph-loop/rss-wiki"),),
    ),
    ChapterSpec(
        chapter_id="ch09",
        phase=5,
        canonical_dir="ch09-orchestration",
        title="제9장: 다중 에이전트 오케스트레이션",
        required_files=(
            "README.md",
            "harness/pyproject.toml",
            "harness/run.py",
            "harness/tests/test_orchestration_harness.py",
        ),
        test_dirs=("ch09-orchestration/harness/tests",),
        symlinks=(("ch09/harness", "ch09-orchestration/harness"),),
    ),
    ChapterSpec(
        chapter_id="ch10",
        phase=5,
        canonical_dir="ch10-outer-loop",
        title="제10장: 아우터 루프 엔지니어링",
        required_files=(
            "README.md",
            "todo-loop/loop.py",
            "todo-loop/models.py",
            "todo-loop/workers.py",
            "todo-loop/cost_logger.py",
            "todo-loop/tests/test_todo_loop.py",
        ),
        test_dirs=("ch10-outer-loop/todo-loop/tests",),
        symlinks=(("ch10/todo-loop", "ch10-outer-loop/todo-loop"),),
    ),
    ChapterSpec(
        chapter_id="ch11",
        phase=5,
        canonical_dir="ch11-eval-and-llmops",
        title="제11장: 평가(Eval)와 LLMOps",
        required_files=(
            "README.md",
            "support-assistant/models.py",
            "support-assistant/seed_prompts.py",
            "support-assistant/prompting.py",
            "support-assistant/evaluator.py",
            "support-assistant/langfuse_ops.py",
            "support-assistant/regression_compare.py",
            "support-assistant/tests/test_support_assistant.py",
        ),
        test_dirs=("ch11-eval-and-llmops/support-assistant/tests",),
        symlinks=(("ch11/support-assistant", "ch11-eval-and-llmops/support-assistant"),),
    ),
    ChapterSpec(
        chapter_id="ch12",
        phase=5,
        canonical_dir="ch12-epilogue",
        title="에필로그: 도입 체크리스트 & Stage 1~4 진단",
        required_files=(
            "README.md",
            "stage_readiness_check.py",
            "tests/test_stage_readiness.py",
        ),
        test_dirs=("ch12-epilogue/tests",),
        cli_commands=(("ch12-epilogue/stage_readiness_check.py", "--format", "json"),),
    ),
)


def discover_test_runner() -> list[str]:
    """pytest 설치 여부를 판별해 pytest 또는 unittest 폴백 실행 커맨드를 반환한다."""
    if importlib.util.find_spec("pytest") is not None:
        return [sys.executable, "-m", "pytest", "-q"]
    return [sys.executable, "-m", "unittest", "discover"]


def check_readme_five_sections(readme_path: Path) -> tuple[bool, list[str]]:
    """표준 5단 README.md 구성(1~5 섹션 및 mermaid 블록)을 검증한다."""
    if not readme_path.is_file():
        return False, ["missing README.md"]
    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    missing: list[str] = []
    for idx in range(1, 6):
        if not re.search(rf"(?m)^##\s+{idx}\.", content):
            missing.append(f"section ## {idx}.")
    if "```mermaid" not in content:
        missing.append("mermaid diagram block")
    return len(missing) == 0, missing


def verify_legacy_removed(repo_root: Path) -> CheckResult:
    """레거시 .agents/, 구 docs/ 자산 및 잔존 레거시 토큰이 0건인지 검증한다."""
    issues: list[str] = []
    if (repo_root / ".agents").exists():
        issues.append(".agents directory still exists")
    for rel in LEGACY_DOCS_PATHS:
        if (repo_root / rel).exists():
            issues.append(f"legacy path still exists: {rel}")

    token_hits: list[str] = []
    for current_root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in TEXT_SCAN_SKIP_DIRS]
        for fname in files:
            fpath = Path(current_root) / fname
            if fpath.is_symlink():
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if LEGACY_MARKER in text.lower():
                token_hits.append(str(fpath.relative_to(repo_root)))

    if token_hits:
        issues.append(f"legacy marker found in files: {token_hits}")

    return CheckResult(
        name="legacy_removed",
        passed=len(issues) == 0,
        details={"issues": issues, "token_hits": token_hits},
    )


def verify_symlinks(repo_root: Path, specs: list[ChapterSpec]) -> CheckResult:
    """선택된 단원의 호환 심볼릭 링크/브릿지가 유효하게 연결되어 있는지 검증한다."""
    errors: list[str] = []
    checked: list[str] = []
    for spec in specs:
        for link_rel, target_rel in spec.symlinks:
            link_path = repo_root / link_rel
            expected_target = (repo_root / target_rel).resolve()
            checked.append(link_rel)
            if not link_path.exists():
                errors.append(f"missing link/target: {link_rel} -> {target_rel}")
                continue
            if link_path.resolve() != expected_target:
                errors.append(
                    f"link mismatch for {link_rel}: resolves to {link_path.resolve()}, expected {expected_target}"
                )
    return CheckResult(
        name="symlinks",
        passed=len(errors) == 0,
        details={"checked": checked, "errors": errors},
    )


def _run_test_dir(repo_root: Path, test_dir_rel: str, runner: list[str]) -> CheckResult:
    test_dir = repo_root / test_dir_rel
    if not test_dir.is_dir():
        return CheckResult(
            name=f"tests:{test_dir_rel}",
            passed=False,
            details={"error": f"missing test directory: {test_dir_rel}"},
        )
    if runner[2] == "pytest":
        cmd = [*runner, str(test_dir)]
    else:
        cmd = [*runner, "-s", str(test_dir), "-p", "test_*.py"]
    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)
    return CheckResult(
        name=f"tests:{test_dir_rel}",
        passed=proc.returncode == 0,
        details={
            "runner": "pytest" if runner[2] == "pytest" else "unittest",
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        },
    )


def _verify_root_phase1(repo_root: Path, runner: list[str]) -> list[CheckResult]:
    results: list[CheckResult] = []

    missing_docs = [doc for doc in ROOT_DOCS if not (repo_root / doc).is_file()]
    if not (repo_root / "docs" / "ARCHITECTURE.md").is_file():
        missing_docs.append("docs/ARCHITECTURE.md")
    results.append(
        CheckResult(
            name="root_docs_exist",
            passed=len(missing_docs) == 0,
            details={"missing": missing_docs},
        )
    )

    agents_path = repo_root / "AGENTS.md"
    agents_lines = len(agents_path.read_text(encoding="utf-8").splitlines()) if agents_path.is_file() else -1
    results.append(
        CheckResult(
            name="agents_md_max_100_lines",
            passed=0 < agents_lines <= 100,
            details={"line_count": agents_lines, "limit": 100},
        )
    )

    readme_ok, readme_missing = check_readme_five_sections(repo_root / "README.md")
    results.append(
        CheckResult(
            name="root_readme_five_sections",
            passed=readme_ok,
            details={"missing": readme_missing},
        )
    )

    results.append(verify_legacy_removed(repo_root))
    results.append(_run_test_dir(repo_root, "tests", runner))
    return results


def _verify_single_chapter(repo_root: Path, spec: ChapterSpec, runner: list[str]) -> list[CheckResult]:
    results: list[CheckResult] = []
    chap_dir = repo_root / spec.canonical_dir
    missing_files = [
        rel for rel in spec.required_files if not (chap_dir / rel).exists()
    ]
    results.append(
        CheckResult(
            name=f"{spec.chapter_id}:required_files",
            passed=chap_dir.is_dir() and len(missing_files) == 0,
            details={"canonical_dir": spec.canonical_dir, "missing": missing_files},
        )
    )

    readme_ok, readme_missing = check_readme_five_sections(chap_dir / "README.md")
    results.append(
        CheckResult(
            name=f"{spec.chapter_id}:readme_five_sections",
            passed=readme_ok,
            details={"missing": readme_missing},
        )
    )

    if spec.symlinks:
        sym_res = verify_symlinks(repo_root, [spec])
        sym_res.name = f"{spec.chapter_id}:symlinks"
        results.append(sym_res)

    for cmd_args in spec.cli_commands:
        script_path = repo_root / cmd_args[0]
        if not script_path.is_file():
            results.append(
                CheckResult(
                    name=f"{spec.chapter_id}:cli:{cmd_args[0]}",
                    passed=False,
                    details={"error": f"missing script {cmd_args[0]}"},
                )
            )
            continue
        proc = subprocess.run(
            [sys.executable, *cmd_args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        cmd_label = " ".join(cmd_args)
        results.append(
            CheckResult(
                name=f"{spec.chapter_id}:cli:{cmd_label}",
                passed=proc.returncode == 0,
                details={"returncode": proc.returncode, "stderr": proc.stderr.strip()},
            )
        )

    for tdir in spec.test_dirs:
        res = _run_test_dir(repo_root, tdir, runner)
        res.name = f"{spec.chapter_id}:{res.name}"
        results.append(res)

    return results


def run_chapter_checks(
    repo_root: Path,
    phase: int | None = None,
    chapter: str | None = None,
    run_all: bool = False,
) -> dict[str, Any]:
    """요청된 Phase/단원 범위에 대해 통합 검증을 수행하고 요약 딕셔너리를 반환한다."""
    runner = discover_test_runner()
    checks: list[CheckResult] = []

    if run_all or phase == 1:
        checks.extend(_verify_root_phase1(repo_root, runner))

    if chapter is not None:
        selected = [s for s in CHAPTER_SPECS if s.chapter_id == chapter]
    elif phase is not None:
        selected = [s for s in CHAPTER_SPECS if s.phase == phase]
    else:
        selected = list(CHAPTER_SPECS)

    for spec in selected:
        checks.extend(_verify_single_chapter(repo_root, spec, runner))

    passed_count = sum(1 for c in checks if c.passed)
    failed_count = len(checks) - passed_count
    return {
        "repo_root": str(repo_root),
        "scope": chapter or (f"phase-{phase}" if phase is not None else "all"),
        "runner": "pytest" if runner[2] == "pytest" else "unittest",
        "overall_passed": failed_count == 0 and len(checks) > 0,
        "total_checks": len(checks),
        "passed_checks": passed_count,
        "failed_checks": failed_count,
        "checks": [asdict(c) for c in checks],
    }


def _format_text(summary: dict[str, Any]) -> str:
    status = "PASS" if summary["overall_passed"] else "FAIL"
    lines = [
        f"=== verify_chapters ({summary['scope']}) [{status}] "
        f"({summary['passed_checks']}/{summary['total_checks']}) runner={summary['runner']} ==="
    ]
    for chk in summary["checks"]:
        mark = "OK" if chk["passed"] else "FAIL"
        lines.append(f"  [{mark}] {chk['name']}")
        if not chk["passed"]:
            lines.append(f"         details={json.dumps(chk['details'], ensure_ascii=False)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="『2026 모던 AI 에이전트 스택』 전 단원 통합 검증 러너",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5], help="특정 Phase만 검증")
    group.add_argument(
        "--chapter",
        choices=[s.chapter_id for s in CHAPTER_SPECS],
        help="특정 단원(ch00~ch12)만 검증",
    )
    group.add_argument("--all", action="store_true", help="전체 Phase 및 전 단원 검증")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 결과 출력")
    args = parser.parse_args(argv)

    run_all = args.all or (args.phase is None and args.chapter is None)
    repo_root = Path(__file__).resolve().parent.parent
    summary = run_chapter_checks(
        repo_root=repo_root,
        phase=args.phase,
        chapter=args.chapter,
        run_all=run_all,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(_format_text(summary))
    return 0 if summary["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
