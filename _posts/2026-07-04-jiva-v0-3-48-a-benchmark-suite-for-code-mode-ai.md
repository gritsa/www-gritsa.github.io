---
layout: post
title: "Jiva v0.3.48: A Benchmark Suite for Code-Mode AI"
date: 2026-07-04 10:42:38 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, LLM"
excerpt: "Jiva v0.3.48 adds a deterministic benchmark that scores a model in code mode with no LLM judge, and separates a model that cannot emit a large enough response from one that got the logic wrong."
description: "What changed in Jiva v0.3.48: the taskstore and micro-CRM benchmark suites, the output-limited flag, the jiva benchmark command and HTTP routes, and the code-mode tool-call fixes the first runs exposed."
keywords: "Jiva, code mode benchmark, AI agent evaluation, tool call fixes, deterministic testing, open-source AI"
featured_image: "/assets/img/posts/2026-07-04-jiva-v0-3-48-a-benchmark-suite-for-code-mode-ai.png"
---

Updated 2026-10-16: rewritten from the v0.3.48 release notes. The original post leaned on adjectives the notes do not support.

Jiva v0.3.48 was released on June 29, 2026. Its headline is a benchmark for code mode. Its most useful idea is smaller than that: when a model fails a coding task, the benchmark can tell you whether it ran out of room to write or got the logic wrong. Those two failures need different fixes, and until this release Jiva could not tell them apart.

## The problem it was built for

Jiva's `--code` mode works well with `gpt-oss-120b` and degrades with other models. The release notes name two: Sarvam-105b, which has a 4096-token output cap and struggles when a task needs a large write or edit, and Krutrim, which struggles with longer multi-step tasks. Until now there was no objective way to measure how a given model and configuration performed in code mode.

## How the scoring works

The benchmark drives a `CodeAgent` through coding tasks in throwaway workspaces and scores each one with Node's built-in test runner (`node --test`). There is no LLM judge and no network call. Each task reports pass or fail plus iterations, tokens, wall time and whether the iteration cap was hit.

Two details keep the score honest. Every test file is hashed before the agent runs, and if the agent edits a test to make it pass, the task fails with the reason `tests-modified`. And each tier's workspace is built from the reference solutions of all earlier tiers plus one new failing test, so tiers build on each other while each is measured on its own.

## Two suites

**`taskstore`** is the baseline and gates. It is a single small task-management library built in eight tiers, scored pass or fail. The tiers run from writing one function, to fixing a targeted bug (tier 3), to splitting the code into modules without regressions (tier 5), to implementing a sort with edge cases (tier 6), to adding JSON serialization (tier 7), to debugging an id collision across modules (tier 8). It answers one question: does this model and config do code mode at all? The CLI reports the highest tier passed, a single capability-ceiling number.

**`microcrm`** is scored by the fraction of tests passed rather than pass or fail. The task is to build a CRM REST API using only Node built-ins (`node:http` and `node:sqlite`), graded by 51 spec tests across five tasks. Tier 1 builds the base API from scratch, which is a real test of large output. Tiers 2 to 5 add atomic bulk insert, combined filtering and sorting with pagination, weighted pipeline analytics, and idempotency-key deduplication. It needs Node 22.5 or later.

## The output-limited flag

`CodeAgent` now counts how many times a turn was cut off by the output-token limit. When a task fails after hitting the cap, the report marks it `[output-limited]`. That distinguishes a model that cannot emit a response big enough from one that wrote enough and got it wrong. The first is a configuration or model-choice problem. The second is a capability problem. Measuring them separately is the reason I would use this over a pass rate alone.

## Fixes the first runs exposed

The notes say the first benchmark runs immediately exposed problems that hurt every model and broke the weaker ones outright:

1. **`write_file` and `edit_file` now accept `path` as an alias for `file_path`.** Models often emit `path`. Provider-side validation on Groq and Sarvam rejected those calls with a 400 before they reached the tool, which wasted iterations and tokens.
2. **Schema errors are no longer treated as truncation.** Groq reports both truncated and schema-invalid tool calls as `tool_use_failed`. Jiva used to treat any such error on a file tool as "content too large" and tell the model to write in stages, which was the wrong remedy for a malformed argument. It now inspects the failed generation. A complete, parseable payload is a schema error and gets a targeted correction. Only a genuinely cut-off payload goes down the write-in-stages path.
3. **The Sarvam-105b preset asked for 8192 completion tokens, but the API caps output at 4096.** The preset now uses 4096.
4. **A "continue?" prompt at the step limit.** When code mode runs out of iterations, the interactive CLI now offers to continue with full history or stop, instead of printing `[Max iterations reached without a final response]`. HTTP behavior is unchanged.

## Running it

```bash
# Tiers 1 to 3 against the configured model
jiva benchmark --max-tier 3

# The whole suite, with a JSON report
jiva benchmark --output report.json

# Specific tasks, machine-readable
jiva benchmark --tasks t05-refactor-split,t08-debug-id-collision --json

# See the suites and tasks
jiva benchmark --list
```

The process exits non-zero when any task fails, so it can run in CI. Over HTTP there are `GET /api/benchmark/tasks`, `GET /api/benchmark/suites`, `POST /api/benchmark/run`, and `POST /api/benchmark/run/stream`, which sends per-task progress as server-sent events. All of them sit behind the existing `/api` authentication. The benchmark reuses the model stack you already configured, and the release notes say no config changes are required. Upgrade with `npm install -g jiva-core@0.3.48`.

## Why a team should care

If you pick a model for an agent by trying it on three tasks and going with your gut, you are doing the unscored version of this. A deterministic test with a tamper check is cheap to build and makes the choice repeatable. It also pairs with a habit I argue for in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/): decide what passing means before you look at the output.

The full notes are in the [Jiva repository](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.48). Gritsa builds and runs agents like this for clients: see [AI agent services](/services/ai-agents/).
