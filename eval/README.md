# Evaluate the workflow

The review suite measures seeded-bug recall, duplicate findings and unmatched
findings. It includes a clean control. The task suite compares a single Builder
with a Builder that drives a Reader through `reader.py`. It measures hidden-test
fail→pass and pass→pass, time, tokens, estimated cost, new lint issues and recorded
workflow rules. The Reader uses the plain Codex CLI route.

Start offline, from the repository root:

```sh
python3 -B -m unittest discover -s eval/tests -v
python3 -B eval/run.py preflight
python3 -B eval/run.py run --suite all --repeats 2 --output /tmp/eval-results
python3 -B eval/run.py report /tmp/eval-results/<timestamp>
```

Fake agents are the default. They replay reference solutions and findings, call
the Reader launcher, and exercise the local push gate. Their scores test the
harness, not agent ability. Optional `fake/config.json` selects `mode`:
`timeout`, `nonzero`, `malformed`, or `push_without_receipt`. The last mode tries
the hook without a receipt and must be rejected.

For live runs, sign into Claude Code and run `claude setup-token`, then export its
value as `CLAUDE_CODE_OAUTH_TOKEN` without putting it in a file in this repo.
Sign into Codex with `codex login`. Run:

```sh
python3 -B eval/run.py preflight --live
python3 -B eval/run.py run --live --suite all --repeats 3 --minutes 30 --max-turns 80 --max-reader-calls 12
```

Live runs spend subscription usage. Preflight checks tool and isolated auth
status without a model prompt. Model and effort flags are recorded in run.json.
Wall time, Builder turns and Reader calls are bounded; Codex cost is not inferred
from tokens. Claude's reported cost is an estimate, not a subscription invoice.
Use a small pilot before increasing repeats.

Each trial gets a temporary HOME, separate Claude/Codex configuration, a private
copy of Codex auth.json, and a local bare Git origin. API/provider variables are
stripped; the Claude OAuth token is retained. Auth copies are removed after a
trial unless `--keep` is supplied. Logs and scratch remain: treat live artifacts
as sensitive. This is configuration isolation, not an OS sandbox. Tools retain
filesystem and network access; machine-managed policy and inherited executable
search paths still matter. The gate observes literal Bash push commands and
receipts, not every possible publication route. Never run untrusted fixtures.

Read report.md alongside results.jsonl. Failed trials appear separately; check
status and coverage before interpreting scores. Review matches require the same
path and a line within three lines of a gold span, one finding per bug. Severity
is separate. Unmatched findings need human adjudication, not automatic rejection.
Write `<trial>/adjudications.json` as `{"0":"real","2":"false"}` using zero-based
finding indices. Current scoring reads this during a review trial; report alone
does not rescore previously recorded results. Preserve the original outputs and
recompute scoring explicitly when adjudicating an existing run.

Quality is secondary and never combined into one score. Ruff, when installed,
counts new versus fixed issues by rule and path. `--quality-cmd 'your-command'`
replaces it: the command runs in each repo root and must print a JSON list such as
`[{"rule":"S001","path":"app.py"}]`. To wire Sonar, supply an adapter that runs
your configured scanner, waits for analysis, checks errors and emits that list.
No tested Sonar server adapter ships here. Do not expose scanner credentials to
agents or commit them.

To add a case, create `cases/<id>/case.json` with `kind` (`review` or `task`) and
`summary`, plus a small fictional Python stdlib `repo/` containing SPEC.md and
public unittest tests. Review cases add a `change/` overlay, optional `delete`
paths and `change_message`, and `gold.json`: a list of `id`, `path`, `start_line`,
`end_line`, `severity`, `what` objects with post-change line numbers. Clean
controls use an empty gold list. Task cases add prompt.md, a `grade` command using
verbose unittest from the grade root, and hidden/ overlaid only during grading.
Some hidden tests must fail on base and all must pass with fake/solution/.
Keep passing regression tests and traps for shallow fixes. Fake review responses
live in fake/findings.json and match findings.schema.json.

Public fixtures can be memorised. Small samples are descriptive, not evidence of
general superiority. Fake transports approximate documented formats; they do not
validate a real CLI installation. Hidden tests are only as good as their spec
coverage. Rule artifacts and receipts demonstrate recorded steps, not independent
reasoning quality or tamper resistance.
