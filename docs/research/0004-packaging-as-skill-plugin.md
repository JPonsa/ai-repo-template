---
type: research
title: Package the template as a skill or plugin with a setup wizard
description: Distribution options, wizard configuration inventory, update propagation, and recommendation against the "copied, not installed" rule.
status: stable
tags: [research, packaging, wizard, distribution]
generated: { by: agent:opencode, at: 2026-10-27T00:00:00Z }
stale_after: 2027-01-27T00:00:00Z
sources: ["https://opencode.ai/docs/skills/", "https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review"]
---

## Summary

Issue #21 asks whether the factory can be packaged as a skill/plugin with a setup wizard (files living as references inside it, instantiated by a wizard) to remove the copy step, make it installable/updatable/configurable. Or whether it breaks the "copied, not installed" design rule. We need to compare distribution shapes, look at Matt Pocock's examples, inventory wizard configuration, understand update propagation, and make a recommendation.

## Provenance
| Item | Value |
| --- | --- |
| OpenCode Skills docs | https://opencode.ai/docs/skills/ (fetched 2026-10-27) |
| Issue #21 | "Research: package the template as a skill or plugin with a setup wizard" |
| Issue #19 findings | docs/research/0001-mattpocock-software-factory.md (merged) |
| Issue #25 findings | docs/research/0002-protected-main.md (merged) |
| Current design | AGENTS.md, TEMPLATE.md, INTENT.md, .claude/skills/setup-project/SKILL.md |
| Upstream patterns | setup-matt-pocock-skills (referenced), skills from mattpocock/skills |

## Current state (facts)
- The template is copied (not installed): "No hidden runtime dependency: the template is copied, not installed." (from TEMPLATE.md, described in the "Why the shape is like this" section). 
- Distribution is: Git repo copied/templated (GitHub template repo), then user runs `setup-project` skill in the copy. `setup-project` rewrites files (README, INTENT, CONTEXT, GLOSSARY, CODING_STANDARDS, CONTRIBUTING, factory.toml, docs/log.md, docs/architectural-overview.md), creates a first test, creates labels via `gh`, reserves upstream delegation outputs, deletes TEMPLATE.md, delegates to `setup-matt-pocock-skills` (global skill installed separately). 
- Local skills live in `.claude/skills/` and are read by both Claude Code and OpenCode (compatibility path). Slash commands exist only for the five local skills (.opencode/commands/). 
- Global skills installed separately (`mattpocock/skills`) - "shipped no third-party skills". Prerequisite recorded in factory.toml. 
- OpenCode skills: discovered from project/global paths (.opencode/skills, .claude/skills, .agents/skills), loaded on-demand via skill tool. Frontmatter with name/description required, name must match directory and follow naming rules. 
- Claude Code plugins/skills - different mechanisms. The template supports both harnesses.

## Distribution shapes

| Shape | Installability | Updatability | Harness Support | Blast Radius | Notes |
| --- | --- | --- | --- | --- | --- |
| **GitHub template repository (current)** | User clicks "Use this template" or clones. No runtime install needed. | Updates don't propagate to derived repos automatically - user must cherry-pick/merge from upstream. | Works for any harness that can run in repo. | Low - each repo is independent copy. No hidden deps. | Current model. Aligns with "copied, not installed". |
| **OpenCode skill/plugin** | Install via skills CLI or copy to skill dirs. Could bundle the whole factory as a skill that scaffolds a new project. | Updates to the skill propagate when reinstalled/updated. But would affect how scaffolding works. | OpenCode-native; also compatible via .claude/skills paths. | Medium - if installed globally, behavior changes affect all uses. But scaffolding is usually one-time. | Skills are loaded on-demand; a "scaffold" skill could create files. But the factory has enforcement (factory.py, CI) that needs to live IN the repo. |
| **Claude Code plugin** | Install via `claude plugin install`. Can bundle skills, commands, hooks, MCPs. | Plugin updates propagate on update. | Claude Code specific primarily. | Similar to skill - global install. | More powerful (hooks) but harness-specific. |
| **npm-style installer (npx/create-*)** | `npx create-ai-factory` or similar. Downloads template and runs setup. | npm package updates; can fetch latest template. | Harness-agnostic at install time. | Low runtime blast radius if it just scaffolds. | Common pattern. Still results in copied files. |
| **Hybrid (template repo + wizard skill)** | Keep template repo, wizard skill (local or global) guides instantiation. | Wizard can be updated globally; template updates still manual. | Works across harnesses. | Low. | Enhances current flow without changing core model. |

