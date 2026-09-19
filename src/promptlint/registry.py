"""Loading the prompt manifest and tool configuration from disk."""

from __future__ import annotations

import tomllib
from pathlib import Path

from promptlint.models import Limits, PromptEntry

PROMPTS_DIR = "prompts"
MANIFEST_NAME = "manifest.toml"
_REQUIRED_FIELDS = ("file", "title", "category", "description")


class ManifestError(ValueError):
    """The manifest is missing, unreadable, or malformed."""


def find_root(start: Path) -> Path:
    """Walk upwards from ``start`` to the directory holding ``prompts/manifest.toml``."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / PROMPTS_DIR / MANIFEST_NAME).is_file():
            return candidate
    return start


def load_manifest(root: Path) -> list[PromptEntry]:
    """Parse ``prompts/manifest.toml`` into ordered entries."""
    path = root / PROMPTS_DIR / MANIFEST_NAME
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"missing manifest: {PROMPTS_DIR}/{MANIFEST_NAME}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ManifestError(f"invalid TOML in {PROMPTS_DIR}/{MANIFEST_NAME}: {exc}") from exc

    entries: list[PromptEntry] = []
    for index, item in enumerate(data.get("prompt", []), start=1):
        missing = [key for key in _REQUIRED_FIELDS if key not in item]
        if missing:
            raise ManifestError(f"prompt #{index}: missing field(s) {missing}")
        entries.append(PromptEntry(**{key: str(item[key]) for key in _REQUIRED_FIELDS}))
    return entries


def load_limits(root: Path) -> Limits:
    """Read ``[tool.promptlint]`` from pyproject.toml, falling back to defaults."""
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return Limits()
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ManifestError(f"invalid TOML in pyproject.toml: {exc}") from exc
    section = data.get("tool", {}).get("promptlint", {})
    defaults = Limits()
    return Limits(
        max_chars=int(section.get("max_chars", defaults.max_chars)),
        target_chars=int(section.get("target_chars", defaults.target_chars)),
    )
