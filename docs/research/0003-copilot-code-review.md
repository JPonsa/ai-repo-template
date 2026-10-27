---
type: research
title: GitHub Copilot as a reviewer in the factory loop
description: How Copilot reviews are triggered and read, the approval defect in the risk gate, and the rule proposal for the review order.
status: stable
tags: [research, review, automation]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review", "https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review", "https://docs.github.com/en/rest/repos/rules"]
---

# Research: GitHub Copilot as a reviewer in the factory loop

## Summary

Issue #20 asks whether GitHub Copilot can review pull requests in this
factory, and whether the factory can automatically consume its reviews
and iterate on them.

The answer is yes, with one real defect found in our own gate. Copilot
code review is requestable through `gh` (`--reviewer @copilot`) or the
REST API (`copilot-pull-request-reviewer[bot]`), or automatically per
pull request through a ruleset. Its review lands as an ordinary review
entity with severity-labelled comments, so `factory.py risk` already
reads it today with zero code changes: the same `gh pr view --json
reviews` call returns it.

The defect: Copilot can submit approving reviews when "Copilot
approvals" are enabled (public preview, off by default). Our risk gate
counts any APPROVED review from an author other than the pull-request
author as human approval (`scripts/factory.py`, `cmd_risk`). A Copilot
bot approval would satisfy that test today: the bot is not the pull
request author. The gate must exclude bot authors, and the factory must
keep Copilot approvals off — an AI approval must never stand in for the
human approval of decision 0002.

The loop composes cleanly: Copilot's findings become inputs to the
finding-verifier, never trusted blockers; confirmed findings get fixed
by our own agent with tests; the review is re-requested on the next
push. GitHub's own documentation carries the validation rule: "Copilot
is not guaranteed to spot all problems... Always validate Copilot's
feedback carefully. Supplement Copilot's feedback with a human review."

## Provenance

| Item | Value |
| --- | --- |
| Using GitHub Copilot code review | https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review (fetched 2026-10-27) |
| GitHub Copilot code review (concepts) | https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review (fetched 2026-10-27) |
| Ruleset `copilot_code_review` rule | REST rules API, fetched 2026-10-27, recorded in `docs/research/0002-protected-main.md` |
| Our gate code | `scripts/factory.py`, `cmd_risk`, the `approved_by` list comprehension |
| Our review order | `AGENTS.md`, Evidence and review order |
| Issue | #20 |

## Mechanism: how a Copilot review is enabled and triggered

- **Per pull request, from the CLI**: `gh pr create --reviewer @copilot`,
  or `gh pr edit <number> --add-reviewer @copilot`. The factory can do
  this in the same command that opens a pull request.
- **Per pull request, from the API**: request
  `copilot-pull-request-reviewer[bot]` as a reviewer through the review
  requests endpoint.
- **Automatic, for every pull request**: a repository ruleset with the
  `copilot_code_review` rule; parameters `review_on_push` (re-review
  every push) and `review_draft_pull_requests`. The protection profile
  from `docs/research/0002-protected-main.md` can carry this rule in the
  same ruleset.
- **Availability**: requires Copilot access (Business or Enterprise for
  organisation repositories; members without a licence can be enabled
  by an administrator). Effort levels: Lite (cheap, targeted) or
  Balanced (default, deeper reasoning).

## What a Copilot review looks like and how the factory reads it

- It is a review entity: by default a "Comment" review, not "Approve"
  or "Request changes", so it does not count toward required approvals.
- Its comments behave like human review comments: reactions, replies,
  resolve, hide. Each comment carries a severity label: High, Medium, or
  Low. Where possible it attaches suggested changes.
- Reading it needs no new code: `gh pr view --json reviews` returns
  bot reviews like any other; `factory.py risk` already calls this
  (`gh_json("body,labels,reviews,author", "pr", "view")`).
- Excluded files: dependency manifests (package.json, lock files), log
  files, SVG files. Copilot will not review supply-chain changes; our
  `security-review` axis and the dependency-audit CI job keep that
  coverage.
- Re-review: on new pushes only when `review_on_push` is enabled or the
  review is re-requested; Copilot may repeat comments already dismissed.

## The defect: Copilot approvals would defeat the human gate

"When Copilot approvals are enabled in repository, organization, and
enterprise settings, Copilot can submit an approving review that
satisfies your repository's required-approval rule the same way a
teammate's approval would" (concepts page, Copilot approvals, public
preview). Approvals are off by default.

