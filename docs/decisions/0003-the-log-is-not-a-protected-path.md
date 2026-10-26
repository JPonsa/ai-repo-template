---
type: decision
title: The update log is not a protected path
description: Why docs/log.md left the risk gate's protected list.
status: stable
tags: [risk, workflow, governance]
generated: { by: agent:opencode, at: 2026-10-26T00:00:00Z }
---

# Context

`CONTRIBUTING.md` requires one log entry in `docs/log.md` for every
merged change. `factory.toml` listed `docs/log.md` as a protected path,
so any pull request that followed the logging rule was automatically
high risk and needed owner approval.

The consequence, observed during the dry run of the loop: a pull
request must either break the logging rule to stay in the low-risk
agent lane, or follow the rule and leave it. An agent-merge share of
zero is the logical end state. The protection made the rule and the
lane contradict each other.

# Decision

`docs/log.md` leaves the protected list. The log is append-only and
mechanical: one dated entry per merged change, never a rewrite of old
entries. Its failure mode (a missing or malformed entry) is a
documentation defect, not a change-everything defect.

`docs/index.md` stays protected: it declares the bundle version and
the allowed vocabulary, and editing it changes how the factory reads
knowledge.

# Consequences

- A pull request that changes code plus its log entry can be low risk.
  The agent lane stays open for ordinary work.
- A pull request that rewrites or deletes existing log entries is
  still suspicious: reviewers check for rewrites of history, and the
  docs-knowledge skill states the append-only rule.
- `factory.py docs` still validates the bundle; the log itself carries
  no frontmatter, so validation does not cover its body. The
  append-only rule is enforced by review, not by the gate.
