"""Isolated gate checks; push strings are input data, never executed."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "bin/review-gate.py"

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        spec = importlib.util.spec_from_file_location("gate", SCRIPT)
        self.g = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, {"AGENT_WORKFLOW_HOME": str(self.root / "state"),
                                     "AGENT_WORKFLOW_SCRATCH": str(self.root / "scratch")}):
            spec.loader.exec_module(self.g)
        self.g.STATE = self.root / "state"
        self.g.SCRATCH = self.root / "scratch"
        self.g.RECEIPTS = self.g.STATE / "receipts"
        self.g.EVIDENCE = self.g.STATE / "evidence"
        self.repo = self.make_repo("one")

    def git(self, repo, *args):
        return self.g.git(repo, *args)

    def make_repo(self, name):
        repo = self.root / name
        repo.mkdir()
        self.git(repo, "init", "-q")
        self.git(repo, "config", "user.name", "Fixture")
        self.git(repo, "config", "user.email", "fixture@localhost")
        (repo / "file.txt").write_text("base\n")
        self.commit(repo)
        return repo

    def commit(self, repo):
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", "test(fixture): snapshot")

    def call(self, fn, *args):
        previous = os.getcwd()
        try:
            os.chdir(self.repo)
            with contextlib.redirect_stdout(io.StringIO()) as out:
                fn(*args)
            return out.getvalue()
        finally:
            os.chdir(previous)

    def hook(self, repo=None, command="git push"):
        payload = {"tool_name": "Bash", "cwd": str(repo or self.repo),
                   "tool_input": {"command": command}}
        with patch("sys.stdin", io.StringIO(json.dumps(payload))):
            return self.call(self.g.hook)

    def opt_in(self, repo=None):
        self.git(repo or self.repo, "config", "review-gate.enabled", "true")

    def test_opt_in_and_missing_receipt(self):
        self.assertEqual(self.hook(), "")
        self.opt_in()
        self.assertEqual(json.loads(self.hook())["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_exact_snapshot_then_changed_commit(self):
        self.opt_in()
        (self.repo / "file.txt").write_text("reviewed\n")
        self.call(self.g.receipt, "EXAMPLE")
        self.commit(self.repo)
        self.assertEqual(self.hook(), "")
        (self.repo / "file.txt").write_text("changed\n")
        self.commit(self.repo)
        self.assertTrue(self.hook())

    def test_documented_head_only_limit(self):
        self.opt_in()
        self.call(self.g.receipt, "EXAMPLE")
        self.assertEqual(self.hook(command="git push origin alternate-ref"), "")
        (self.repo / "file.txt").write_text("uncommitted\n")
        self.assertEqual(self.hook(), "")  # Only committed HEAD is checked.

    def test_identity(self):
        self.call(self.g.receipt, "EXAMPLE")
        other = self.make_repo("two")
        self.opt_in(other)
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD^{tree}"), self.git(other, "rev-parse", "HEAD^{tree}"))
        self.assertTrue(self.hook(other))

    def test_skip_logs(self):
        self.opt_in()
        self.assertEqual(self.hook(command='REVIEW_GATE_SKIP="fixture approval" git push'), "")
        self.assertIn("fixture approval", (self.g.STATE / "gate-overrides.log").read_text())

    def test_snapshot_preserves_real_index(self):
        (self.repo / "file.txt").write_text("staged\n")
        self.git(self.repo, "add", ".")
        (self.repo / "file.txt").write_text("unstaged\n")
        index = self.repo / ".git/index"
        before = hashlib.sha256(index.read_bytes()).digest()
        self.g.working_tree(self.repo)
        self.assertEqual(before, hashlib.sha256(index.read_bytes()).digest())

    def test_guide_security_and_evidence(self):
        folder = self.g.SCRATCH / "EXAMPLE"
        folder.mkdir(parents=True)
        hostile = 'D1"><img src=x onerror=alert(1)>'
        (self.repo / "old name.txt").write_text("moved\n" * 20)
        self.commit(self.repo)
        self.git(self.repo, "mv", "old name.txt", 'new "name".txt')  # rename to a Git-quoted path
        paths = ['file.txt', '<img onerror=alert(1)>.txt', 'tab\there.txt', 'café.txt', 'new "name".txt']
        for path in paths[:4]:
            (self.repo / path).write_text('<!--<script></script><script>alert(1)</script>\n')
        guide = {"base": "HEAD", "summary": "fixture", "order": [
            {"path": paths[0], "why": "fixture", "decisions": ["D1", hostile]}],
            "decisions": {"D1": "safe", hostile: "unsafe"}}
        (folder / "review-guide.json").write_text(json.dumps(guide))
        for name in ["map.md", "decisions.md", "app-review-ledger.md", "outcomes.csv", "unrelated.txt"]:
            (folder / name).write_text("fixture")
        with patch.object(self.g.webbrowser, "open") as browser:
            self.call(self.g.guide, "EXAMPLE")
            browser.assert_called_once()
        html = (folder / "review.html").read_text()
        blob = html.split('id="data">', 1)[1].split('</script>', 1)[0]
        data = json.loads(blob)
        self.assertEqual({f["path"] for f in data["files"]}, set(paths))
        self.assertNotIn(hostile, data["decisions"])
        self.assertNotIn(hostile, data["files"][0]["decisions"])
        self.assertNotIn('<', blob)  # nothing in the data can close or comment out its script tag
        self.assertIn("rename from old name.txt", next(f for f in data["files"] if f["path"] == paths[4])["diff"])
        self.assertIn("${esc(f.path)}", html)
        self.assertTrue((folder / "pr.md").is_file())
        archive = next((self.g.EVIDENCE / "EXAMPLE").iterdir())
        self.assertEqual({p.name for p in archive.iterdir()}, {
            "map.md", "decisions.md", "app-review-ledger.md", "outcomes.csv",
            "review-guide.json", "review.html", "pr.md"})

    def test_paths_are_literal(self):
        (self.repo / ":(glob)*.txt").write_text("magic\n")
        (self.repo / "file.txt").write_text("other\n")
        files = self.g.changed_files(self.repo, "HEAD")
        self.assertNotIn("file.txt", files[":(glob)*.txt"])

    def test_bad_ticket_cli(self):
        env = {**os.environ, "AGENT_WORKFLOW_HOME": str(self.g.STATE), "AGENT_WORKFLOW_SCRATCH": str(self.g.SCRATCH)}
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "guide", "--ticket", "../x"],
                                cwd=self.repo, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Bad ticket name", result.stderr)
