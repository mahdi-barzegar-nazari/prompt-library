# Architecture

`promptlint` is a small, dependency-free tool that keeps the prompt catalogue consistent. This page explains how it is put together and how to extend it.

## Design goals

- **One source of truth.** `prompts/manifest.toml` declares every prompt. The README table, the smoke-test coverage check, and the title check are all derived from it, so they cannot drift apart.
- **Pure, small rules.** Each rule is a function from a loaded file to findings. Rules do no I/O of their own, which makes them trivial to test.
- **Zero runtime dependencies.** The tool uses only the standard library (`tomllib`, `argparse`, `re`, `pathlib`). It runs anywhere Python 3.11+ does.
- **Fail loudly, explain clearly.** Every finding names the file and says what to change.

## Data flow

1. `registry.load_manifest` parses the manifest into `PromptEntry` objects; `registry.load_limits` reads `[tool.promptlint]` from `pyproject.toml`.
2. `checks.run_checks` compares the manifest with the files on disk, loads each prompt as a `PromptFile`, and runs every function in `rules.PROMPT_RULES`.
3. Repo-level checks then verify the smoke-test sections, the README table, and relative Markdown links.
4. The resulting `Report` is printed by `cli.cmd_check`, which exits 1 when it contains errors (or warnings under `--strict`).

## Adding a rule

```python
# src/promptlint/rules.py
def check_no_all_caps_shouting(prompt: PromptFile, _ctx: RuleContext) -> Iterator[Finding]:
    if re.search(r"\b[A-Z]{12,}\b", prompt.text):
        yield _error(prompt, "contains a very long ALL-CAPS word")

PROMPT_RULES = (*PROMPT_RULES, check_no_all_caps_shouting)
```

Then add a test in `tests/test_rules.py` that builds a prompt violating the rule and asserts the finding appears. Rules are additive: existing rules never need to change.

## Why a manifest instead of parsing the README?

Earlier versions extracted the prompt list from README links with a regular expression. That coupled documentation formatting to validation logic and made it easy to break either by editing a table cell. Generating the table from structured data removes that failure mode.
