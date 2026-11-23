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
ROOT_DOCS: tuple[str, ...] = ("README.md", "AGENTS.md", "CLAUDE.md", "CHATGPT.md", "GEMINI.md")
CHAPTER_AI_FILES: tuple[str, ...] = ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".claude", ".gemini")
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


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)


CHAPTER_SPECS: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        chapter_id="webppt",
        phase=1,
        canonical_dir="docs",
        title="5시간 과정 GitHub Pages 웹 PPT (ch00~ch12 실습·모범답안)",
        required_files=(
            "ARCHITECTURE.md",
            ".nojekyll",
            "index.html",
            "assets/qr_facebook.svg",
            "assets/qr_linkedin.svg",
            "assets/profile_ohsanghun.jpg",
            "slides/p_prologue.js",
            "lecture.html",
            "prologue.html",
            "presenter.html",
            "deck.css",
            "engine.js",
            "ui.js",
            "slides/00_manifest.js",
            "slides/s0_opening.js",
            "slides/s1_part1.js",
            "slides/s2_part2.js",
            "slides/s3_part3.js",
            "slides/s4_part4_a.js",
            "slides/s5_part4_b.js",
        ),
    ),
    ChapterSpec(
        chapter_id="platforms",
        phase=1,
        canonical_dir="platforms",
        title="공용 멀티 플랫폼 어댑터 (claude / chatgpt / gemini)",
        required_files=("__init__.py", "base.py", "adapter_claude.py", "adapter_chatgpt.py", "adapter_gemini.py", "tests/test_platforms.py"),
        test_dirs=("platforms/tests",),
    ),
    ChapterSpec(
        chapter_id="ch00",
        phase=1,
        canonical_dir="ch00-prologue",
        title="프롤로그: 4계층 12대 스택 환경 진단",
        required_files=(*CHAPTER_AI_FILES, "README.md", "stack_check.py", "agent_check.py", "tests/test_stack_check.py"),
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
            *CHAPTER_AI_FILES,
            "README.md",
            "quotes.json",
            "quote_cli.py",
            "interactive_demo.py",
            "tests/test_quote_cli.py",
        ),
        test_dirs=("ch01-agentic-coding/tests",),
        cli_commands=(
            ("ch01-agentic-coding/quote_cli.py", "--all"),
            ("ch01-agentic-coding/quote_cli.py", "--tag", "engineering"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch02",
        phase=2,
        canonical_dir="ch02-mcp-and-hooks",
        title="제2장: MCP와 훅(Hooks)",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "main.py",
            "quotes.json",
            ".mcp.json",
            ".claude/settings.json",
            "hooks/block_dangerous_bash.py",
            "hooks/audit_logger.py",
            "tests/test_quote_mcp_and_hooks.py",
            "mcp_config_claude.json",
            "mcp_config_chatgpt.json",
            "mcp_config_gemini.json",
            "hooks/platform_hook_bridge.py",
        ),
        test_dirs=("ch02-mcp-and-hooks/tests",),
    ),
    ChapterSpec(
        chapter_id="ch03",
        phase=2,
        canonical_dir="ch03-skills",
        title="제3장: 온디맨드 노하우 모듈: 스킬(Skills)",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "gh-issue/SKILL.md",
            "gh-issue/reference.md",
            "gh-issue/examples/sample_issue.md",
            "gh-issue/scripts/validate_issue.py",
            "git-commit/SKILL.md",
            "git-commit/reference.md",
            "git-commit/examples/sample_commit.txt",
            "git-commit/scripts/validate_commit.py",
            "gh-pr/SKILL.md",
            "gh-pr/reference.md",
            "gh-pr/examples/sample_pr.md",
            "gh-pr/scripts/validate_pr.py",
            "gh-review/SKILL.md",
            "gh-review/reference.md",
            "gh-review/examples/sample_review.md",
            "gh-review/scripts/validate_review.py",
            "gh-address-review/SKILL.md",
            "gh-address-review/reference.md",
            "gh-address-review/examples/sample_address_review.md",
            "gh-address-review/scripts/validate_address_review.py",
            "tests/test_github_workflow_skills.py",
            "skills_claude.md",
            "skills_chatgpt.md",
            "skills_gemini.md",
        ),
        test_dirs=("ch03-skills/tests",),
    ),
    ChapterSpec(
        chapter_id="ch04",
        phase=3,
        canonical_dir="ch04-context-engineering",
        title="제4장: 컨텍스트 엔지니어링과 윈도우의 한계",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "prompt_template.txt",
            "few_shot_reference.txt",
            "claude_working_guidelines.md",
            ".claude/rules/api.md",
            "context_budget.py",
            "guidelines_claude.md",
            "guidelines_chatgpt.md",
            "guidelines_gemini.md",
            "tests/test_context_engineering.py",
        ),
        test_dirs=("ch04-context-engineering/tests",),
        cli_commands=(
            ("ch04-context-engineering/context_budget.py",),
            ("ch04-context-engineering/context_budget.py", "--json"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch05",
        phase=3,
        canonical_dir="ch05-rag-and-memory",
        title="제5장: 외부 지식(RAG)과 세션 너머의 기억(Memory)",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "memory_manager.py",
            "agentic_rag.py",
            "TASKS.md",
            "JOURNAL.md",
            "corpus/01_context_budget.md",
            "corpus/02_agentic_rag.md",
            "corpus/03_durable_memory.md",
            "tests/test_memory_pattern.py",
        ),
        test_dirs=("ch05-rag-and-memory/tests",),
    ),
    ChapterSpec(
        chapter_id="ch06",
        phase=4,
        canonical_dir="ch06-subagents-workflow",
        title="제6장: 서브에이전트와 워크플로",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "quote_cli.py",
            "dynamic_workflow.py",
            "agents_chatgpt.json",
            "agents_gemini.json",
            "tests/test_dynamic_workflow.py",
            "tests/test_quote_cli_search.py",
        ),
        test_dirs=("ch06-subagents-workflow/tests",),
    ),
    ChapterSpec(
        chapter_id="ch07",
        phase=4,
        canonical_dir="ch07-harness-engineering",
        title="제7장: 하네스 엔지니어링",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "arch_linter.py",
            "guardrails.py",
            "doc_gardening.py",
            "tests/test_harness_templates.py",
        ),
        test_dirs=("ch07-harness-engineering/tests",),
    ),
    ChapterSpec(
        chapter_id="ch08",
        phase=4,
        canonical_dir="ch08-inner-ralph-loop",
        title="제8장: 이너 루프와 랄프 루프",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "db.py",
            "collector.py",
            "app.py",
            "ralph_loop.sh",
            "worker_claude.sh",
            "worker_chatgpt.sh",
            "worker_gemini.sh",
            "goal_evaluator.py",
            "tests/test_rss_wiki.py",
        ),
        test_dirs=("ch08-inner-ralph-loop/tests",),
    ),
    ChapterSpec(
        chapter_id="ch09",
        phase=5,
        canonical_dir="ch09-orchestration",
        title="제9장: 다중 에이전트 오케스트레이션",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "pyproject.toml",
            "run.py",
            "tests/test_orchestration_harness.py",
        ),
        test_dirs=("ch09-orchestration/tests",),
    ),
    ChapterSpec(
        chapter_id="ch10",
        phase=5,
        canonical_dir="ch10-outer-loop",
        title="제10장: 아우터 루프 엔지니어링",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "loop.py",
            "models.py",
            "workers.py",
            "cost_logger.py",
            "tests/test_todo_loop.py",
        ),
        test_dirs=("ch10-outer-loop/tests",),
    ),
    ChapterSpec(
        chapter_id="ch11",
        phase=5,
        canonical_dir="ch11-eval-and-llmops",
        title="제11장: 평가(Eval)와 LLMOps",
        required_files=(
            *CHAPTER_AI_FILES,
            "README.md",
            "models.py",
            "seed_prompts.py",
            "prompting.py",
            "evaluator.py",
            "langfuse_ops.py",
            "trace_to_prompt.py",
            "fetch_prompt.py",
            "regression_compare.py",
            "litellm_proxy/litellm_config.yaml",
            "litellm_proxy/docker-compose.litellm.yml",
            "litellm_proxy/.env.example",
            "litellm_proxy/zero_code_proxy_demo.py",
            "litellm_proxy/client_claude.py",
            "litellm_proxy/client_chatgpt.py",
            "litellm_proxy/client_gemini.py",
            "tests/test_support_assistant.py",
        ),
        test_dirs=("ch11-eval-and-llmops/tests",),
        cli_commands=(
            ("ch11-eval-and-llmops/litellm_proxy/zero_code_proxy_demo.py",),
            ("ch11-eval-and-llmops/trace_to_prompt.py", "--demo", "--json"),
            ("ch11-eval-and-llmops/fetch_prompt.py", "--demo", "--json"),
        ),
    ),
    ChapterSpec(
        chapter_id="ch12",
        phase=5,
        canonical_dir="ch12-epilogue",
        title="에필로그: 도입 체크리스트 & Stage 1~4 진단",
        required_files=(
            *CHAPTER_AI_FILES,
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


def check_readme_five_sections(readme_path: Path, require_prompts: bool = False) -> tuple[bool, list[str]]:
    """표준 5단 README.md 구성(1~5 섹션, mermaid 블록, 3개 이상 프롬프트 예시)을 검증한다."""
    if not readme_path.is_file():
        return False, ["missing README.md"]
    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    missing: list[str] = []
    for idx in range(1, 6):
        if not re.search(rf"(?m)^##\s+{idx}\.", content):
            missing.append(f"section ## {idx}.")
    if "```mermaid" not in content:
        missing.append("mermaid diagram block")
    if require_prompts:
        for p_idx in range(1, 4):
            if f"프롬프트 예시 {p_idx}" not in content:
                missing.append(f"프롬프트 예시 {p_idx}")
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

    readme_ok, readme_missing = check_readme_five_sections(repo_root / "README.md", require_prompts=True)
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

    is_chapter = spec.chapter_id.startswith("ch")
    readme_ok, readme_missing = check_readme_five_sections(chap_dir / "README.md", require_prompts=is_chapter)
    results.append(
        CheckResult(
            name=f"{spec.chapter_id}:readme_five_sections",
            passed=readme_ok,
            details={"missing": readme_missing},
        )
    )


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
