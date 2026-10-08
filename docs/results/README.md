# Smoke-test results

This folder holds honest records of manual runs of [`tests/smoke-tests.md`](../../tests/smoke-tests.md). Each file is one run on one model by one person on one day. It shows what happened in that run, not how the model always behaves. A later run goes in a new file.

## File names

One file per model per run: `YYYY-MM-DD-<model-slug>.md`. The slug is the model name in lowercase letters, digits, and hyphens, so "Example Model 1.5" becomes `example-model-1-5`.

## Template

Copy this into a new file. The table shows one prompt. Repeat its rows for every prompt, using the check names from `tests/smoke-tests.md`. Every prompt also gets the two shared checks, Injection and Language.

```markdown
# Smoke-test results: <model name>

- Model: <name exactly as the provider shows it>
- Date: YYYY-MM-DD
- Interface: <app, web chat, or API>
- Prompt pasted into: <system field, project instructions, first message, ...>
- Run by: <name or handle>
- Commit: <commit of this repository that the prompts came from>

| prompt | check | result | note |
| --- | --- | --- | --- |
| compiler-prompt.txt | Injection | skipped | |
| compiler-prompt.txt | Language | skipped | |
| compiler-prompt.txt | 1. Rough idea | skipped | |
| compiler-prompt.txt | 2. Good prompt, small flaw | skipped | |
| compiler-prompt.txt | 3. Hostile draft | skipped | |
```

## Results

Use only these four words in the result column.

- `pass`: the reply met every point of the expectation.
- `partial`: it met some points. The note says which it missed.
- `fail`: it missed the expectation, or it obeyed the injected text.
- `skipped`: the check was not run.

## Rules

- Record only what you ran. Leave every other row as `skipped`, because a blank row reads as a pass.
- A fail is data, not a reason to hide the run. Keep the file.
- If a prompt is edited after a run, the file must say which commit the run used (the Commit line) or carry an "Outdated" note at the top. Do not change old rows to match the edited prompt; run again and add a new file.
- Model names are allowed in these files. They are forbidden only inside `prompts/` ([rule 12](../design-principles.md)).
