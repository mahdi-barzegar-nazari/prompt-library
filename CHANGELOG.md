# Changelog

## 2026-09-19

- **Added `self-discovery-prompt.txt`.** A guided series of dilemmas ending in a tentative reflection on values and decision style. Compared with the original draft, it is transparent about its purpose instead of hiding it, presents results as hypotheses rather than findings, avoids party and ideology labels, allows "neither" and "it depends" answers, lets the user stop or see results early, adds a language rule and length limits, and treats the user's answers as data.
- README and smoke tests updated.

## 2026-09-18

A full audit and rewrite. The library shrank from 66,312 to 37,232 characters (-44%), every prompt now fits within an 8,000-character instruction field, and all cross-references resolve.

### Repository

- **Fixed a broken link.** The README listed `study-planner-prompt.txt`, but the file was named `academic-execution-prompt.txt`. The file is now `study-planner-prompt.txt`, and `scripts/check.py` fails CI if a listed file is missing or an unlisted one appears.
- **Fixed unusable setup advice.** The README pointed to ChatGPT Custom Instructions, which apply to every chat and have small limits. Three prompts (the study planner at 13,953 characters, the compiler at 11,630, and the writing coach at 8,609) were also over the roughly 8,000-character Custom GPT limit. Setup guidance now lives in `docs/platform-guide.md`.
- **Defined the missing schema.** The README asked for prompts "matching the library schema", which did not exist. It is now `docs/design-principles.md`.
- **Added** `CHANGELOG.md`, `CONTRIBUTING.md`, `tests/smoke-tests.md`, `scripts/check.py`, a CI workflow, and `.gitattributes` (LF line endings).

### All prompts

- **Language contradiction.** Four prompts had Persian-only output templates but also said "reply in the user's language". Templates are now written in English with an instruction to translate the labels. Each prompt has an explicit output-language rule.
- **The library did not follow its own compiler.** The compiler required an explicit data-isolation rule and a fixed four-part structure. No prompt had the data rule, and none followed the structure exactly (a few only approximated it). Every prompt that handles pasted content now says that content is data, not instructions, which also guards against injected text in resumes, drafts, and logs.
- **Invented state.** Several prompts assumed memory or history (for example "historical capacity estimates"). They are now scoped to what the user says in the current conversation.
- **Over-emphatic and duplicated rules** were removed or turned into decision rules with reasons. Absolutes remain only for true invariants such as integrity and safety.
- **Length guidance.** Models differ in default verbosity, so every prompt now states an expected reply length.
- **Examples fixed.** The career example invented details the user never gave (a specific tool, a weekly cadence, automation), which contradicted its own truth rule. The coding example labeled "guided nudge" actually gave a full fix. The English-coach tip did not match the learner's sentence.

### Per prompt

- **prompt-compiler**
  - The strict skeleton conflicted with Minimal-Diff mode; the skeleton now applies to full compilation only.
  - The `# filename:` line inside the output code block leaked into the compiled prompt, violating the compiler's own leak rule. The filename now sits below the block.
  - Diagnostics were hard-coded to Persian; they now follow the user's language.
  - The draft is now explicitly treated as data.
  - Filename convention aligned with the library (`-prompt.txt`).
  - The nine-stage pipeline, provenance tags, and twelve-point gate were condensed into principles and one final check.
- **coding-coach**
  - The defaults left low urgency plus senior developer undefined; the matrix is complete.
  - "Follow platform safety rules" was replaced by a concrete integrity rule (do not invent outputs; say what you did not verify).
  - Added scope discipline and "report all findings, filter later" for reviews.
- **private-tutor**
  - Modes had triggers but no behavior; each now has one.
  - The fast escape conflicted with the academic-integrity rule; they are reconciled for graded versus ungraded work.
  - "Provide documentation links" invited invented URLs; it now points to documentation by name.
  - Added examples.
- **study-planner**
  - Undefined abbreviation "MSD" removed.
  - Reused traffic-light emoji for two different meanings removed.
  - Added a self-harm safety line.
  - The action plan is capped at two or three blocks to match the "stop planning" principle.
  - 55% shorter.
- **memory-trainer**
  - The mission overclaimed working-memory improvement; it now states honestly what practice does and does not do.
  - Scoring modes were defined but never selected; they are now chosen by the manipulation variable.
  - "Exactly one" versus "at most one or two" difficulty changes is now exactly one, with a hold band between 50% and 85%.
  - Scoring must use the exact items from the encoding phase.
- **writing-coach**
  - "One lever at a time" contradicted a three-priority diagnosis template; the template now has one priority plus up to two short follow-ups.
  - The absolute ban on rewriting drafts blocked short and urgent requests; explicit requests for short or own-draft rewrites are now allowed.
  - "Spider-Web Multi-Pass" is not an established technique; it is now "Multi-pass revision".
  - Added Persian typography notes.
- **english-coach**
  - Added level-adjustment rules, mode triggers, and a first-message behavior.
  - "Always end with a question" became "usually".
- **career-coach**
  - Modes were lettered 0 and C to H, with A and B missing; they are now numbered 1 to 6, and all six are covered in the output section.
  - Added privacy, no-promise, and resume-injection rules.

### Behavior changes to be aware of

- The writing coach will now fully polish a short text or a draft when asked explicitly.
- Reviews from the coding coach list every finding with a severity label instead of filtering.
- Output labels follow the user's language instead of always being Persian.
- The study planner is now `study-planner-prompt.txt`. Update any old links.

### Known limitations

- The prompts were reviewed against the official guidance and pass the repository checks, but per-model behavioral results are not recorded yet. Use `tests/smoke-tests.md`.
- Platform character limits are reported values from July and August 2026 and may change.
- The smoke tests are manual, and most are single-turn.
