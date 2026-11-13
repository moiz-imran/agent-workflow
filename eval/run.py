#!/usr/bin/env python3
"""Evaluate the agent workflow on small fictional repos.

  preflight [--live]                 check tools and (with --live) isolated auth, without spending usage
  run --suite review|task|all        run trials; fake agents unless --live
  report <results-dir>               summarise results.jsonl as Markdown

Suites:
  review  A fresh Reader reviews a change with seeded bugs. Scores recall and false alarms.
  task    The same task done by one agent alone (single) and by the Builder + Reader workflow
          (workflow). Scores hidden tests, time, tokens, new lint issues and, for the workflow,
          whether the rules were kept.

Every trial runs in its own folder with its own HOME, Claude config and Codex home, a local bare
`origin`, and only the arm's instructions. See eval/README.md.
"""
import argparse
import importlib.util
import json
import os
import random
import re
import shutil
import signal
import statistics
import subprocess
import sys
import time
from pathlib import Path

EVAL = Path(__file__).resolve().parent
ROOT = EVAL.parent
CASES = EVAL / "cases"
GATE = ROOT / "bin" / "review-gate.py"
SCHEMA = EVAL / "findings.schema.json"
sys.path.insert(0, str(EVAL))
import reader  # noqa: E402  (shared Codex flags and usage parsing)

# Anything that could switch billing to an API key or leak a credential into a trial.
SECRET = re.compile(r"API_KEY|TOKEN|SECRET|PASSWORD|^ANTHROPIC_|^OPENAI_|^AWS_|^GH_|^GITHUB_|^CLAUDE_|^CODEX_", re.I)
PASS_THROUGH = {"CLAUDE_CODE_OAUTH_TOKEN"}
TEST_LINE = re.compile(r"^(test\w*) \(([\w.]+)\)(?:\n.*?)? \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)$",
                       re.M)


# ---------- staging ----------

def git(cwd, *args, env=None, check=True):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env,
                          check=check).stdout.strip()


def load_cases(suite, only=None):
    cases = []
    for d in sorted(CASES.iterdir()):
        if (d / "case.json").exists():
            c = json.loads((d / "case.json").read_text())
            if suite in ("all", c["kind"]) and (not only or d.name in only):
                cases.append({**c, "id": d.name, "dir": d})
    return cases


def stage(case, trial_dir):
    """Base commit (tagged `base`), the change under review on top for review cases, and a bare origin."""
    repo = trial_dir / "repo"
    shutil.copytree(case["dir"] / "repo", repo)
    env = {**os.environ, "GIT_AUTHOR_NAME": "Eval", "GIT_AUTHOR_EMAIL": "eval@localhost",
           "GIT_COMMITTER_NAME": "Eval", "GIT_COMMITTER_EMAIL": "eval@localhost"}
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Eval")
    git(repo, "config", "user.email", "eval@localhost")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base", env=env)
    git(repo, "tag", "base")
    if (case["dir"] / "change").exists():
        shutil.copytree(case["dir"] / "change", repo, dirs_exist_ok=True)
        for rel in case.get("delete", []):
            (repo / rel).unlink()
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", case.get("change_message", "change under review"), env=env)
    origin = trial_dir / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    git(repo, "remote", "add", "origin", str(origin))
    git(repo, "push", "-q", "origin", "main")
    return repo


def child_env(trial_dir, args, ticket):
    """Isolated environment: own HOME and configs, no API keys, harness settings for the trial."""
    env = {k: v for k, v in os.environ.items() if k in PASS_THROUGH or not SECRET.search(k)}
    home = trial_dir / "home"
    (home / ".claude").mkdir(parents=True, exist_ok=True)
    (home / ".codex").mkdir(parents=True, exist_ok=True)
    if args.live:
        auth = Path.home() / ".codex" / "auth.json"
        shutil.copy(auth, home / ".codex" / "auth.json")
        os.chmod(home / ".codex" / "auth.json", 0o600)
    for d in ("logs", "scratch", "state"):
        (trial_dir / d).mkdir(exist_ok=True)
    env.update({
        "HOME": str(home), "CLAUDE_CONFIG_DIR": str(home / ".claude"), "CODEX_HOME": str(home / ".codex"),
        "AGENT_WORKFLOW_HOME": str(trial_dir / "state"), "AGENT_WORKFLOW_SCRATCH": str(trial_dir / "scratch"),
        "EVAL_RUN": str(trial_dir), "EVAL_TICKET": ticket,
        "EVAL_MAX_READER_CALLS": str(args.max_reader_calls), "EVAL_READER_EFFORT": args.codex_effort,
        "EVAL_CODEX_BIN": json.dumps(agent_bin("codex", args)),
        "GIT_CONFIG_NOSYSTEM": "1", "PYTHONDONTWRITEBYTECODE": "1",
    })
    if args.codex_model:
        env["EVAL_READER_MODEL"] = args.codex_model
    if not args.live:
        env["EVAL_FAKE_CASE"] = str(trial_dir / "case")
    return env


