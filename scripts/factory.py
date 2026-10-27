#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""The software factory: one entry point for checking and auditing this repository.

Commands:
    check   Run the configured checks and report the result.
    docs    Validate the OKF bundle under docs/.
    risk    Classify a diff as low risk or high risk.
    audit   Report drift across the harness.

Run with ``uv run scripts/factory.py <command>``.

The script uses the standard library only. ``tomllib`` supplies the
configuration, so Python 3.11 or later is required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "factory.toml"

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)")


class FactoryError(Exception):
    """A failure that the operator can act on."""


# --------------------------------------------------------------------------
# Configuration and git
# --------------------------------------------------------------------------


def load_config() -> dict:
    """Read factory.toml from the repository root."""
    if not CONFIG_PATH.is_file():
        raise FactoryError("factory.toml is missing")
    try:
        with CONFIG_PATH.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise FactoryError(f"factory.toml: {exc}") from exc


def git(*args: str, check: bool = True) -> str:
    """Run a git command in the repository root and return its output."""
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise FactoryError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def resolve_base(requested: str | None) -> str | None:
    """Return the first git ref that exists, or None."""
    if requested:
        candidates = (requested, f"origin/{requested}")
    else:
        candidates = ("origin/main", "main", "HEAD~1")
    for candidate in candidates:
        if git("rev-parse", "--verify", "--quiet", candidate, check=False):
            return candidate
    return None


