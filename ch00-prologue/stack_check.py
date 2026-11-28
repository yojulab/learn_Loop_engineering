"""프롤로그: 2026 모던 AI 에이전트 4계층 11대 스택 환경 및 저장소 진단 CLI."""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

FOUR_LAYERS_ELEMENTS: tuple[dict[str, Any], ...] = (
    {
        "layer_index": 1,
        "layer_name": "지식과 컨텍스트",
        "element_index": 1,
        "id": "prompt_engineering",
        "name": "구조화된 프롬프트 & Few-shot",
        "chapter": "ch04",
        "canonical_dir": "ch04-context-engineering",
        "description": "7항목 프롬프트 템플릿과 참조 구현 기반 Few-shot 패턴",
    },
    {
        "layer_index": 1,
        "layer_name": "지식과 컨텍스트",
        "element_index": 2,
        "id": "context_engineering",
        "name": "컨텍스트 엔지니어링 & 예산 관리",
        "chapter": "ch04",
        "canonical_dir": "ch04-context-engineering",
        "description": "컨텍스트 윈도우 점유율 계산, 오염 방지 및 /compact·/clear 기준",
    },
    {
        "layer_index": 2,
        "layer_name": "행동과 도구",
        "element_index": 3,
        "id": "agent_loop_cli",
        "name": "에이전트 코딩 루프 & CLI",
        "chapter": "ch01",
        "canonical_dir": "ch01-agentic-coding",
        "description": "컨텍스트 수집-수행-검증 루프 및 파이프 비대화형 실행",
    },
    {
        "layer_index": 2,
        "layer_name": "행동과 도구",
        "element_index": 4,
        "id": "mcp_protocol",
        "name": "MCP (Model Context Protocol)",
        "chapter": "ch02",
        "canonical_dir": "ch02-mcp-and-hooks",
        "description": "Tools·Resource·Prompt 표준 서버 및 환경변수 확장 연결",
    },
    {
        "layer_index": 2,
        "layer_name": "행동과 도구",
        "element_index": 5,
        "id": "hooks_guardrails",
        "name": "훅(Hooks) 실행 제어",
        "chapter": "ch02",
        "canonical_dir": "ch02-mcp-and-hooks",
        "description": "PreToolUse 위험 명령 차단 및 PostToolUse 감사 로그 기록",
    },
    {
        "layer_index": 3,
        "layer_name": "표준과 확장",
        "element_index": 6,
        "id": "layered_instructions",
        "name": "4대 층위 상시 지침",
        "chapter": "ch04",
        "canonical_dir": "ch04-context-engineering",
        "description": "CLAUDE.md, .claude/rules/, AGENTS.md, GEMINI.md 계층화 규칙",
    },
    {
        "layer_index": 3,
        "layer_name": "표준과 확장",
        "element_index": 7,
        "id": "skills_modules",
        "name": "온디맨드 스킬(Skills)",
        "chapter": "ch03",
        "canonical_dir": "ch03-skills",
        "description": "SKILL.md, reference.md, examples, 검증 스크립트 3단계 확장",
    },
    {
        "layer_index": 3,
        "layer_name": "표준과 확장",
        "element_index": 8,
        "id": "harness_engineering",
        "name": "하네스 엔지니어링",
        "chapter": "ch06",
        "canonical_dir": "ch06-harness-engineering",
        "description": "100줄 목차형 AGENTS.md, 아키텍처 린터, 가드레일, 문서 정원가꾸기",
    },
    {
        "layer_index": 4,
        "layer_name": "위임과 검증",
        "element_index": 9,
        "id": "subagents_workflow",
        "name": "서브에이전트 & 동적 워크플로",
        "chapter": "ch05",
        "canonical_dir": "ch05-subagents-workflow",
        "description": "읽기 전용/실행형 에이전트 역할 분리 및 병렬 결과 요약 병합",
    },
    {
        "layer_index": 4,
        "layer_name": "위임과 검증",
        "element_index": 10,
        "id": "loops_and_orchestration",
        "name": "이너·아우터 루프 & 3-Agent 오케스트레이션",
        "chapter": "ch07-ch09",
        "canonical_dir": "ch08-orchestration",
        "description": "Ralph 서킷 브레이커, 블라인드 합의, 5단계·7대 조건 장기 루프",
    },
    {
        "layer_index": 4,
        "layer_name": "위임과 검증",
        "element_index": 11,
        "id": "eval_and_llmops",
        "name": "Eval & LLMOps 관측/회귀",
        "chapter": "ch10-ch11",
        "canonical_dir": "ch10-eval-and-llmops",
        "description": "프롬프트 버전 라벨, 3종 Eval, 오프라인 Trace, Stage 1~4 진단",
    },
)
FOUR_LAYERS_12_ELEMENTS = FOUR_LAYERS_ELEMENTS

DEFAULT_PACKAGE_SPECS: tuple[tuple[str, str, str], ...] = (
    ("pydantic", "pydantic", "core"),
    ("PyYAML", "yaml", "core"),
    ("requests", "requests", "core"),
    ("beautifulsoup4", "bs4", "core"),
    ("openai", "openai", "core"),
    ("python-dotenv", "dotenv", "core"),
    ("anyio", "anyio", "core"),
    ("pytest", "pytest", "optional_fallback"),
    ("fastapi", "fastapi", "optional_fallback"),
    ("jinja2", "jinja2", "optional_fallback"),
    ("mcp", "mcp", "optional_fallback"),
    ("langfuse", "langfuse", "optional_fallback"),
)


