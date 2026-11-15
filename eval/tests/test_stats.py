import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("stats", Path(__file__).resolve().parents[1] / "stats.py")
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)


class Stats(unittest.TestCase):
    def test_counts(self):
        rows = "\n".join([
            "2026-01-01,T1,app,1,aaa,1,1,0,0,0,NEEDS_BUILDER,,",
            "2026-01-01,T1,app,1,aaa,1,1,0,0,0,NEEDS_BUILDER,,",   # exact duplicate: dropped
            "2026-01-01,T1,app,1b,aaa,1,1,0,0,0,INCOMPLETE,,",     # same snapshot: findings counted once
            "2026-01-02,T1,app,2,bbb,0,0,2,0,0,CLEAN,,",
            "2026-01-03,T1,app,human,bbb,,,,,,APPROVED,2,1",
            "2026-01-03,X1,app,1,ccc,5,5,0,0,0,BLOCK,,",           # excluded below
        ])
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(rows + "\n")
        s = stats.summarize(stats.load([f.name], exclude="^X"))
        self.assertEqual((s["internal_rounds"], s["incomplete_rounds"], s["reached_clean"]), (3, 1, 1))
        self.assertEqual((s["blocking"], s["should_fix"], s["optional_accepted"]), (1, 1, 2))
        self.assertEqual((s["human_reviews"], s["human_changes"], s["human_bugs"]), (1, 2, 1))
        self.assertIn("2 of 3 (67%)", stats.markdown(s))
