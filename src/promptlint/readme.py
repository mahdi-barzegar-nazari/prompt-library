"""Keeps the README prompt table in sync with ``prompts/manifest.toml``."""

from __future__ import annotations

from collections.abc import Sequence

from promptlint.models import PromptEntry
from promptlint.registry import PROMPTS_DIR

START_MARKER = "<!-- prompts:start -->"
END_MARKER = "<!-- prompts:end -->"


class MarkerError(ValueError):
    """The README does not contain exactly one start/end marker pair."""


def render_table(entries: Sequence[PromptEntry]) -> str:
    """Render the Markdown table of prompts, in manifest order."""
    lines = [
        "| Prompt | Category | Description |",
        "| :--- | :--- | :--- |",
    ]
    for entry in entries:
        link = f"[`{entry.file}`](./{PROMPTS_DIR}/{entry.file})"
        lines.append(f"| {link} | {entry.category} | {entry.description} |")
    return "\n".join(lines)


def replace_block(readme: str, table: str) -> str:
    """Return ``readme`` with the marked block replaced by ``table``."""
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise MarkerError(f"README must contain one {START_MARKER} and one {END_MARKER}")
    start = readme.index(START_MARKER)
    end = readme.index(END_MARKER)
    if end < start:
        raise MarkerError(f"{END_MARKER} appears before {START_MARKER}")
    head = readme[:start]
    tail = readme[end + len(END_MARKER) :]
    return f"{head}{START_MARKER}\n{table}\n{END_MARKER}{tail}"
