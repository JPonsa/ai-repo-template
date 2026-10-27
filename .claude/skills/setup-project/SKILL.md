---
name: setup-project
description: Fill the identity documents and factory.toml for a new project, configure the check command, delete TEMPLATE.md, and delegate to upstream setup-matt-pocock-skills.
---

# Setup project

Turn this template into a real project. Ask, confirm, then write.
Never guess an answer the user can give.

## What to ask first

1. **Project type** - Choose one to pre-select sensible defaults:
   - `prototype` - Faster iteration, higher risk ceilings, fewer CI constraints
   - `simple` (default) - Balanced defaults matching current template
   - `production-ready` - Stricter risk ceilings, full protections
2. Project name, purpose, and consumers.
3. Domain terms and the system boundary.
4. The technology stack and its real check command.
5. Issue-tracker labels to use.
6. The document types the project needs.

### Project type defaults

| Setting | prototype | simple | production-ready |
| --- | --- | --- | --- |
| `risk.max_files` | 30 | 20 | 15 |
| `risk.max_added_lines` | 1000 | 600 | 400 |
| CI workflows | Minimal (check only if desired) | Standard factory workflow | Full suite as provided |
| Notes | Speed over strictness; checks still run | Balanced defaults | Maximum guardrails |

Only risk thresholds change based on project type. The check gate (`uv run scripts/factory.py check`) is never weakened.

## Prerequisites check

Before setup, check for required global skills:

1. **Detect harness** - Determine if running in Claude Code or OpenCode (check environment/files).
2. **Find mattpocock/skills** - Search in common locations:
   - `~/.config/opencode/skills/`
   - `~/.claude/skills/`
   - `~/.agents/skills/`
   - Any paths in `FACTORY_SKILL_PATHS`
3. **Look for `setup-matt-pocock-skills`** specifically.
4. **If not found** - Do NOT auto-install. Present install options based on detected harness:
   - Claude Code: `claude plugin install mattpocock-skills@claude-plugins-official`
   - OpenCode/others: `npx skills@latest add mattpocock/skills -a opencode`
   Ask for explicit permission before running any install command. If user declines, explain it's required and stop.

## Files this skill rewrites

| File | Change |
| --- | --- |
| `README.md` | project name, purpose, setup, usage |
| `INTENT.md` | purpose, consumers, success criteria, out of scope |
| `CONTEXT.md` | bounded context and domain model |
| `GLOSSARY.md` | approved terms |
| `CODING_STANDARDS.md` | real, verifiable code rules |
| `CONTRIBUTING.md` | project-specific setup and validation commands |
| `factory.toml` | project identity, check commands, risk ceilings per project type |
| `docs/log.md` | first entry for the new project |
| `docs/project-mng/architectural-overview.md` | replace template placeholders with the real architecture |

When rewriting `CODING_STANDARDS.md`, keep each section's HTML comment
instructions. The user fills the sections; the comments explain how.

## Before you write, setup steps

1. **Scaffold a first passing test.** A check command with no tests
   fails closed on the new baseline. When the check command runs a
   test runner, write one placeholder test under the test directory
   so `factory.py check` passes before the first ticket lands.
2. **Create the label set on the tracker.** Run `gh label create` for
   every label in `[labels]` in `factory.toml`. The upstream delegation
   creates only the triage labels; the factory labels (`spec`,
   `blocked`, `risk:low`, `risk:high`, `agent-merge`) are yours.
3. **Reserve the upstream delegation output.** The upstream skill
   writes `docs/agents/*.md` inside the OKF bundle, without typed
   frontmatter. Add the reserved paths to `[docs].reserved` in
   `factory.toml` (for example `agents/issue-tracker.md`,
   `agents/domain.md`, `agents/triage-labels.md`).

## AGENTS.md review (opt-in)

After core setup, offer to review `AGENTS.md`:
- Use patterns from the claude-md-improver skill/approach
- Check for clarity, length, duplication with other files, single source of truth
- Suggest improvements only - **require explicit user approval before applying any changes**
- Never add a `CLAUDE.md` file; `AGENTS.md` remains the only instruction file

## Config lifecycle

Document to the user which settings are safe to change:

| Setting | Lifecycle | Notes |
| --- | --- | --- |
| Project identity (name/purpose) | Rarely changed | Affects docs; update carefully |
| Check command | Updatable | Must remain a single entry point producing pass/fail |
| Labels | Updatable | Add/remove as project evolves |
| Doc types | Updatable | Can add new types as needed |
| Risk ceilings (max_files, max_added_lines) | Updatable with caution | Affects gate behavior |
| Protected paths | **Do not change** | Changing bypasses protections - dangerous |
| Reserved paths (docs) | Updatable if structure changes | Update with care |

## Files this skill deletes

- `TEMPLATE.md`, because the project is no longer a template.

`docs/decisions/0001-use-okf-for-docs-bundle.md` stays. It explains
the knowledge format the project now uses.

## Delegate

Call the Skill tool with `setup-matt-pocock-skills` to configure the
issue tracker and the label vocabulary for the upstream workflow.
Only do this after confirming mattpocock/skills is installed or user has been instructed.

## Verify

Run these and show the output:

```bash
uv run scripts/factory.py check
uv run scripts/factory.py docs
```

Both must pass before you report done.
