---
okf_version: "0.2"
---

# Knowledge bundle

This directory holds durable knowledge. Specs and tickets live on the
issue tracker, not here.

Every concept carries a `type`. The allowed types are `decision`,
`concept`, `runbook`, `research`, `metric`, `retro`, and `playbook`.
The list is defined in `factory.toml` and checked by
`uv run scripts/factory.py docs`.

Use `adr/` for architecture decision records when the upstream
workflow expects them, and keep the OKF bundle for other durable
knowledge.

Align with `mattpocock/skills` vocabulary where practical: the three
brakes (automated checks, automated review, human review) map to the
check, the review order, and the risk gate, as recorded in
[the glossary](../GLOSSARY.md) and in
[the research on their software-factory skill](research/0001-mattpocock-software-factory.md).
Their autonomous-run terms (Run, Runner, Orchestrator) are not adopted:
this factory is local and human-gated.

# Decisions

* [Use OKF v0.2 for the docs bundle](decisions/0001-use-okf-for-docs-bundle.md) - Why `docs/` carries typed frontmatter and root documents do not.
* [The owner's merge is the human approval](decisions/0002-owner-merge-is-human-approval.md) - Why high-risk pull requests merge red in a solo-owner repository.
* [The update log is not a protected path](decisions/0003-the-log-is-not-a-protected-path.md) - Why the logging rule no longer closes the agent lane.

# Project documents

Project-wide documents such as `architectural-overview.md` may live at the
root of `docs/` or in an appropriate folder when they need frontmatter.
Root documents without frontmatter are reserved (see `factory.toml`).
The agent must keep `architectural-overview.md` up to date when
architecture changes (module boundaries, dependencies, data flows, or
public interfaces).

# Folders

Create a folder when the first document of that type arrives. Keep the
folder name equal to the plural of the type.

* `adr/` - architecture decision records (compatible with `mattpocock/skills`).
* `decisions/` - a choice, its reason, and its consequence (OKF type).
* `concepts/` - domain terms and system models.
* `runbooks/` - repeatable operational steps.
* `research/` - findings from sources, with provenance.
* `metrics/` - definitions and formulas.
  The set the factory tracks is [factory.md](metrics/factory.md).
* `retros/` - what changed after a piece of work.
* `playbooks/` - multi-step procedures that are not tied to operations.
* `how-to/` - task-focused guides for common procedures.
