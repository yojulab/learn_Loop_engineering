"""gh-issue 필수 섹션 검증 스크립트."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def validate_issue(text: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not re.search(r"(?m)^(#\s+.+|제목\s*:)", text):
        errors.append("Missing issue title ('# ...' or '제목:')")
    if not re.search(r"(?im)(라벨\s*:|labels\s*:)", text):
        errors.append("Missing labels line ('라벨:' or 'Labels:')")
    if not re.search(r"(?im)(재현\s*절차|steps\s+to\s+reproduce)", text):
        errors.append("Missing reproduction steps section")
    if not re.search(r"(?im)(기대\s*결과|expected)", text):
        errors.append("Missing expected behavior section")
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate GitHub issue markdown")
    parser.add_argument("path", nargs="?", help="이슈 마크다운 파일 경로")
    parser.add_argument("--text", default=None, help="직접 전달할 이슈 텍스트")
    args = parser.parse_args(argv)

    content = args.text if args.text is not None else Path(args.path).read_text(encoding="utf-8")
    ok, errors = validate_issue(content)
    if not ok:
        for err in errors:
            print(f"[INVALID] {err}", file=sys.stderr)
        return 1
    print("[VALID] issue format ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
