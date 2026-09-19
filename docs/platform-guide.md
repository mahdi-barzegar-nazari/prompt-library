# Platform Guide

Where to paste a prompt, and what to watch for. Limits below were reported in July and August 2026 and change often, so treat them as a guide and confirm in the product.

## Recommended places

| Platform | Where | Notes |
| :--- | :--- | :--- |
| Claude | Project, then "Set project instructions" | No fixed character cap is published; instructions count against the context window. One project per prompt keeps behavior clean. |
| ChatGPT | Custom GPT (Instructions field) or a Project's instructions | Custom GPT instructions are commonly reported to allow about 8,000 characters. Every prompt in this library is under 7,500. |
| Gemini | Gem (Instructions field) | Reported limits differ between sources (roughly 4,000 up to tens of thousands of characters). If a prompt is rejected or truncated, use one of the fallbacks below. |
| API | System message (or developer message on models that use that name) | No practical limit for these prompts. Keep the prompt at the start of the request so it stays stable and cache-friendly. |

## Fallback for any chat

Paste the prompt as your first message, preceded by one line: "Follow these instructions for this whole conversation." This works everywhere but is less durable than a saved instruction, because it can scroll out of a long context.

## Why not ChatGPT Custom Instructions

Custom Instructions (Settings, Personalization) apply to all conversations, so a coach persona leaks into unrelated chats. They are also small: reported at 1,500 characters on Free and Go plans and 5,000 on paid plans as of July 2026. Several prompts here would not fit. Use a Custom GPT or a Project instead.

## Tips

- **One prompt per assistant.** Do not paste two prompts into the same place; their rules will conflict.
- **Language.** Write in Persian or English. The prompts follow your language, and code and standard technical terms stay in English.
- **Length.** Each prompt sets a length expectation. If a model still answers too long or too short, add one line to the end of the instructions, such as "Keep replies under 120 words" or "Give fuller explanations".
- **Reasoning settings.** If your platform lets you choose a reasoning or thinking level, start with the default. These prompts do not need a high setting.
- **Editing.** Keep local edits small and re-run the smoke tests in [`../tests/smoke-tests.md`](../tests/smoke-tests.md) after changing a prompt.
