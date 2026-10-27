---
type: research
title: The software-factory-skill branch of mattpocock/skills
description: What the branch adds, how it compares with this template, and what to adopt, reject, or grill.
status: stable
tags: [research, upstream, factory-design]
generated: { by: agent:opencode, at: 2026-10-26T00:00:00Z }
stale_after: 2027-01-26T00:00:00Z
sources: [mattpocock/skills branch software-factory-skill at b59cab42bf1206e1363eafc37f71b21c3bcaa12f, "https://github.com/mattpocock/skills/tree/software-factory-skill"]
---

# Research: the `software-factory-skill` branch of `mattpocock/skills`

## Summary

The branch adds one new skill, `software-factory`, to the `skills/in-progress/` bucket (SHA `99f13ca65db9`, path `skills/in-progress/software-factory/SKILL.md`). The skill is a **design-time glossary and reference set** for designing a *different kind* of factory from ours: a system of agents that turns "tickets, PRs and schedules into merged code, deployed on remote infrastructure the user chooses" (SKILL.md, first paragraph). It ships no scripts, no templates, no wizard and no configuration. It ships language: nine canonical terms, eleven example task patterns, four slot surveys for the products that fill the service slots, and a design-checking method ("start slow", "three brakes", "fill every slot", "question every task").

Our template is an implemented factory for one repository: a check CLI, a risk gate, an audit, typed knowledge, adapters and a setup skill. Their branch is a vocabulary for designing an autonomous, multi-run, remote factory. The overlap is conceptual, not mechanical. Their three brakes (automated checks, automated review, human review) match mechanisms our template already enforces (`.factory/factory.py` check; `code-review` in the review order in `AGENTS.md`; the risk gate in `CONTRIBUTING.md`/`factory.toml`). Their survey format carries staleness discipline that matches our OKF research conventions. The branch is 12 commits ahead of our exact pinned commit and lives in a bucket that the upstream README says "can change or disappear without warning" (path `skills/in-progress/README.md`). Our pin needs no change now.

Issue: #19 ("Research: mattpocock/skills software-factory-skill branch").

## Provenance

