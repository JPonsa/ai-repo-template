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

    print(f"commit: {git('rev-parse', 'HEAD')}")
    if base:
        print(f"base:   {git('rev-parse', '--short', base)} ({configured_base or 'default'})")
    print(f"change: {len(changed)} file(s), {len(source_changed)} source file(s)")

    if source_changed and not commands:
        print(
            "fail: source changed but factory.toml configures no check commands",
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


def cmd_docs(args: argparse.Namespace) -> int:
    """Validate the OKF bundle and report every problem it finds."""
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
        is_reserved = path.name in reserved

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

    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"fail: {error}", file=sys.stderr)

    print(f"docs: {concepts} concept(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


# --------------------------------------------------------------------------
# risk and audit
# --------------------------------------------------------------------------


def cmd_risk(args: argparse.Namespace) -> int:
    """Classify a diff. Implemented by the enforcement ticket."""
    raise FactoryError("risk: not implemented yet")


def cmd_audit(args: argparse.Namespace) -> int:
    """Report harness drift. Implemented by the feedback ticket."""
    raise FactoryError("audit: not implemented yet")


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
        description="Classify a diff as low risk or high risk (not implemented yet).",
    )
    risk.add_argument(
        "--base",
        help="git ref to compare against (for future use)",
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
