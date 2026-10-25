---
name: security-review
description: Review a diff for trust boundaries, OWASP-class bugs, secrets, authorisation gaps, and supply-chain risk. Read-only.
---

# Security review

Review a diff along the security axis. This skill is read-only: it never
applies fixes, never edits files, and never pushes.

## Scope

Review the diff since the agreed base ref, or the pull request the user
names. Read the surrounding code, not just the changed lines.

## What to look for

- **Trust boundaries**: where input crosses from an untrusted source to a
  trusted context. Injection, deserialisation, path traversal.
- **OWASP-class bugs**: broken access control, cryptographic failures,
  SSRF, and insecure defaults in the changed code.
- **Secrets**: credentials, tokens, keys, and personal data in the diff.
  A secret in the diff is an immediate blocker.
- **Authorisation gaps**: endpoints or functions reachable without a
  permission check.
- **Supply-chain risk**: new dependencies, lockfile changes, install
  scripts, and pinned versions that cannot be verified.

## Output format

Every finding must name:

1. the file and line,
2. the failure path: how an attacker or a mistake reaches it,
3. the severity: blocker, major, or minor,
4. the smallest test that would expose it.

A finding that cannot name all four is a question, not a finding.

## Rules

- Read-only. No edits, no commits, no pushes.
- Report only what the diff introduces or fails to handle. Pre-existing
  issues are noted as context, not as blockers for this change.
- Say "no blockers found" only after checking every category above.
