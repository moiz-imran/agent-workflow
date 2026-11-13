# Map: document-followers (illustrative)

Read-only fictional investigation, 2026-11-13. Base `example-base` on main; clean baseline. All paths below belong to the imagined app.

## Current behaviour

`src/documents/edit.ts:20` sends on every save. `src/documents/move.ts:18` retains followers. `src/documents/copy.ts:42` clones the document fields, including followers.

## Options and checks

Separate text changes from formatting saves; explicitly reset followers on copy. Check text edit, formatting edit, move and copy, including an original with zero followers. Example check command: `npm test -- documents` (not executed here).

## NEEDS_BUILDER

1. Notify on moves? Options: notify / keep moves outside this change. Recommend no notification because the text did not change.
2. Notify on formatting saves? Options: every save / text changes only. Recommend text changes only to reduce noise.
