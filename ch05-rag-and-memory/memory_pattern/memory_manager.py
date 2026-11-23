"""제5장: TASKS.md & JOURNAL.md 지속 상태 파싱/갱신/결정·증거 기록 관리자."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

TASK_LINE_RE = re.compile(
    r"^-\s+\[(?P<mark>[xX !])\]\s+\*\*(?P<id>[A-Za-z0-9_-]+)\*\*:\s*(?P<body>.+)$"
)


@dataclass
class TaskItem:
    task_id: str
    title: str
    status: str  # "done" | "pending" | "blocked"
    note: str = ""


class MemoryManager:
    """파일 기반 지속 기억(TASKS.md, JOURNAL.md) 관리자."""

    def __init__(self, tasks_path: Path | str, journal_path: Path | str) -> None:
        self.tasks_path = Path(tasks_path)
        self.journal_path = Path(journal_path)

    def parse_tasks(self) -> list[TaskItem]:
        if not self.tasks_path.is_file():
            return []
        items: list[TaskItem] = []
        for raw_line in self.tasks_path.read_text(encoding="utf-8").splitlines():
            m = TASK_LINE_RE.match(raw_line.strip())
            if not m:
                continue
            mark = m.group("mark").lower()
            body = m.group("body").strip()
            note = ""
            if " (" in body and body.endswith(")"):
                title_part, note_part = body.rsplit(" (", 1)
                title = title_part.strip()
                note = note_part[:-1].strip()
            else:
                title = body

            if mark == "x":
                status = "done"
            elif mark == "!" or "[BLOCKED]" in body:
                status = "blocked"
            else:
                status = "pending"
            items.append(TaskItem(task_id=m.group("id"), title=title, status=status, note=note))
        return items

    def next_pending_task(self) -> TaskItem | None:
        for item in self.parse_tasks():
            if item.status == "pending":
                return item
        return None

    def _update_task_line(self, task_id: str, new_mark: str, suffix_note: str) -> bool:
        if not self.tasks_path.is_file():
            return False
        lines = self.tasks_path.read_text(encoding="utf-8").splitlines()
        updated = False
        new_lines: list[str] = []
        for line in lines:
            m = TASK_LINE_RE.match(line.strip())
            if m and m.group("id") == task_id:
                body = m.group("body").strip()
                base_title = body.rsplit(" (", 1)[0].strip() if (" (" in body and body.endswith(")")) else body
                note_text = f" ({suffix_note})" if suffix_note else ""
                new_lines.append(f"- [{new_mark}] **{task_id}**: {base_title}{note_text}")
                updated = True
            else:
                new_lines.append(line)
        if updated:
            self.tasks_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return updated

    def mark_task_done(self, task_id: str, note: str = "완료") -> bool:
        return self._update_task_line(task_id, "x", note)

    def mark_task_blocked(self, task_id: str, reason: str = "차단됨") -> bool:
        return self._update_task_line(task_id, "!", f"[BLOCKED] {reason}")

    def append_journal(self, actor: str, decision: str, evidence: str) -> dict[str, str]:
        """대화 전문 덤프 없이 결정과 검증 증거만 한 줄 요약으로 JOURNAL.md에 추가한다."""
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        clean_decision = " ".join(decision.strip().splitlines())
        clean_evidence = " ".join(evidence.strip().splitlines())
        entry_line = f"- `{ts}` | **{actor.strip()}** | 결정: {clean_decision} | 증거: {clean_evidence}"
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        existing = self.journal_path.read_text(encoding="utf-8") if self.journal_path.is_file() else "# JOURNAL\n"
        if existing and not existing.endswith("\n"):
            existing += "\n"
        self.journal_path.write_text(existing + entry_line + "\n", encoding="utf-8")
        return {
            "timestamp": ts,
            "actor": actor.strip(),
            "decision": clean_decision,
            "evidence": clean_evidence,
        }


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    parser = argparse.ArgumentParser(description="TASKS.md / JOURNAL.md 지속 메모리 상태 조회기")
    parser.add_argument("--dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--status", action="store_true", help="현재 TASKS/JOURNAL 상태 출력")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args(argv)
    base = Path(args.dir)
    mgr = MemoryManager(base / "TASKS.md", base / "JOURNAL.md")
    tasks_lines = mgr.tasks_path.read_text(encoding="utf-8").splitlines() if mgr.tasks_path.is_file() else []
    journal_lines = mgr.journal_path.read_text(encoding="utf-8").splitlines() if mgr.journal_path.is_file() else []
    report = {
        "tasks_total": sum(1 for ln in tasks_lines if ln.strip().startswith("- [")),
        "tasks_done": sum(1 for ln in tasks_lines if ln.strip().startswith("- [x]")),
        "tasks_pending": sum(1 for ln in tasks_lines if ln.strip().startswith("- [ ]")),
        "journal_entries": sum(1 for ln in journal_lines if ln.strip().startswith("- ")),
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"TASKS: {report['tasks_done']}/{report['tasks_total']} done | JOURNAL entries: {report['journal_entries']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
