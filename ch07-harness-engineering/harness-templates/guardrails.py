"""제7장: 파괴적 명령 5줄 가드레일 규칙 검증기."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CORE_GUARDRAIL_RULES: tuple[tuple[str, str, str], ...] = (
    ("GR-01", r"(^|\s|;|&&|\|\|)rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)", "재귀 강제 삭제(rm -rf) 금지"),
    ("GR-02", r"\bgit\s+push\b[^\n]*(--force-with-lease|--force|\s-f(\s|$))", "원격 강제 푸시(git push --force/-f) 금지"),
    ("GR-03", r"\bgit\s+reset\s+--hard\b", "하드 리셋(git reset --hard) 금지"),
    ("GR-04", r"\bdrop\s+table\b", "SQL DROP TABLE 파괴 명령 금지"),
    ("GR-05", r"(\bfind\b[^\n]*\s-delete\b|(^|\s)mkfs(\.[a-z0-9]+)?\b)", "파일시스템 포맷(mkfs) 및 find -delete 금지"),
)


def check_command_safety(cmd: str) -> tuple[bool, list[str]]:
    """명령 문자열이 5줄 가드레일을 위반하는지 검사한다."""
    violations: list[str] = []
    for rule_id, pattern, msg in CORE_GUARDRAIL_RULES:
        if re.search(pattern, cmd, flags=re.IGNORECASE):
            violations.append(f"[{rule_id}] {msg}")
    return len(violations) == 0, violations


def check_script_file(path: Path | str) -> tuple[bool, list[str]]:
    """스크립트 파일의 각 줄을 검사해 가드레일 위반 내역을 반환한다."""
    violations: list[str] = []
    for idx, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        ok, msgs = check_command_safety(stripped)
        if not ok:
            for msg in msgs:
                violations.append(f"line {idx}: {msg}")
    return len(violations) == 0, violations


def main(argv: list[str] | None = None) -> int:
    import json
    parser = argparse.ArgumentParser(description="5줄 파괴 명령 가드레일 검증기")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cmd", help="검사할 명령 문자열")
    group.add_argument("--file", help="검사할 스크립트 파일 경로")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args(argv)

    ok, msgs = check_command_safety(args.cmd) if args.cmd is not None else check_script_file(args.file)
    if args.json:
        print(json.dumps({"safe": ok, "violations": msgs}, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    if not ok:
        for m in msgs:
            print(f"[BLOCKED] {m}")
        return 1
    print("[SAFE] Guardrail check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