def _check_sqlite_fts5() -> bool:
    """In-memory SQLite FTS5 확장 사용 가능 여부를 확인한다."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE VIRTUAL TABLE _fts5_probe USING fts5(body)")
        return True
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()


def check_python_runtime() -> dict[str, Any]:
    """Python 버전과 SQLite FTS5 지원 여부를 점검한다."""
    ver = sys.version_info
    return {
        "python_version": f"{ver.major}.{ver.minor}.{ver.micro}",
        "python_supported": (ver.major, ver.minor) >= (3, 11),
        "sqlite_version": sqlite3.sqlite_version,
        "sqlite_fts5_enabled": _check_sqlite_fts5(),
        "executable": sys.executable,
    }


def check_installed_packages() -> dict[str, Any]:
    """핵심 및 선택(폴백 지원) 서드파티 패키지 설치 상태를 점검한다."""
    packages: dict[str, dict[str, Any]] = {}
    for dist_name, module_name, tier in DEFAULT_PACKAGE_SPECS:
        spec = importlib.util.find_spec(module_name)
        installed = spec is not None
        version: str | None = None
        if installed:
            try:
                version = importlib.metadata.version(dist_name)
            except importlib.metadata.PackageNotFoundError:
                version = "unknown"
        packages[dist_name] = {
            "module": module_name,
            "tier": tier,
            "installed": installed,
            "version": version,
        }
    core_missing = [
        name for name, info in packages.items()
        if info["tier"] == "core" and not info["installed"]
    ]
    return {
        "packages": packages,
        "core_missing": core_missing,
        "offline_fallback_needed": [
            name for name, info in packages.items()
            if info["tier"] == "optional_fallback" and not info["installed"]
        ],
    }


def check_repo_layers(root: str | Path | None = None) -> dict[str, Any]:
    """저장소 루트 문서 및 4계층 11대 요소 단원 디렉터리 준비 상태를 점검한다."""
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parent.parent
    root_docs = ["README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "docs/ARCHITECTURE.md"]
    root_doc_status = {rel: (repo_root / rel).is_file() for rel in root_docs}

    elements_status = []
    for elem in FOUR_LAYERS_ELEMENTS:
        target_dir = repo_root / elem["canonical_dir"]
        elements_status.append({
            "layer_index": elem["layer_index"],
            "layer_name": elem["layer_name"],
            "element_index": elem["element_index"],
            "id": elem["id"],
            "name": elem["name"],
            "canonical_dir": elem["canonical_dir"],
            "present": target_dir.is_dir(),
        })

    layer_summary: dict[int, dict[str, Any]] = {}
    for item in elements_status:
        idx = item["layer_index"]
        bucket = layer_summary.setdefault(
            idx,
            {"layer_name": item["layer_name"], "total": 0, "present": 0},
        )
        bucket["total"] += 1
        if item["present"]:
            bucket["present"] += 1

    return {
        "repo_root": str(repo_root),
        "prologue_present": (repo_root / "ch00-prologue" / "stack_check.py").is_file(),
        "root_docs": root_doc_status,
        "elements": elements_status,
        "layer_summary": layer_summary,
    }


def format_report(as_json: bool = False, root: str | Path | None = None) -> str:
    """런타임·패키지·저장소 4계층 11대 요소 점검 결과를 JSON 또는 텍스트로 반환한다."""
    payload = {
        "runtime": check_python_runtime(),
        "packages": check_installed_packages(),
        "repo_layers": check_repo_layers(root),
        "elements_count": len(FOUR_LAYERS_ELEMENTS),
        "layers_count": len({e["layer_index"] for e in FOUR_LAYERS_ELEMENTS}),
    }
    if as_json:
        return json.dumps(payload, ensure_ascii=False, indent=2)

    rt = payload["runtime"]
    pkg = payload["packages"]
    repo = payload["repo_layers"]

    lines = [
        "=== 2026 모던 AI 에이전트 스택 (4계층 11대 요소) 환경 진단 ===",
        f"Python: {rt['python_version']} (supported={rt['python_supported']}) | "
        f"SQLite: {rt['sqlite_version']} (FTS5={rt['sqlite_fts5_enabled']})",
        f"Core missing: {pkg['core_missing'] or 'None'} | "
        f"Offline adapter targets: {pkg['offline_fallback_needed'] or 'None'}",
        f"Repo root: {repo['repo_root']}",
        "",
        "[4계층 11대 요소 매핑 현황]",
    ]
    for elem in repo["elements"]:
        mark = "READY" if elem["present"] else "PENDING"
        lines.append(
            f"  L{elem['layer_index']} ({elem['layer_name']}) #{elem['element_index']:02d} "
            f"{elem['name']} -> {elem['canonical_dir']} [{mark}]"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="프롤로그: 4계층 11대 AI 에이전트 스택 환경 진단 CLI",
    )
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    parser.add_argument("--root", default=None, help="점검할 저장소 루트 경로")
    args = parser.parse_args(argv)
    print(format_report(as_json=args.json, root=args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
