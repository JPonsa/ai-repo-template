---
name: blocker-verifier
description: Take one blocker and start from the position that it is false. Reproduce or trace it, then return confirmed, refuted, or unproven. Runs with fresh context.
---

# Finding verifier

Take exactly one blocker finding and try to prove it false. This skill
runs with fresh context: assume nothing from the review that produced
the finding.

## Process

1. Restate the finding in your own words: the claim, the file and line,
   and the failure path it names. If any of these are missing from the
   input, return unproven and ask for the missing part.
2. Start from the position that the finding is false. Your job is to
   break it, not to confirm it.
3. Reproduce if possible: write a test, a script, or a command in a
   throwaway location that demonstrates the claimed failure. Clean up
   after yourself.
4. If reproduction is not possible, trace the code path line by line.
   Follow the actual call chain, not the one the finding describes.
5. Return exactly one verdict.

## Verdicts

- **confirmed**: the failure path exists and was reproduced or traced
  end to end. Attach the reproduction or the trace.
- **refuted**: the failure path does not exist, or a guard already
  handles it. Name the guard, with file and line.
- **unproven**: neither. State what evidence would settle it.

## Rules

- Never assume a finding is true because a reviewer wrote it.
- Never assume a finding is false because the code looks clean.
- One finding per run. A second finding goes to a second run.
- The verdict is the first line of your reply.
