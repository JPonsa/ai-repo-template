---
name: docs-knowledge
description: Read and write the OKF v0.2 bundle under docs/. Enforce typed frontmatter, provenance, freshness, reserved files, and log.md discipline.
---

# Docs knowledge

Read and write the knowledge bundle in `docs/`. The bundle follows
Open Knowledge Format v0.2. `uv run .factory/factory.py docs` validates
the structure; this skill governs how you write into it.

## The seven allowed types

Every concept document under `docs/` carries a `type` in its
frontmatter. The allowed types are:

| Type | Folder | Holds |
| --- | --- | --- |
| `decision` | `decisions/` | a choice, its reason, and its consequence |
| `concept` | `concepts/` | domain terms and system models |
| `runbook` | `runbooks/` | repeatable operational steps |
| `research` | `research/` | findings from sources, with provenance |
| `metric` | `metrics/` | definitions and formulas |
| `retro` | `retros/` | what changed after a piece of work |
| `playbook` | `playbooks/` | multi-step procedures, not tied to operations |

Create a folder when the first document of that type arrives. Keep the
folder name equal to the plural of the type.

## Reserved files

`index.md`, `log.md`, and `architectural-overview.md` are reserved at
the bundle root. They carry no typed frontmatter. Only `index.md`
declares `okf_version`. Do not move them into folders.

## Writing a concept

Frontmatter fields: `type` is required. Optional: `title`,
`description`, `status`, `tags`, `generated`, `verified`,
`stale_after`.

- `generated`: who or what wrote it, and when. Example:
  `generated: { by: agent:<session>, at: 2026-10-25T00:00:00Z }`.
- `verified`: the date and the verifier, when a human confirmed it.
- `stale_after`: an ISO 8601 date. A passed date produces a warning in
  `factory.py docs`, never a failure. Use it for knowledge that decays.

Research documents must carry `sources` with provenance the reader can
follow. A research document without sources is not research.

## log.md discipline

`docs/log.md` is newest-first. One entry per merged change, under a
`YYYY-MM-DD` date heading. Use the entry shape: **Creation**, **Change**,
or **Removal**, followed by a single sentence and the issue or pull
request number. Append the entry for your change; never rewrite old
entries.

## Rules

- Run `uv run .factory/factory.py docs` after every write. It must pass.
- Never put specs or tickets in the bundle. They live on the issue
  tracker.
- Never restate a decision in a second document. Link to it.
- Keep `architectural-overview.md` current when module boundaries,
  dependencies, data flows, or public interfaces change.