| Item | Value |
| --- | --- |
| Repository | https://github.com/mattpocock/skills |
| Branch | `software-factory-skill` |
| Branch head SHA | `b59cab42bf1206e1363eafc37f71b21c3bcaa12f` (committed 2026-10-22T09:35:26Z) |
| Base (merge base) | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` (main tip; committed 2026-10-19T15:51:40Z) |
| Ahead / behind | 12 commits ahead of `main`, 0 behind (compare API `main...software-factory-skill`) |
| Date fetched | 2026-10-26 |
| Fetch method | `gh api repos/mattpocock/skills/compare/main...software-factory-skill`; per-commit `gh api repos/mattpocock/skills/commits/<sha>`; per-file `gh api repos/mattpocock/skills/contents/<path>?ref=software-factory-skill` |
| Our repository | `/mnt/c/Users/joanp/Projects/ai-repo-template`, read at `HEAD` on 2026-10-26 |
| Note on the base | The merge base equals the commit our `factory.toml` records as the tested prerequisite pin (`[prerequisites] commit = "5beb35b040e3de97e54fa9e386d7e42d15c295c2"`, version 1.3.1) |

## Commit inventory

All 12 commits are authored with "Co-Authored-By: Claude Opus 5.5". All messages start with `software-factory:`. Source: compare API and per-commit API, 2026-10-26.

| # | SHA | Date (UTC) | Message |
| --- | --- | --- | --- |
| 1 | `99f13ca65db9cfd2ce5b7c6744e0183761c6db74` | 2026-10-21 14:30 | add glossary skill for designing a factory |
| 2 | `314685d8aab34d6cdb3acd8dc5eacae11cf3d57d` | 2026-10-22 09:03 | add example runs grouped by problem |
| 3 | `30e286ea0b829f38e5c47ed879d740189547eeca` | 2026-10-22 09:07 | separate automated review from human review, add ratchet example |
| 4 | `0923e01e0dec33159a067a662805f38cf55626ae` | 2026-10-22 09:08 | drop review definitions, keep the stricter wording |
| 5 | `471c5d4b17921e3b2d03ad9131a3a1be139ad03c` | 2026-10-22 09:18 | optional observability platform, slot surveys |
| 6 | `0ce32720705f0171e939a8b16fc3b7efc8ea8efc` | 2026-10-22 09:22 | slot surveys orient, the agent researches current options |
| 7 | `9981d80c0d6e0ec45469dc32973ea2b58aee6ade` | 2026-10-22 09:29 | add Task; example runs become example tasks |
| 8 | `0d83ab2defc008d5b8cf236074728bb313d03346` | 2026-10-22 09:32 | start slow, accelerators and brakes |
| 9 | `d77f4ba10f776f06f391fca8d799b4fd5680e3f6` | 2026-10-22 09:33 | start slow with throttled automated triggers |
| 10 | `e986694a18bb2671f91eb5a65e02b3232d78ab76` | 2026-10-22 09:33 | tighten start slow |
| 11 | `af6eaba654604ee7eb274dfcb59be75a119dcfe2` | 2026-10-22 09:34 | define the three brakes |
| 12 | `b59cab42bf1206e1363eafc37f71b21c3bcaa12f` | 2026-10-22 09:35 | tasks work on tickets, PRs or the codebase |

## File inventory

Source: compare API file list, cross-checked with per-commit file lists. Additions: 517 lines across 8 files; no deletions except the rename of `EXAMPLE-RUNS.md` to `EXAMPLE-TASKS.md`.

| File | Status | Lines | Purpose | Introduced by |
| --- | --- | --- | --- | --- |
| `.changeset/software-factory-skill.md` | added | +5 | Release note: patch bump for the plugin; announces the skill and says "Call it alongside a grilling session" | `99f13ca65db9` (edited by `314685d8`, `471c5d4b`, `9981d80c`) |
| `skills/in-progress/README.md` | modified | +1 | Adds the skill to the in-progress list with a one-line description | `99f13ca65db9` (edited by `9981d80c`) |
| `skills/in-progress/software-factory/SKILL.md` | added | +98 | The skill body: frontmatter, the glossary, the design method (start slow, three brakes, fill every slot, question every task) | `99f13ca65db9` (edited by all later commits) |
| `skills/in-progress/software-factory/EXAMPLE-TASKS.md` | added (renamed from `EXAMPLE-RUNS.md`) | +80 | Eleven task patterns grouped by the problem each solves | `314685d8aab3` as EXAMPLE-RUNS.md; renamed in `9981d80c0d6e` |
| `skills/in-progress/software-factory/TICKET-TRACKERS.md` | added | +85 | Survey of ticket-tracker products, six types, selection questions, durable gotchas | `471c5d4b1792` |
| `skills/in-progress/software-factory/GIT-HOSTS.md` | added | +84 | Survey of git hosts, six types, five selection questions, durable gotchas | `471c5d4b1792` |
| `skills/in-progress/software-factory/RUNNERS.md` | added | +94 | Survey of runner products, five types in a table, selection questions, staleness list | `471c5d4b1792` |
| `skills/in-progress/software-factory/OBSERVABILITY-PLATFORMS.md` | added | +75 | Survey of observability options, four types (type 1 is "none"), five hooks, selection questions | `471c5d4b1792` |

## Feature descriptions

### F1. Glossary skill with canonical terms and avoid-lists

**Provenance**: `skills/in-progress/software-factory/SKILL.md`, added in `99f13ca65db9`, edited through `b59cab4`.

The skill defines nine terms, each with an *Avoid* list the agent must correct: **Task** (a kind of work defined once and run many times: review, explore, implement, ratchet), **Trigger**, **Run** (one execution, "treated as a black box", "a run never waits for a human"; *Avoid*: session), **Runner** (the disposable machine; nothing survives a run; the only memory is the ticket tracker, the git host and the orchestrator), **Ticket tracker** (the human interface), **Ticket source** (anything outside that files tickets: a feedback button, a monitor, an error tracker), **Git host**, **Orchestrator** (receives triggers, starts runs, records queue state), **Observability platform** (optional; "a run never decides on it until something writes it into the ticket tracker or git host").

The frontmatter sets `disable-model-invocation: true`: the skill is user-invoked only. The description in the changeset says "Call it alongside a grilling session" (`.changeset/software-factory-skill.md`).

### F2. Example tasks grouped by problem

**Provenance**: `skills/in-progress/software-factory/EXAMPLE-TASKS.md`, added as EXAMPLE-RUNS.md in `314685d8aab3`, reworked in `30e286ea0b82`, `0923e01e0dec`, `d77f4ba10f77`, renamed in `9981d80c0d6e`.

Eleven patterns, each with trigger, action and what it triggers next: **Explore** (triage a new ticket), **Implementer** (build a ready ticket until automated checks pass, open a draft PR), **Automated review** (review the diff against standards and ticket; on a fail trigger rework; on a pass end and wait for human review), **Rework** (fix only what the review named; after a set number of fails, end with the PR labelled waiting for a human), **Decompose** (split a spec into dependency-ordered tickets), **Ratchet** (a daily clock takes one file off an exception list, fixes it under the stricter check, opens a PR; "one small PR a day"), **Fix** (the factory repairs its own failed runs; fix runs never chain; always human-reviewed), **Architecture** (nightly scan files refactoring candidates as one ticket), **Retro** (throttled to one merged PR in ten; proposes changes to the factory's own instructions as a PR). Two ticket-source patterns: a feedback button, and a monitor that reopens tickets when a problem persists.

### F3. Start slow: accelerators, throttling and the three brakes

**Provenance**: `skills/in-progress/software-factory/SKILL.md`, section "Start slow"; introduced `0d83ab2defc0`, tightened `d77f4ba10f77`, `e986694a18bb`, finalised in `af6eaba65460` ("define the three brakes").

"Every trigger is an accelerator. Accelerators without brakes make a slop cannon." The three brakes: **automated checks** (deterministic gates: types, lint, tests), **automated review** (a separate run that reads the diff cold against the standards and the ticket), **human review** (what it catches becomes new automated checks and sharper automated review). Triggers are added one at a time, throttled at first (one bug report in ten, a clock once a day), with human review on every PR; every loop of runs is capped at a few tries before a human.

### F4. Slot surveys with staleness discipline

**Provenance**: the four survey files, added in `471c5d4b1792`, reoriented in `0ce32720705f` ("slot surveys orient, the agent researches current options").

Each survey: a header "Surveyed 2026-10, and not guaranteed to be up to date"; product types grouped by when a factory picks them; a "Researching further" section of the questions that decide the slot; named primary sources (API and webhook references, pricing pages, changelogs — "Prefer these over blog posts and comparison sites", TICKET-TRACKERS.md); a ranked "what goes stale fastest" list; and "durable gotchas" that must be re-verified before use (for example the `GITHUB_TOKEN` chain trap, GIT-HOSTS.md). The surveys orient the user; the agent then researches current options itself.

### F5. Design-completion criteria

**Provenance**: `skills/in-progress/software-factory/SKILL.md`, sections "Fill every slot", "Question every task"; evolved in `9981d80c0d6e` and `b59cab42bf12` ("tasks work on tickets, PRs or the codebase").

A design has slots (services) and tasks. Each slot names a product, or a deliberate none for the observability platform. One product may fill several slots ("All on GitHub" example table). Each task answers five questions: what triggers it; what it does and which services it reads and writes; what it triggers next; where a human re-enters; what stops two runs doing the same work. Each ticket source answers: what stops it filing the same ticket twice. "Buy the services and build the tasks."

### F6. In-progress distribution channel

**Provenance**: `skills/in-progress/README.md` on the branch; `.changeset/software-factory-skill.md`.

The README states: beta skills are "excluded from the plugin and the top-level README until they graduate to a stable bucket", get no docs pages, and "can change or disappear without warning". A user installs one directly: `npx skills@latest add mattpocock/skills --skill=<name>`. The changeset nevertheless records a **patch** bump for the plugin.

### F7. Their existing setup skill (baseline, on main, not on the branch)

**Provenance**: `skills/engineering/setup-matt-pocock-skills/SKILL.md` at `main` (`5beb35b`).

`setup-matt-pocock-skills` is a prompt-driven, user-invoked setup skill: it explores the repo, then asks three sections — issue tracker (GitHub, GitLab, local markdown, other), triage label vocabulary (five canonical roles), domain docs layout (single-context or multi-context) — writes `docs/agents/issue-tracker.md`, `triage-labels.md`, `domain.md`, and adds an `## Agent skills` block to `CLAUDE.md` or `AGENTS.md` (never creating one when the other exists). Our `.claude/skills/setup-project/SKILL.md` delegates to it and wraps it with factory-specific steps (identity documents, `factory.toml`, first passing test, factory labels, reserved docs paths).

