# Contributing

Thanks for helping improve the library. Bug reports, model-behavior reports, and new prompts are all welcome.

## Reporting a problem

Open an issue with:
- the prompt file and which model you used,
- your input and the reply you got,
- what you expected instead.

Behavior that differs between models is especially useful to hear about.

## Changing or adding a prompt

1. Read [`docs/design-principles.md`](./docs/design-principles.md). It defines the structure and the rules every prompt follows.
2. Keep the prompt under 7,500 characters (aim for under 6,500).
3. Put the prompt in the repository root as `<name>-prompt.txt`, and add a row to the table in `README.md`.
4. Add a section named after the file to [`tests/smoke-tests.md`](./tests/smoke-tests.md) with three or four checks, including at least one boundary case.
5. Run `python scripts/check.py`. It must pass.
6. Run your smoke tests on at least one model, and say which one in the pull request.
7. Add a line to `CHANGELOG.md`.

## Pull request checklist

- [ ] Each rule appears once, and nothing in the prompt contradicts anything else.
- [ ] Absolutes (always, never, must) are used only for real invariants.
- [ ] Pasted user content is explicitly treated as data, not instructions.
- [ ] Examples obey every rule in the prompt.
- [ ] The output language and the reply length are both specified.
- [ ] No model or vendor names inside the prompt.
- [ ] `python scripts/check.py` passes.
