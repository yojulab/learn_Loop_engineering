"""dockers/ Docker Compose 구성 정합성 테스트 (포트 미게시, 필수 서비스, .env 변수 일치)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCKERS = REPO_ROOT / "dockers"


def _env_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*#?\s*([A-Z][A-Z0-9_]*)=", line)
        if m:
            keys.add(m.group(1))
    return keys


class DockersComposeTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        for name in ("docker-compose.yml", "Dockerfile", "requirements.txt", ".env.example", "README.md"):
            self.assertTrue((DOCKERS / name).is_file(), f"dockers/{name} 누락")

    def test_compose_has_services_and_langfuse_port_only(self) -> None:
        compose = (DOCKERS / "docker-compose.yml").read_text(encoding="utf-8")
        for service in ("db_postgres:", "langfuse:", "app:"):
            self.assertIn(f"\n  {service}", compose, f"서비스 누락: {service}")
        self.assertIn("${LANGFUSE_PORT:-3000}:3000", compose)
        self.assertEqual(len(re.findall(r"(?m)^\s*ports:\s*$", compose)), 1)

    def test_dockerfile_installs_claude_cli_and_python_packages(self) -> None:
        dockerfile = (DOCKERS / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("@anthropic-ai/claude-code", dockerfile)
        self.assertIn("https://antigravity.google/cli/install.sh", dockerfile)
        self.assertIn("/root/.local/bin", dockerfile)
        self.assertIn("pip install", dockerfile)
        self.assertIn("langfuse", (DOCKERS / "requirements.txt").read_text(encoding="utf-8"))

    def test_every_compose_variable_is_declared_in_env_example(self) -> None:
        compose = (DOCKERS / "docker-compose.yml").read_text(encoding="utf-8")
        used = set(re.findall(r"(?<!\$)\$\{([A-Z][A-Z0-9_]*)", compose))
        declared = _env_keys(DOCKERS / ".env.example")
        missing = sorted(used - declared)
        self.assertEqual(missing, [], f".env.example 에 없는 compose 변수: {missing}")

    def test_volume_paths_are_configurable_via_env(self) -> None:
        compose = (DOCKERS / "docker-compose.yml").read_text(encoding="utf-8")
        for var in ("APP_SOURCE_DIR",):
            self.assertIn(f"${{{var}:-", compose)
            self.assertIn(var, _env_keys(DOCKERS / ".env.example"))

    def test_env_file_is_git_ignored(self) -> None:
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("dockers/.env", ignore)
        self.assertIn("dockers/volumes/", ignore)


if __name__ == "__main__":
    unittest.main()
