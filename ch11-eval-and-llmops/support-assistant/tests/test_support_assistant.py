from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from langfuse_ops import LangfuseOpsClient
from models import SupportTicket
from prompting import compile_prompt
from regression_compare import compare_prompt_versions
from seed_prompts import seed_default_prompts


class TestSupportAssistant(unittest.TestCase):
    def test_offline_jsonl_seed_compile_and_compare(self) -> None:
        raw = json.loads((APP_DIR / "sample_dataset.json").read_text(encoding="utf-8"))
        dataset = [SupportTicket(**item) for item in raw]
        with tempfile.TemporaryDirectory() as tmp:
            ops = LangfuseOpsClient(Path(tmp))
            self.assertTrue(ops.offline_mode)
            seed_default_prompts(ops)
            p1 = ops.get_prompt("support-answer", label="production")
            compiled = compile_prompt(p1, dataset[0])
            self.assertIn("T-101", compiled)

            cmp_res = compare_prompt_versions(dataset, "production", "candidate", ops)
            self.assertGreater(cmp_res["candidate"]["avg_score"], cmp_res["production"]["avg_score"])
            self.assertTrue((Path(tmp) / "traces.jsonl").is_file())

            ops.promote_label("support-answer", version=2, label="production")
            promoted = ops.get_prompt("support-answer", label="production")
            self.assertEqual(promoted.version, 2)


if __name__ == "__main__":
    unittest.main()