Our gate, `cmd_risk` in `scripts/factory.py`:

```python
approved_by = [
    (review.get("author") or {}).get("login", "")
    for review in pr.get("reviews", [])
    if review.get("state") == "APPROVED"
    and (review.get("author") or {}).get("login", "") != pr_author
]
```

A Copilot approving review has state APPROVED and author
`copilot-pull-request-reviewer[bot]`, which is not the pull request
author. It would be counted as human approval, and a `risk:high` pull
request would pass rule 4 without any human involved.

**Fix, two layers**: exclude bot authors (login ending in `[bot]`)
from `approved_by` in `cmd_risk`; and keep Copilot approvals disabled in
this factory's configuration guidance. The first layer is defence in
depth: it protects the gate even when an organisation enables approvals
at a level the repository cannot turn off.

## The iterate loop

1. The pull request opens; Copilot reviews (requested by the factory or
   automatically by the ruleset), under 30 seconds typically.
2. The factory reads the review: comments with file, line, severity,
   and body.
3. Each High or Medium finding becomes one input to the
   `finding-verifier`: confirmed, refuted, or unproven. Copilot's
   findings get no special trust — the same rule as every reviewer.
4. Confirmed findings are fixed by our own agent, with a test at the
   seam; "Fix with Copilot" cloud agent is available but not preferred,
   because a fix through our agent goes through `check` and the review
   axes.
5. The review is re-requested after the fix commits, or re-runs on push
   when `review_on_push` is on.
6. Low-severity findings are recorded and dismissed if unproven; the
   override rate metric covers false-positive pressure.

## Rule proposal: where Copilot sits in the review order

Copilot becomes the first pass, before the fresh-context agent
reviewers, as a cheap finding generator (Lite effort for routine
changes, Balanced for protected paths):

```text
copilot-review (first pass, advisory, never gates)
→ code-review (standards and spec axes, fresh contexts)
→ security-review (with an attack list)
→ verify (evidence bound to the exact commit)
→ finding-verifier (challenges every blocker, Copilot's included)
```

Guardrails, stated as rules:

- Copilot never approves: approvals stay off; the gate filters bots.
- Copilot never gates: its findings gate only through the
  finding-verifier, as confirmed and reproduced.
- Copilot reads the same contracts: it reads `AGENTS.md` from the
  head branch natively; `.github/copilot-instructions.md` can point it
  at `CODING_STANDARDS.md` and `GLOSSARY.md` for review guidance.

## Costs

An estimated USD 0.05 to 1 per Lite review, USD 0.25 to 5 per Balanced
review, in AI credits, plus GitHub Actions minutes for the agentic
capabilities (context gathering). For automatic reviews, usage is
billed to the pull request author by default; reviews on bot-authored
pull requests bill the organisation. The dry run of #21 (packaging)
should treat this as a per-review cost line.

## Open questions for the grilling session

1. Automatic review by ruleset for every pull request, or
   factory-requested per pull request only when it wants one?
2. Effort level: Lite as the default first pass, Balanced for
   protected paths — or Balanced everywhere?
3. Land the `cmd_risk` bot filter now, even with approvals off?
4. Does `AGENTS.md` add the copilot first pass to the review order
   (a protected-path change)?
5. Write `.github/copilot-instructions.md` pointing at
   `CODING_STANDARDS.md` and `GLOSSARY.md`?
6. Who fixes confirmed findings: our agent through `check` (proposed),
   or the "Fix with Copilot" cloud agent?
7. Can `factory.py audit` read the Copilot approvals setting through
   the API? The setting is repository and organisation configuration;
   the endpoint was not confirmed in this research.

## Sources

- https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review
- https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review
- https://docs.github.com/en/rest/repos/rules (the `copilot_code_review` rule, via `docs/research/0002-protected-main.md`)
- `scripts/factory.py` (`cmd_risk`), `AGENTS.md`,
  `docs/decisions/0002-owner-merge-is-human-approval.md`

## Limits of this research

- No Copilot review was exercised live: no Copilot plan is confirmed on
  this account, so the review entity was read from documentation, not
  observed. The severity labels, the Comment review state, and the
  review entity shape are documented behaviour.
- The repository or organisation settings endpoint that reads the
  Copilot approvals configuration was not found in this research; the
  audit feasibility question stays open.
- Pricing ranges are GitHub's published estimates and may change.
