"""git-commit Conventional Commits 규격 검증 스크립트."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COMMIT_PATTERN = re.compile(
    r"^(feat|fix|docs|refactor|test|chore)(\([a-z0-9_-]+\))?: .{3,}$"
)


def validate_commit(text: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return False, ["Empty commit message"]
    header = lines[0]
    if not COMMIT_PATTERN.match(header):
        errors.append(
            f"Header {header!r} does not match Conventional Commits pattern"
        )
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Conventional Commit message")
    parser.add_argument("path", nargs="?", help="커밋 메시지 파일 경로")
    parser.add_argument("--text", default=None, help="직접 전달할 커밋 메시지")
    args = parser.parse_args(argv)

    content = args.text if args.text is not None else Path(args.path).read_text(encoding="utf-8")
    ok, errors = validate_commit(content)
    if not ok:
        for err in errors:
            print(f"[INVALID] {err}", file=sys.stderr)
        return 1
    print("[VALID] commit message ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
