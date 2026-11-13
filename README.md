# agent-workflow

How I run a large coding task across two AI agents: one builds, one reads and reviews, and nothing gets pushed until the exact code has passed review. This is the setup from my talk **[Building Agent Workflows for Better Code](https://moiz-imran.github.io/agent-workflow/deck/)**, packaged so you can try it yourself.

It isn't a framework. It's a few instruction files, two skills, file templates and one Python script.

## The idea

- **The Builder** (Claude Code) owns the work: the spec, the decisions and the code.
- **The Reader** (Codex) investigates in its own context and hands back a **map**: what the code does today, with `path:line` evidence, options, and the questions only the Builder should answer.
- **Decisions** are numbered (`D1`, `D2`…) and kept with their history in `decisions.md`, so the Builder and the reviewer work from the same answers.
- **Review** is a loop. A fresh reviewer checks the exact snapshot against the spec and decisions. Findings (`F1`…) get fixed and checked again until the result is **CLEAN**, and every round is written to a ledger.
- **The push gate** is the one thing that's enforced rather than asked for: `git push` and `gh pr create` are blocked until the code being pushed has a CLEAN receipt.
- **You read it first.** A generated review page shows the diff in reading order, with the decisions and where review pushed back. A human can still send it back, and a repeated human comment becomes a new rule.

Use it when the work is big enough to justify the handoffs: long investigations, real decisions, several review rounds. Small edits don't need any of it.

## What's here

| Path | What it is |
|---|---|
| [`templates/CLAUDE.md`](templates/CLAUDE.md) | The Builder's standing instructions. |
| [`templates/AGENTS.md`](templates/AGENTS.md) | The Reader's standing instructions. |
| [`skills/review-loop/`](skills/review-loop/SKILL.md) | The review, repair and verify cycle the Reader runs. |
| [`skills/review-rubric/`](skills/review-rubric/SKILL.md) | What an independent reviewer checks, and how severe each finding is. |
| [`templates/standards.md`](templates/standards.md) | Your team's rules, each marked Required or Advisory. |
| [`bin/review-gate.py`](bin/review-gate.py) | The push gate, review receipts, and the self-review page. Python standard library only. |
| [`templates/`](templates/) | `map.md`, `decisions.md`, review ledger, review guide and the hook snippet. |
| [`docs/scratch-files.md`](docs/scratch-files.md) | What each scratch file is for and who writes it. |
| [`docs/routes.md`](docs/routes.md) | Ways for the Builder to start the Reader. |
| [`examples/document-followers/`](examples/document-followers/) | The talk's running example, worked end to end. |
| [`deck/`](deck/) | The talk itself. |

## Set it up

You need [Claude Code](https://code.claude.com/docs/en/setup), the [Codex CLI](https://github.com/openai/codex) signed in, Git, and Python 3. macOS and Linux are tested; on Windows, use WSL.

1. **Connect the two agents.** Install the Codex plugin for Claude Code (see [routes](docs/routes.md) for other options):
   ```
   /plugin marketplace add openai/codex-plugin-cc
   /plugin install codex@openai-codex
   /reload-plugins
   /codex:setup
   ```
2. **Get this repo.**
   ```sh
   git clone https://github.com/moiz-imran/agent-workflow ~/agent-workflow
   ```
3. **Add the instructions.** Merge [`templates/CLAUDE.md`](templates/CLAUDE.md) into `~/.claude/CLAUDE.md` and [`templates/AGENTS.md`](templates/AGENTS.md) into `~/.codex/AGENTS.md`. Edit them: they're a starting point, not a spec.
4. **Install the skills for the Reader.**
   ```sh
   mkdir -p ~/.codex/skills && cp -R ~/agent-workflow/skills/* ~/.codex/skills/
   ```
5. **Add the push gate.** Merge the `hooks` block from [`templates/settings.json`](templates/settings.json) into `~/.claude/settings.json`. Don't replace your whole file. If you cloned somewhere other than `~/agent-workflow`, change the path. Then check it:
   ```sh
   python3 -I ~/agent-workflow/bin/review-gate.py test
   ```
6. **Turn the gate on per repo.** The gate ignores every repository until you opt it in:
   ```sh
   git -C path/to/your/repo config review-gate.enabled true
   ```
7. **Write your standards.** Copy [`templates/standards.md`](templates/standards.md) somewhere your team owns it, and name its path in review briefs.

## Try it

Ask Claude Code for something real, for example: *"Moving a document shouldn't lose its followers. Investigate first, then fix it."* Then watch for:

1. A Reader brief that says read-only, and a `map.md` in `/tmp/<ticket>/` that ends with `NEEDS_BUILDER`.
2. The Builder asking you, or recording, `D1` in `decisions.md`.
3. After the build, a `review-loop` run with a ledger, findings and a final status.
4. `git push` refused until the loop returns CLEAN and writes a receipt.
5. `review-gate.py guide --ticket <ticket>` opening the review page for you to read.

[`examples/document-followers/`](examples/document-followers/) shows what each of those files looks like for the talk's example.

## Evaluate it

[`eval/`](eval/README.md) measures the workflow on small fictional repos: whether review catches planted bugs, whether the full workflow beats one agent on the same tasks (hidden tests, time, tokens, new lint issues), and whether the agents kept the rules. Start with fake agents, which cost nothing:

```sh
python3 -B eval/run.py run --suite all --repeats 2
```

Then see [eval/README.md](eval/README.md) to run it with real agents.

## What the gate does and doesn't do

- It blocks the literal commands `git push` and `gh pr create` run through Claude Code's Bash tool, in repos you've opted in. It follows `cd`, `git -C` and leading `VAR=value`.
- It checks the tree of `HEAD` in that checkout against a receipt for the same repository. Commit exactly what was reviewed, or the push is blocked.
- It doesn't see a push inside a script, alias or another tool, and it doesn't inspect every ref you push.
- Receipts are local files. The gate keeps an agent honest about the process; it doesn't prove the review was good, and it isn't tamper-proof.
- `REVIEW_GATE_SKIP="<reason>" git push` lets a push through and logs it to `~/.agent-workflow/gate-overrides.log`. The instructions tell the Builder to use it only when you've approved.

Settings: `AGENT_WORKFLOW_HOME` (default `~/.agent-workflow`) holds receipts and evidence, and `AGENT_WORKFLOW_SCRATCH` (default `/tmp`) is where ticket folders live.

## Related

- [talk-deck](https://github.com/moiz-imran/talk-deck): the skill I used to build the talk.

## License

[MIT](LICENSE)
