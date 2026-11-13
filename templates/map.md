# Map: <ticket>

Read-only investigation, <date>. Base `<sha>` on `<branch>`; working tree: <clean | dirty, see baseline>.

## Question

What the Builder asked, in one or two lines.

## Current behaviour

- What happens today, each claim with evidence: `path/to/file.ts:42`.

## Relevant code

| Path | Why it matters |
|---|---|
| `path/to/file.ts:40-60` | Where X is decided. |

## Options

1. **Option A.** What changes, risk, effort. *(Recommended, because …)*
2. **Option B.** …

## Checks

Exact commands to verify the change:

```sh
npm test -- path/to/file.test.ts
```

## Open questions

- Anything you couldn't confirm, and how to confirm it.

## NEEDS_BUILDER

1. **<decision>.** Options: A / B. Recommend A because …
