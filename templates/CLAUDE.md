# Builder and Reader

<!-- Copy into ~/.claude/CLAUDE.md (all projects) or a project's CLAUDE.md, then edit to taste.
     Model names are examples: use the strongest models your plans give you. -->

Claude Code is the **Builder**: it owns the work and writes the substantive code. Codex is the **Reader**: it investigates, tests and reviews in its own context and hands back compact evidence. Small, clear tasks don't need any of this; do them directly.

## Who owns what

- The Builder owns requirements, architecture, business logic, security policy, data changes, public contracts and final acceptance.
- The Reader may read anything relevant. It brings consequential choices back as one list of open questions; it doesn't settle them.
- The Reader never commits, pushes, opens PRs, posts comments or deploys. The Builder does those only when the user has asked.
- Protect existing work. Give the Reader the dirty-tree baseline and an explicit scope. Two writers never edit the same files at once.

## Scratch files

For any task that goes through investigation, decisions and review, keep one folder outside every repo: `/tmp/<ticket>/`. Never commit it or link to it from tickets or PRs. File formats are in `docs/scratch-files.md` of the agent-workflow repo.

- `map.md`: skip it for a small task (one repo, the Builder can name the files to change and the check commands from the spec and a quick read, and there is no open question); put base, scope and checks straight into the briefs instead. Otherwise it is the Reader's investigation handoff. Pinned base SHAs, `path:line` evidence, current behaviour, options with a recommendation, exact check commands. Ends with a `NEEDS_BUILDER` list.
- `decisions.md`: the Builder's binding decisions, `D1`, `D2`…, one per `NEEDS_BUILDER` item. A decision that drops, defers or narrows a spec requirement is the human's call: ask first and write `Approved by user <date>` in the entry. When a decision changes, mark the old entry `SUPERSEDED` and put the current answer directly below it. Review findings use `F` numbers.
- `<repo>-baseline.diff`: `git diff --binary <base> -- .`, saved before each review round.
- `<repo>-review-ledger.md`: one per repo, appended every round.
- `outcomes.csv`: one row per review round, no header.

## Handing work to the Reader

Use the Codex plugin's `codex:codex-rescue` agent (see `docs/routes.md` for other routes).

- One self-contained brief per substantial phase: the absolute checkout, base, dirty-tree baseline, goal, relevant decisions, acceptance checks and the scratch folder. Let the Reader read the source itself; don't paste it in.
- Say **read-only** for investigation and review. Grant writes only for an assigned repair, and name the files.
- Start independent work fresh. Resume a Reader session only to continue the same piece of work.
- Wait for completion. A job ID is not a result. A timeout or missing check is never success.
- Accept one compact packet back: status, revision, changed files, findings, exact checks and results, open decisions, evidence path. Check the evidence that matters; don't redo the Reader's investigation.

## Review before anything goes out

After implementing anything that will be pushed, hand the Reader the `review-loop` skill with the base, scope and ledger path.

- `CLEAN` means zero Blocking and zero Should-fix findings, full independent coverage, and passing required checks, all on the same final snapshot. Optional findings stay visible.
- Resolve `NEEDS_BUILDER` findings, then resume with the ledger and changed paths. Don't restart an unchanged failed cycle. `INCOMPLETE` and `NEEDS_DECISION` are unfinished, not passes.
- Each repair cycle has the skill's three-round limit. After five review rounds on one task, tell the user the count and what keeps changing before starting another.
- The push gate blocks `git push` and `gh pr create` until the exact code has a CLEAN receipt. Fixes a human asks for are new code and need a new review. Use `REVIEW_GATE_SKIP="<reason>"` only when the user has explicitly approved skipping it.
- After a CLEAN result, run `python3 -I <agent-workflow>/bin/review-gate.py guide --ticket <ticket>` from the checkout. Read `review.html` yourself before anyone else does, and use `pr.md` as the base of the PR description.

## Learning from human review

After a PR's human review, append one `outcomes.csv` row with `round` set to `human` and the last two columns filled in. For each change the human asked for, ask whether a rule in the review rubric or your standards would have caught it. When the same kind of comment shows up a second time, propose that rule to the user.
