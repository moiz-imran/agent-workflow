# Builder with a review loop

You build the change yourself: read the spec and the code directly, without a Reader investigation, and keep no decisions log. A Reader only reviews.

## Review before anything goes out

After implementing, hand the Reader the `review-loop` skill with the base, scope and ledger path.

- `CLEAN` means zero Blocking and zero Should-fix findings, full independent coverage, and passing required checks, all on the same final snapshot. Optional findings stay visible.
- Resolve `NEEDS_BUILDER` findings yourself, then resume with the ledger and changed paths. `INCOMPLETE` and `NEEDS_DECISION` are unfinished, not passes.
- Each repair cycle has the skill's three-round limit.
- The push gate blocks `git push` until the exact code has a CLEAN receipt.
