# Agent software-factory template

> **Template.** Read [TEMPLATE.md](TEMPLATE.md) before you change
> anything, then run the `setup-project` skill. That skill rewrites this
> file for the new project.

A minimal starting repository for projects built with coding agents.

It ships the durable contracts, the workflow, the guardrails, and the
knowledge format. It does not ship a framework, and it does not ship
third-party skills. Those are installed once, globally, and recorded as
prerequisites.

## What you get

- One instruction router, `AGENTS.md`, that both OpenCode and Claude Code
  read.
- Domain contracts: `INTENT.md`, `CONTEXT.md`, `GLOSSARY.md`, and
  `CODING_STANDARDS.md`.
- A workflow built on `mattpocock/skills`: grill, spec, tickets,
  implementation, test-driven development, review, pull request, retro.
- A knowledge bundle in `docs/`, using Open Knowledge Format v0.2.
- One check entry point, `scripts/factory.py`, with a risk gate that
  decides whether an agent may merge.
- Five local skills in `.claude/skills/`, read by both harnesses.

## Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| `git` | any current version | version control |
| `uv` | 0.12 or later | runs `scripts/factory.py` |
| `gh` | any current version, authenticated | issues, pull requests, CI |
| `mattpocock/skills` | 1.3.1 | the workflow skills |

An agent harness is also required: OpenCode or Claude Code.

### Install the global skills

Install them once, for your harness, in a global skill directory.

Claude Code:

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

OpenCode or another agent:

```bash
npx skills@latest add mattpocock/skills -a opencode
```

The tested pin is plugin 1.3.1 at commit
`5beb35b040e3de97e54fa9e386d7e42d15c295c2`. It is recorded in
`factory.toml` with the list of required skills. See
[TEMPLATE.md](TEMPLATE.md) for the discovery paths and the harness
differences.

## Quick start

```bash
git clone <this-repository> my-project
cd my-project
uv run scripts/factory.py check
```

Then start your agent and run the `setup-project` skill. It asks for the
project identity, the stack, and the check command, writes the contracts,
and deletes `TEMPLATE.md`.

## Layout

```text
.
├── AGENTS.md              # instruction router for both harnesses
├── TEMPLATE.md            # instantiation guide; deleted on setup
├── factory.toml           # check command, risk paths, labels, doc types
├── scripts/factory.py     # check | docs | risk | audit
├── docs/                  # OKF v0.2 knowledge bundle
├── .claude/skills/        # local skills, read by both harnesses
├── .opencode/commands/    # OpenCode slash-command adapters
└── .github/               # CI and templates
```

## The loop

1. Grill the idea and record hard decisions.
2. Write a spec as an issue.
3. Split the spec into tickets with blocking edges.
4. Implement one ticket in a fresh context, with a test.
5. Verify the check on the exact commit.
6. Review standards, spec, and security in fresh contexts.
7. Merge, when the risk gate allows it.
8. Record the retro and the log entry.

## Licence

MIT. See [LICENSE](LICENSE).
