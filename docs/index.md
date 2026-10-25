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

# Decisions

* [Use OKF v0.2 for the docs bundle](decisions/0001-use-okf-for-docs-bundle.md) - Why `docs/` carries typed frontmatter and root documents do not.

# Folders

Create a folder when the first document of that type arrives. Keep the
folder name equal to the plural of the type.

* `decisions/` - a choice, its reason, and its consequence.
* `concepts/` - domain terms and system models.
* `runbooks/` - repeatable operational steps.
* `research/` - findings from sources, with provenance.
* `metrics/` - definitions and formulas.
* `retros/` - what changed after a piece of work.
* `playbooks/` - multi-step procedures that are not tied to operations.
