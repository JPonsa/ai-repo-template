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