## Comparison table: their software factory vs our template

Sources: their `skills/in-progress/software-factory/SKILL.md` and surveys (branch head `b59cab4`); our `AGENTS.md`, `TEMPLATE.md`, `factory.toml`, `.factory/factory.py`, `docs/index.md`, `.claude/skills/setup-project/SKILL.md`.

| Axis | Their software-factory skill | Our template |
| --- | --- | --- |
| **Kind of artefact** | A reference skill: glossary, example tasks, product surveys, design questions. No code. | A working repository: contracts, CLI, CI, labels, adapters, setup skill. |
| **Object designed** | An autonomous multi-agent system on remote infrastructure: "a run never waits for a human" (SKILL.md, Run). | A single repository worked by one agent in one session, with a human at every merge decision (`AGENTS.md`, Risk). |
| **Contracts** | Language contract only: canonical terms with avoid-lists. | Written contracts: `INTENT.md`, `CONTEXT.md`, `GLOSSARY.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md` (`TEMPLATE.md`, "Why the shape is like this"). |
| **Knowledge** | Survey documents with survey date, staleness ranking, durable gotchas; the agent researches current options. | `docs/` as an OKF v0.2 bundle: typed frontmatter, `stale_after` deadlines, provenance in research docs (`docs/index.md`; `factory.py docs`). |
| **Check CLI** | Named as a brake: "deterministic gates (types, lint, tests) that every run must pass" (SKILL.md, three brakes). No CLI shipped. | `.factory/factory.py`: `check` (fails closed when source changed and nothing ran), `docs`, `risk`, `audit` (`.factory/factory.py`). |
| **Risk gate** | Human review as one brake among three; throttling and loop caps as soft design guidance. | A hard gate: protected paths, size ceiling, evidence block bound to `HEAD`, `risk:high` label plus human approval (`factory.py` `cmd_risk`; `factory.toml` `[risk]`). |
| **Review order** | Automated review separated from human review; rework loops capped (EXAMPLE-TASKS.md). | `code-review` → `security-review` → `verify` → `finding-verifier`, each with fresh context, four inputs, no author reasoning (`AGENTS.md`, Evidence and review order). |
| **Audit** | Not present. | `factory.py audit`: prerequisite skills present, docs valid, no unreferenced skills, no duplicated instructions between contract files, no permission drift between harnesses. |
| **Adapters** | Not present; the surveys name integration surfaces (webhooks, bot identities, OTel hooks). | `.claude/skills/` (one location, no mirror), `.opencode/commands/`, permission files kept in step by `audit` (`TEMPLATE.md`, Layers table). |
| **Distribution** | Global `mattpocock/skills`; in-progress skills installed one by one with `npx skills add --skill=<name>`; excluded from the plugin (`skills/in-progress/README.md`). | Global install of the same upstream, tested pin recorded in `factory.toml` `[prerequisites]`; local skills in `.claude/skills/` only (`TEMPLATE.md`). |
| **Wizard / setup** | `setup-matt-pocock-skills` on main: tracker, labels, domain docs, `docs/agents/*.md`. | `.claude/skills/setup-project/SKILL.md`: rewrites identity documents and `factory.toml`, scaffolds a first passing test, creates factory labels, reserves `docs/agents/` paths, then delegates to that upstream skill. |
| **Updates** | Surveys dated and ranked by staleness; gotchas must be re-verified; the agent researches current options. | `stale_after` frontmatter checked by `factory.py docs`; provenance and commit-bound evidence; review order re-verifies every ticket. |
| **Task patterns** | Eleven named tasks (explore, implementer, automated review, rework, decompose, ratchet, fix, architecture, retro) plus ticket sources. | Workflow pieces exist but are not named as a pattern catalogue: `implement`, `tdd`, `code-review`, `to-spec`, `to-tickets`, `retro` skills (`factory.toml` `[prerequisites]`), spec→tickets→implement in `AGENTS.md` Workflow. |
| **Failure of the factory itself** | A Fix task: failed runs file a ticket; fix runs never chain; always human-reviewed (EXAMPLE-TASKS.md). | Not automated. CI fixes land on `main` with owner approval (`TEMPLATE.md`, first tickets). |

