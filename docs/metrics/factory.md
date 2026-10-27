---
type: metric
title: Software-factory metrics
description: Definitions and formulas for lead time, review round-trips, escaped defects, rework, agent-merge share, and override rate.
status: stable
tags: [metrics, workflow]
generated: { by: agent:opencode, at: 2026-10-25T00:00:00Z }
---

# Purpose

These metrics measure the factory, not the people. Each has a formula
and a collection cadence. No dashboard: collect by hand, from the issue
tracker and the update log, on the cadence stated below.

# Metrics

## Lead time

The time from the first commit on a branch to the merge of its pull
request.

```text
lead time = merge time - first commit time (branch)
```

Unit: days, one decimal. Cadence: collect for every merged pull request;
review monthly.

## Review round-trips

The number of review cycles a pull request needs before it merges.

```text
round-trips = count of review comments + 1 (per pull request)
```

Count a round-trip only when the author changes code in response. The
initial review is the baseline, not a round-trip. Unit: cycles. Cadence:
collect for every merged pull request; review monthly.

## Escaped defects

A defect found on `main` that a review or a check should have caught.

```text
escaped defects = count of issues labelled bug after merge (per month)
```

Unit: defects per month. Cadence: count monthly; review quarterly.

## Rework

The share of merged lines that a later change removed or rewrote within
30 days.

```text
rework = lines rewritten within 30 days / lines merged (per month)
```

Unit: per cent. Cadence: compute monthly from the diffs; review
quarterly.

## Agent-merge share

The share of merged pull requests that an agent merged on its own
authority, under the low-risk lane.

```text
agent-merge share = agent-merged pull requests / merged pull requests (per month)
```

Unit: per cent. Cadence: compute monthly from the `agent-merge` label;
review monthly.

## Override rate

The share of high-risk pull requests merged while the risk gate was
red, per the owner-merge decision
([0002](../decisions/0002-owner-merge-is-human-approval.md)).

```text
override rate = red-risk merges / high-risk merges (per month)
```

Unit: per cent. A rising override rate means the ceiling or the protected
list no longer matches the work. Cadence: compute monthly; review
monthly.

# Reading the numbers

- Lead time up and round-trips flat: the tickets are too large.
- Escaped defects up: the check list is missing a class of defect.
- Agent-merge share falling: the protected list or the size ceiling is
  too tight, or the agent needs more help than the lane allows.
- Override rate above zero for two months: re-cut the tickets so that
  harness changes become rare.

Record a monthly retro in `docs/project-mng/retros/` when any metric moves by more
than half of its previous value.
