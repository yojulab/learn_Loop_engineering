"""gh-address-review 리뷰 대응 3요소 검증 스크립트."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def validate_address_review(text: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not re.search(r"(?i)(#comment-\d+|\bR-\d+\b|comment\s+id)", text):
        errors.append("Missing review comment ID (e.g. #comment-101 or R-1)")
    if not re.search(r"(?im)(수정\s*내역|fix\s*:)", text):
        errors.append("Missing fix summary ('수정 내역:' or 'Fix:')")
    if not re.search(r"(?im)(회신|reply\s*:)", text):
        errors.append("Missing reply note ('회신:' or 'Reply:')")
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate review response note")
    parser.add_argument("path", nargs="?", help="리뷰 대응 마크다운 파일 경로")
    parser.add_argument("--text", default=None, help="직접 전달할 리뷰 대응 텍스트")
    args = parser.parse_args(argv)

    content = args.text if args.text is not None else Path(args.path).read_text(encoding="utf-8")
    ok, errors = validate_address_review(content)
    if not ok:
        for err in errors:
            print(f"[INVALID] {err}", file=sys.stderr)
        return 1
    print("[VALID] address-review format ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
