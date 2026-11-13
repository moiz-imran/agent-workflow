# Review ledger: <repo> (<ticket>)

## Round 1, <date time>

- Checkout: `<absolute path>`. Base `<sha>`, HEAD `<sha>`, snapshot tree `<sha>`.
- Scope: <paths>. Excluded: <paths and why>.
- Reviewed against: spec <revision>, decisions D1–D3, standards <path@revision>.
- Baseline: `<repo>-baseline.diff` (sha256 `<hash>`); untracked in scope: <files and hashes>.
- Reviewer coverage: <all N files | missing: …>.

| Id | Severity | Where | Finding | Disposition | Repair | Verified by |
|---|---|---|---|---|---|---|
| F1 | Should-fix | `src/copy.ts:88` | Copying a document also copies its followers. | Accepted | Skip followers on copy. | `npm test -- copy` passes |

- Checks: `<command>`: pass / fail (output excerpt).
- Status: <CLEAN | repairing | NEEDS_BUILDER | NEEDS_DECISION | INCOMPLETE>.
