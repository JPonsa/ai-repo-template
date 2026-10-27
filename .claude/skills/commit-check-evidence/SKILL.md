---
name: commit-check-evidence
description: Run the one check command, record the exact commit, and produce a machine-readable evidence block bound to that commit.
---

# Verify

Run the check and produce evidence that a reviewer can trust without
re-running it. Fail closed: never report success without observed output.

## Process

1. Identify the one check command from `factory.toml` under
   `[check].commands`. The entry point is always
   `uv run scripts/factory.py check`. Do not add a second entry point.
2. Record the exact commit before running:
   `git rev-parse HEAD`. If the working tree is dirty, stop and report
   that the evidence is not bound to a commit. Commit or stash first.
3. Run `uv run scripts/factory.py check` and capture the full output,
   including exit status.
4. Assess test adequacy: does the observed output exercise the change?
   A passing check that never touched the changed code is not evidence.
5. Emit the evidence block below, verbatim, with observed values only.

## Evidence block

```markdown
## Evidence

- commit: `<full sha>`
- command: `uv run scripts/factory.py check`
- result: pass | fail
- output (last line): `<observed last line>`
```

## Rules

- Never fabricate output. If the check did not run, the result is fail.
- A non-zero exit status is fail, even when the output looks correct.
- If the check fails, report the first failing line and stop. Do not
  attempt fixes; that is the implement step.
- The evidence block is machine-readable: keep the exact keys and the
  backtick formatting.
