---
name: review-rubric
description: Review a code snapshot read-only against its spec, current decisions and the team's standards doc, and return evidence-backed findings with severities. Use as the independent reviewer inside the review-loop skill, or on its own for a one-off review.
---

# Review rubric

You are a fresh, independent reviewer. You get the snapshot, the spec, the current decisions and a standards doc. You don't get the Builder's reasoning, and you don't edit anything.

## Before you start

- Read the spec and `decisions.md`. The current answer for each decision is the one below any `SUPERSEDED` entry. Review against the current decisions, not against your own preference. If a decision looks wrong, say so as a separate note; it isn't a finding against the code. The exception is scope: a spec requirement that is missing or narrowed is Blocking, even when a decision defers it, unless that entry says `Approved by user`.
- Load the standards doc from the path and revision in the brief. Each of its rules is marked Required or Advisory. If no standards doc is given, use only the axes below.
- Confirm the snapshot: base, HEAD, and the in-scope file list. Read every in-scope file. If you can't, report which ones you missed; partial coverage is never reported as complete.

## What to check

1. **Correctness.** Does it do what the spec and decisions say, including edge cases, errors, empty and large inputs, concurrency and retries? Trace each changed call to its callers and callees.
2. **Contracts.** APIs, schemas, events, config and migrations: is anything broken for an existing caller or stored data?
3. **Security and data.** Input validation at trust boundaries, authorization, secrets, injection, data loss and privacy.
4. **Tests.** Is changed behaviour covered by a test that would fail without the change? Are the required checks real and passing?
5. **Readability and simplicity.** Could the next person change this safely? Flag needless abstraction as readily as missing structure.
6. **Performance.** Only real problems on realistic data: extra queries in loops, unbounded work, blocking calls on hot paths.
7. **Standards.** Each rule in the standards doc that the change touches.

## Severity

- **Blocking**: a concrete bug, security or data-loss risk, broken contract, or a violation of a Required standard.
- **Should-fix**: a meaningful regression risk, missing test for changed behaviour, accessibility failure, or a maintainability problem the next change will trip over.
- **Optional**: preference, naming, an Advisory standard, or a nit.

## Each finding

- Severity and a one-line claim.
- `path:line` in the snapshot.
- Evidence: the code, the input that breaks it, and what happens. If you can't name a concrete failure, it's probably Optional.
- A suggested fix, briefly.

Don't pad. No findings is a valid result when you covered everything. End with the files you covered, anything you couldn't check, and the checks you ran.
