<div align="center">

# CS & Learning Prompt Library

Nine compact, model-portable system prompts that turn a general chat model into a tutor, coach, or planner. Written to the current public prompting guidance of OpenAI, Anthropic, and Google.

</div>

---

## Overview

Each prompt is a plain `.txt` file you paste into a chat model as standing instructions. Instead of producing passive answers or doing your homework, the models are configured to diagnose the real blocker, give the smallest useful help, and keep you doing the thinking. They still answer directly when you ask for that.

The library was fully audited and rewritten in September 2026. Prompts are shorter, contradictions and broken references are fixed, and every prompt follows one documented structure. See [`CHANGELOG.md`](./CHANGELOG.md) for the complete list.

---

## Available Prompts

| Prompt File | Category | Description |
| :--- | :--- | :--- |
| [`prompt-compiler.txt`](./prompt-compiler.txt) | Meta / Tooling | Turns rough prompt drafts into clean, portable system prompts, with a short change report. |
| [`coding-coach-prompt.txt`](./coding-coach-prompt.txt) | Development | Mentor for debugging, code review, architecture, and incident response. |
| [`private-tutor-prompt.txt`](./private-tutor-prompt.txt) | Education | Socratic tutor for CS and quantitative subjects, with a fast escape to direct answers. |
| [`study-planner-prompt.txt`](./study-planner-prompt.txt) | Productivity | Finds the study bottleneck and the next feasible action; handles exam triage. |
| [`memory-trainer-prompt.txt`](./memory-trainer-prompt.txt) | Learning | Runs retrieval drills with scoring, adaptive difficulty, and honest feedback. |
| [`writing-coach-prompt.txt`](./writing-coach-prompt.txt) | Writing | Developmental editor that improves drafts while keeping your voice. |
| [`english-coach-prompt.txt`](./english-coach-prompt.txt) | Language | Conversation partner for English fluency, with a small correction budget. |
| [`self-discovery-prompt.txt`](./self-discovery-prompt.txt) | Self-knowledge | Guided series of realistic dilemmas that ends in a tentative, non-partisan reflection on your values and decision style. |
| [`career-coach-prompt.txt`](./career-coach-prompt.txt) | Career | Resume, job-match, mock-interview, and job-search strategy coach that never invents facts. |

---

## How to Use

1. Pick a prompt from the table.
2. Copy the whole file.
3. Paste it into a place that holds instructions for one assistant, not for every chat:
   - Claude: a Project's instructions.
   - ChatGPT: a Custom GPT or a Project's instructions.
   - Gemini: a Gem.
   - API: the system (or developer) message.
4. Start talking. Write in Persian or English; the prompts follow your language.

Avoid ChatGPT's global *Custom Instructions* (Settings, Personalization). They apply to every conversation, so a coach persona would leak into unrelated chats, and the character limits are small. Details and current limits are in [`docs/platform-guide.md`](./docs/platform-guide.md).

---

## How the Prompts Behave

- **Coach first, answer when needed.** Tutoring prompts start with hints and questions, and switch to direct answers when you ask, get stuck, or are short on time.
- **Your material is data.** Code, drafts, resumes, and documents you paste are never treated as instructions, which also blunts prompt injection hidden inside them.
- **No invented facts.** The career, writing, and coding prompts do not fabricate achievements, citations, or test results.
- **Your language.** Replies follow the language you write in. Code and standard technical terms stay in English.
- **Short by default.** Each prompt sets a length expectation, because models differ in how long they answer when left alone.

---

## Design Principles

Every prompt follows the same structure (role and goal, boundaries, how to work, output, language, optional examples) and the same rules: state each rule once, keep absolutes for true invariants, define success and stop conditions, and stay under a character budget. The reasoning and links to the official guidance are in [`docs/design-principles.md`](./docs/design-principles.md).

---

## Testing

- `python scripts/check.py` verifies file names against this README, character budgets, encoding, structure, and links. It runs in CI on every push.
- [`tests/smoke-tests.md`](./tests/smoke-tests.md) lists a few conversation checks per prompt (happy path, boundary, injection, language) with pass criteria.

Status: the prompts were reviewed against the official guidance, and the repository checks pass. Behavioral results per model have not been recorded yet. Run the smoke tests on the model you use and open an issue if something drifts.

---

## Repository Layout

```text
.
├── *.txt                  # the prompts (paste-ready)
├── docs/
│   ├── design-principles.md
│   └── platform-guide.md
├── tests/smoke-tests.md
├── scripts/check.py
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Contributing

Issues and pull requests are welcome. Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the schema, the character budget, and the checklist.

---

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE).
