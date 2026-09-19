"""Per-prompt rules.

Each rule is a small pure function ``(PromptFile, RuleContext) -> Iterator[Finding]``.
To add a rule, write the function and append it to ``PROMPT_RULES``; nothing else changes.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass

from promptlint.models import Finding, Limits, PromptEntry, PromptFile, Severity

FILENAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-prompt\.txt$")
VENDOR_WORDS = re.compile(
    r"\b(ChatGPT|GPT-?\d|OpenAI|Claude|Anthropic|Gemini|Google|Copilot)\b", re.IGNORECASE
)
LEFTOVER_MARKERS = re.compile(r"SYSTEM PROMPT|TODO|FIXME")
# Persian/Arabic block and the zero-width non-joiner are the only allowed non-ASCII text.
ALLOWED_NON_ASCII = re.compile(r"[\u0600-\u06FF\u200c]")
BOUNDARIES_HEADING = re.compile(r"^## (Boundaries|Principles)\b", re.MULTILINE)
LANGUAGE_MENTION = re.compile(r"language", re.IGNORECASE)
DATA_RULE = re.compile(r"not instructions", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class RuleContext:
    """What a rule may need besides the file itself."""

    limits: Limits
    entry: PromptEntry | None


Rule = Callable[[PromptFile, RuleContext], Iterator[Finding]]


def _error(prompt: PromptFile, message: str) -> Finding:
    return Finding(Severity.ERROR, prompt.name, message)


def check_filename(prompt: PromptFile, _ctx: RuleContext) -> Iterator[Finding]:
    if not FILENAME_PATTERN.match(prompt.name):
        yield _error(prompt, "name must be lowercase-hyphenated and end in '-prompt.txt'")


def check_encoding(prompt: PromptFile, _ctx: RuleContext) -> Iterator[Finding]:
    if prompt.raw.startswith(b"\xef\xbb\xbf"):
        yield _error(prompt, "has a UTF-8 BOM")
    if b"\r\n" in prompt.raw:
        yield _error(prompt, "has CRLF line endings (use LF)")
    if not prompt.valid_utf8:
        yield _error(prompt, "not valid UTF-8")
    elif not prompt.text.endswith("\n"):
        yield _error(prompt, "missing trailing newline")


def check_length(prompt: PromptFile, ctx: RuleContext) -> Iterator[Finding]:
    size = len(prompt.text)
    if size > ctx.limits.max_chars:
        yield _error(prompt, f"{size} characters exceeds the {ctx.limits.max_chars} limit")
    elif size > ctx.limits.target_chars:
        yield Finding(
            Severity.WARNING,
            prompt.name,
            f"{size} characters is above the {ctx.limits.target_chars} target",
        )


def check_structure(prompt: PromptFile, ctx: RuleContext) -> Iterator[Finding]:
    text = prompt.text
    if not text.startswith("# "):
        yield _error(prompt, "must start with a '# Title' line")
    elif ctx.entry is not None:
        first_line = text.splitlines()[0]
        if first_line != f"# {ctx.entry.title}":
            yield _error(prompt, f"title line {first_line!r} does not match the manifest title")
    if not BOUNDARIES_HEADING.search(text):
        yield _error(prompt, "needs a '## Boundaries' or '## Principles' section")
    if not LANGUAGE_MENTION.search(text):
        yield _error(prompt, "has no output-language rule")
    if not DATA_RULE.search(text):
        yield _error(prompt, "has no data-isolation rule (pasted content is 'not instructions')")


def check_content(prompt: PromptFile, _ctx: RuleContext) -> Iterator[Finding]:
    text = prompt.text
    if LEFTOVER_MARKERS.search(text):
        yield _error(prompt, "contains a leftover marker (SYSTEM PROMPT, TODO, or FIXME)")
    if match := VENDOR_WORDS.search(text):
        yield _error(prompt, f"mentions a vendor or model name ({match.group(0)})")
    bad = sorted({c for c in text if ord(c) > 127 and not ALLOWED_NON_ASCII.match(c)})
    if bad:
        yield _error(prompt, f"unexpected non-ASCII characters {bad!r}")


PROMPT_RULES: tuple[Rule, ...] = (
    check_filename,
    check_encoding,
    check_length,
    check_structure,
    check_content,
)