## Per-feature recommendations

### F1 Glossary terms — **NEEDS GRILLING**

Their vocabulary names objects our template partly has (ticket tracker, git host, automated checks) and partly does not (orchestrator, runner, ticket source). `docs/index.md` already says "Align with `mattpocock/skills` conventions where practical", so adopting the overlapping terms in `GLOSSARY.md` is consistent with that decision. But their term **Run** carries the rule "a run never waits for a human" (SKILL.md), which contradicts our risk gate: "High risk: anything else. A human approves the merge" (`AGENTS.md`, Risk). We must not import a term whose definition fights our own gate. The owner decides which terms enter `GLOSSARY.md`, with that sentence removed or amended.

### F2 Example tasks, especially the ratchet — **NEEDS GRILLING**, with one **ADOPT**

Most patterns already exist here as upstream skills (`implement`, `code-review`, `retro` in `factory.toml` `[prerequisites]`), so recording them again would duplicate the workflow layer and violate "One meaning, one place" (`TEMPLATE.md`, Why the shape is like this). The **ratchet** pattern is new: an exception list under a stricter check, one file fixed per day, one small PR (`EXAMPLE-TASKS.md`, Migrating to a stricter automated check). Nothing in our template or upstream records it. **ADOPT the ratchet as a `playbook` in `docs/playbooks/`** with provenance to `EXAMPLE-TASKS.md` — it is cheap, matches the OKF type list (`factory.toml` `[docs]` types), and helps any derived project migrating a check. The remaining patterns: needs grilling; most are already covered.

