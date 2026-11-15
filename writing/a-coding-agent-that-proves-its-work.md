# A coding agent that proves its work

*Notes on [nextharness](https://github.com/dev-the-dev-while-deving/nextharness), an alpha coding agent harness.*

## The irritation

Coding agents say "Done! All tests pass." Often that's true, and the change is still wrong, because the tests never covered what you asked for. The agent's own summary is the least trustworthy part of the run, and it's the part you read first.

I wanted the harness, not the model, to decide whether a run worked. And I wanted it to show its evidence, not just a verdict.

## How it works

nextharness (`nh`) is a single Python file with no dependencies. It talks to any OpenAI-compatible endpoint: a local model through Ollama, LM Studio or vLLM, a company gateway, or OpenRouter's free models.

Around every run, the harness does things the model can't skip:

1. **Runs your checks before and after.** It reads them from a `Checks` list in `AGENTS.md` or detects the obvious test command. A check that passed before and fails after is a regression, and the agent gets fix rounds.
2. **Asks the agent to prove the request.** The agent writes a reproduction, for example `test_issue.py`, and calls `reproduce(command=...)`.
3. **Tests the proof against the original code.** The harness runs the reproduction on a copy of the code from before the change. It has to **fail** there, otherwise it doesn't prove anything. After the change it has to **pass**.
4. **Freezes the proof.** Once recorded, the reproduction's files are locked, so the agent can't weaken the test to make it pass.
5. **Keeps evidence.** Every run writes a report with the diff, every command, the before/after check table and the full transcript, and `nh undo` reverts it.

Only a run whose reproduction failed before, passes after, and breaks no check is labelled **VERIFIED**.

## Verdicts that don't overclaim

| Verdict | Meaning |
|---|---|
| VERIFIED | The reproduction failed on the original code and passes now, and no check fails |
| CHECKS PASS (no reproduction) | Checks pass, but nothing proved the request |
| FAILED (regressions) | Something that passed before now fails |
| NOT VERIFIED | A check or the reproduction still fails |

The second row exists because "checks pass" and "done" are different claims. Most agents blur them.

## Measuring it

I built a yardstick of 16 small tasks. Each has a prompt, a starting repo, a reference solution, and a hidden `accept.sh` the agent never sees. The runner tracks four numbers: pass rate, verified pass rate, **false-done rate** (the agent finished but the hidden check failed) and **false-verified rate** (VERIFIED but wrong).

On the 6 hard tasks, a local 9B model, 3 runs each:

- **VERIFIED once, and that run was correct.**
- **CHECKS PASS 12 times, and 7 of those were wrong.**
- The hidden check passed in 6 of 18 runs.

That middle line is the whole argument for the project. If I'd stopped at "the tests pass", I would have shipped 7 wrong changes and called them done. The verified label was rarer, but when it appeared it was right.

The catch: small models rarely bother to write a reproduction, so most runs end at CHECKS PASS. The harness can't make a weak model rigorous. It can only stop the run from claiming more than it showed.

## Known limits

It's alpha, and the README says so: no sandbox yet (commands ask for approval unless you pass `-y`), no context summarisation for long sessions, macOS-only testing, and a reproduction copy that leaves out gitignored files like `node_modules`.

## What I'd do next

- Run the yardstick on more models and publish the false-done rate per model. I think that's a better number to compare models on than raw pass rate.
- Nudge small models to write reproductions more often. That's where VERIFIED runs come from.
- Add a sandbox, so `-y` stops being a footgun.

## What I took from it

An agent's confidence isn't evidence. A test that fails before the change and passes after it is. Most of the work was deciding what the harness is allowed to claim, and making it claim less.

Source: [github.com/dev-the-dev-while-deving/nextharness](https://github.com/dev-the-dev-while-deving/nextharness)
