"""Plain data types shared by every promptlint module."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Severity(StrEnum):
    """How seriously a finding should be taken."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class Finding:
    """One problem discovered by a check."""

    severity: Severity
    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity}: {self.location}: {self.message}"


@dataclass(frozen=True, slots=True)
class Limits:
    """Character budget for a single prompt (see docs/design-principles.md)."""

    max_chars: int = 7500
    target_chars: int = 6500


@dataclass(frozen=True, slots=True)
class PromptEntry:
    """A prompt as declared in ``prompts/manifest.toml``."""

    file: str
    title: str
    category: str
    description: str


@dataclass(frozen=True, slots=True)
class PromptFile:
    """A prompt file read from disk, kept as raw bytes and decoded text."""

    path: Path
    raw: bytes
    text: str
    valid_utf8: bool

    @property
    def name(self) -> str:
        return self.path.name

    @classmethod
    def load(cls, path: Path) -> PromptFile:
        raw = path.read_bytes()
        try:
            return cls(path, raw, raw.decode("utf-8"), valid_utf8=True)
        except UnicodeDecodeError:
            return cls(path, raw, "", valid_utf8=False)


@dataclass(frozen=True, slots=True)
class PromptStats:
    """Size of one prompt, for the summary table."""

    name: str
    chars: int
    words: int


@dataclass(slots=True)
class Report:
    """Everything a run of the checks produced."""

    findings: list[Finding]
    stats: list[PromptStats]

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARNING]
