# Standards

<!-- Your team's rules for the review-rubric skill. Keep it short: rules a reviewer can check in a diff.
     Mark each one Required (violations are Blocking) or Advisory (violations are Optional).
     Add a rule here when the same human review comment shows up a second time. -->

## Required

- R1. Every new API endpoint checks the caller's permission before reading data.
- R2. Database migrations are backwards-compatible with the previous release.
- R3. User-facing errors never include stack traces or internal IDs.

## Advisory

- A1. Prefer the platform's built-in feature over a new dependency.
- A2. Name tests after the behaviour they check.
