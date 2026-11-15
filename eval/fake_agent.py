#!/usr/bin/env python3
"""Deterministic transport fixture. Never invokes a model CLI.

Optional fake/config.json: {"mode": "timeout|nonzero|malformed|push_without_receipt"}.
solution/ is copied only by the fake Builder; findings.json is a Reader response.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

EVAL = Path(__file__).resolve().parent


def main():
    provider, *args = sys.argv[1:]
    sys.stdin.read()
    case = Path(os.environ.get("EVAL_FAKE_CASE", "/nonexistent"))
    config = case / "config.json"
    mode = json.loads(config.read_text()).get("mode") if config.exists() else None
    if mode == "timeout":
        time.sleep(3600)
    if mode == "nonzero":
        sys.exit(7)
    if mode == "malformed":
        print("not json")
        return
    if provider == "codex":
        out = Path(args[args.index("-o") + 1])
        findings = case / "findings.json"
        out.write_text(findings.read_text() if "--output-schema" in args and findings.exists()
                       else json.dumps({"findings": [], "covered": [], "not_covered": []}))
        print(json.dumps({"type": "turn.completed", "usage": {
            "input_tokens": 100, "cached_input_tokens": 20, "output_tokens": 30}}))
        return
    if provider != "claude":
        sys.exit("expected claude or codex")
    system = args[args.index("--append-system-prompt") + 1]
    workflow = "How this evaluation wires the workflow" in system
    ticket = os.environ["EVAL_TICKET"]
    scratch = Path(os.environ["AGENT_WORKFLOW_SCRATCH"]) / ticket
    gate = EVAL.parent / "bin" / "review-gate.py"

    def command(*argv, text=None):
        return subprocess.run(argv, input=text, text=True, check=True, capture_output=True)

    if workflow:
        scratch.mkdir(parents=True, exist_ok=True)
        (scratch / "map.md").write_text("Read SPEC.md and app.py.\nNEEDS_BUILDER: follow the specified contract.\n")
        (scratch / "decisions.md").write_text("- D1. Implement SPEC.md without extra behavior.\n")
        (scratch / "brief.md").write_text("Read SPEC.md and review app.py read-only. Return findings.\n")
        command(sys.executable, str(EVAL / "reader.py"), "--brief", str(scratch / "brief.md"),
                "--out", str(scratch / "reader.md"), "--skill", "review-rubric")
    if (case / "solution").exists():
        shutil.copytree(case / "solution", Path.cwd(), dirs_exist_ok=True)
    if workflow:
        command(sys.executable, str(EVAL / "reader.py"), "--brief", str(scratch / "brief.md"),
                "--out", str(scratch / "review.md"), "--skill", "review-rubric")
        command("git", "add", "-A")
        tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True, check=True).stdout.strip()
        (scratch / "repo-review-ledger.md").write_text(f"## Round 1, fake: full\nSnapshot tree {tree}. Fake transport review: CLEAN.\n")
        (scratch / "outcomes.csv").write_text(f"2000-01-01,{ticket},repo,1,fake,0,0,0,0,0,CLEAN,,\n")
        if mode != "push_without_receipt":
            command(sys.executable, "-I", str(gate), "receipt", "--ticket", ticket)
    command("git", "add", "-A")
    command("git", "commit", "-qm", "fix(fixture): apply reference solution")
    if workflow:
        # Exercise the same PreToolUse payload as Claude's Bash hook before the local push.
        command(sys.executable, "-I", str(gate), text=json.dumps({
            "tool_name": "Bash", "tool_input": {"command": "git push origin main"},
            "cwd": str(Path.cwd())}))
    command("git", "push", "origin", "main")
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False,
                      "uuid": "00000000-0000-0000-0000-000000000001",
                      "session_id": "fake-session", "duration_api_ms": 0,
                      "modelUsage": {}, "permission_denials": [],
                      "result": "Applied reference fixture", "num_turns": 3, "duration_ms": 100,
                      "total_cost_usd": 0, "usage": {"input_tokens": 200, "output_tokens": 80}}))


if __name__ == "__main__":
    main()
