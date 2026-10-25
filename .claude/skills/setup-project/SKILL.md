---
name: setup-project
description: Fill the identity documents and factory.toml for a new project, configure the check command, delete TEMPLATE.md, and delegate to upstream setup-matt-pocock-skills.
---

# Setup project

Turn this template into a real project. Ask, confirm, then write.
Never guess an answer the user can give.

## What to ask

1. Project name, purpose, and consumers.
2. Domain terms and the system boundary.
3. The technology stack and its real check command.
4. Issue-tracker labels to use.
5. The document types the project needs.

## Files this skill rewrites

| File | Change |
| --- | --- |
| `README.md` | project name, purpose, setup, usage |
| `INTENT.md` | purpose, consumers, success criteria, out of scope |
| `CONTEXT.md` | bounded context and domain model |
| `GLOSSARY.md` | approved terms |
| `CODING_STANDARDS.md` | real, verifiable code rules |
| `CONTRIBUTING.md` | project-specific setup and validation commands |
| `factory.toml` | project identity and the check commands |
| `docs/log.md` | first entry for the new project |
| `docs/architectural-overview.md` | replace template placeholders with the real architecture |

When rewriting `CODING_STANDARDS.md`, keep each section's HTML comment
instructions. The user fills the sections; the comments explain how.

## Files this skill deletes

- `TEMPLATE.md`, because the project is no longer a template.

`docs/decisions/0001-use-okf-for-docs-bundle.md` stays. It explains
the knowledge format the project now uses.

## Delegate

Call the Skill tool with `setup-matt-pocock-skills` to configure the
issue tracker and the label vocabulary for the upstream workflow.

## Verify

Run these and show the output:

```bash
uv run scripts/factory.py check
uv run scripts/factory.py docs
```

Both must pass before you report done.
