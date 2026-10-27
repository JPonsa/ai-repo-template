# Repository instructions

These instructions apply to the whole repository. A deeper `AGENTS.md`
overrides them. Read `INTENT.md` for purpose and scope, and `CONTEXT.md`
and `GLOSSARY.md` for domain language.

## Always-relevant context

- **Identity**: mirror the Purpose and Primary consumers from `INTENT.md`,
  in one or two sentences. Do not copy `README.md` sections here.
- **Stack**: languages, frameworks, package managers, and the real check
  command. Setup detail lives in `CONTRIBUTING.md`.

## Where to look

| Need | Read |
| --- | --- |
| Purpose, consumers, scope | `INTENT.md` |
| Domain model and terms | `CONTEXT.md`, `GLOSSARY.md` |
| Code rules | `CODING_STANDARDS.md` |
| Branch, commit, and review rules | `CONTRIBUTING.md` |
| Decisions, runbooks, research | `docs/index.md` |
| Architecture, kept current | `docs/project-mng/architectural-overview.md` |
| Harness configuration | `factory.toml` |
| Starting a derived project | `TEMPLATE.md` |

## One command

`uv run scripts/factory.py check` is the only check entry point. It runs
the commands in `factory.toml` and fails closed when source changed and
nothing ran.

## Workflow

Create or pick an issue, then branch from `main` as
`<type>/<issue>-<short-description>`. Write a spec when the work spans
more than one commit, and split it into tickets that each fit in one
context window. Implement one ticket at a time, with a test at each
agreed seam. Update `docs/project-mng/architectural-overview.md` when module
boundaries, dependencies, data flows, or public interfaces change.
Use conventional commits: `type(scope): short description`.
Review and pull-request detail is in `CONTRIBUTING.md`.

## Skills

Local skills live in `.claude/skills/`. OpenCode and Claude Code both read
that path. Upstream `mattpocock/skills` are installed globally; the tested
pin is in `factory.toml`.

A missing skill is an install error. Stop and ask the user to install it.
Never reimplement a missing skill inline, and never vendor a copy.

## Risk

- **Low risk**: no protected path, diff below the size ceiling, evidence
  that matches `HEAD`, and no surviving review blocker. The agent merges.
- **High risk**: anything else. A human approves the merge.

Protected paths and the size ceiling are in `factory.toml`. The gate
decides. Never judge your own diff as low risk.

## Evidence and review order

A change is not done until the check passes on the exact commit. Every
pull request carries the evidence block defined in `CONTRIBUTING.md`;
its commit must equal `HEAD`, or it is stale and rejected.

Review order: `code-review` (standards and spec axes, fresh contexts),
`security-review` (with an attack list, even for a clean verdict),
`commit-check-evidence` (check result bound to the exact commit), `blocker-verifier`
(every blocker starts as false).

Each reviewer receives four inputs: the task contract, the spec, the
exact commit, and the check command. No reviewer receives the author's
reasoning or a draft verdict. A blocker gates the merge only when traced
or reproduced. The verifier outcomes are confirmed, refuted, and
unproven. Unproven findings are recorded and dismissed.

## Voice

Use ASD-STE100 Simplified Technical English and British English spelling.
`CONTRIBUTING.md` holds the writing and visualisation rules.

## Never

- Commit secrets, credentials, tokens, or personal data.
- Edit a generated file instead of its source.
- Weaken or skip a check to make a change pass.
- Push to `main` or force-push a shared branch.

## Retrospectives
Run the `factory-retro` skill (mattpocock/skills) on demand or after significant milestones. Follow `docs/runbook/retro.md` for factory-specific checklist items.
