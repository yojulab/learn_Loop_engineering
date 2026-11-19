"""제6장: 작업 유형별 서브에이전트 동적 선택, 격리 병렬 실행 및 단일 요약 병합기."""

from __future__ import annotations

import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_AGENTS_DIR = Path(__file__).resolve().parent / ".claude" / "agents"

TASK_AGENT_MATRIX: dict[str, tuple[str, ...]] = {
    "api_change": ("api-reviewer", "security-scanner", "test-runner", "doc-writer"),
    "security_audit": ("security-scanner", "code-quality"),
    "release_check": ("test-runner", "code-quality", "security-scanner", "doc-writer"),
    "docs_update": ("doc-writer", "code-quality"),
}


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    description: str
    tools: tuple[str, ...]
    model: str
    prompt_body: str
    read_only: bool


@dataclass
class SubagentResult:
    agent_name: str
    task_type: str
    status: str
    findings: list[str] = field(default_factory=list)
    summary: str = ""
    duration_ms: int = 0


def _parse_agent_markdown(md_path: Path) -> AgentDefinition:
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, flags=re.DOTALL)
    if not m:
        raise ValueError(f"Missing YAML frontmatter in {md_path}")
    frontmatter, body = m.group(1), m.group(2).strip()
    meta: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()

    tools_raw = meta.get("tools", "[]").strip("[]")
    tools = tuple(t.strip() for t in tools_raw.split(",") if t.strip())
    read_only = not any(t in ("Write", "Edit", "Bash") for t in tools)
    return AgentDefinition(
        name=meta.get("name", md_path.stem),
        description=meta.get("description", ""),
        tools=tools,
        model=meta.get("model", "sonnet"),
        prompt_body=body,
        read_only=read_only,
    )


def _load_platform_json_agents(json_path: Path) -> list[AgentDefinition]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    out: list[AgentDefinition] = []
    for item in data.get("agents", []):
        tools = tuple(item.get("tools", []))
        read_only = not any(t in ("Write", "Edit", "Bash") for t in tools)
        out.append(
            AgentDefinition(
                name=item["name"],
                description=item.get("description", ""),
                tools=tools,
                model=item.get("model", "auto"),
                prompt_body=item.get("description", ""),
                read_only=read_only,
            )
        )
    return out


class AgentRegistry:
    """`.claude/agents/*.md` 정의를 로드하고 작업 유형별 서브에이전트를 동적 선택한다."""

    def __init__(self, agents_dir: Path | str = DEFAULT_AGENTS_DIR, platform: str = "claude") -> None:
        self.agents_dir = Path(agents_dir)
        self.platform = platform
        self._agents: dict[str, AgentDefinition] = {}
        ch06_root = Path(__file__).resolve().parent
        if platform == "chatgpt" and (ch06_root / "agents_chatgpt.json").is_file():
            for defn in _load_platform_json_agents(ch06_root / "agents_chatgpt.json"):
                self._agents[defn.name] = defn
        elif platform == "gemini" and (ch06_root / "agents_gemini.json").is_file():
            for defn in _load_platform_json_agents(ch06_root / "agents_gemini.json"):
                self._agents[defn.name] = defn
        elif self.agents_dir.is_dir():
            for md in sorted(self.agents_dir.glob("*.md")):
                defn = _parse_agent_markdown(md)
                self._agents[defn.name] = defn

    def list_agents(self) -> list[AgentDefinition]:
        return [self._agents[k] for k in sorted(self._agents)]

    def get(self, name: str) -> AgentDefinition | None:
        return self._agents.get(name)

    def select_for_task(self, task_type: str) -> list[AgentDefinition]:
        names = TASK_AGENT_MATRIX.get(task_type, ("code-quality", "test-runner"))
        return [self._agents[n] for n in names if n in self._agents]


class WorkflowOrchestrator:
    """선택된 서브에이전트를 ThreadPoolExecutor로 격리 실행 후 교차 검증·요약한다."""

    def __init__(self, registry: AgentRegistry | None = None, max_workers: int = 4) -> None:
        self.registry = registry or AgentRegistry()
        self.max_workers = max_workers

    def _run_isolated_agent(
        self,
        agent: AgentDefinition,
        task_type: str,
        target_summary: str,
    ) -> SubagentResult:
        started = time.perf_counter()
        findings = [
            f"[{agent.name}] model={agent.model} read_only={agent.read_only} inspected '{target_summary}'",
        ]
        if agent.name == "security-scanner":
            findings.append("No destructive shell or secret leaks detected in target scope.")
        elif agent.name == "test-runner":
            findings.append("Deterministic unit suite verified cleanly.")
        elif agent.name == "api-reviewer":
            findings.append("Input schema and JSON output contract consistent.")
        elif agent.name == "doc-writer":
            findings.append("Documentation references synchronized.")
        else:
            findings.append("Modularity and helper boundaries within limits.")

        elapsed = max(1, int((time.perf_counter() - started) * 1000))
        return SubagentResult(
            agent_name=agent.name,
            task_type=task_type,
            status="OK",
            findings=findings,
            summary=f"{agent.name}: {findings[-1]}",
            duration_ms=elapsed,
        )

    def run_workflow(self, task_type: str, target_summary: str = "quote-cli search") -> dict[str, Any]:
        selected = self.registry.select_for_task(task_type)
        isolated_results: dict[str, SubagentResult] = {}

        with ThreadPoolExecutor(max_workers=min(self.max_workers, max(1, len(selected)))) as pool:
            futures = {
                agent.name: pool.submit(self._run_isolated_agent, agent, task_type, target_summary)
                for agent in selected
            }
            for agent_name, fut in futures.items():
                isolated_results[agent_name] = fut.result()

        ordered = [isolated_results[a.name] for a in selected]
        blockers = [r.agent_name for r in ordered if r.status != "OK"]
        cross_verified = len(blockers) == 0 and len(ordered) > 0
        merged_summary = (
            f"task_type={task_type} | agents={len(ordered)} | "
            f"cross_verified={cross_verified} | highlights="
            + "; ".join(r.summary for r in ordered)
        )
        return {
            "task_type": task_type,
            "target": target_summary,
            "selected_agents": [a.name for a in selected],
            "cross_verified": cross_verified,
            "blockers": blockers,
            "results": [asdict(r) for r in ordered],
            "merged_summary": merged_summary,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="제6장 동적 병렬 서브에이전트 워크플로 시뮬레이터")
    parser.add_argument("--task-type", default="api_change", choices=sorted(TASK_AGENT_MATRIX.keys()))
    parser.add_argument("--target", default="quote-cli search extension")
    parser.add_argument("--platform", default="claude", choices=["claude", "chatgpt", "gemini"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    orch = WorkflowOrchestrator(registry=AgentRegistry(platform=args.platform))
    report = orch.run_workflow(task_type=args.task_type, target_summary=args.target)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["merged_summary"])
    return 0 if report["cross_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
