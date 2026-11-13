#!/usr/bin/env python3
"""The only way the Builder reaches the Reader during an eval run.

Usage (from inside the repo under test):
  python3 <eval>/reader.py --brief brief.md --out result.md [--sandbox read-only|workspace-write]
                           [--skill review-loop|review-rubric]

Runs `codex exec` with fixed flags, inlines the skill text, logs the call, and snapshots the
scratch folder after it, so the harness can check what happened. The Builder can't change the
flags; workspace-write is only for an assigned repair, the same as in the real workflow.
"""
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

EVAL = Path(__file__).resolve().parent
SKILLS = EVAL.parent / "skills"


def codex_argv(cwd, sandbox, out, schema=None, env=None):
    """Fixed flags for every Reader call. Shared with run.py so review runs use the same ones."""
    env = os.environ if env is None else env
    argv = [*json.loads(env.get("EVAL_CODEX_BIN", '["codex"]')), "-a", "never", "exec",
            "--ignore-user-config", "--ignore-rules", "--json", "-s", sandbox, "-C", str(cwd), "-o", str(out)]
    if env.get("EVAL_READER_MODEL"):
        argv += ["-m", env["EVAL_READER_MODEL"]]
    argv += ["-c", f'model_reasoning_effort="{env.get("EVAL_READER_EFFORT", "medium")}"']
    if schema:
        argv += ["--output-schema", str(schema)]
    return argv + ["-"]


def usage_from_jsonl(text):
    """Sum token usage over every turn.completed event; None when there were none."""
    total = None
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            total = total or {}
            for k, v in event["usage"].items():
                if isinstance(v, int):
                    total[k] = total.get(k, 0) + v
    return total


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--brief", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--sandbox", choices=["read-only", "workspace-write"], default="read-only")
    p.add_argument("--skill", choices=sorted(d.name for d in SKILLS.iterdir() if d.is_dir()))
    a = p.parse_args()

    run = Path(os.environ["EVAL_RUN"])
    logs = run / "logs"
    log = logs / "reader.jsonl"
    calls = len(log.read_text().splitlines()) if log.exists() else 0
    if calls >= int(os.environ.get("EVAL_MAX_READER_CALLS", "12")):
        sys.exit(f"Reader call limit reached ({calls}). Finish with what you have.")

    brief = a.brief.read_text()
    if a.skill:
        brief = f"Follow this skill.\n\n{(SKILLS / a.skill / 'SKILL.md').read_text()}\n\n---\n\n{brief}"
    cwd = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         check=True).stdout.strip()
    n = calls + 1
    start = time.time()
    with open(logs / f"reader-{n}.jsonl", "w") as stdout, open(logs / f"reader-{n}.err", "w") as stderr:
        proc = subprocess.Popen(codex_argv(cwd, a.sandbox, a.out.resolve()), stdin=subprocess.PIPE, text=True,
                                stdout=stdout, stderr=stderr, start_new_session=True)
        # Its own session escapes the trial's process group, so tell the harness to sweep it too.
        (logs / f"reader-{n}.pgid").write_text(str(proc.pid))
        try:
            proc.communicate(brief, timeout=int(os.environ.get("EVAL_READER_TIMEOUT", "1200")))
            code = proc.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
        try:
            os.killpg(proc.pid, signal.SIGKILL)  # the whole group, timeout or not
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait()
        # Done and swept: drop the record so a later sweep can't hit a reused group id.
        (logs / f"reader-{n}.pgid").unlink(missing_ok=True)
    seconds = round(time.time() - start, 1)

    scratch = Path(os.environ["AGENT_WORKFLOW_SCRATCH"])
    if scratch.exists():  # what the scratch folder held after this call, for the append-only check
        shutil.copytree(scratch, logs / f"scratch-{n}", dirs_exist_ok=True)
    with open(log, "a") as f:
        f.write(json.dumps({
            "n": n, "sandbox": a.sandbox, "skill": a.skill, "exit": code, "seconds": seconds,
            "usage": usage_from_jsonl((logs / f"reader-{n}.jsonl").read_text()),
            "brief_sha256": hashlib.sha256(brief.encode()).hexdigest()}) + "\n")
    if a.out.exists():
        print(a.out.read_text())
    sys.exit(0 if code == 0 else 1)


if __name__ == "__main__":
    main()
