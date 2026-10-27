---
type: runbook
title: Factory retrospectives
description: How to run retros aligned with the factory workflow.
status: stable
tags: [retro, runbook, process]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2028-01-27T00:00:00Z
sources: ["https://github.com/mattpocock/skills/tree/main/skills/engineering/retro"]
---

# Factory retrospectives

## When to run
- On demand after a difficult session
- After N merged PRs (suggest starting at 5, adjust to team cadence)
- After incidents or repeated friction points

## Using the retro skill
Use the global `retro` skill from mattpocock/skills: `skill({ name: "retro" })`. It will follow the engineering/retro workflow.

## Factory-specific checklist
When running a retro in a factory repo, also check:

- [ ] **Check command**: Is `uv run .factory/factory.py check` catching issues? Any gaps?
- [ ] **CI workflow**: Are all required checks running? Any flaky jobs?
- [ ] **Evidence blocks**: Are PRs consistently including valid evidence blocks?
- [ ] **Risk gate**: Any false positives/negatives? Protected paths correct?
- [ ] **Review order**: Is the review order being followed? Are blockers being properly verified?
- [ ] **AGENTS.md**: Can we move steering to automated checks or navigation pointers?
- [ ] **Navigation**: Are there hidden dependencies? Need pointers?
- [ ] **Skills**: Are local skills working well? Any missing?

## Recording outcomes
Add actionable items to `docs/log.md` or create tickets. Prefer automating fixes (add checks/hooks) over adding rules to AGENTS.md.
