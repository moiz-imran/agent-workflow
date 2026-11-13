# Review ledger: app (document-followers, illustrative)

All snapshots, checks and reviewer results below are fictional teaching examples.

## Round 1, 2026-11-13

- Base: example-base; HEAD/snapshot: v1; clean baseline, no untracked files.
- Scope and independent coverage: all three changed app files, copy.ts, move.ts and edit.ts; spec revision 1, D1–D2. Baseline: illustrative app-baseline.diff (not supplied).

| Id | Severity | Where | Finding | Disposition | Repair | Verified by |
|---|---|---|---|---|---|---|
| F1 | Should-fix | src/documents/copy.ts:42 | Copying a document copies its followers. | Accepted | Reset the copied follower list; leave original intact. | Fictional copy acceptance check at v2 |

- Status: repairing. One required issue; no other findings.

## Round 2, 2026-11-13

- Base: example-base; HEAD/snapshot: v2. Fresh independent full review of the same three files, spec revision 1 and D1–D2.
- F1: repaired and verified; copy starts with no followers and original retains its list.
- Checks: fictional text-edit, formatting, move, copy and zero-follower acceptance checks pass. No repair regressions; no Blocking or Should-fix findings.
- Status: CLEAN (illustrative only; not a review receipt).

## Human review, 2026-11-13

- Snapshot v2: no changes requested and no bugs found. Example metrics only.
