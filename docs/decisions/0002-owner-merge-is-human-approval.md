---
type: decision
title: The owner's merge is the human approval for high-risk diffs
description: Why the risk gate reports red on agent-authored pull requests in a solo-owner repository.
status: stable
tags: [risk, workflow, governance]
generated: { by: agent:opencode, at: 2026-10-25T00:00:00Z }
---

# Context

The risk gate in `.factory/factory.py risk` fails a pull request that is
structurally high risk unless it is labelled `risk:high` and carries an
APPROVED review from an account other than the pull-request author.

Agents create pull requests under the owner's account. GitHub does not
allow a user to approve their own pull request. In a repository with one
human account, the review-based approval signal can never fire.

# Decision

In a solo-owner repository, the owner's merge of a high-risk pull request
is the human approval. The risk gate reports red, the owner reads the
report, and the merge is the recorded decision.

The gate stays honest: it never silently passes a high-risk diff. CI
remains the reporting layer; the owner is the enforcement layer.

Where a second account exists, use an APPROVED review instead. It is the
stronger signal and it is what the gate looks for first.

# Consequences

- A high-risk pull request in a solo-owner repository merges with a red
  risk job. This is expected, not a failure of the gate.
- Branch protection must not require the risk job to pass, or the owner
  must merge with an admin override.
- The `agent-merge` lane stays closed to high-risk diffs: an agent never
  merges a red risk job on its own authority.
