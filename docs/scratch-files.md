# Scratch files

Each task that goes through investigation, decisions and review gets one folder outside every repo: `/tmp/<ticket>/`. Both agents read and write it, so a new session can pick up where the last one stopped. Nothing in it is committed, and nothing links to it from a ticket or PR.

| File | Written by | What it holds | Template |
|---|---|---|---|
| `map.md` | Reader | The investigation handoff: pinned base, `path:line` evidence, current behaviour, options with a recommendation, check commands, and a closing `NEEDS_BUILDER` list. | [map.md](../templates/map.md) |
| `decisions.md` | Builder | Binding decisions `D1`, `D2`…, one per `NEEDS_BUILDER` item. Briefs cite them by number. | [decisions.md](../templates/decisions.md) |
| `<repo>-baseline.diff` | Review controller | `git diff --binary <base> -- .`, saved before each review round, so the round knows exactly what it reviewed. | — |
| `<repo>-round-<n>.diff` | Review controller | The repair since the last reviewed snapshot: all a delta review reads besides the findings and the callers it touches. | — |
| `<repo>-review-ledger.md` | Review controller | One section per round: snapshot, scope, coverage, findings `F1`, `F2`… with outcomes, repairs and checks. | [review-ledger.md](../templates/review-ledger.md) |
| `outcomes.csv` | Controller, then Builder | One row per round, no header. The Builder adds a `human` row after PR review. | below |
| `review-guide.json` | Review controller | Reading order, decisions per file, checks and pushback for the self-review page. | [review-guide.json](../templates/review-guide.json) |
| `review.html`, `pr.md` | `review-gate.py guide` | The self-review page and a PR description draft. | — |

## Decisions keep their history

A decision is never edited in place. When the answer changes, mark the old entry `SUPERSEDED` and put the current answer directly below it, with the same id:

```md
- D2. SUPERSEDED: Notify followers on every save.
- D2. Formatting-only edits don't notify. Changed after review found notification noise.
```

Everyone works from the current answer, and anyone can see how it got there. Briefs cite `D2`; they never restate or override it.

## outcomes.csv

```
date,ticket,repo,round,snapshot,blocking,should_fix,accepted,rejected,repair_regressions,status,human_changes_requested,human_bugs_found
```

Internal rounds leave the last two columns empty. After the PR's human review, the Builder appends a row with `round` set to `human` and those two filled in. When the same kind of human comment appears twice, that's a rule missing from your standards doc.

## Keeping evidence

`/tmp` gets wiped. After a CLEAN review, `review-gate.py guide` copies `map.md`, `decisions.md`, the ledgers, `outcomes.csv`, the guide, `pr.md` and the receipt to `~/.agent-workflow/evidence/<ticket>/<checkout>-<tree>/`. That folder is yours: it may hold private code context, so never commit or publish it.
