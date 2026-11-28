"""ch05-subagents-workflow/dynamic_workflow.py 단위 테스트."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

CH05_DIR = Path(__file__).resolve().parent.parent
if str(CH05_DIR) not in sys.path:
    sys.path.insert(0, str(CH05_DIR))

import dynamic_workflow  # noqa: E402


class TestDynamicWorkflow(unittest.TestCase):
    def test_registry_loads_five_agents_and_read_only_roles(self) -> None:
        reg = dynamic_workflow.AgentRegistry()
        agents = reg.list_agents()
        self.assertEqual(len(agents), 5)
        for ro_name in ("api-reviewer", "security-scanner", "code-quality"):
            defn = reg.get(ro_name)
            self.assertIsNotNone(defn)
            assert defn is not None
            self.assertTrue(defn.read_only, f"{ro_name} must be read-only")

    def test_orchestrator_parallel_isolated_execution(self) -> None:
        orch = dynamic_workflow.WorkflowOrchestrator()
        report = orch.run_workflow("api_change", "quote-cli --search")
        self.assertTrue(report["cross_verified"])
        self.assertEqual(report["selected_agents"], ["api-reviewer", "security-scanner", "test-runner", "doc-writer"])
        self.assertEqual(len(report["results"]), 4)
        self.assertIn("cross_verified=True", report["merged_summary"])

    def test_cli_json_exit_zero(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CH05_DIR / "dynamic_workflow.py"), "--task-type", "security_audit", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["selected_agents"], ["security-scanner", "code-quality"])


    def test_multi_platform_agent_registries(self) -> None:
        for plat in ("claude", "chatgpt", "gemini"):
            reg = dynamic_workflow.AgentRegistry(platform=plat)
            self.assertEqual(len(reg.list_agents()), 5, f"{plat} must load 5 agents")
            self.assertTrue(reg.get("api-reviewer").read_only)


if __name__ == "__main__":
    unittest.main()
