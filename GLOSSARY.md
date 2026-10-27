# Glossary

<!--
Shared vocabulary for this project. Skills read this file to ensure consistent
terminology in test names, issue titles, refactor proposals, and documentation.

Format each entry as:
  **Term** — _definition._
  - Avoid: synonym1, synonym2.

Rules:
- Only add terms that have project-specific meanings, or that the team uses
  inconsistently.
- Domain model terms (entities, events, aggregates) belong in CONTEXT.md.
  Keep only workflow and operational terms here, unless CONTEXT.md is absent.
- Do not define terms that carry their plain English meaning without
  project-specific nuance.
- Update via the /domain-modeling skill, not by editing directly.
-->

## Domain terms

> <!--
> Terms from the problem domain: entities, events, and core concepts.
> Mirror the Ubiquitous language table in CONTEXT.md.
> If CONTEXT.md covers domain terms fully, keep this section empty or remove it.
> -->

**[Term]** — _[definition]._
- Avoid: [synonym1], [synonym2].

## Workflow terms

> <!--
> Terms used in the development workflow: issue states, PR conventions,
> environment names, deployment stages, and similar operational vocabulary.
> The factory terms below are the baseline every derived project keeps;
> add project terms after them.
> -->

**Check** — _`uv run .factory/factory.py check`: the one entry point that runs the automated checks. Upstream vocabulary: an **automated check**, one of the three brakes._
- Avoid: build, test run, CI run.

**Review order** — _`code-review`, `security-review`, `verify`, `finding-verifier`, each in a fresh context. Upstream vocabulary: **automated review**, the second brake._
- Avoid: code review pass, review round (a round-trip is a metric).

**Risk gate** — _`factory.py risk`: protected paths, size ceiling, and the evidence block decide whether a human approves the merge. Upstream vocabulary: **human review**, the third brake. Unlike upstream's autonomous runs, a merge in this factory always waits for a human when the gate is red._
- Avoid: approval gate, merge check.

**Evidence block** — _the `factory:evidence` comment in a pull request: commit, check, result, risk. Its commit must equal `HEAD`._
- Avoid: PR checklist.

**Agent lane** — _a low-risk pull request that an agent merges on its own authority: no protected path, below the ceiling, evidence that matches `HEAD`, no surviving blocker._
- Avoid: auto-merge.

**Owner merge** — _the owner's merge of a high-risk pull request; it is the human approval (decision 0002)._
- Avoid: override, force-merge.

**Ticket tracker** — _GitHub Issues: where specs and tickets live and where the human interface is. Upstream term, adopted as-is._
- Avoid: task board.

**Ticket source** — _anything that files a ticket: the issue templates, a bug report, a monitor, a feedback button. Upstream term, adopted as-is._
- Avoid: issue funnel.

**Ratchet** — _an exception list under a stricter check; one file leaves the list per day, fixed in one small pull request (upstream pattern; see `docs/research/0001`)._
- Avoid: migration, cleanup sprint.

Terms not adopted from upstream: **Run**, **Runner**, **Orchestrator** name objects of an autonomous remote factory; this factory is local and human-gated. **Run** also carries the rule "a run never waits for a human", which contradicts the risk gate.
