#!/usr/bin/env python3
"""Repository checks for the prompt library.

Run from anywhere:  python scripts/check.py
Exits with status 1 if any check fails.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_CHARS = 7500      # hard limit (see docs/design-principles.md)
TARGET_CHARS = 6500   # soft target; only a warning
VENDOR_WORDS = re.compile(r"\b(ChatGPT|GPT-?\d|OpenAI|Claude|Anthropic|Gemini|Google|Copilot)\b", re.I)
ALLOWED_NON_ASCII = re.compile(r"[\u0600-\u06FF\u200c]")  # Persian/Arabic block and ZWNJ

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def read_bytes_text(path):
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        err(f"{path.name}: has a UTF-8 BOM")
    if b"\r\n" in raw:
        err(f"{path.name}: has CRLF line endings (use LF)")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        err(f"{path.name}: not valid UTF-8")
        return ""
    if not text.endswith("\n"):
        err(f"{path.name}: missing trailing newline")
    return text


def check_prompts():
    prompts = sorted(ROOT.glob("*.txt"))
    if not prompts:
        err("no prompt files (*.txt) found in the repository root")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(\./([\w\-]+\.txt)\)", readme))
    on_disk = {p.name for p in prompts}

    for name in sorted(linked - on_disk):
        err(f"README links to {name}, which does not exist")
    for name in sorted(on_disk - linked):
        err(f"{name} is not listed in the README table")

    smoke = (ROOT / "tests" / "smoke-tests.md")
    smoke_text = smoke.read_text(encoding="utf-8") if smoke.exists() else ""

    print(f"{'file':32s} {'chars':>6s} {'words':>6s}")
    for path in prompts:
        text = read_bytes_text(path)
        n = len(text)
        print(f"{path.name:32s} {n:6d} {len(text.split()):6d}")
        if n > MAX_CHARS:
            err(f"{path.name}: {n} characters exceeds the {MAX_CHARS} limit")
        elif n > TARGET_CHARS:
            warn(f"{path.name}: {n} characters is above the {TARGET_CHARS} target")
        if not text.startswith("# "):
            err(f"{path.name}: must start with a '# Title' line")
        if not re.search(r"^## (Boundaries|Principles)\b", text, re.M):
            err(f"{path.name}: needs a '## Boundaries' or '## Principles' section")
        if not re.search(r"language", text, re.I):
            err(f"{path.name}: has no output-language rule")
        if re.search(r"SYSTEM PROMPT|TODO|FIXME", text):
            err(f"{path.name}: contains a leftover marker (SYSTEM PROMPT, TODO, or FIXME)")
        m = VENDOR_WORDS.search(text)
        if m:
            err(f"{path.name}: mentions a vendor or model name ({m.group(0)})")
        bad = sorted({c for c in text if ord(c) > 127 and not ALLOWED_NON_ASCII.match(c)})
        if bad:
            err(f"{path.name}: unexpected non-ASCII characters {bad!r}")
        if not re.search(rf"^## {re.escape(path.name)}\s*$", smoke_text, re.M):
            err(f"tests/smoke-tests.md has no section for {path.name}")


def check_links():
    docs = [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "CONTRIBUTING.md"]
    docs += sorted((ROOT / "docs").glob("*.md")) + sorted((ROOT / "tests").glob("*.md"))
    for doc in docs:
        if not doc.exists():
            err(f"missing file: {doc.relative_to(ROOT)}")
            continue
        text = read_bytes_text(doc)
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            rel = target.split("#")[0]
            if rel and not (doc.parent / rel).exists():
                err(f"{doc.relative_to(ROOT)}: broken link {target}")


def main():
    check_prompts()
    check_links()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