### F3 Start slow / three brakes — **REJECT (as new wording); keep as confirmation**

Our template already implements all three brakes as mechanisms: automated checks (`uv run .factory/factory.py check`, the only check entry point, `AGENTS.md` One command); automated review (`code-review` in the review order, `AGENTS.md`); human review (the risk gate and the owner's approval, `AGENTS.md` Risk). Restating their wording in our contract files would add a second statement of the same rules, which `factory.py audit` itself flags as a defect (`_duplicated_instructions`, `.factory/factory.py`). Reject the wording; cite their formulation only as external confirmation that our shape matches upstream thinking, if anything.

### F4 Slot-survey format — **ADOPT (the format conventions, not the content)**

Their survey discipline fits our OKF research type: a survey date at the top; answers ranked by how fast they go stale; "durable" facts separated from stale ones and marked for re-verification; primary sources preferred over commentary; the agent researches current options instead of trusting the file (all four survey files, "Researching further" sections). Our `factory.py docs` already checks `stale_after` (`docs_findings`), and `docs/index.md` already defines `research/` as "findings from sources, with provenance". Adopt the "stalest first" ordering and the durable-gotcha split as writing rules for `docs/research/` documents. This costs little and strengthens the existing convention.

### F5 Design-completion criteria — **NEEDS GRILLING**

The five questions per task and the "what stops two runs doing the same work" question are good grilling material for any derived project that adds CI automation or scheduled agents. But our template has no orchestrator and no scheduled runs, and `INTENT.md` is still placeholder in this template, so there is no scope statement to justify adding a design checklist yet. The owner decides whether a `concept` or `playbook` document records the checklist for future use.

### F6 In-progress distribution — **REJECT for the pin (no change); watch it**

See the pin analysis below. Do not add `software-factory` to `[prerequisites]` while it is in the in-progress bucket: the bucket README says these skills "can change or disappear without warning" (`skills/in-progress/README.md`), and `AGENTS.md` says "A missing skill is an install error" — a prerequisite that can disappear turns an install error into a certainty. Revisit when it graduates to a stable bucket.

### F7 Their setup skill vs our setup-project — **NO CHANGE (ours supersedes)**

Our `.claude/skills/setup-project/SKILL.md` already wraps and extends `setup-matt-pocock-skills`: it rewrites the identity documents, configures the check command, scaffolds a first passing test, creates the factory labels the upstream skill does not create (`spec`, `blocked`, `risk:low`, `risk:high`, `agent-merge`), and reserves `docs/agents/*.md` paths in `[docs].reserved` so the upstream output does not break the OKF validation. Nothing on the branch changes the upstream setup skill (compare API: no changes under `skills/engineering/`). No action.

### The pin: tested-prerequisite relevance — **report**

Our `factory.toml` pins `mattpocock/skills` version 1.3.1 at commit `5beb35b040e3de97e54fa9e386d7e42d15c295c2`. Facts: (1) the compare API reports `main` is 0 commits ahead of the branch's fork point and the merge base is `5beb35b`, i.e. **our pinned commit is exactly main's tip** as of 2026-10-26; the branch is our pin plus 12 commits. (2) The changeset on the branch declares a **patch** bump (`.changeset/software-factory-skill.md`), so a merge and release would produce a 1.3.x release. (3) The skill sits in `skills/in-progress/`, which the bucket README says is excluded from the plugin; the direct-install path is `npx skills@latest add mattpocock/skills --skill=software-factory`. What this means for the pin: nothing now — `software-factory` is not in our `required` or `optional` lists, so a patch release that carries it changes no behaviour for us. When and if the skill graduates to a stable bucket, a future release could make it installable through the plugin; only then should we consider adding it to `optional`. A patch release does not invalidate the tested pin by itself, but our rule "A missing skill is an install error" (`AGENTS.md`, Skills) argues for pinning releases, not branches, and for re-running the audit after any pin bump (`factory.py audit` checks installed skills).

## Open questions for the grilling session

1. Which of their glossary terms (if any) enter our `GLOSSARY.md` and `CONTEXT.md`, given that their **Run** definition ("a run never waits for a human") conflicts with our risk gate?
2. Do we record the ratchet pattern as a `docs/playbooks/` entry now, or wait for a derived project that needs it?
3. Do we adopt the survey-writing rules (survey date, stalest-first ranking, durable-gotcha split, primary sources) into the `docs-knowledge` skill or `CONTRIBUTING.md` writing rules, and where do they live under "one meaning, one place"?
4. Is the design-completion checklist (five questions per task) worth a `concept` document, or is it out of scope for a template whose factory is local-first?
5. Should `factory.toml` `[prerequisites].optional` gain `software-factory` the day it graduates to a stable bucket, with the pin bumped to the release that carries it?
6. Does the owner want any of the template's own machinery (check, risk gate, review order) renamed to match their vocabulary (for example "automated checks", "automated review", "human review")? Renaming touches protected paths (`AGENTS.md`, `factory.toml`) and is therefore high risk by our own rules.

## Sources

- Compare API, `main...software-factory-skill`: https://api.github.com/repos/mattpocock/skills/compare/main...software-factory-skill (fetched 2026-10-26)
- Branch head metadata: https://api.github.com/repos/mattpocock/skills/branches/software-factory-skill (fetched 2026-10-26)
- `skills/in-progress/software-factory/SKILL.md` at `b59cab4`: https://github.com/mattpocock/skills/blob/software-factory-skill/skills/in-progress/software-factory/SKILL.md
- `skills/in-progress/software-factory/EXAMPLE-TASKS.md` at `b59cab4`: https://github.com/mattpocock/skills/blob/software-factory-skill/skills/in-progress/software-factory/EXAMPLE-TASKS.md
- `skills/in-progress/software-factory/TICKET-TRACKERS.md`, `GIT-HOSTS.md`, `RUNNERS.md`, `OBSERVABILITY-PLATFORMS.md` at `b59cab4` (same directory)
- `.changeset/software-factory-skill.md` at `b59cab4`: https://github.com/mattpocock/skills/blob/software-factory-skill/.changeset/software-factory-skill.md
- `skills/in-progress/README.md` at `b59cab4`: https://github.com/mattpocock/skills/blob/software-factory-skill/skills/in-progress/README.md
- `skills/engineering/setup-matt-pocock-skills/SKILL.md` at `main` (`5beb35b`): https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md
- Our repository (read-only, at `HEAD`, 2026-10-26): `AGENTS.md`, `INTENT.md`, `TEMPLATE.md`, `factory.toml`, `.factory/factory.py`, `docs/index.md`, `.claude/skills/setup-project/SKILL.md`
- Issue #19: `gh issue view 19` in `/mnt/c/Users/joanp/Projects/ai-repo-template`

## Limits of this research

- The upstream repo's release process beyond the changeset (which release will carry the branch, and when) cannot be determined from the branch; only the patch bump and the in-progress exclusion are facts.
- `INTENT.md` and `GLOSSARY.md` in this template are still placeholder documents (see `INTENT.md` comment blocks), so recommendations that cite "our design rules" cite `AGENTS.md`, `TEMPLATE.md`, `docs/index.md`, and `factory.toml` instead.
- Per-commit attribution of paragraphs inside `SKILL.md` (which commit wrote which term) was not traced line by line; the file-level provenance in the commit inventory is complete.
