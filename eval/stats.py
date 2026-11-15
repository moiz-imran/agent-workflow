#!/usr/bin/env python3
"""Summarize real workflow history from outcomes.csv files. Prints Markdown; reads only.

Usage:
  python3 eval/stats.py [CSV ...] [--exclude REGEX]

With no CSVs it reads ~/.agent-workflow/evidence/**/outcomes.csv and /tmp/*/outcomes.csv.
Rows have no header: date,ticket,repo,round,snapshot,blocking,should_fix,accepted,rejected,
repair_regressions,status,human_changes_requested,human_bugs_found.

The output has aggregate numbers only (no ticket keys or repo names) so it can be shared.
"""
import argparse
import csv
import glob
import os
import re
import sys

FIELDS = ["date", "ticket", "repo", "round", "snapshot", "blocking", "should_fix", "accepted", "rejected",
          "repair_regressions", "status", "human_changes_requested", "human_bugs_found"]
CLEAN = {"clean", "approve", "approved"}
INCOMPLETE = {"incomplete"}  # anything else (NEEDS_*, BLOCK, NOT_CLEAN, REPAIRED) means findings were open


def num(v):
    return int(v) if v and v.strip().isdigit() else None


def load(paths, exclude=None):
    seen, rows = set(), []
    for path in paths:
        with open(path, newline="") as f:
            for raw in csv.reader(f):
                if len(raw) < len(FIELDS) or tuple(raw) in seen:
                    continue
                seen.add(tuple(raw))
                r = dict(zip(FIELDS, raw))
                if r["ticket"] in ("", "none") or (exclude and re.search(exclude, r["ticket"])):
                    continue
                rows.append(r)
    return rows


def summarize(rows):
    internal = [r for r in rows if r["round"] != "human"]
    human = [r for r in rows if r["round"] == "human"]
    # The same snapshot reviewed twice reports the same findings twice: count each snapshot once.
    per_snapshot = {}
    for r in internal:
        key = (r["ticket"], r["repo"], r["snapshot"][:12])
        b, s = num(r["blocking"]) or 0, num(r["should_fix"]) or 0
        old = per_snapshot.get(key, (0, 0))
        per_snapshot[key] = (max(old[0], b), max(old[1], s))
    changes = {(r["ticket"], r["repo"]) for r in internal}
    status = lambda r: r["status"].strip().lower()  # noqa: E731
    reached_clean = {(r["ticket"], r["repo"]) for r in internal if status(r) in CLEAN}
    human_bugs = [num(r["human_bugs_found"]) for r in human]
    human_changes = [num(r["human_changes_requested"]) for r in human]
    return {
        "dates": (min(r["date"][:10] for r in rows), max(r["date"][:10] for r in rows)) if rows else None,
        "tickets": len({r["ticket"] for r in rows}),
        "changes": len(changes),
        "internal_rounds": len(internal),
        "rounds_per_change": len(internal) / len(changes) if changes else None,
        "incomplete_rounds": sum(status(r) in INCOMPLETE for r in internal),
        "reached_clean": len(reached_clean & changes),
        "blocking": sum(b for b, _ in per_snapshot.values()),
        "should_fix": sum(s for _, s in per_snapshot.values()),
        "optional_accepted": sum(num(r["accepted"]) or 0 for r in internal),
        "rejected": sum(num(r["rejected"]) or 0 for r in internal),
        "repair_regressions": sum(num(r["repair_regressions"]) or 0 for r in internal),
        "human_reviews": len(human),
        "human_prs": len({(r["ticket"], r["repo"]) for r in human}),
        "human_changes": sum(v for v in human_changes if v is not None),
        "human_bugs": sum(v for v in human_bugs if v is not None),
        "human_reviews_no_bugs": sum(v == 0 for v in human_bugs),
        "human_reviews_unknown": sum(v is None for v in human_bugs),
    }


def markdown(s):
    caught = s["blocking"] + s["should_fix"]
    total = caught + s["human_bugs"]
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "–"  # noqa: E731
    lines = [
        "# Workflow history", "",
        f"{s['tickets']} tickets, {s['changes']} reviewed changes, {s['dates'][0]} to {s['dates'][1]}." if s["dates"]
        else "No rows.", "",
        "| Measure | Value |", "|---|---|",
        f"| Internal review rounds | {s['internal_rounds']} ({s['rounds_per_change']:.1f} per change) |"
        if s["rounds_per_change"] else f"| Internal review rounds | {s['internal_rounds']} |",
        f"| Changes that reached CLEAN | {s['reached_clean']} of {s['changes']} |",
        f"| Rounds that ended INCOMPLETE | {s['incomplete_rounds']} |",
        f"| Blocking findings caught before human review | {s['blocking']} |",
        f"| Should-fix findings caught before human review | {s['should_fix']} |",
        f"| Optional findings accepted | {s['optional_accepted']} |",
        f"| Findings rejected as wrong | {s['rejected']} |",
        f"| Repairs that introduced a regression | {s['repair_regressions']} |",
        f"| Human reviews logged | {s['human_reviews']} on {s['human_prs']} PRs |",
        f"| Changes humans requested | {s['human_changes']} |",
        f"| Bugs humans found | {s['human_bugs']} |",
        f"| Human reviews that found no bug | {s['human_reviews_no_bugs']} of "
        f"{s['human_reviews'] - s['human_reviews_unknown']} |",
        f"| Required bugs caught before a human saw the code | {caught} of {total} ({pct(caught, total)}) |",
        "",
        "Findings are counted once per reviewed snapshot. \"Caught before a human\" counts internal Blocking and "
        "Should-fix findings, which are not all bugs, against bugs humans found later; read it as a rough split.",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="*")
    p.add_argument("--exclude", help="regex of ticket names to leave out")
    a = p.parse_args()
    paths = a.csv or sorted(glob.glob(os.path.expanduser("~/.agent-workflow/evidence/**/outcomes.csv"), recursive=True)
                            + glob.glob("/tmp/*/outcomes.csv"))
    if not paths:
        sys.exit("No outcomes.csv files found.")
    print(markdown(summarize(load(paths, a.exclude))))


if __name__ == "__main__":
    main()
