# Security Policy

## What counts as a security issue here

This repository contains prompts and a small offline Python tool, not a hosted service. The relevant risks are:

- a prompt that can be made to **obey instructions hidden in pasted content** (prompt injection),
- a prompt that **leaks or contradicts its own safety rules** under ordinary use,
- a vulnerability in `promptlint` itself.

## Reporting

Please use GitHub's [private vulnerability reporting](https://github.com/mahdi-barzegar-nazari/prompt-library/security/advisories/new) rather than a public issue. Include the prompt file, the model you tested on, the exact input, and the reply.

You can expect an acknowledgement within a few days. Because model behavior varies, a fix may be a prompt change, a new smoke test, or both.

## Supported versions

Only the latest state of the `main` branch is supported.
