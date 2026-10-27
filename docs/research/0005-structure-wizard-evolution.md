---
type: research
title: Structure evolution and wizard-driven project setup
description: Compare proposed final structure/wizard flow against current template, identify migration gaps and recommendations.
status: draft
tags: [research, structure, wizard, migration]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md", "https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-code-setup/skills/claude-automation-recommender/SKILL.md", "https://github.com/github/awesome-copilot/blob/main/agents/github-actions-expert.agent.md"]
---

# Research: Structure evolution and wizard-driven project setup

## Summary
This research analyzes the proposed "Final structure" and wizard flow against the current template (v1.0 as built through issues #1-#9,21,20,25). It identifies what to adopt, what conflicts with existing contracts, and proposes a migration path that preserves the factory's enforcement model.

## Provenance
| Item | Value |
| --- | --- |
| Proposed structure/wizard | User message (2026-10-27) |
| Current template | Repo state at 478b7da (main) |
| Referenced skills/agents | Claude MD improver, Claude automation recommender, GitHub Actions expert (awesome-copilot) |

## Current vs Proposed Structure

### Skills location
- Current: `.claude/skills/` contains local skills (verify, security-review, finding-verifier, docs-knowledge, setup-project). Both harnesses read via compatibility. Slash commands in `.opencode/commands/` for the 5 local skills.
- Proposed: `.agents/skills/factory/` with docs-knowledge, blocker-verifier (vs finding-verifier), commit-check-evidence (vs verify), security-review, setup-project (with scripts/references/assets). 
- Gap: Need to understand if OpenCode/Claude Code will discover `.agents/skills/` as primary path. OpenCode docs say it searches `.agents/skills/` (we saw in earlier fetch). Claude Code compatibility - need to verify. Moving would be cleaner for "agent-agnostic" but breaks existing symlink/compat assumptions.

### GitHub workflows
- Current: single `factory.yml` with jobs check, docs, risk, secret-scan, dep-audit
- Proposed: ci.yml, create-pr.yml, pr.yml, push.yml, sonar-scan.yml
- Gap: More granular workflows. Need to see if this matches factory.py expectations. factory.py doesn't care about workflow names, CI just needs to run checks. But "sonar-scan.yml" suggests external integration - need to be careful not to add required deps that break the factory.

### Docs structure
- Current: `docs/adr/` exists (empty?), `docs/decisions/` has 3 files, `docs/research/` has 5 files, `docs/how-to/` exists, `docs/architectural-overview.md` at docs root, `docs/index.md`, `docs/log.md`, `docs/metrics/`
- Proposed: `docs/project-mng/` with `architectural-overview.md` inside it; `docs/adr/` for technical ADRs, `docs/decisions/` for non-technical decisions (current has both concepts mixed? decision 0001 says "use OKF for docs bundle" - technical/process decision; 0002 "owner merge is human approval" - process/governance; 0003 "log is not protected" - process. Proposed split makes sense.)
- Gap: Need to migrate architectural-overview.md to docs/project-mng/, clarify adr vs decisions taxonomy.

## Wizard flow analysis

The proposed wizard checks:
1. For key files (INTENT.md, README.md, CONTRIBUTING.md, CODING_STANDARDS.md, AGENTS.md) - if not created, copy from template and set /grill-me session
2. Is docs/ set up? copy from template
3. Is .github/ set up? copy from template  
4. Is CONTEXT.md created? copy from template
5. Is GLOSSARY.md created? copy from template
6. mattpocock skills installed? If no, ask permission to install or tell user command; use /mattpocock-skills:setup-matt-pocock-skills
7. Do user want AI Software factory? setup factory config by project type (prototype/simple/production-ready), identify must vs optional config, what can be updated through project lifecycle
8. GH Actions set?
9. Review AGENTS.md using claude-md-improver patterns
10. Should any retrospective process review?
11. CI/CD review suggestions
12. (factory) automatizations suggestions

This is more comprehensive than current setup-project. Current setup-project asks 5 questions and delegates to setup-matt-pocock-skills. The wizard adds project typing, config lifecycle management, AGENTS.md review, retrospectives, automation suggestions.

## Recommendations

### Structure migration
1. **Skills migration**: Moving to `.agents/skills/factory/` is reasonable if both harnesses support it. OpenCode already searches it. Need to update factory.py audit to look in both places? Or migrate fully. Better to support both for compatibility, or follow the new standard. The rename blocker-verifier (vs finding-verifier) and commit-check-evidence (vs verify) - need to update all references.
2. **Workflows**: Current factory.yml works. Splitting into multiple workflows could be cleaner but adds complexity. Need to ensure check/docs/risk jobs still run as required. The risk gate logic is in factory.py, not workflows.
3. **Docs reorg**: Moving architectural-overview to docs/project-mng/ makes sense. Clarifying adr (technical) vs decisions (governance/process) is good. Need to add migration notes.

### Wizard implementation
The wizard should be implemented as a skill (local) that guides through this flow. It could enhance or replace setup-project. Key points:
- "Copy from template" - the wizard needs access to template files. If running inside a copied template repo, files exist; if running to SET UP a new repo, it needs to copy them.
- Project types (prototype/simple/production-ready) should set different defaults in factory.toml (risk ceilings, protected paths strictness, etc.)
- Config lifecycle: some things fixed after init (project identity), some updatable (labels, doc types), some need care (protected paths, risk ceilings)
- Integration with claude-md-improver patterns for AGENTS.md review - could load that skill or follow its patterns
- Automation recommender for factory automatizations and CI/CD

### Integration with existing research
Our #21 research said keep template repo as primary, optionally add global wizard skill that COPIES files. This wizard could be that global wizard, or enhanced local setup-project.

## Next steps
1. Create grilling session for this structural evolution
2. Create spec if approved
3. Implement incrementally to avoid breaking existing checks
