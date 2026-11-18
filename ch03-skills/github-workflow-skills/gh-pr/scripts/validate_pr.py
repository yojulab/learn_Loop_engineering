"""gh-pr 본문 필수 요소 검증 스크립트."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def validate_pr(text: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not re.search(r"(?im)(closes|fixes)\s+#\d+", text):
        errors.append("Missing issue link ('Closes #N' or 'Fixes #N')")
    if not re.search(r"(?im)^##\s+(요약|summary)", text):
        errors.append("Missing summary section ('## 요약' or '## Summary')")
    if not re.search(r"(?m)^-\s+\[[xX ]\]\s+.+", text):
        errors.append("Missing test checklist item ('- [x] ...')")
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Pull Request description")
    parser.add_argument("path", nargs="?", help="PR 마크다운 파일 경로")
    parser.add_argument("--text", default=None, help="직접 전달할 PR 텍스트")
    args = parser.parse_args(argv)

    content = args.text if args.text is not None else Path(args.path).read_text(encoding="utf-8")
    ok, errors = validate_pr(content)
    if not ok:
        for err in errors:
            print(f"[INVALID] {err}", file=sys.stderr)
        return 1
    print("[VALID] PR description ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
