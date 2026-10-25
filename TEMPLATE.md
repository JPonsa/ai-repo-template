# Start a project from this template

> This file is for the template only. The `setup-project` skill rewrites
> the project files and then deletes this file.

## What this is

A starting repository for work with coding agents. It ships the contracts,
the workflow, the guardrails, and the knowledge format. It ships no
third-party skills: those are installed once, globally, and recorded as
prerequisites.

## Before the first session

| Tool | Why | Check |
| --- | --- | --- |
| `git` | version control | `git --version` |
| `uv` 0.12 or later | runs `scripts/factory.py` | `uv --version` |
| `gh` | issues, pull requests, CI | `gh auth status` |
| An agent harness | OpenCode or Claude Code | the harness starts |

## Install the global skills

Both harnesses read `.claude/skills/`. OpenCode reads it as a
compatibility path. Claude Code reads it natively. The template uses that
one location, with no mirror and no symlink.

Install `mattpocock/skills` once, globally, for your harness.

Claude Code:

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

OpenCode or another agent:

```bash
npx skills@latest add mattpocock/skills -a opencode
```

Confirm that the skills landed in a global skill directory, such as
`~/.config/opencode/skills` or `~/.claude/skills`. A project-local copy
defeats the contract.

The tested pin is plugin 1.3.1 at commit
`5beb35b040e3de97e54fa9e386d7e42d15c295c2`. It is recorded in
`factory.toml`.

Claude Code exposes each skill as `/name`. OpenCode exposes the ID as
`@skill-id`, because it has no automatic slash command for a skill. This
template adds slash commands only for the five local skills.

## The first session

Start the agent in this directory and run the `setup-project` skill. It
asks five things:

1. Project name, purpose, and consumers.
2. Domain terms and the system boundary.
3. The technology stack and its real check command.
4. Issue-tracker labels.
5. The document types the project needs.

Then it delegates to the upstream `setup-matt-pocock-skills` skill, which
configures the issue tracker and the label vocabulary for the upstream
workflow.

## What `setup-project` rewrites

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

## What `setup-project` deletes

- `TEMPLATE.md`, because the project is no longer a template.

`docs/decisions/0001-use-okf-for-docs-bundle.md` stays. It explains the
knowledge format the project now uses.

## Keep `AGENTS.md` and do not add `CLAUDE.md`

`AGENTS.md` is the only instruction file. OpenCode and Claude Code both
read it.

A committed `CLAUDE.md` at or above the working directory makes Claude
Code ignore `AGENTS.md`. If a derived project already has one, make its
first line `@AGENTS.md` instead of copying content into it.

## Verify the result

```bash
uv run scripts/factory.py check
uv run scripts/factory.py docs
```

`check` runs the commands in `factory.toml`. `docs` validates the
knowledge bundle.

## Why the shape is like this

| Layer | Owner |
| --- | --- |
| Contracts | `INTENT.md`, `CONTEXT.md`, `GLOSSARY.md`, `CODING_STANDARDS.md` |
| Workflow | global `mattpocock/skills` |
| Knowledge | `docs/` as an OKF v0.2 bundle |
| Enforcement | `scripts/factory.py`, CI, ticket labels |
| Adapters | `.claude/skills/`, `.opencode/commands/`, permission files |

One meaning, one place. A rule lives in one file and is referenced
everywhere else.
