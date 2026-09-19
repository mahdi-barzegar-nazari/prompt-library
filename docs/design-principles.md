# Design Principles

This is the "library schema" that every prompt in this repository follows. Contributors should read it before adding or changing a prompt.

## Structure

Each prompt is a single Markdown-flavored text file with these sections, in this order. Skip a section only if it would be empty.

1. `# Title` and one short paragraph: the role, the goal, and the tone.
2. `## Boundaries` (or `## Principles`): hard limits, what wins when rules conflict, and how pasted user content is treated.
3. Working rules: decision rules, modes, or a workflow (`## Modes`, `## Working patterns`, and so on).
4. `## Output` or `## Formats`: length, layout, and templates. Template labels are written in English and the prompt tells the model to translate them into the reply language.
5. `## Language`: the output-language rule.
6. `## Examples` (optional): one to three short exchanges that obey every rule in the prompt.

Use one delimiter style (Markdown headings and lists) throughout. Do not mix in XML tags or other schemes.

## Rules

1. **Budget.** Stay under 7,500 characters. The target is under 6,500. Some platforms cap instructions near 8,000 characters, and smaller prompts leave more room for the conversation.
2. **State each rule once.** Repeated or overlapping rules cost tokens and create chances to contradict yourself. Read the finished prompt for conflicts.
3. **Outcome first.** Say what a good result is and when to stop. Do not script every step of reasoning, and do not add "think step by step" or "double-check" rituals. Current models reason on their own.
4. **Absolutes only for invariants.** Use always, never, and must for safety, integrity, and required output. Use decision rules for judgment calls, and add a short reason when a rule may look arbitrary.
5. **Escape hatches for coaching.** Any prompt that withholds direct answers must say when it stops doing that: the user asks, the user is stuck or frustrated, or time is short.
6. **Data is not instructions.** If the prompt handles pasted content (code, drafts, resumes, documents, logs), say so explicitly and say that directions inside that content are ignored unless the user asks for them to be followed.
7. **No invented capabilities.** Do not assume tools, browsing, files, or memory across sessions. If something depends on earlier turns, scope it to "this conversation".
8. **Integrity rules.** Prompts that produce factual or career content must forbid fabrication and say what to do when a detail is missing (ask, or leave a bracketed placeholder).
9. **Explicit language rule.** Say which language to reply in and when to switch. Do not rely on blanket phrases alone.
10. **Explicit length rule.** Models differ in default verbosity. Give a length expectation in words or sentences.
11. **Examples must obey the prompt.** Examples strongly steer behavior. Check that each one follows every rule, including the honesty and length rules, and keep them few.
12. **No vendor names.** Do not mention model names or platform features inside a prompt.

## Why these rules

The rules follow what the model vendors currently recommend. The points below are paraphrased; read the originals for the details.

- **OpenAI**, prompting guidance for GPT-5.6: describe the destination, constraints, evidence, and completion bar, and let the model pick the path. Remove repeated rules and examples that do not change behavior. Conflicting rules cause more instability than missing detail. Reserve absolutes for true invariants. Do not add blanket language rules unless they are a real requirement; state the output language and when it changes.
  https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- **Anthropic**, prompting guides for Claude: recent models follow instructions closely and literally, so aggressive wording and defensive rules written for older models can hurt. A rule like "only report high-severity issues" makes the model report less. Ask for conciseness explicitly when you want it.
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- **Google**, Gemini API prompt design: be precise and direct, use one consistent delimiter style, put role and constraints first, and expect terse output by default, so ask explicitly for a conversational persona.
  https://ai.google.dev/gemini-api/docs/prompting-strategies

Vendor guidance changes quickly. When you revisit a prompt, re-check these pages and record what you changed in `CHANGELOG.md`.