def agent_bin(name, args):
    if args.live:
        return [shutil.which(name) or name]
    return [sys.executable, str(EVAL / "fake_agent.py"), name]


def run_proc(argv, cwd, env, stdin_text, timeout, out, err):
    """Run in its own process group; on timeout, TERM then KILL the whole group."""
    start = time.time()
    with open(out, "w") as o, open(err, "w") as e:
        p = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=o, stderr=e, text=True,
                             start_new_session=True)
        try:
            p.communicate(stdin_text, timeout=timeout)
            status = "ok" if p.returncode == 0 else f"exit {p.returncode}"
        except subprocess.TimeoutExpired:
            status = "timeout"
            kill_group(p.pid, signal.SIGTERM)
            deadline = time.time() + 5  # give the whole group, not just the leader, a chance to exit cleanly
            while time.time() < deadline and group_alive(p.pid):
                p.poll()
                time.sleep(0.1)
        kill_group(p.pid, signal.SIGKILL)  # descendants can outlive the leader; sweep them every time
        p.wait()
    return status, round(time.time() - start, 1)


def group_alive(pid):
    try:
        os.killpg(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def kill_group(pid, sig):
    try:
        os.killpg(pid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def clean_env(home):
    """For grading and lint: no credentials and a throwaway HOME, so fixture code can't reach either."""
    home.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not SECRET.search(k)}
    return {**env, "HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1"}


# ---------- review suite ----------

def review_trial(case, trial_dir, args):
    repo = stage(case, trial_dir)
    env = child_env(trial_dir, args, case["id"])
    rubric = (ROOT / "skills" / "review-rubric" / "SKILL.md").read_text()
    brief = f"Follow this skill.\n\n{rubric}\n\n---\n\n{(EVAL / 'arms' / 'review.md').read_text()}"
    result = trial_dir / "logs" / "findings.json"
    argv = reader.codex_argv(repo, "read-only", result, SCHEMA, env)
    status, seconds = run_proc(argv, repo, env, brief, args.minutes * 60,
                               trial_dir / "logs" / "codex.jsonl", trial_dir / "logs" / "codex.err")
    row = {"seconds": seconds, "status": status,
           "codex_usage": reader.usage_from_jsonl((trial_dir / "logs" / "codex.jsonl").read_text())}
    try:
        findings = valid_findings(json.loads(result.read_text()))
    except (OSError, ValueError) as e:
        return {**row, "status": "invalid output" if status == "ok" else status, "error": str(e)[:200]}
    gold = json.loads((case["dir"] / "gold.json").read_text())
    adjudicated = json.loads((trial_dir / "adjudications.json").read_text()) \
        if (trial_dir / "adjudications.json").exists() else {}
    return {**row, **score_review(findings["findings"], gold, args.window, adjudicated),
            "not_covered": findings["not_covered"]}


def valid_findings(data):
    """Check the shape --output-schema promised. Raises ValueError when it's wrong."""
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        raise ValueError("no findings list")
    for key in ("covered", "not_covered"):
        if not (isinstance(data.get(key), list) and all(isinstance(x, str) for x in data[key])):
            raise ValueError(f"{key} must be a list of paths")
    for f in data["findings"]:
        if not (isinstance(f, dict) and all(isinstance(f.get(k), str) and f[k] for k in ("path", "title", "evidence"))
                and all(isinstance(f.get(k), int) and not isinstance(f[k], bool) and f[k] > 0 for k in ("start_line", "end_line"))
                and f["start_line"] <= f["end_line"] and f.get("severity") in ("Blocking", "Should-fix", "Optional")):
            raise ValueError(f"bad finding: {json.dumps(f)[:120]}")
    return data


def score_review(findings, gold, window=3, adjudicated=None):
    """One-to-one match of findings to seeded bugs by path and line window.

    Unmatched findings are 'unadjudicated' unless adjudications.json ({finding index: "real"|"false"})
    says otherwise. Duplicates (a second finding on an already-caught bug) are counted on their own.
    """
    adjudicated = adjudicated or {}
    caught, dupes, unmatched = {}, 0, []
    for i, f in enumerate(findings):
        path = os.path.normpath(f["path"]).lstrip("./")
        hits = [g for g in gold if g["path"] == path
                and f["start_line"] <= g["end_line"] + window and f["end_line"] >= g["start_line"] - window]
        free = [g for g in hits if g["id"] not in caught]
        if free:
            caught[free[0]["id"]] = f["severity"]
        elif hits:
            dupes += 1
        else:
            unmatched.append(i)
    verdict = {i: adjudicated.get(str(i), "unadjudicated") for i in unmatched}
    required = [g for g in gold if g["severity"] in ("Blocking", "Should-fix")]
    return {
        "seeded": len(gold), "caught": len(caught),
        "caught_required": sum(g["id"] in caught for g in required), "seeded_required": len(required),
        "missed": [g["id"] for g in gold if g["id"] not in caught],
        "duplicates": dupes,
        "false_alarms": sum(v == "false" for v in verdict.values()),
        "novel_real": sum(v == "real" for v in verdict.values()),
        "unadjudicated": sum(v == "unadjudicated" for v in verdict.values()),
        "unmatched_by_severity": {s: sum(findings[i]["severity"] == s for i in unmatched)
                                  for s in ("Blocking", "Should-fix", "Optional")},
    }


# ---------- task suite ----------

def task_trial(case, arm, trial_dir, args):
    repo = stage(case, trial_dir)
    env = child_env(trial_dir, args, case["id"])
    settings = trial_dir / "settings.json"
    if arm == "workflow":
        system = (EVAL / "arms" / "workflow.md").read_text() \
            .replace("__CLAUDE_MD__", (ROOT / "templates" / "CLAUDE.md").read_text()) \
            .replace("__READER__", str(EVAL / "reader.py")).replace("__GATE__", str(GATE)) \
            .replace("__TICKET__", case["id"]).replace("__SCRATCH__", env["AGENT_WORKFLOW_SCRATCH"])
        settings.write_text(json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": f'python3 -I "{GATE}"', "timeout": 60}]}]}}))
        git(repo, "config", "review-gate.enabled", "true")
    else:
        system = (EVAL / "arms" / "single.md").read_text()
        settings.write_text("{}")
    argv = [*agent_bin("claude", args), "-p", "--output-format", "stream-json", "--verbose",
            "--model", args.claude_model, "--effort", args.claude_effort, "--max-turns", str(args.max_turns),
            "--permission-mode", "dontAsk",
            "--allowedTools", "Read", "Edit", "Write", "Glob", "Grep", "Bash(python3:*)", "Bash(git:*)",
            "--settings", str(settings), "--setting-sources", "project",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--append-system-prompt", system]
    prompt = (case["dir"] / "prompt.md").read_text()
    status, seconds = run_proc(argv, repo, env, prompt, args.minutes * 60,
                               trial_dir / "logs" / "claude.jsonl", trial_dir / "logs" / "claude.err")
    sweep_readers(trial_dir)
    result = claude_result((trial_dir / "logs" / "claude.jsonl").read_text())
    if status == "ok" and not result:
        status = "no result"
    elif status == "ok" and (result.get("is_error") or result.get("subtype") != "success"):
        status = f"agent stopped: {result.get('subtype')}"  # e.g. error_max_turns; still graded below
    row = {"seconds": seconds, "status": status, "claude": result, "reader_calls": reader_calls(trial_dir)}
    row["codex_usage"] = sum_usage(c.get("usage") for c in row["reader_calls"])
    if (trial_dir / "scratch").exists():
        shutil.copytree(trial_dir / "scratch", trial_dir / "logs" / "scratch-final", dirs_exist_ok=True)
    row["tests"] = grade(case, repo, trial_dir)
    row["quality"] = quality(repo, args.quality_cmd)
    row["pushed"] = git(trial_dir / "origin.git", "rev-parse", "main") != git(repo, "rev-parse", "base")
    if arm == "workflow":
        row["rules"] = rules(trial_dir, repo, case["id"])
    return row


def sweep_readers(trial_dir):
    """Reader calls run in their own sessions, outside the trial's process group: kill what's left."""
    for pgid in (trial_dir / "logs").glob("reader-*.pgid"):
        kill_group(int(pgid.read_text()), signal.SIGKILL)


def claude_result(text):
    """Fields from the final `result` event of a stream-json run; missing means unknown."""
    for line in reversed(text.splitlines()):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "result":
            return {k: e.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms",
                                          "total_cost_usd", "usage", "modelUsage", "permission_denials")}
    return None


def reader_calls(trial_dir):
    log = trial_dir / "logs" / "reader.jsonl"
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def sum_usage(usages):
    total = None
    for u in usages:
        if u:
            total = total or {}
            for k, v in u.items():
                total[k] = total.get(k, 0) + v
    return total


def unittest_results(cwd, command):
    """({test id: outcome}, exit code) from verbose unittest output; ({}, code) if nothing ran."""
    try:
        out = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300,
                             env=clean_env(Path(cwd).parent / f"{Path(cwd).name}-home"), start_new_session=True)
    except subprocess.TimeoutExpired:
        return {}, "timeout"
    # Python 3.11+ prints "test_x (pkg.mod.Class.test_x)"; older versions omit the method name.
    return {m[1] if m[1].endswith("." + m[0]) else f"{m[1]}.{m[0]}": m[2]
            for m in TEST_LINE.findall(out.stderr + out.stdout)}, out.returncode


def grade(case, repo, trial_dir):
    """Hidden tests on the base and on the result, in separate copies the agent never saw.

    fail_to_pass: tests that fail on base and pass now (the task). pass_to_pass: tests that
    passed on base and still pass (nothing broken).
    """
    results = {}
    for name, ref in (("base", "base"), ("after", None)):
        copy = trial_dir / f"grade-{name}"
        if ref:
            copy.mkdir()
            subprocess.run(f"git -C '{repo}' archive {ref} | tar -x -C '{copy}'", shell=True, check=True)
        else:  # the working tree as the agent left it, committed or not
            shutil.copytree(repo, copy, ignore=shutil.ignore_patterns(".git"))
        shutil.copytree(case["dir"] / "hidden", copy, dirs_exist_ok=True)
        results[name] = unittest_results(copy, case["grade"])
    (base, _), (after, after_exit) = results["base"], results["after"]
    if not base:
        raise RuntimeError(f"hidden tests didn't run on base for {case['id']}: fix the case")
    f2p = [t for t, r in base.items() if r != "ok"]
    p2p = [t for t, r in base.items() if r == "ok"]
    failing = sorted(t for t, r in {**dict.fromkeys(base, None), **after}.items() if r != "ok")
    return {
        "fail_to_pass": sum(after.get(t) == "ok" for t in f2p), "fail_to_pass_total": len(f2p),
        "pass_to_pass": sum(after.get(t) == "ok" for t in p2p), "pass_to_pass_total": len(p2p),
        "solved": after_exit == 0 and not failing,  # every hidden test ran and passed, and the run exited cleanly
        "after_exit": after_exit, "failing": failing,
    }


def quality(repo, quality_cmd=None):
    """Lint issues the agent introduced: issues after minus issues on base, matched by (rule, path).

    Default analyzer is ruff. --quality-cmd replaces it with any command that prints a JSON list of
    {"rule": ..., "path": ...} for the current directory (for example a Sonar adapter).
    """
    def issues(cwd):
        argv = quality_cmd if quality_cmd else \
            ["ruff", "check", "--no-cache", "--exit-zero", "--output-format", "json", "."]
        r = subprocess.run(argv, shell=bool(quality_cmd), cwd=cwd, capture_output=True, text=True, timeout=600,
                           env=clean_env(repo.parent / "quality-home"))
        data = json.loads(r.stdout)  # empty or broken output raises: never read as "no issues"
        if r.returncode != 0 or not isinstance(data, list):
            raise RuntimeError(f"exit {r.returncode}: {r.stderr[:200]}")
        if quality_cmd:
            found = [(i.get("rule"), i.get("path")) for i in data]
            if not all(isinstance(x, str) and x for pair in found for x in pair):
                raise ValueError("every issue needs a non-empty rule and path")
            return found
        return [(i["code"] or "syntax-error", os.path.relpath(i["filename"], cwd)) for i in data]

    if not quality_cmd and not shutil.which("ruff"):
        return None
    base = repo.parent / "quality-base"
    base.mkdir(exist_ok=True)
    subprocess.run(f"git -C '{repo}' archive base | tar -x -C '{base}'", shell=True, check=True)
    try:
        before, after = issues(base), issues(repo)
    except (ValueError, KeyError, TypeError, AttributeError, OSError, RuntimeError, subprocess.TimeoutExpired) as e:
        return {"error": f"{type(e).__name__}: {e}"[:300]}
    left = list(before)
    new = []
    for i in after:
        if i in left:
            left.remove(i)
        else:
            new.append(i)
    return {"analyzer": "custom" if quality_cmd else "ruff", "new": len(new), "fixed": len(left),
            "new_rules": sorted({r for r, _ in new})}


def rules(trial_dir, repo, ticket):
    """Did the workflow arm keep its rules? Each check is True, False, or None when it can't tell."""
    scratch = trial_dir / "logs" / "scratch-final" / ticket
    calls = reader_calls(trial_dir)
    read = lambda p: p.read_text() if p.exists() else ""  # noqa: E731
    ledgers = sorted(scratch.glob("*-review-ledger.md")) if scratch.exists() else []

    # Append-only: each later snapshot of a ledger starts with the earlier one.
    versions = {}
    for snap in sorted((trial_dir / "logs").glob("scratch-[0-9]*"), key=lambda p: int(p.name.split("-")[1])):
        for f in (snap / ticket).glob("*-review-ledger.md"):
            versions.setdefault(f.name, []).append(f.read_text())
    for f in ledgers:
        versions.setdefault(f.name, []).append(f.read_text())
    append_only = all(b.startswith(a) for v in versions.values() for a, b in zip(v, v[1:])) if versions else None

    gate = load_gate(trial_dir)
    origin_url = git(repo, "remote", "get-url", "origin")
    base_tree = git(repo, "rev-parse", "base^{tree}")
    pushed = git(trial_dir / "origin.git", "rev-parse", "main^{tree}")
    return {
        "reader_used": bool(calls),
        "reviews_read_only": all(c["sandbox"] == "read-only" for c in calls if c.get("skill") == "review-rubric"),
        # Small tasks skip the investigation map, so no map is "not applicable", not broken.
        "map_has_needs_builder": ("NEEDS_BUILDER" in read(scratch / "map.md")) if (scratch / "map.md").exists() else None,
        "decisions_numbered": bool(re.search(r"(?m)^\W*D\d+\b", read(scratch / "decisions.md"))),
        "review_ledger": any("## Round" in f.read_text() for f in ledgers),
        "ledger_append_only": append_only,
        "outcomes_rows": bool(read(scratch / "outcomes.csv").strip()),
        "push_had_receipt": None if pushed == base_tree else gate.receipt_path(origin_url, pushed).exists(),
        "no_gate_skip": not (trial_dir / "state" / "gate-overrides.log").exists(),
    }


def load_gate(trial_dir):
    spec = importlib.util.spec_from_file_location("review_gate", GATE)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    g.RECEIPTS = trial_dir / "state" / "receipts"
    return g


# ---------- commands ----------

def preflight(args):
    """Check tools; with --live, check isolated auth with one tiny model call."""
    ok = True
    def say(good, what):
        nonlocal ok
        ok &= bool(good)
        print(("ok   " if good else "FAIL ") + what)
    for tool in ("git", "python3"):
        say(shutil.which(tool), tool)
    print(("ok   " if shutil.which("ruff") else "warn ") + "ruff (lint scoring is skipped without it)")
    if args.live:
        for tool in ("claude", "codex"):
            say(shutil.which(tool), tool)
        say(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"), "CLAUDE_CODE_OAUTH_TOKEN set (create one with `claude setup-token`)")
        say((Path.home() / ".codex" / "auth.json").exists(), "~/.codex/auth.json (sign in with `codex login`)")
        if ok:
            tmp = Path(args.output) / "preflight"
            shutil.rmtree(tmp, ignore_errors=True)
            tmp.mkdir(parents=True)
            env = child_env(tmp, args, "preflight")
            # `claude auth status` passes with a mangled token, so make one tiny real call instead.
            for argv in (["claude", "-p", "Reply with the word ok.", "--model", "haiku", "--max-turns", "1"],
                         ["codex", "login", "status"]):
                r = subprocess.run(argv, env=env, cwd=tmp, capture_output=True, text=True, timeout=120,
                                   stdin=subprocess.DEVNULL)
                say(r.returncode == 0, " ".join(argv[:2]) + " in the isolated environment")
            shutil.rmtree(tmp, ignore_errors=True)
    return ok


def run(args):
    if args.live and not preflight(args):
        sys.exit("Preflight failed; nothing was run.")
    out = Path(args.output) / time.strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    cases = load_cases(args.suite, args.case)
    if not cases:
        sys.exit("No matching cases.")
    rng = random.Random(args.seed)
    meta = {k: v for k, v in vars(args).items() if k != "func"}
    (out / "run.json").write_text(json.dumps({**meta, "started": time.strftime("%FT%T%z")}, indent=2))
    with open(out / "results.jsonl", "a") as results:
        for case in cases:
            arms = ["review"] if case["kind"] == "review" else ["single", "workflow"]
            for trial in range(1, args.repeats + 1):
                rng.shuffle(arms)  # random arm order per trial
                for arm in arms:
                    trial_dir = out / f"{case['id']}-{arm}-{trial}"
                    trial_dir.mkdir()
                    if not args.live and (case["dir"] / "fake").exists():
                        shutil.copytree(case["dir"] / "fake", trial_dir / "case")
                    print(f"{case['id']} {arm} #{trial} …", flush=True)
                    try:
                        row = review_trial(case, trial_dir, args) if arm == "review" \
                            else task_trial(case, arm, trial_dir, args)
                    except Exception as e:  # an infrastructure failure, never an agent result
                        row = {"status": "harness error", "error": f"{type(e).__name__}: {e}"[:300]}
                    row = {"case": case["id"], "kind": case["kind"], "arm": arm, "trial": trial,
                           "live": args.live, **row}
                    results.write(json.dumps(row) + "\n")
                    results.flush()
                    print(f"  {row['status']}", flush=True)
                    if not args.keep:
                        shutil.rmtree(trial_dir / "home", ignore_errors=True)  # holds the auth copy
    print(out)
    report(argparse.Namespace(results=out))


def report(args):
    rows = [json.loads(line) for line in (Path(args.results) / "results.jsonl").read_text().splitlines()]
    md = [f"# Eval results: {Path(args.results).name}", ""]
    if any(not r.get("live") for r in rows):
        md += ["> Fake agents: these numbers test the harness, not the workflow.", ""]

    def stat(values):
        values = [v for v in values if v is not None]
        if not values:
            return "–"
        mean = statistics.mean(values)
        def num(v):
            return f"{v:,.0f}" if abs(v) >= 100 else f"{v:.3g}"
        return num(mean) + (f" ({num(min(values))}–{num(max(values))})" if len(values) > 1 else "")

    review = [r for r in rows if r["kind"] == "review"]
    if review:
        md += ["## Review: seeded bugs", "",
               "| Case | Trials ok | Caught / seeded | Required caught | Unadjudicated | False alarms | Duplicates |",
               "|---|---|---|---|---|---|---|"]
        for case in sorted({r["case"] for r in review}):
            rs = [r for r in review if r["case"] == case]
            good = [r for r in rs if "caught" in r]
            md.append(f"| {case} | {len(good)}/{len(rs)} | "
                      f"{stat([r['caught'] for r in good])} / {good[0]['seeded'] if good else '–'} | "
                      f"{stat([r['caught_required'] for r in good])} | {stat([r['unadjudicated'] for r in good])} | "
                      f"{stat([r['false_alarms'] for r in good])} | {stat([r['duplicates'] for r in good])} |")
        md.append("")

    task = [r for r in rows if r["kind"] == "task"]
    if task:
        md += ["## Task: workflow vs single agent", "",
               "| Case | Arm | Trials ok | Solved | Hidden fail→pass | Broke pass→pass | Minutes | Claude tokens out | "
               "Codex tokens out | Est. cost $ | New lint issues |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
        for case in sorted({r["case"] for r in task}):
            for arm in ("single", "workflow"):
                rs = [r for r in task if r["case"] == case and r["arm"] == arm]
                good = [r for r in rs if r.get("tests")]
                md.append(
                    f"| {case} | {arm} | {sum(r['status'] == 'ok' for r in rs)}/{len(rs)} | "
                    f"{sum(r['tests']['solved'] for r in good)}/{len(good)} | "
                    f"{stat([r['tests']['fail_to_pass'] for r in good])} / {good[0]['tests']['fail_to_pass_total'] if good else '–'} | "
                    f"{stat([r['tests']['pass_to_pass_total'] - r['tests']['pass_to_pass'] for r in good])} | "
                    f"{stat([r['seconds'] / 60 for r in rs if r.get('seconds')])} | "
                    f"{stat([((r.get('claude') or {}).get('usage') or {}).get('output_tokens') for r in rs])} | "
                    f"{stat([(r.get('codex_usage') or {}).get('output_tokens') for r in rs])} | "
                    f"{stat([(r.get('claude') or {}).get('total_cost_usd') for r in rs])} | "
                    f"{stat([(r.get('quality') or {}).get('new') for r in rs])} |")
        md.append("")
        wf = [r for r in task if r["arm"] == "workflow" and r.get("rules")]
        if wf:
            checks = list(wf[0]["rules"])
            md += ["## Workflow rules kept", "", "| Check | Kept | Broken | N/A or couldn't tell |", "|---|---|---|---|"]
            for c in checks:
                v = [r["rules"].get(c) for r in wf]
                md.append(f"| {c} | {v.count(True)} | {v.count(False)} | {v.count(None)} |")
            md.append("")
    failed = [r for r in rows if r["status"] != "ok"]
    if failed:
        md += ["## Trials that didn't finish cleanly", ""]
        md += [f"- {r['case']} {r['arm']} #{r['trial']}: {r['status']} {r.get('error', '')}".rstrip() for r in failed]
        md.append("")
    text = "\n".join(md)
    (Path(args.results) / "report.md").write_text(text)
    print(text)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(required=True)

    def common(sp):
        sp.add_argument("--live", action="store_true", help="use the real claude and codex CLIs (spends usage)")
        sp.add_argument("--output", default="/tmp/agent-workflow-eval-results")
        sp.add_argument("--claude-model", default="opus")
        sp.add_argument("--claude-effort", default="medium")
        sp.add_argument("--codex-model", help="Reader model; Codex's default when omitted")
        sp.add_argument("--codex-effort", default="medium")
        sp.add_argument("--max-reader-calls", type=int, default=12)

    sp = sub.add_parser("preflight")
    common(sp)
    sp.set_defaults(func=lambda a: sys.exit(0 if preflight(a) else 1))
    sp = sub.add_parser("run")
    common(sp)
    sp.add_argument("--suite", choices=["review", "task", "all"], default="all")
    sp.add_argument("--case", action="append", help="only this case (repeatable)")
    sp.add_argument("--repeats", type=int, default=3)
    sp.add_argument("--minutes", type=int, default=30, help="wall-clock limit per trial")
    sp.add_argument("--max-turns", type=int, default=80)
    sp.add_argument("--window", type=int, default=3, help="line tolerance when matching review findings")
    sp.add_argument("--quality-cmd", help="replace ruff: command printing JSON [{rule, path}]")
    sp.add_argument("--seed", type=int, default=0)
    sp.add_argument("--keep", action="store_true", help="keep each trial's isolated home folder")
    sp.set_defaults(func=run)
    sp = sub.add_parser("report")
    sp.add_argument("results")
    sp.set_defaults(func=report)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
