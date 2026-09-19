"""Command-line interface: ``promptlint check`` and ``promptlint sync-readme``."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from promptlint import __version__
from promptlint.checks import run_checks
from promptlint.models import PromptStats
from promptlint.readme import MarkerError, render_table, replace_block
from promptlint.registry import ManifestError, find_root, load_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="promptlint", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--root", type=Path, default=None, help="repository root (default: auto-detect)"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="validate prompts, docs, and repository layout")
    check.add_argument("--strict", action="store_true", help="treat warnings as errors")

    sync = commands.add_parser("sync-readme", help="regenerate the README prompt table")
    sync.add_argument("--check", action="store_true", help="exit 1 if the README is stale")
    return parser


def _print_stats(stats: Sequence[PromptStats]) -> None:
    print(f"{'prompt':32s} {'chars':>6s} {'words':>6s}")
    for stat in stats:
        print(f"{stat.name:32s} {stat.chars:6d} {stat.words:6d}")


def cmd_check(root: Path, strict: bool) -> int:
    report = run_checks(root)
    _print_stats(report.stats)
    print()
    for finding in report.findings:
        print(finding)
    failed = bool(report.errors) or (strict and bool(report.warnings))
    if failed:
        print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s).")
        return 1
    print("All checks passed.")
    return 0


def cmd_sync_readme(root: Path, check_only: bool) -> int:
    try:
        table = render_table(load_manifest(root))
        readme_path = root / "README.md"
        current = readme_path.read_text(encoding="utf-8")
        updated = replace_block(current, table)
    except (ManifestError, MarkerError, FileNotFoundError) as exc:
        print(f"error: {exc}")
        return 1
    if updated == current:
        print("README is up to date.")
        return 0
    if check_only:
        print("README prompt table is stale; run 'promptlint sync-readme'.")
        return 1
    readme_path.write_text(updated, encoding="utf-8")
    print("README prompt table updated.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_root(args.root or Path.cwd())
    if args.command == "check":
        return cmd_check(root, args.strict)
    return cmd_sync_readme(root, args.check)
