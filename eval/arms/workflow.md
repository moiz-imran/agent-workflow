__CLAUDE_MD__

# How this evaluation wires the workflow

This run uses the plain-CLI route. Reach the Reader only through this launcher; it runs Codex for you with fixed flags:

```sh
python3 __READER__ --brief <brief.md> --out <result.md> [--sandbox workspace-write] [--skill review-loop|review-rubric]
```

- Write the brief to a file first. Read-only is the default; pass `--sandbox workspace-write` only for an assigned repair.
- `--skill review-loop` makes the Reader the review controller; `--skill review-rubric` makes it an independent reviewer.
- A read-only Reader can't write scratch files. Have it return their content and save them yourself.
- The ticket is `__TICKET__`, so its scratch folder is `__SCRATCH__/__TICKET__/`.
- The review gate is `python3 __GATE__`. The controller runs `python3 __GATE__ receipt --ticket __TICKET__` from the repo when the review is CLEAN.
- The spec is SPEC.md. When you're done, commit and push with `git push origin main`.
- No human is available during this run: record each decision you'd normally ask about in decisions.md with your reasoning, and continue.
