---
type: research
title: The factory under a protected main branch
description: How branch protection and rulesets interact with the owner lane, the agent lane, and the evidence protocol, with a protection profile.
status: stable
tags: [research, governance, risk]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets", "https://docs.github.com/en/rest/repos/rules"]
---

# Research: the factory under a protected main branch

## Summary

Issue #25 asks how the factory operates when `main` is protected: no
direct pushes, every change through a pull request, possibly required
approvals. Three findings matter most.

First, the solo-owner deadlock is narrower than the issue feared: by
default, classic branch protection does not apply to administrators,
so the owner's merge of a high-risk pull request — decision 0002's
owner lane — keeps working. The deadlock bites only when bypass is
explicitly disallowed, and rulesets offer a better escape than the
classic default: `bypass_mode: pull_request`, which lets the owner
merge pull requests without required approvals but never push `main`
directly, and writes a bypass audit entry that becomes the recorded
human approval.

Second, the agent lane survives the same way (the agent merges with
the owner's credentials), but `required_approving_review_count` above
zero would block it in any repository where the merging identity cannot
bypass: GitHub never allows a user to approve their own pull request,
and agent pull requests are authored by the owner's account.

Third, the batch pattern from the issue works only with changes to the
evidence protocol and the gate's arithmetic: an aggregate of low-risk
changes can exceed the size ceiling by itself, and one evidence block
binds one commit. For busy repositories, GitHub's merge queue delivers
the batching benefit (grouped merges, one grouped check run) while
keeping per-pull-request revertability; for this factory, a capped
batch with one evidence line per constituent is the cheaper option.

## Provenance

| Item | Value |
| --- | --- |
| GitHub docs, protected branches | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches (fetched 2026-10-27) |
| GitHub docs, rulesets | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets (fetched 2026-10-27) |
| GitHub REST, rules API | https://docs.github.com/en/rest/repos/rules (fetched 2026-10-27), including `GET /repos/{owner}/{repo}/rules/branches/{branch}` and `bypass_mode` semantics |
| Self-approval block | Observed directly in this repository: `gh pr review` returns "Review Can not approve your own pull request" (session of 2026-10-25, PR #11) |
| Our repository | `/mnt/c/Users/joanp/Projects/ai-repo-template` at merge commit of PR #24, 2026-10-27: `AGENTS.md`, `CONTRIBUTING.md`, `TEMPLATE.md`, `factory.toml`, `scripts/factory.py`, `.github/workflows/factory.yml`, `docs/decisions/0002-*`, `docs/decisions/0003-*` |
| Issue | #25 |

## The three write paths and what protection touches

| Path | What it is today | Breaks when |
| --- | --- | --- |
| Owner lane | The owner merges a high-risk pull request; the merge is the human approval (`docs/decisions/0002-owner-merge-is-human-approval.md`) | `required_approving_review_count` above zero with bypass disallowed: the owner cannot approve a pull request authored by their own account |
| Agent lane | The agent merges a low-risk pull request on its own authority (`AGENTS.md`, Risk) | Any required approval the merging identity cannot satisfy, or required checks the diff cannot pass |
| Direct fixes | `TEMPLATE.md` says CI fixes land on `main` directly | Any protection that blocks direct pushes for the pushing identity |

## Protection options mapped to the lanes

Sources: the two GitHub documentation pages above; every row cites the
option as GitHub names it.

| Option | Enforcement | Effect on the factory |
| --- | --- | --- |
| Require pull request before merging | All merges go through a pull request | Closes the direct-fix path. Both other lanes already use pull requests: no change. |
| Require approvals (count above 0) | Merge needs N approving reviews from users with write access | Blocks both lanes unless the merging identity can bypass: agent pull requests are authored by the owner, and GitHub blocks self-approval. |
| Dismiss stale approvals on push | New commits void approvals | No effect while no approvals are required. |
| Require code owner review | CODEOWNERS must approve | Same deadlock as required approvals for solo owners: the owner is the only code owner. |
| Require status checks (check, docs, secret scan, dependency audit) | Deterministic jobs must be green | Strengthens both lanes: the agent cannot merge a red check even if instructed to. No conflict: these jobs pass on every conforming diff. |
| Require status checks (risk gate) | The risk job must be green | Fails by design on high-risk diffs (`scripts/factory.py`, `cmd_risk`). Requiring it hard-blocks high-risk merges for anyone without bypass; with owner bypass it becomes the audited record of decision 0002. |
| Require conversation resolution | All threads resolved | Compatible; no lane depends on open threads. |
| Require signed commits | Commits must be signed | Adds key management for the agent identity; no factory conflict, but setup cost. |
| Require linear history | Squash or rebase merges only | Changes revertability: today's merge commits revert one pull request each. Squash rewrites SHAs the evidence blocks bind (the pull request keeps the record, but `git revert` targets change). |
| Require merge queue | Merges happen in grouped batches | Delivers the batching benefit with per-PR revertability; see the batch analysis. |
| Do not allow bypassing | Rules apply to admins too | Creates the solo-owner deadlock. The factory must not enable this without a second approver. |

## The solo-owner deadlock and each escape

The deadlock: with required approvals and no bypass, a repository with
one human account cannot merge agent-authored pull requests, because
GitHub blocks self-approval (observed directly, see provenance).

1. **Admin bypass, default posture** — classic protection does not
   apply to administrators by default. The owner merges; both lanes
   keep working. This is what happens today in an unprotected personal
   repository plus protection defaults. It preserves decision 0002
   unchanged, but the bypass is not recorded anywhere except the merge
   itself.
2. **Ruleset bypass with `bypass_mode: pull_request`** — the owner can
   merge pull requests without the required approvals but cannot push
   `main` directly. Every bypass writes an audit entry, so the human
   approval of decision 0002 becomes a GitHub-audited event. This is
   the recommended escape: it closes the direct-fix path while keeping
   the owner lane, and it records the approval.
3. **A second approver account** — required approvals work as
   designed. Costs an account and its access. Only real fix when the
   organisation forbids bypass entirely.
4. **A GitHub App or bot as pull-request author** — the owner's account
   is no longer the author, so the owner can approve the pull request
   and the approval is a genuine review. Requires app infrastructure;
   overlaps with issues #20 (Copilot) and #21 (packaging). Strongest
   audit trail, highest setup cost.
5. **Do not require approvals; rely on the factory's own gate** —
   `required_approving_review_count: 0`, the risk gate and required
   checks carry the enforcement. No deadlock, no bypass needed. Loses
   GitHub's own approval record; the evidence block and the merge
   remain the record. This is the closest to the factory's current
   shape.

## The batch pattern analysed

The issue's example: collect multiple low-risk changes on one branch,
merge to `main` in a single pull request, one human review instead of
many.

- **Size ceiling.** `factory.toml` `[risk]` sets `max_files = 20` and
  `max_added_lines = 600`. The risk gate counts the aggregate diff
  (`scripts/factory.py`, `cmd_risk`, the `git diff --numstat` against
  the merge base). Ten low-risk changes of 70 added lines each already
  breach the line ceiling: the batch is high risk by the gate's own
  arithmetic. Batching without changing the arithmetic closes the very
  lane it tries to feed.
- **Evidence block.** The block binds one commit to one result
  (`CONTRIBUTING.md`, Pull requests). A batch carries several commits.
  A batch needs either one block per constituent (the pull request
  body lists them) or a new `batch:` field; one aggregate block would
  lie about which commit was verified.
- **Review axes.** Fresh-context review of an aggregate reviews the
  sum, not each change. The failure mode is a regression inside a
  constituent that the aggregate review treats as noise.
- **Revertability.** One revert reverts every constituent. The log
  discipline (`docs/log.md`) then needs a removal entry per
  constituent.
- **What batching actually saves here.** In a solo-owner repository
  there are no approvals to save: the owner never reviews their own
  pull requests. What batching saves is merge ceremonies and CI runs.
  What it costs is revert granularity and review dilution.

**Merge queue alternative.** GitHub's merge queue
(`required_status_checks` plus `merge_queue` rule) groups pull requests
into one batch check run (`grouping_strategy` ALLGREEN or HEADGREEN)
and merges the group, while each pull request stays a separately
revertable unit. This delivers the batching benefit without the
evidence and revert problems, but it does not reduce approvals, and it
matters only when several pull requests queue at once — not this
factory's current cadence.

**When to batch, proposal.** Batch only when: every constituent was
already gated and reviewed on its own branch; the batch is
documentation-only or one-spec work; the pull request body carries one
evidence line per constituent commit (a `batch:` list in the
`factory:evidence` block); and the gate evaluates each constituent
(`commit^..commit`) instead of the aggregate. Otherwise, merge each
change on its own branch. When more than a few pull requests queue per
day, prefer the merge queue to hand-built batches.

## A protection profile for the factory

Recommended ruleset on `main` (rulesets over classic protection:
readable by anyone, layered, with explicit bypass modes):

| Rule | Setting | Reason |
| --- | --- | --- |
| `pull_request` | required, `required_approving_review_count: 0` | No direct pushes; the risk gate replaces required reviews, avoiding the self-approval deadlock |
| `required_status_checks` | check, docs, secret scan, dependency audit; risk included | The agent cannot merge a red job even if instructed to; the owner's bypass of a red risk job is the audited owner merge of decision 0002 |
| `dismiss_stale_reviews_on_push` | off | No approvals to dismiss |
| `required_linear_history` | off | Keep merge commits: one revert per pull request |
| `bypass_actors` | the owner, `bypass_mode: pull_request` | The owner merges pull requests (recorded, audited) but never pushes `main` directly |
| `merge_queue` | off for now | Cadence does not justify it; revisit when pull requests queue daily |

If a second approver exists: raise `required_approving_review_count`
to 1 and drop the bypass, or keep the bypass for the agent lane only.

## What TEMPLATE.md should say under protection

Replace "land CI fixes on `main` directly" with: open a fix pull
request, label it `risk:high`, and let the owner merge it; the bypass
audit entry is the recorded approval. Never push `main` directly, and
never disable protection to ship a fix.

## factory.py detection feasibility

`GET /repos/{owner}/{repo}/rules/branches/{branch}` returns all active
rules for a branch and needs only read access: `factory.py audit` can
report the protection profile and warn when a configuration deadlocks
a lane (for example: required approvals above zero with no bypass for
the owner). Classic branch protection, by contrast, is readable only
by administrators, so detection covers rulesets fully and classic
rules partially. Feasible, small, and a natural `audit` extension.

## Open questions for the grilling session

1. Is the risk job required (bypass becomes the audited owner merge)
   or advisory (bypass unused, evidence block stays the record)?
2. `required_approving_review_count: 0` relies on the factory's own
   gate; does the owner accept GitHub holding no approval record?
3. Owner bypass mode: `pull_request` (recommended) or `always` (also
   restores the direct-fix path)?
4. Should the template ship the ruleset as part of `setup-project`
   (a `gh api` call creating it), or document it only?
5. Adopt the batch evidence format (`batch:` list) and per-constituent
   gate evaluation, or reject batching until cadence demands it?
6. Merge method: keep merge commits (current, revert-friendly) or
   move to squash (linear history, SHAs rewritten after merge)?

## Sources

- About protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- About rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- REST endpoints for rules: https://docs.github.com/en/rest/repos/rules
- Our repository: `AGENTS.md`, `CONTRIBUTING.md`, `TEMPLATE.md`, `factory.toml`, `scripts/factory.py`, `.github/workflows/factory.yml`, `docs/decisions/0002-owner-merge-is-human-approval.md`, `docs/decisions/0003-the-log-is-not-a-protected-path.md`

## Limits of this research

- Pricing and plan gating of rulesets (rulesets are a Team/Enterprise
  feature for organisation-owned repositories; personal repositories
  use classic protection) was not verified per plan: the branch
  protection documentation states bypass lists require an organisation;
  a personal repository falls back to classic protection with its
  admin default.
- The observed self-approval block is GitHub behaviour at the time of
  the session; the error message is quoted in provenance.
- Merge queue behaviour with required-workflow rules was read from the
  documentation, not exercised: no repository of ours currently uses a
  merge queue.
