"""제7장: 깨진 경로 참조, 고아 문서, 오래된 목차 점검(Doc Gardening) 도구."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ENTRY_DOCS = {"README.md", "INDEX.md", "AGENTS.md"}


@dataclass
class DocIssue:
    file: str
    issue_type: str  # "broken_link" | "orphan_doc" | "stale_index"
    detail: str


def audit_docs(repo_root: Path | str) -> list[DocIssue]:
    """대상 저장소의 마크다운 링크 무결성 및 고아 문서를 감사한다."""
    root = Path(repo_root)
    if not root.is_dir():
        return []

    md_files = sorted(root.rglob("*.md"))
    referenced: set[Path] = set()
    issues: list[DocIssue] = []

    for md in md_files:
        rel_md = str(md.relative_to(root))
        text = md.read_text(encoding="utf-8", errors="ignore")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                itype = "stale_index" if md.name in ENTRY_DOCS else "broken_link"
                issues.append(
                    DocIssue(
                        file=rel_md,
                        issue_type=itype,
                        detail=f"Target does not exist: {raw_target}",
                    )
                )
            else:
                referenced.add(resolved)

    for md in md_files:
        if md.name in ENTRY_DOCS:
            continue
        if md.resolve() not in referenced:
            issues.append(
                DocIssue(
                    file=str(md.relative_to(root)),
                    issue_type="orphan_doc",
                    detail="Document is not referenced by any README/INDEX/markdown link",
                )
            )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="제7장 문서 정원 가꾸기(Doc Gardening) 점검기")
    parser.add_argument("--root", required=True, help="점검할 문서 루트 경로")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    issues = audit_docs(args.root)
    if args.json:
        print(json.dumps([asdict(i) for i in issues], ensure_ascii=False, indent=2))
    else:
        if not issues:
            print(f"[DOCS-OK] No broken links or orphan docs in {args.root}")
        else:
            for issue in issues:
                print(f"[{issue.issue_type.upper()}] {issue.file}: {issue.detail}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
