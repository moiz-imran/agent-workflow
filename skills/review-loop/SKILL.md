---
name: review-loop
description: Run an internal review, repair and verification cycle on a working tree after implementation, and return CLEAN with a receipt or a concrete reason it isn't. Use when the Builder hands over a finished change for review before it is pushed. Never publishes anything.
---

# Review loop

You are the controller. You own one cycle: review the snapshot, get the required findings repaired, verify, and review again until the snapshot is CLEAN or you can say exactly why it isn't. You never commit, push, open PRs or post reviews.

## Inputs (from the brief)

- Absolute checkout, base ref, ticket name and scratch folder (`/tmp/<ticket>/`).
- Scope: which paths are in and out. Default to everything that differs from base: committed, staged, unstaged and relevant untracked files.
- The spec revision, `decisions.md`, and the standards doc to apply (see the `review-rubric` skill).
- Required checks: the exact commands that must pass.
- Repair authority: which kinds of fix you may make yourself. Anything else goes back to the Builder.

If any input is missing and you can't infer it safely, stop and return `INCOMPLETE` with what's missing.

## The cycle

1. **Baseline.** Record the checkout, base and HEAD, `git diff --binary <base> -- . > /tmp/<ticket>/<repo>-baseline.diff`, the list and hashes of untracked files in scope, exclusions, and the spec and decision revisions you're reviewing against. Append them to the ledger as a new round.
2. **Independent full review.** Run a fresh, read-only reviewer with the `review-rubric` skill over the whole scope. Give it the spec, the current decisions, the standards doc and the snapshot; don't give it the Builder's reasoning. A reviewer that couldn't cover everything means `INCOMPLETE`, never CLEAN.
3. **Triage.** Give each finding a stable id (`F1`, `F2`…) and keep it for the life of the ticket. Record the severity, `path:line`, evidence, and whether you accept or reject it and why. Never relabel a severity to get to CLEAN.
4. **Repair.** Fix accepted Blocking and Should-fix findings that are within your authority, in small batches. Anything that changes behaviour, a contract or a decision goes back as `NEEDS_BUILDER` with options and a recommendation.
5. **Verify.** Run the required checks, and a targeted check for each repair. A targeted check proves the fix; it doesn't give the snapshot full coverage.
6. **Final review.** After any repair, run a new full independent review on the final snapshot. If the first full review found nothing required and nothing changed since, it is the final review.
7. **Receipt.** Only when the final snapshot is CLEAN, run `python3 -I <agent-workflow>/bin/review-gate.py receipt --ticket <ticket>` from the checkout. Then write `review-guide.json` (below).

**Limits.** At most three repair rounds per cycle. If the same finding keeps coming back, or a fix keeps breaking something else, stop with `NEEDS_DECISION`. If you run out of time or evidence, stop with `INCOMPLETE`. Missing checks count as missing, not as passing.

**Several repos.** Each affected repo needs its own ledger and final full review. A change to a shared contract or decision invalidates any repo that was cleared against the old one.

## Severity

- **Blocking**: a concrete bug, security or data-loss risk, broken contract, or a violation of a Required rule in the standards doc.
- **Should-fix**: a meaningful regression risk, missing test for changed behaviour, accessibility failure, or a real maintainability problem the next change will trip over.
- **Optional**: preference, naming, style the standards doc marks Advisory, and nits.

CLEAN means zero Blocking and zero Should-fix, full independent coverage, and passing required checks, all on the same final snapshot. Optional findings are listed but never block.

## Ledger

Append one section per round to `/tmp/<ticket>/<repo>-review-ledger.md` (format: `templates/review-ledger.md`). Append one row per round to `/tmp/<ticket>/outcomes.csv`, with no header:

```
date,ticket,repo,round,snapshot,blocking,should_fix,accepted,rejected,repair_regressions,status,human_changes_requested,human_bugs_found
```

Leave the last two columns empty; the Builder fills them after human review.

## Review guide

When CLEAN, write `/tmp/<ticket>/review-guide.json` (format: `templates/review-guide.json`) so the Builder can read the change before anyone else does: a summary, the base, the files in reading order with why each matters and which decisions it implements, files to skim, the checks you ran, every place review pushed back (`path`, new-file `line`, what, fixed or not) and follow-ups.

## Result

Return one compact packet:

- **Status:** `CLEAN`, `NEEDS_BUILDER`, `NEEDS_DECISION` or `INCOMPLETE`.
- Final snapshot (tree hash) and HEAD.
- Changed files, and which repairs you made.
- Findings by id and severity, with their outcome.
- Exact checks and results.
- `NEEDS_BUILDER` items, each with options and a recommendation.
- Ledger and guide paths.
