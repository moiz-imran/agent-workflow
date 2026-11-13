# Document followers — illustrative example

This fictional app and its review history illustrate the running example in the talk. No code was run and no real customer data or review metrics appear here.

1. The human agrees to the [spec](spec.md).
2. The Reader investigates and returns the [map](map.md), ending with questions for the Builder.
3. The Builder records [decisions](decisions.md): D1 excludes move notifications; D2 preserves a superseded answer.
4. Fresh review finds F1: copying a document copies its followers. The Builder repairs it; a second review is CLEAN. See the [app ledger](app-review-ledger.md).
5. The controller records each round and the later human review in [outcomes.csv](outcomes.csv).
6. The [guide](review-guide.json) describes the fictional app diff for self-review.

The guide uses `HEAD` as a valid local base placeholder. To render a useful diff, copy it into an external scratch ticket and replace the base with the app's pinned pre-change commit. Its source paths refer to the fictional app, not files supplied here. Snapshot labels v1/v2 below are illustrative, not Git object IDs.
