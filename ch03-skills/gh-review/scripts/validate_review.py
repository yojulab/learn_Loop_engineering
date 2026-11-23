"""gh-review 심각도 태그 및 파일/라인 근거 검증 스크립트."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def validate_review(text: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not re.search(r"\[(BLOCKER|MAJOR|MINOR|NIT)\]", text):
        errors.append("Missing severity tag ([BLOCKER|MAJOR|MINOR|NIT])")
    if not re.search(r"([\w./-]+:\d+|\bL\d+\b)", text):
        errors.append("Missing file/line reference (e.g. file.py:12 or L12)")
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate code review comments")
    parser.add_argument("path", nargs="?", help="리뷰 마크다운 파일 경로")
    parser.add_argument("--text", default=None, help="직접 전달할 리뷰 텍스트")
    args = parser.parse_args(argv)

    content = args.text if args.text is not None else Path(args.path).read_text(encoding="utf-8")
    ok, errors = validate_review(content)
    if not ok:
        for err in errors:
            print(f"[INVALID] {err}", file=sys.stderr)
        return 1
    print("[VALID] review format ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
