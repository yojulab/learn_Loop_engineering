"""ch05-rag-and-memory/memory_pattern 단위 테스트."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

MP_DIR = Path(__file__).resolve().parent.parent
if str(MP_DIR) not in sys.path:
    sys.path.insert(0, str(MP_DIR))

from agentic_rag import AgenticRetriever  # noqa: E402
from memory_manager import MemoryManager  # noqa: E402


class TestMemoryPattern(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.tasks_file = self.tmpdir / "TASKS.md"
        self.journal_file = self.tmpdir / "JOURNAL.md"
        shutil.copy(MP_DIR / "TASKS.md", self.tasks_file)
        shutil.copy(MP_DIR / "JOURNAL.md", self.journal_file)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_memory_manager_parse_update_and_journal(self) -> None:
        mgr = MemoryManager(self.tasks_file, self.journal_file)
        tasks = mgr.parse_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].status, "done")
        next_task = mgr.next_pending_task()
        self.assertIsNotNone(next_task)
        assert next_task is not None
        self.assertEqual(next_task.task_id, "CALC-002")

        self.assertTrue(mgr.mark_task_done("CALC-002", "무료 배송 테스트 통과"))
        self.assertTrue(mgr.mark_task_blocked("CALC-003", "운영팀 환율 승인 대기"))

        updated = {t.task_id: t for t in mgr.parse_tasks()}
        self.assertEqual(updated["CALC-002"].status, "done")
        self.assertEqual(updated["CALC-003"].status, "blocked")
        self.assertIsNone(mgr.next_pending_task())

        entry = mgr.append_journal("worker-1", "CALC-002 완료", "unittest 4건 통과")
        self.assertEqual(entry["actor"], "worker-1")
        journal_text = self.journal_file.read_text(encoding="utf-8")
        self.assertIn("CALC-002 완료", journal_text)
        self.assertIn("unittest 4건 통과", journal_text)

    def test_agentic_rag_topk_and_excerpt_limit(self) -> None:
        corpus_files = list((MP_DIR / "corpus").glob("*.md"))
        self.assertGreaterEqual(len(corpus_files), 3)

        retriever = AgenticRetriever(MP_DIR / "corpus")
        results = retriever.search("Top-K max_chars_per_excerpt 발췌", top_k=2, max_chars_per_excerpt=120)
        self.assertGreaterEqual(len(results), 1)
        self.assertLessEqual(len(results), 2)
        self.assertEqual(results[0].source, "02_agentic_rag.md")
        for chunk in results:
            self.assertLessEqual(len(chunk.excerpt), 120)

        empty = retriever.search("zzzznonexistentkeywordzzzz", top_k=3)
        self.assertEqual(empty, [])


if __name__ == "__main__":
    unittest.main()