def changed_paths(base: str | None) -> list[str]:
    """Return committed, staged, unstaged, and untracked paths that differ."""
    paths: set[str] = set()
    if base:
        merge_base = git("merge-base", base, "HEAD", check=False)
        if merge_base:
            paths.update(git("diff", "--name-only", f"{merge_base}..HEAD", check=False).splitlines())
    paths.update(git("diff", "--name-only", "HEAD", check=False).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard", check=False).splitlines())
    return sorted(path for path in paths if path)


def matches(path: str, patterns: list[str]) -> bool:
    """Match a repository path against glob patterns.

    Patterns match the whole path. An asterisk also matches a directory
    separator, so ``docs/**`` and ``*.md`` both cover nested files.
    """
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------


def detect_stack_commands() -> list[str]:
    """Guess the project's own test command from its markers.

    Used only when ``factory.toml`` configures no commands. The detected
    command is a starting point, not a contract: ``setup-project`` writes
    the real command into ``factory.toml``.
    """
    commands: list[str] = []
    if (ROOT / "pyproject.toml").is_file() or (ROOT / "uv.lock").is_file():
        commands.append("uv run pytest")
    elif any(ROOT.glob("requirements*.txt")):
        commands.append("python -m pytest")
    package = ROOT / "package.json"
    if package.is_file():
        try:
            import json

            scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
            if "test" in scripts:
                commands.append("npm test")
        except (OSError, ValueError):
            pass
    if (ROOT / "go.mod").is_file():
        commands.append("go test ./...")
    if (ROOT / "Cargo.toml").is_file():
        commands.append("cargo test")
    return commands


def cmd_check(args: argparse.Namespace) -> int:
    """Run every configured check and fail closed when nothing runs."""
    settings = load_config().get("check", {})
    configured_base = args.base or settings.get("base")
    base = resolve_base(configured_base)
    changed = changed_paths(base)
    source_patterns = settings.get("source_paths", [])
    ignored_patterns = settings.get("ignored_paths", [])
    source_changed = [
        path
        for path in changed
        if matches(path, source_patterns) and not matches(path, ignored_patterns)
    ]
    commands = settings.get("commands", [])
    if not commands:
        commands = detect_stack_commands()
        if commands:
            print("note:  no commands configured; detected the project stack")

    print(f"commit: {git('rev-parse', 'HEAD')}")
    if base:
        print(f"base:   {git('rev-parse', '--short', base)} ({configured_base or 'default'})")
    print(f"change: {len(changed)} file(s), {len(source_changed)} source file(s)")

    if source_changed and not commands:
        print(
            "fail: source changed but no check command is configured or detected",
            file=sys.stderr,
        )
        return 1

    if not commands:
        print("pass: no check commands configured; no source change")
        return 0

    for command in commands:
        print(f"run:    {command}")
        result = subprocess.run(command, cwd=ROOT, shell=True, check=False)
        if result.returncode != 0:
            print(
                f"fail: {command} exited with status {result.returncode}",
                file=sys.stderr,
            )
            return result.returncode or 1

    print("pass: every check succeeded")
    return 0


# --------------------------------------------------------------------------
# docs
# --------------------------------------------------------------------------


def unquote_scalar(value: str) -> str:
    """Remove one pair of matching quotes from a frontmatter value."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, object] | None:
    """Parse the frontmatter subset that this repository writes.

    Supported: ``key: value`` scalars and ``key:`` lists of ``- item``
    lines. Nested mappings stay strings. This is not a general YAML parser,
    and it is documented as such.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in match.group(1).splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list is not None:
                items = data[current_list]
                if isinstance(items, list):
                    items.append(unquote_scalar(stripped[2:]))
            continue
        key, separator, value = stripped.partition(":")
        if not separator or not key.strip():
            continue
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = unquote_scalar(value)
            current_list = None
        else:
            data[key] = []
            current_list = key
    return data


def resolve_link(source: Path, target: str, bundle: Path) -> Path:
    """Resolve a markdown link target to a path on disk."""
    target = target.split("#", 1)[0]
    if target.startswith("/"):
        return (bundle / target.lstrip("/")).resolve()
    return (source.parent / target).resolve()


def docs_findings() -> tuple[list[str], list[str], int]:
    """Validate the OKF bundle. Return errors, warnings, concept count."""
    settings = load_config().get("docs", {})
    bundle = ROOT / settings.get("bundle", "docs")
    version = settings.get("okf_version", "0.2")
    allowed_types = list(settings.get("types", []))
    reserved = set(settings.get("reserved", ["index.md", "log.md"]))
    required = list(settings.get("required_fields", ["type"]))

    if not bundle.is_dir():
        raise FactoryError(f"{bundle.relative_to(ROOT).as_posix()} is missing")

    errors: list[str] = []
    warnings: list[str] = []
    concepts = 0

    index = bundle / "index.md"
    if not index.is_file():
        errors.append("docs/index.md: missing")
    else:
        frontmatter = parse_frontmatter(index.read_text(encoding="utf-8"))
        declared = frontmatter.get("okf_version") if frontmatter else None
        if declared != version:
            errors.append(
                f'docs/index.md: expected okf_version "{version}", found {declared!r}'
            )

    for path in sorted(bundle.rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        # Reserved entries match either a bare file name anywhere in the
        # bundle or a path relative to the bundle root, so generated
        # subdirectories such as docs/agents/ can be reserved as a whole.
        bundle_relative = path.relative_to(bundle).as_posix()
        is_reserved = path.name in reserved or bundle_relative in reserved

        if not is_reserved:
            concepts += 1
            frontmatter = parse_frontmatter(text)
            if frontmatter is None:
                errors.append(f"{relative}: missing frontmatter block")
            else:
                for field in required:
                    if not frontmatter.get(field):
                        errors.append(f"{relative}: missing required field '{field}'")
                concept_type = frontmatter.get("type")
                if concept_type and allowed_types and concept_type not in allowed_types:
                    errors.append(
                        f"{relative}: type '{concept_type}' is not one of "
                        + ", ".join(allowed_types)
                    )

                stale_after = frontmatter.get("stale_after")
                if isinstance(stale_after, str):
                    try:
                        deadline = dt.datetime.fromisoformat(stale_after)
                    except ValueError:
                        errors.append(f"{relative}: stale_after is not ISO 8601")
                    else:
                        if deadline.tzinfo is None:
                            deadline = deadline.replace(tzinfo=dt.timezone.utc)
                        if dt.datetime.now(dt.timezone.utc) >= deadline:
                            warnings.append(f"{relative}: stale since {stale_after}")

        if is_reserved and path.name == "index.md" and path != index:
            if parse_frontmatter(text) is not None:
                errors.append(f"{relative}: only the bundle-root index may carry frontmatter")

        in_fence = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                    continue
                if not target:
                    continue
                resolved = resolve_link(path, target, bundle)
                if not resolved.exists():
                    errors.append(f"{relative}:{line_number}: broken link '{target}'")

    return errors, warnings, concepts


def cmd_docs(args: argparse.Namespace) -> int:
    """Validate the OKF bundle and report every problem it finds."""
    errors, warnings, concepts = docs_findings()
    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"fail: {error}", file=sys.stderr)

    print(f"docs: {concepts} concept(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


# --------------------------------------------------------------------------
# risk and audit
# --------------------------------------------------------------------------


EVIDENCE_BLOCK_RE = re.compile(
    r"<!--\s*factory:evidence\s*\n(.*?)-->", re.S
)


def parse_evidence_block(text: str) -> dict[str, str] | None:
    """Parse the ``factory:evidence`` comment from a pull-request body."""
    match = EVIDENCE_BLOCK_RE.search(text)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields


def gh_json(fields: str, *args: str) -> dict | None:
    """Run a read-only gh command and return its JSON, or None."""
    result = subprocess.run(
        ["gh", *args, "--json", fields],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        import json

        return json.loads(result.stdout)
    except ValueError:
        return None


def cmd_risk(args: argparse.Namespace) -> int:
    """Classify the diff as low risk or high risk. Fail on high risk."""
    config = load_config()
    risk = config.get("risk", {})
    labels_cfg = config.get("labels", {})
    protected = list(risk.get("protected_paths", []))
    max_files = int(risk.get("max_files", 20))
    max_added_lines = int(risk.get("max_added_lines", 600))
    risk_high_label = labels_cfg.get("risk_high", "risk:high")

    base = resolve_base(args.base or config.get("check", {}).get("base"))
    merge_base = None
    if base:
        merge_base = git("merge-base", base, "HEAD", check=False)
    if not merge_base:
        print("fail: risk: no base ref to compare against", file=sys.stderr)
        return 1

    # Committed diff against the merge base.
    changed = [
        path
        for path in git(
            "diff", "--name-only", f"{merge_base}..HEAD", check=False
        ).splitlines()
        if path
    ]
    numstat = git("diff", "--numstat", f"{merge_base}..HEAD", check=False)
    added = 0
    for line in numstat.splitlines():
        first = line.split()[0] if line.split() else ""
        if first.isdigit():
            added += int(first)

    print(f"commit: {git('rev-parse', 'HEAD')}")
    print(f"change: {len(changed)} file(s), {added} added line(s)")

    failures: list[str] = []
    high_reasons: list[str] = []

    # Rule 1: protected paths.
    touched_protected = [path for path in changed if matches(path, protected)]
    if touched_protected:
        for path in touched_protected:
            print(f"risk:  protected path changed: {path}")
        high_reasons.append("protected paths")

    # Rule 2: size ceiling.
    if len(changed) > max_files or added > max_added_lines:
        print(
            f"risk:  diff exceeds the ceiling: {len(changed)} file(s) > {max_files}, "
            f"{added} added line(s) > {max_added_lines}"
        )
        high_reasons.append("diff size")

    # Rule 3: evidence block, from the pull request for this branch.
    # FACTORY_PR names the pull request explicitly, for CI checkouts
    # that carry no branch context.
    pr_number = os.environ.get("FACTORY_PR")
    pr = (
        gh_json("body,labels,reviews,author", "pr", "view", pr_number)
        if pr_number
        else gh_json("body,labels,reviews,author", "pr", "view")
    )
    head = git("rev-parse", "HEAD")
    evidence = parse_evidence_block(pr.get("body", "")) if pr else None
    if not pr:
        failures.append("no pull request found for this branch; the gate cannot read the evidence")
    elif not evidence:
        failures.append("pull request has no factory:evidence block")
    else:
        evidence_commit = evidence.get("commit", "")
        if evidence_commit != head:
            failures.append(
                f"evidence commit {evidence_commit[:12] or '(missing)'} does not equal HEAD {head[:12]}"
            )
        else:
            print("risk:  evidence block matches HEAD")

    # Rule 4: the risk:high label and human approval.
    # A bot approval is not a human approval: Copilot can submit
    # APPROVED reviews when "Copilot approvals" are enabled (public
    # preview). Decision 0002 keeps the human gate human, so bot
    # authors (login ending in "[bot]") never count here.
    label_present = False
    approved_by: list[str] = []
    if pr:
        pr_labels = [label.get("name", "") for label in pr.get("labels", [])]
        label_present = risk_high_label in pr_labels
        pr_author = (pr.get("author") or {}).get("login", "")
        approved_by = [
            reviewer
            for review in pr.get("reviews", [])
            if review.get("state") == "APPROVED"
            and (reviewer := (review.get("author") or {}).get("login", ""))
            and reviewer != pr_author
            and not reviewer.endswith("[bot]")
        ]

    if label_present and not approved_by:
        failures.append(f"labelled {risk_high_label} without human approval")

    # Verdict. A structurally high-risk diff passes only when it is
    # labelled risk:high and a human has approved it. Evidence problems
    # and an unapproved risk:high label are never excused.
    if failures:
        for failure in failures:
            print(f"fail: risk: {failure}", file=sys.stderr)
    if high_reasons:
        if label_present and approved_by:
            print(
                f"result: risk is high ({'; '.join(high_reasons)}), "
                f"approved by {', '.join(approved_by)}"
            )
            return 0
        for reason in high_reasons:
            print(
                f"fail: risk: high risk ({reason}); label '{risk_high_label}' "
                "and obtain human approval to merge",
                file=sys.stderr,
            )
        return 1
    if failures:
        return 1
    print("result: risk is low")
    return 0


def _skill_search_paths() -> list[Path]:
    """Return candidate global skill directories for different harnesses.

    Extra machine-specific directories come from the
    ``FACTORY_SKILL_PATHS`` environment variable, colon-separated.
    Use it when the global skill directory lives outside ``$HOME``,
    for example under a Windows profile mounted in WSL.
    """
    home = Path.home()
    paths = [
        home / ".claude" / "skills",
        home / ".config" / "opencode" / "skills",
        home / ".local" / "share" / "opencode" / "skills",
        home / ".agents" / "skills",
        home / ".claude" / "plugins",
        home / ".config" / "claude" / "plugins",
    ]
    extra = os.environ.get("FACTORY_SKILL_PATHS", "")
    paths.extend(Path(part) for part in extra.split(":") if part)
    return paths


def _find_skill(skill_id: str, paths: list[Path]) -> bool:
    """Return True if a skill appears to exist in any search path."""
    for base in paths:
        if not base.exists():
            continue
        # Direct directory match
        if (base / skill_id).exists():
            return True
        # Look for skill files
        for child in base.iterdir():
            if child.is_dir() and child.name == skill_id:
                return True
            # Some installations nest by plugin name
            if child.is_dir():
                candidate = child / skill_id
                if candidate.exists():
                    return True
        # Recursive search (shallow)
        try:
            for p in base.rglob(skill_id):
                if p.is_dir():
                    return True
        except Exception:
            continue
    return False


def _prose_lines(path: Path) -> set[str]:
    """Return normalized non-trivial prose lines, excluding code fences."""
    lines: set[str] = set()
    in_fence = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = raw.strip()
        if len(stripped) < 40 or stripped.startswith(("#", "|", "-", "*", ">")):
            continue
        lines.add(" ".join(stripped.split()))
    return lines


def _duplicated_instructions() -> list[str]:
    """Report identical instruction lines shared by the contract files."""
    files = ["AGENTS.md", "CONTRIBUTING.md", "CODING_STANDARDS.md"]
    corpora: dict[str, set[str]] = {}
    for name in files:
        path = ROOT / name
        if path.is_file():
            corpora[name] = _prose_lines(path)
    findings: list[str] = []
    names = list(corpora)
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            shared = corpora[left] & corpora[right]
            for line in sorted(shared):
                findings.append(
                    f"instruction duplicated in {left} and {right}: \"{line}\""
                )
    return findings


def _normalize_permission(value: str) -> str:
    """Normalize a permission pattern for drift comparison."""
    value = value.lower().replace(" ", "")
    return value.strip("*")


TOOL_MAP = {"shell": "bash", "read": "read", "edit": "edit"}


def _opencode_rules() -> list[tuple[str, str, str]]:
    """Read permission rules from .opencode/opencode.jsonc."""
    path = ROOT / ".opencode" / "opencode.jsonc"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    # Strip // comments so the JSONC parses as JSON.
    cleaned = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    import json

    try:
        data = json.loads(cleaned)
    except ValueError:
        return []
    rules: list[tuple[str, str, str]] = []
    for rule in data.get("permissions", []):
        action, resource, effect = rule.get("action", ""), rule.get("resource", ""), rule.get("effect", "")
        if action in TOOL_MAP and resource != "*":
            rules.append((TOOL_MAP[action], _normalize_permission(resource), effect))
    return rules


def _claude_rules() -> dict[str, list[tuple[str, str]]]:
    """Read permission rules from .claude/settings.json."""
    path = ROOT / ".claude" / "settings.json"
    if not path.is_file():
        return {}
    import json

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return {}
    rules: dict[str, list[tuple[str, str]]] = {}
    permissions = data.get("permissions", {})
    for effect, patterns in permissions.items():
        if not isinstance(patterns, list):
            continue
        for pattern in patterns:
            match = re.match(r"([A-Za-z]+)\((.*)\)$", pattern)
            if not match:
                continue
            tool, resource = match.group(1).lower(), match.group(2)
            rules.setdefault(tool, []).append(
                (resource.lower().replace(" ", "").strip("*"), effect)
            )
    return rules


def _permission_drift() -> list[str]:
    """Report permission rules present in one harness but not the other."""
    findings: list[str] = []
    opencode = _opencode_rules()
    claude = _claude_rules()
    claude_flat = [(tool, res, eff) for tool, pairs in claude.items() for res, eff in pairs]

    def has_counterpart(rule: tuple[str, str, str], pool: list[tuple[str, str, str]]) -> bool:
        tool, resource, _ = rule
        return any(
            other_tool == tool
            and (other_res.startswith(resource) or resource.startswith(other_res))
            for other_tool, other_res, _ in pool
        )

    for tool, resource, effect in opencode:
        if not has_counterpart((tool, resource, effect), claude_flat):
            findings.append(
                f"permission drift: opencode rule {tool} '{resource}' ({effect}) "
                "has no counterpart in .claude/settings.json"
            )
    for tool, resource, effect in claude_flat:
        if not has_counterpart((tool, resource, effect), opencode):
            findings.append(
                f"permission drift: claude rule {tool} '{resource}' ({effect}) "
                "has no counterpart in .opencode/opencode.jsonc"
            )
    return findings


def _unreferenced_skills() -> list[str]:
    """Report local skills that no command file or contract document names."""
    config = load_config()
    local = list(config.get("skills", {}).get("local", []))
    if not local:
        return []
    corpus: list[str] = []
    commands_dir = ROOT / ".opencode" / "commands"
    if commands_dir.is_dir():
        corpus.extend(
            p.read_text(encoding="utf-8") for p in commands_dir.glob("*.md")
        )
    for name in ("AGENTS.md", "CONTRIBUTING.md", "README.md", "TEMPLATE.md"):
        path = ROOT / name
        if path.is_file():
            corpus.append(path.read_text(encoding="utf-8"))
    blob = "\n".join(corpus)
    return [
        skill
        for skill in local
        if skill not in blob
    ]


def cmd_audit(args: argparse.Namespace) -> int:
    """Report harness drift: prerequisites, docs, references, duplication, permissions."""
    config = load_config()
    prereqs = config.get("prerequisites", {})
    required = list(prereqs.get("required", []))
    optional = list(prereqs.get("optional", []))
    upstream = prereqs.get("upstream", "mattpocock/skills")

    print(f"upstream: {upstream}")

    findings: list[str] = []

    # 1. Prerequisite skills that are missing on this machine.
    paths = _skill_search_paths()
    for skill_id in required:
        if _find_skill(skill_id, paths):
            print(f"found (required): {skill_id}")
        else:
            print(f"missing (required): {skill_id}")
            findings.append(
                f"prerequisite skill missing: {skill_id} "
                "(install it globally; never reimplement it inline)"
            )
    for skill_id in optional:
        status = "found" if _find_skill(skill_id, paths) else "missing"
        print(f"{status} (optional): {skill_id}")

    # 2-4. Docs bundle: frontmatter, types, links, staleness.
    errors, warnings, concepts = docs_findings()
    print(f"docs: {concepts} concept(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    findings.extend(f"docs: {error}" for error in errors)
    findings.extend(f"docs: {warning}" for warning in warnings)

    # 5. Skills that nothing references.
    for skill in _unreferenced_skills():
        findings.append(f"skill '{skill}' is referenced by no command or document")

    # 6. Instructions duplicated between contract files.
    findings.extend(_duplicated_instructions())

    # 7. Permission drift between the harnesses.
    findings.extend(_permission_drift())

    for finding in findings:
        print(f"fail: audit: {finding}", file=sys.stderr)
    print(f"audit: {len(findings)} finding(s)")
    return 1 if findings else 0


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="factory",
        description=(
            "The software factory: one entry point for checking and auditing "
            "this repository."
        ),
        epilog=(
            "Examples:\n"
            "  uv run scripts/factory.py check\n"
            "  uv run scripts/factory.py check --base origin/main\n"
            "  uv run scripts/factory.py docs\n"
            "  uv run scripts/factory.py risk\n"
            "  uv run scripts/factory.py risk --base main\n"
            "  uv run scripts/factory.py audit\n"
            "\n"
            "Configuration is read from factory.toml. "
            "`check` fails closed when source changes but no checks are configured. "
            "`docs` validates the OKF bundle under docs/."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser(
        "check",
        help="run the configured checks",
        description=(
            "Run every command in [check].commands in order. If source files "
            "changed relative to the base ref and no commands are configured, "
            "this command fails closed."
        ),
        epilog=(
            "Notes:\n"
            "  - Base ref resolution: --base, then [check].base, then origin/main, "
            "main, HEAD~1.\n"
            "  - Source detection uses [check].source_paths and ignores "
            "[check].ignored_paths.\n"
            "  - Prints the commit, base, and change counts before running."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    check.add_argument(
        "--base",
        help="git ref to compare against (default: [check].base or origin/main)",
    )
    check.set_defaults(handler=cmd_check)

    docs = commands.add_parser(
        "docs",
        help="validate the OKF bundle",
        description=(
            "Validate the OKF bundle under docs/. Checks frontmatter, required "
            "fields, allowed types, stale_after dates, reserved files, and "
            "broken internal links."
        ),
        epilog=(
            "Notes:\n"
            "  - Bundle path and version from [docs] in factory.toml.\n"
            "  - Only non-reserved files require frontmatter with a type.\n"
            "  - Frontmatter is a minimal key: value parser (not full YAML)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    docs.set_defaults(handler=cmd_docs)

    risk = commands.add_parser(
        "risk",
        help="classify the current diff",
        description=(
            "Classify the diff as low risk or high risk. Fails when a "
            "protected path changed, the diff exceeds the size ceiling, the "
            "evidence block is missing or stale, or the pull request is "
            "labelled risk:high without human approval. A high-risk diff "
            "passes only when labelled risk:high and approved by a human."
        ),
    )
    risk.add_argument(
        "--base",
        help="git ref to compare against (default: [check].base or origin/main)",
    )
    risk.set_defaults(handler=cmd_risk)

    audit = commands.add_parser(
        "audit",
        help="report harness drift",
        description=(
            "Report drift across the harness (not implemented yet)."
        ),
    )
    audit.set_defaults(handler=cmd_audit)

    return parser


def main(argv: list[str] | None = None) -> int:
    # Keep our own messages in order when a checked command writes to stdout.
    sys.stdout.reconfigure(line_buffering=True)
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except FactoryError as exc:
        print(f"fail: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
