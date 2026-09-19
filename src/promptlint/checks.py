"""Repository-level checks: manifest vs. disk, smoke tests, README sync, doc links."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote

from promptlint.models import Finding, PromptEntry, PromptFile, PromptStats, Report, Severity
from promptlint.readme import MarkerError, render_table, replace_block
from promptlint.registry import PROMPTS_DIR, ManifestError, load_limits, load_manifest
from promptlint.rules import PROMPT_RULES, RuleContext

MIN_SMOKE_CHECKS = 3
SMOKE_TESTS = Path("tests") / "smoke-tests.md"
_SKIPPED_DIRS = {".git", ".venv", "venv", "node_modules", "build", "dist"}
_FENCE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


def _error(location: str, message: str) -> Finding:
    return Finding(Severity.ERROR, location, message)


def check_manifest_against_disk(root: Path, entries: list[PromptEntry]) -> Iterator[Finding]:
    listed = [e.file for e in entries]
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        yield _error("manifest", f"{name} is listed more than once")
    on_disk = {p.name for p in (root / PROMPTS_DIR).glob("*.txt")}
    for name in sorted(set(listed) - on_disk):
        yield _error("manifest", f"lists {name}, which does not exist in {PROMPTS_DIR}/")
    for name in sorted(on_disk - set(listed)):
        yield _error(name, "is not listed in the manifest")


def smoke_check_counts(text: str) -> dict[str, int]:
    """Map each ``## file.txt`` section of the smoke tests to its number of numbered checks."""
    counts: dict[str, int] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            counts[current] = 0
        elif current is not None and re.match(r"\d+\. ", line):
            counts[current] += 1
    return counts


def check_smoke_tests(root: Path, entries: list[PromptEntry]) -> Iterator[Finding]:
    path = root / SMOKE_TESTS
    if not path.is_file():
        yield _error(str(SMOKE_TESTS), "file is missing")
        return
    counts = smoke_check_counts(path.read_text(encoding="utf-8"))
    for entry in entries:
        found = counts.get(entry.file)
        if found is None:
            yield _error(str(SMOKE_TESTS), f"has no section for {entry.file}")
        elif found < MIN_SMOKE_CHECKS:
            yield _error(
                str(SMOKE_TESTS),
                f"{entry.file} has {found} check(s); at least {MIN_SMOKE_CHECKS} are required",
            )


def check_readme_in_sync(root: Path, entries: list[PromptEntry]) -> Iterator[Finding]:
    path = root / "README.md"
    if not path.is_file():
        yield _error("README.md", "file is missing")
        return
    current = path.read_text(encoding="utf-8")
    try:
        expected = replace_block(current, render_table(entries))
    except MarkerError as exc:
        yield _error("README.md", str(exc))
        return
    if expected != current:
        yield _error("README.md", "prompt table is stale; run 'promptlint sync-readme'")


def iter_markdown(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*.md")):
        relative_parts = path.relative_to(root).parts
        if not _SKIPPED_DIRS.intersection(relative_parts):
            yield path


def check_doc_links(root: Path) -> Iterator[Finding]:
    for doc in iter_markdown(root):
        text = doc.read_text(encoding="utf-8")
        text = _INLINE_CODE.sub("", _FENCE.sub("", text))
        for target in _LINK.findall(text):
            if _SCHEME.match(target) or target.startswith("#"):
                continue
            relative = unquote(target.split("#", maxsplit=1)[0])
            if relative and not (doc.parent / relative).exists():
                yield _error(str(doc.relative_to(root)), f"broken link {target}")


def run_checks(root: Path) -> Report:
    """Run every check against the repository at ``root``."""
    try:
        entries = load_manifest(root)
        limits = load_limits(root)
    except ManifestError as exc:
        return Report([_error("config", str(exc))], [])

    findings: list[Finding] = list(check_manifest_against_disk(root, entries))
    by_name = {entry.file: entry for entry in entries}
    stats: list[PromptStats] = []

    for path in sorted((root / PROMPTS_DIR).glob("*.txt")):
        prompt = PromptFile.load(path)
        ctx = RuleContext(limits=limits, entry=by_name.get(prompt.name))
        for rule in PROMPT_RULES:
            findings.extend(rule(prompt, ctx))
        stats.append(PromptStats(prompt.name, len(prompt.text), len(prompt.text.split())))

    findings.extend(check_smoke_tests(root, entries))
    findings.extend(check_readme_in_sync(root, entries))
    findings.extend(check_doc_links(root))
    return Report(findings, stats)
