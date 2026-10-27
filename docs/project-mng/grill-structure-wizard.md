---
type: how-to
title: Grill session - Structure evolution and wizard-driven setup
description: Questions to stress-test the proposed structure and wizard flow against factory constraints.
status: draft
tags: [grill, structure, wizard, migration]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md", "https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-code-setup/skills/claude-automation-recommender/SKILL.md", "https://github.com/github/awesome-copilot/blob/main/agents/github-actions-expert.agent.md"]
---

# Grill session: Structure evolution and wizard-driven setup

## Goal
Stress-test the proposed final structure and wizard flow against the factory's hard constraints.

## Constraints to enforce
- "Copied, not installed" - enforcement (factory.py, risk gate) must live in repo, no runtime dependency on global skills/plugins
- AGENTS.md is the only instruction file; don't add CLAUDE.md
- Both harnesses must work (OpenCode and Claude Code)
- Local skills in `.claude/skills/` read by both; slash commands only for local skills
- `uv run scripts/factory.py check` must remain the only check entry point
- Risk gate, protected paths, evidence blocks unchanged in principle
- Never reimplement missing upstream skill inline

## Questions to grill

### Structure
1. **Skills location**: Move from `.claude/skills/` to `.agents/skills/factory/`? If we do, do we break Claude Code discovery? OpenCode searches both - fine. But existing repos and habits use `.claude/skills/`. Migration path?
2. **Naming changes**: `blocker-verifier` vs `finding-verifier`, `commit-check-evidence` vs `verify` - are these renames or new skills? Renames would break all references (AGENTS.md, commands, scripts). Why rename?
3. **Workflows split**: Current `factory.yml` works. Splitting into 5 files - does it help or hurt? Will CI still run all required checks? Any impact on risk gate?
4. **Docs reorg**: Move `docs/architectural-overview.md` to `docs/project-mng/` - factory.py docs validation might have expectations?
5. **adr vs decisions**: Clearer taxonomy but need to update index/docs validation rules.

### Wizard
6. **"Copy from template" mechanism**: If wizard runs in a fresh directory (to create new project), where does it get template files from? If it runs inside a cloned template, files are there. Need both cases.
7. **Project types**: "prototype", "simple", "production-ready" - what concrete differences in factory.toml? Risk ceilings? Protected paths? Strictness of reviews? Need to define precisely.
8. **Config lifecycle**: "must vs optional", "what can be updated through project life cycle" - need explicit rules. Changing protected paths mid-project is dangerous.
9. **mattpocock skills**: Wizard should check and offer to install or instruct. But must not auto-install without permission. Installation is harness-specific (claude plugin vs npx skills). Wizard needs to detect harness.
10. **AGENTS.md review**: Using claude-md-improver patterns - should this be automatic or opt-in? AGENTS.md is critical.
11. **Retrospectives**: "Should any retrospective process review" - what does this mean concretely?
12. **Automation suggestions**: Factory automatizations via claude-automation-recommender - need to be careful not to suggest things that violate constraints.

### Integration
13. **Relationship to setup-project**: Replace it or enhance it? Current setup-project works. Big changes risk breaking.
14. **Global wizard vs local**: Our #21 research recommended hybrid - global wizard that COPIES files is fine. This wizard could be that global wizard.
15. **Backwards compatibility**: Existing projects using current structure must still work.

## Desired outcome
A concrete plan: what to do now vs later, migration script needs, risks, and a spec outline if we proceed.
