# Contributing

Thanks for helping improve the library. Bug reports, model-behavior reports, and new prompts are all welcome. By participating you agree to the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Reporting a problem

Open an [issue](https://github.com/mahdi-barzegar-nazari/prompt-library/issues/new/choose) with:

- the prompt file and which model you used,
- your input and the reply you got,
- what you expected instead.

Behavior that differs between models is especially useful to hear about. If you found a way to make a prompt leak its instructions or obey pasted text, follow [`SECURITY.md`](./SECURITY.md) instead.

## Development setup

You need Python 3.11 or newer.

```bash
git clone https://github.com/mahdi-barzegar-nazari/prompt-library.git
cd prompt-library
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pre-commit install                 # optional: run the checks on every commit
```

Run everything CI runs:

```bash
ruff check . && ruff format --check .
mypy
python -m unittest discover -s tests
promptlint check
promptlint sync-readme --check
```

`make all` runs the same sequence if you have `make`.

## Changing or adding a prompt

1. Read [`docs/design-principles.md`](./docs/design-principles.md). It defines the structure and the rules every prompt follows.
2. Keep the prompt under 7,500 characters (aim for under 6,500). The limit is configured in `pyproject.toml`.
3. Put the prompt in `prompts/` as `<name>-prompt.txt` (lowercase letters, digits, single hyphens).
4. Add an entry to [`prompts/manifest.toml`](./prompts/manifest.toml). The `title` must equal the `# Title` line of the file.
5. Run `promptlint sync-readme` to regenerate the README table. Never edit the table by hand.
6. Add a section named after the file to [`tests/smoke-tests.md`](./tests/smoke-tests.md) with three or four checks, including at least one boundary case.
7. Run `promptlint check`. It must pass.
8. Run your smoke tests on at least one model, and say which one in the pull request.
9. Add a line under **Unreleased** in `CHANGELOG.md`.

## Changing the tooling

- Rules live in `src/promptlint/rules.py`. Add a function and append it to `PROMPT_RULES`.
- Every rule needs a test in `tests/` that fails without the rule.
- Code must pass `ruff` and `mypy --strict`. Runtime dependencies stay at zero.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(prompt): ...`, `fix(rules): ...`, `docs: ...`, `ci: ...`.

## Pull request checklist

- [ ] Each rule appears once, and nothing in the prompt contradicts anything else.
- [ ] Absolutes (always, never, must) are used only for real invariants.
- [ ] Pasted user content is explicitly treated as data, not instructions.
- [ ] Examples obey every rule in the prompt.
- [ ] The output language and the reply length are both specified.
- [ ] No model or vendor names inside the prompt.
- [ ] `promptlint check` and the test suite pass.
- [ ] `CHANGELOG.md` is updated.
