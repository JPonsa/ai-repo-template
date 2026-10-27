---
name: retro
description: Run a factory-aligned retrospective using the global retro skill with factory-specific checklist.
---

# Factory retrospective

Run a retrospective aligned with this factory's workflow.

## Steps
1. Call the Skill tool with `retro` (the global mattpocock/skills retro) for the general analysis.
2. Follow `docs/runbook/retro.md` for factory-specific checklist items.
3. Focus on factory concerns: check command, CI, evidence blocks, risk gate, review order, AGENTS.md navigation, skills.
4. Present findings in order of severity.
5. Record actionable items in `docs/log.md` or create issues/tickets.
6. Prefer automating fixes (checks/hooks) over adding rules to AGENTS.md.

## Notes
- Opt-in only; not automatic
- Requires global `retro` skill from mattpocock/skills
