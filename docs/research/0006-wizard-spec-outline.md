---
type: research
title: Wizard and structure evolution - spec outline
description: Concrete plan for incremental implementation based on grill results.
status: draft
tags: [spec-outline, wizard, structure]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["docs/project-mng/grill-structure-wizard.md", "docs/research/0004-packaging-as-skill-plugin.md", "docs/research/0005-structure-wizard-evolution.md"]
---

# Wizard and structure evolution - spec outline

## Decision: Incremental, not big-bang

### Phase 1: Enhance setup-project (low risk)
- Add project type selection (prototype/simple/production-ready) with defined defaults
- Add mattpocock skills detection and install guidance (respecting permission)
- Add AGENTS.md review step using claude-md-improver patterns
- Add config lifecycle documentation
- Keep all existing behavior working

### Phase 2: Create global wizard skill (optional, follows #21)
- Create as separate skill that can copy template files
- Must copy (not reference) all files for self-contained result
- Support both "inside cloned template" and "fresh directory" modes
- Download from pinned tag if needed

### Phase 3: Structure improvements (careful)
- Keep `.claude/skills/` as primary; add `.agents/skills/` support if needed for compatibility
- DO NOT rename existing skills (keep verify, finding-verifier)
- Keep single factory.yml
- Only reorganize docs if necessary, with full migration

## Project types - concrete proposal

| Aspect | prototype | simple (default) | production-ready |
| --- | --- | --- | --- |
| max_files | 30 | 20 | 15 |
| max_added_lines | 1000 | 600 | 400 |
| Protected paths | Minimal set | Current defaults | Current + stricter |
| Review strictness | Relaxed (can skip some) | Normal | Strict |
| CI checks | Same checks run | Same checks run | Same checks run |

Note: Checks must always run. Only risk thresholds/review expectations change.

## Config lifecycle matrix
| Config | When set | Updatable | Notes |
| --- | --- | --- | --- |
| project identity | init | Rarely | Changing breaks references |
| check command | init | Yes with care | Must always produce pass/fail |
| labels | init | Yes | Add/remove as needed |
| doc types | init | Yes | Add new types |
| protected paths | init | NO - dangerous | Could bypass protections |
| risk ceilings | init | Yes with caution | Affects gate behavior |
| reserved paths | init | Yes if docs structure changes | Update carefully |

## Skills detection
Check paths in order:
1. `~/.config/opencode/skills/mattpocock*` or check for setup-matt-pocock-skills
2. `~/.claude/skills/*` for mattpocock related
3. Use `FACTORY_SKILL_PATHS` if set

If not found, present install commands for detected harness or ask user.

## AGENTS.md review
Load patterns from claude-md-improver: check length, clarity, organization, avoid duplication with other files, ensure it's the single source of truth. Suggest improvements, don't auto-apply.

## Implementation notes
- All changes must pass `uv run scripts/factory.py check`
- Update AGENTS.md if skill names/locations change
- Update commands in .opencode/commands/ if skill names change
- factory.py audit needs to understand new structure if skills move

## Updates based on grill feedback

### [1] Skills location
- Keep `.claude/skills/` as primary (Claude Code native). OpenCode reads it as compatibility path (as stated in AGENTS.md).
- Add support for `.agents/skills/` discovery for OpenCode/other agents.
- If setup-project detects harness is Claude Code and `.agents/skills/` is used but `.claude/skills/` missing, create symlink from `.claude/skills/` to `.agents/skills/` (or copy). Be careful about symlinks on different filesystems.

### [2] Renames done
- `verify` -> `commit-check-evidence`, `finding-verifier` -> `blocker-verifier`. All references updated, commands renamed.

### [4] Docs reorganization recommendation
- **adr/** - must keep for Architecture Decision Records (technical). 
- **decisions/** - keep for non-technical/process decisions. Clear separation is good.
- **architectural-overview.md** - recommend moving to `docs/project-mng/architectural-overview.md`. Update AGENTS.md references, update `factory.toml` reserved paths, update any links. This groups project management docs together.
- Need to update docs validation/index if it has assumptions.

### [6] Skills packaging
- Skills can include `assets/`, `references/`, `scripts/` subdirectories - OpenCode skills support additional files. Wizard can package entire skill directories.

### [7] Project types
Project type only affects pre-selected config during wizard to speed setup:
- **prototype**: fewer CI checks/workflows, less restrictive (maybe skip sonar-scan, simpler workflows), higher risk ceilings
- **simple/standard**: current defaults
- **production-ready**: full CI suite, stricter thresholds

Never weaken the `check` gate itself.

### [11] Retro integration
Matt Pocock has a `retro` skill (engineering/retro) - useful. Factory should integrate with it:
- Can be triggered automatically after N PRs merged, or on demand
- Focus on factory environment improvements (navigation, automated checks, coding standards, AGENTS.md, guardrails)
- Align with factory's check command and CI - read factory.yml, factory.toml
- May need factory-specific extensions to cover evidence blocks, risk gate, review order
- Don't duplicate - delegate to retro skill where appropriate, extend for factory-specific concerns

### [13] setup-project vs wizard
- **setup-project** (local skill in .claude/skills/): Customizes an EXISTING copied template. Runs in-repo, asks 5 questions, rewrites files, creates test/labels, delegates to setup-matt-pocock-skills, deletes TEMPLATE.md.
- **Wizard**: Creates a NEW project from scratch or guides full setup. Broader scope - project type selection, prerequisite checking/installation guidance, AGENTS.md review, automation suggestions, retro setup, config lifecycle management. Can be global skill that copies template files, or enhanced local skill. Wizard may call setup-project or incorporate its logic.