## Matt Pocock's examples (from #19 research)
From docs/research/0001-mattpocock-software-factory.md:
- `mattpocock/skills` provides global skills (setup-matt-pocock-skills for issue tracker/labels). The template delegates to it.
- The "software-factory-skill" branch exists but is beta in skills/in-progress (excluded from plugin). Not to add as prerequisite yet.
- The approach uses global skills + project-local setup. 

The pattern is: global skills provide reusable workflows, project gets instantiated via a setup skill that asks questions and delegates to upstream skills.

## Wizard configuration inventory
Based on current `setup-project` and TEMPLATE.md, what needs configuration:

| Option | Default | Factory.toml target | Notes |
| --- | --- | --- | --- |
| Project name | (ask) | identity.name / used in files | Required |
| Purpose/consumers/success/out of scope | (ask) | INTENT.md | Required |
| Domain terms/bounded context | (ask) | CONTEXT.md, GLOSSARY.md | Required |
| Tech stack | (ask) | Used in CODING_STANDARDS, CONTRIBUTING | Required |
| Check command | (ask) | factory.toml [commands].check (array) | Required - must be real and verifiable |
| Issue tracker labels | (ask) | factory.toml [labels] (triage + factory labels) | Required |
| Document types | (ask) | factory.toml [docs].types | Required |
| Risk ceilings | (keep defaults or ask?) | factory.toml [risk].max_files, max_added_lines | Defaults exist (20, 600). Maybe advanced option? |
| Protected paths | (keep defaults?) | factory.toml [risk].protected_paths | Defaults include factory.toml, docs/index.md, AGENTS.md, CONTRIBUTING.md, scripts/factory.py etc. Template-specific; usually keep. |
| Harness adapters | (auto-detect?) | .claude/skills/*, .opencode/commands/* | Already in template; setup doesn't change much. |
| First test location | (infer from stack) | New test file | setup-project creates placeholder test |
| Reserved doc paths | (auto-add from delegation) | factory.toml [docs].reserved | Added after delegating to setup-matt-pocock-skills |

Most of this is already in setup-project. A "wizard" could be the same thing, maybe more interactive/form-driven.

## Update propagation
- **Current (copied):** No automatic propagation. Derived projects can pull upstream changes via git remote and merge - but conflicts likely. The knowledge bundle format (OKF) and contracts help, but it's manual.
- **If installed as global skill/plugin:** The scaffolding logic updates, but already-scaffolded projects are unaffected. That’s good for the tool, bad for getting updates to enforcement/check logic into existing projects.
- **If using npm installer:** Can pin template version, but still copied once.
- **Key insight:** The enforcement (scripts/factory.py, CI workflow, risk gate logic) MUST live in the repo to work without network/external deps. Contracts (AGENTS.md, INTENT.md etc.) must live in repo. So "updates" to enforcement require changes in each repo - you can't update enforcement by updating a global skill. Only scaffolding/setup logic can be updated globally.

This reinforces the "copied, not installed" rule - it's not just about convenience, it's about the enforcement model.

## The trade-off
From TEMPLATE.md line 10: "It ships no third-party skills: those are installed once, globally, and recorded as prerequisites."  
From AGENTS.md: "Local skills live in `.claude/skills/`. OpenCode and Claude Code both read that path. Upstream `mattpocock/skills` are installed globally; the tested pin is in `factory.toml`. A missing skill is an install error. Stop and ask the user to install it. Never reimplement a missing skill inline, and never vendor a copy."

So "copied, not installed" means:
1. The factory's OWN code/logic (factory.py, local skills, adapters) lives IN the repo (copied) - no runtime dependency on fetching them
2. THIRD-PARTY skills (mattpocock/skills) are installed globally (installed) - they're a prerequisite, not bundled
3. Updates to third-party skills are managed separately (pinned in factory.toml)

Packaging the TEMPLATE ITSELF as a skill/plugin would blur this line. If the wizard that creates the factory is installed globally, that's fine as long as what it CREATES is a full copy with all enforcement code. The question is whether the act of "packaging" changes the model.

Also OpenCode's skill model - skills contain instructions; they can instruct the agent to create files. So a global skill could say "scaffold this factory structure". That would still result in copied files in the target repo. That might actually HONOUR the rule better (separates scaffolding logic from the template content).

But we need to be careful not to make the factory itself require a global skill to function after setup.

## Recommendation (preliminary)
The cleanest approach that honours "copied, not installed":
1. **Keep GitHub template repo as the primary distribution** - it's simple, discoverable, works everywhere.
2. **Make the setup wizard a global skill OR a local skill** - `setup-project` already exists as local skill in the template. It could also be published as a global skill for convenience, but the template must not REQUIRE it to be global.
3. **Consider an npm create-package** as a thin wrapper around template cloning + running setup - also fine as long as output is a full copy.
4. **Do NOT bundle factory.py/enforcement into a global plugin that the repo depends on at runtime** - that would violate the rule.
5. **The "packaging as skill/plugin" idea is good for the WIZARD/scaffolding, not for packaging the factory's runtime components.**

The issue says "package the template as a skill or plugin with a setup wizard" - so packaging the TEMPLATE (the whole thing) as installable. That could mean the template files live inside a skill package and get copied out by the wizard. Similar to how some project generators work.

But we need to be precise about what "template" means here. Looking up issue again: "The factory is a repository you copy. Setup assumes the user runs `setup-project` from inside a clone. Packaging the whole factory as a skill or plugin — files living as references inside it, instantiated by a wizard — may remove the copy step and make the factory installable, updatable, and configurable. Or it may break the \"copied, not installed\" design rule."

So the TEMPLATE FILES would live as references inside a skill/plugin package; the wizard instantiates them into a new repo. That means after instantiation, the repo has its own copies of factory.py etc. - so runtime is still copied. The packaging is just distribution mechanism. That could work if done right.

## Detailed analysis

### OpenCode plugin/skill capabilities
From OpenCode docs: skills are directories with SKILL.md (frontmatter + instructions), discovered from multiple paths, loaded on-demand. They can instruct agents to do things - including creating files, running commands. A skill could contain all the template files as embedded content or reference them. But skills are loaded into the agent context, not "installed" as runtime deps in the target project.

Plugins in OpenCode (different from skills) can extend functionality - add tools, modify behavior. The issue says "skill or plugin" - both options.

### Comparison matrix with concrete details

| Criterion | Template repo (current) | Global skill with wizard | OpenCode plugin | npm create-package | Claude Code plugin |
| --- | --- | --- | --- | --- | --- |
| Remove copy step? | No - you copy/clone | Yes - wizard creates files in new dir | Yes - plugin could scaffold | Yes - downloads and scaffolds | Yes - plugin could scaffold |
| Installability | Easy (GitHub template) | Need to install skill globally | Need to install plugin | `npx` works if published | Need to install plugin |
| Updatability of wizard/scaffolder | N/A | Update skill globally | Update plugin | Update npm package | Update plugin |
| Updatability of enforcement in existing repos | Manual git merge | Not possible - enforcement is copied | Not possible | Not possible | Not possible |
| Works offline after scaffold | Yes | Yes (files copied) | Yes | Yes | Yes |
| Harness support | All | OpenCode/Claude Code compatible if in right paths | Primarily OpenCode | All | Claude Code primarily |
| Discoverability | High (GitHub) | Lower unless published | Lower | Medium (npm search) | Lower |
| Respects "copied, not installed" | Yes perfectly | Yes IF wizard copies all files; No IF it makes repo depend on global skill | Yes IF copies; No IF depends on plugin at runtime | Yes if copies | Yes if copies |
| Can configure via wizard | Via running setup-project skill after copy | Wizard can ask questions interactively | Possible | Possible (prompts) | Possible |
| Complexity | Low | Medium | Medium-High | Medium | Medium-High |

### What stays fixed vs configurable
From the inventory above, most things are configurable via setup-project already. A wizard could make this smoother (GUI-like prompts, validation). But the core questions are the same.

### Update propagation reality
This is critical. The factory's value is in enforcement: the risk gate, check orchestration, docs validation, review order, CI workflow. ALL of these must live in the repo. You cannot make a repo depend on a global skill to run `uv run scripts/factory.py check` - that would break if the skill is removed/moved and violates "copied, not installed". 

So even if packaged as a skill/plugin, after instantiation the repo must be fully self-contained. The packaging only affects HOW you create the repo, not how it operates. That means "updatability" benefit is limited to the scaffolding process itself. Existing repos won't auto-update enforcement.

That actually means the current model is correct for enforcement. Packaging as skill/plugin is mainly a UX/distribution improvement for new projects.

### Recommendation
**Recommend a hybrid approach that preserves "copied, not installed":**

1. **Primary: Keep GitHub template repository** - this is the clearest model, works everywhere, no special installation needed. Add support for "Use this template" workflow.

2. **Add a global wizard skill (optional enhancement)** - Create a skill like `scaffold-factory` that can be installed globally and creates a new factory repo in a target directory by copying template files. This removes the "clone then run setup" friction - user installs skill once, runs it anywhere to create a configured project. But the skill must COPY files (not reference them at runtime). The resulting repo is fully self-contained.

3. **Keep local setup-project as fallback** - Template still ships with .claude/skills/setup-project for in-repo configuration. This ensures the template works even if global wizard isn't installed.

4. **Do NOT make the repo depend on global skills at runtime** - factory.py must not import/call global skills. Local skills in .claude/skills are fine because they're copied into the repo. Third-party skills (mattpocock/skills) are only needed for specific delegated workflows (setup-matt-pocock-skills) - and that's already documented as prerequisite.

5. **npm create-package as alternative** - Also viable, language-agnostic. Could be `npx @jponta/create-ai-factory` or similar. But requires publishing to npm.

**Key constraint:** "packaging the whole factory as a skill or plugin" - if the plugin/skill CONTAINS all the files and the wizard COPIES them out to create a new project, that's fine. The instantiated project has copies. The skill/plugin is just a delivery mechanism, not a runtime dependency. That HONOURS the rule.

**What would VIOLATE the rule:** Making factory.py do `skill({name: "some-global-factory-skill"})` or having the repo load code from a global plugin at runtime. We must not do that.

### Wizard configuration inventory (detailed)
Mapping every configurable option:

From factory.toml structure:
```toml
[project] # name - set by setup
[commands] check = [...] # must be configured
[labels] triage = [...], factory = [...] # configured
[risk] max_files, max_added_lines, protected_paths, size_ceiling_message # defaults usually fine
[docs] types = [...], reserved = [...] # configured, reserved grows with delegation
[prerequisites] skills = [...] # upstream skills, pinned - usually don't change
```

From setup-project questions:
1. Project name, purpose, consumers → INTENT.md, README.md
2. Domain terms, system boundary → CONTEXT.md, GLOSSARY.md  
3. Tech stack, real check command → CODING_STANDARDS.md, CONTRIBUTING.md, factory.toml [commands]
4. Issue tracker labels → factory.toml [labels]
5. Document types needed → factory.toml [docs].types

Plus automatic steps:
- Create first placeholder test (stack-dependent)
- Create labels on tracker via gh
- Reserve paths from setup-matt-pocock-skills delegation → factory.toml [docs].reserved
- Delete TEMPLATE.md

A wizard should ask these questions, validate the check command works, scaffold the test, create labels, etc. Same flow as setup-project but potentially more polished.

### Implementation notes for a global skill approach
If we create a global skill like `scaffold-ai-factory`:
- It would need access to template files. Options:
  a) Embed all template files as base64/text in the skill (large, but doable)
  b) Download from a repo (e.g., GitHub raw) - adds network dependency at scaffold time (acceptable, one-time)
  c) Clone the template repo - also needs network/git
- The skill would run in the agent context, ask questions, create directory structure, write files
- Result is a fully copied project - no runtime dependency

Option (b) or (c) with a pinned version/tag would be good for updatability of the scaffolder.

## Open questions for grilling
1. Should we publish as GitHub template repo AND also offer as global skill/npx? Or pick one primary?
2. For the global skill approach, where do template files come from (embedded vs downloaded)? Downloaded allows updating scaffolder to use newer template version.
3. Should setup-project remain as a local skill in the template, or be removed if using global wizard?
4. How to handle the "tested pin" of mattpocock/skills - does the wizard install it or just instruct?
5. Should factory.toml.prerequisites be validated differently if using skill packaging?
6. Does packaging change anything about the CI/risk gate model? (Probably not if files are copied)
7. What about the OpenCode command files (.opencode/commands/) - they reference local skills by name; if packaged differently, do they still work?

## Sources
- OpenCode Skills docs: https://opencode.ai/docs/skills/
- Issue #21, #19, #25
- AGENTS.md, TEMPLATE.md, INTENT.md, .claude/skills/setup-project/SKILL.md
- factory.toml
