# Ways to hand work to the Reader

The workflow only needs the Builder to start a Reader with a self-contained brief and wait for the result. Pick the route that fits your tools.

## 1. Codex plugin for Claude Code (recommended)

Requires Node 18.18 or newer and a signed-in Codex CLI.

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

Check that `codex:codex-rescue` appears in `/agents`. The Builder starts it as an **agent** (not the slash command) with the brief, and says explicitly whether the run is read-only. The agent can write by default, so read-only has to be stated every time.

- Start independent work fresh. Resume only to continue the same piece of work.
- For long jobs, run it in the background and wait for completion. A job ID on its own is not a result.
- Leave the plugin's optional stop-time review gate off (`/codex:setup --disable-review-gate`). This workflow reviews through the review loop instead.

## 2. Plain `codex exec`

Works anywhere Codex is installed. Write the brief to a file, then:

```sh
codex exec -m <model> -c 'model_reasoning_effort="medium"' \
  -s read-only -C /abs/path/to/checkout \
  -o /tmp/<ticket>/result.md - < /tmp/<ticket>/brief.md
```

Use `-s workspace-write` only for an assigned repair. Keep the exit status and stderr, and read the result file. In a read-only sandbox the Reader may not be able to write scratch files, so have it return them in the result and save them yourself.

## 3. An orchestrator such as T3 Code (optional)

If your editor can start child agents on other providers, use its native delegation instead of the plugin: choose the Codex model and effort explicitly, pass the same brief, and let it notify you on completion rather than polling. Don't wrap native delegation in the plugin.

## Choosing models

The talk's setup uses Claude Opus at medium effort as the Builder and a GPT model at medium effort as the Reader, because that's how the author's two subscriptions split best. Use whatever your plans give you; the structure matters more than the models. Raise effort for a hard decision, not by default.
