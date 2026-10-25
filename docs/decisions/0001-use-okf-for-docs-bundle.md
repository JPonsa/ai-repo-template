---
type: decision
title: Use OKF v0.2 for the docs bundle
description: Why docs/ carries typed frontmatter while root documents do not.
status: stable
tags: [documentation, knowledge]
generated: { by: human:JPonsa, at: 2026-10-25T00:00:00Z }
---

# Context

An agent needs durable knowledge: why a decision was made, how a runbook
works, what a metric means. Narrative documents rot. A reader cannot tell
whether a page is current, verified, or a guess.

Root documents have a different reader. `README.md`, `INTENT.md`, and
`CONTRIBUTING.md` are read by people at a glance. Frontmatter on those
files is noise.

# Decision

`docs/` is an OKF v0.2 bundle. Every concept carries a `type` and may
carry `status`, `sources`, `generated`, `verified`, and `stale_after`.
The bundle roots at `docs/index.md`, which declares the version.

Root documents carry no frontmatter.

Specs and tickets do not live here. They live on the issue tracker, where
they can be reviewed and linked to the work.

# Consequences

- `uv run scripts/factory.py docs` fails on a missing `type`, a broken
  relative link, or a missing bundle index.
- A stale `stale_after` produces a warning, because time passing must not
  break continuous integration. `factory.py audit` reports it.
- A new concept type needs a change to `factory.toml` and this decision.
- A reader can see trust and freshness without opening the body.
