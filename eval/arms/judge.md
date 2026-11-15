You are reviewing two independent implementations, A and B, of the same ticket in this repository.
The working directory is the repository before either change; read any code you need for context.
Do not modify anything.

Find real defects in each diff: wrong behaviour against the ticket, regressions of existing behaviour,
broken edge cases that real input will hit, data-loss or error-handling bugs, contract breaks.
Do not count style, naming, missing docs or test-only nitpicks. Do not credit or penalise size.
Each defect needs a concrete input or scenario that goes wrong. If unsure, leave it out.

Reply with only a JSON object, no prose and no code fence:
{"A": [{"severity": "blocking|should_fix", "file": "...", "defect": "...", "scenario": "..."}],
 "B": [ ...same shape... ],
 "prefer": "A|B|tie",
 "why": "one sentence"}

# Ticket

__TICKET__

# Diff A

```diff
__A__
```

# Diff B

```diff
__B__
```
