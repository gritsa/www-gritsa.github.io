---
layout: post
title: "How to run a coding agent on Sarvam-105B"
date: 2026-10-28 09:00:00 -0400
author: "Amy Loomis"
categories: "AI Agents"
tags:
  - Sarvam-105B
  - Coding agents
  - Open models
  - Jiva
excerpt: "On Sarvam's Starter plan, Sarvam-105B caps output at 4096 tokens. A coding agent that plans around the cap works. One that ignores it writes broken files."
description: "How to run an autonomous coding agent on Sarvam-105B: the output cap, reasoning tokens, rate limits, tool-call quirks, and how Jiva handles each. With setup and a benchmark to verify it."
keywords: "Sarvam-105B coding agent, run coding agent on Sarvam, Sarvam-105B tool calling, open source coding agent, Jiva"
featured_image: "/assets/img/posts/2026-10-28-run-a-coding-agent-on-sarvam-105b.jpg"
---

# How to run a coding agent on Sarvam-105B

You can run an autonomous coding agent on Sarvam-105B if the agent is built around the model's limits. The one that matters most is the output cap: on Sarvam's Starter plan the API stops a reply at 4096 tokens, and part of that budget goes to the model's own reasoning before it writes a word of code. An agent that tries to write a whole file in one call will cut it off halfway and leave a broken file behind.

I read the source and release notes of [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent Gritsa builds on, to see how it deals with this. As far as I know it is the only autonomous agent with first-class coding support that runs with Sarvam-105B. I can't prove a negative, so treat "only" as "the only one I could find." Sarvam has its own coding product, Sarvam Code, in early beta; its launch post says it routes work across 100B, 700B and 3T-scale models and builds on Codex, so it is not a coding agent you can point at Sarvam-105B today. What follows is what I checked, what it does, and where it still hurts.

## Why is Sarvam-105B harder to drive than other models?

Four reasons, and all four bite in the first hour.

**Reasoning eats the output budget.** Sarvam-105B is a reasoning model. It thinks first, in a separate field, and the thinking counts against the same completion limit as the answer. Jiva's own integration notes, written from live testing in March, record what happens without an explicit limit: the reply comes back empty with a finish reason of "length", because the thinking used everything.

**The cap depends on your plan, and Jiva plans for the smallest one.** Sarvam's model page (opened 2026-10-25) lists `max_tokens` limits of 4096 on Starter, 16384 on Pro and 128000 on Business. Jiva's v0.3.48 release notes record that its setup preset had asked for 8192 output tokens and that the API rejected anything above 4096, which matches the Starter limit. The preset was fixed to 4096. If you are on a larger plan, check your own limit before you copy that number; Jiva's default is the safe floor, not the ceiling.

**Tool calls arrive as text.** Jiva's v0.3.44 notes say the model emits tool calls as XML inside the message content rather than in the structured tool-call field. An agent that only looks at the structured field sees a model that never uses its tools.

**The rate limit is low.** Jiva's v0.3.50 notes cite 40 requests per minute. An agent loop that edits, checks and edits again makes a lot of requests.

None of these are flaws to hide. They are the shape of the model, the kind of quirk I wrote about in [where LLM lock-in actually hides](/blog/2026/10/26/llm-lock-in-is-not-where-you-think-it-is/). The question is whether the agent notices.

## How does Jiva handle the output cap?

By never asking for a big write. This is the part I find most interesting, because it is a design choice, not a patch.

When the configured output budget is 8192 tokens or less, Jiva's code mode changes its instructions to the model. Every new file, not just large ones, must be written in two stages. First a skeleton: the file split into named sections, each holding a one-line stub between a `### section-name` marker and a `### endsection` marker. Then one edit per section, using a regex edit that matches the whole section by its markers and swaps in the real code. The model is told its exact token budget in the prompt.

Why markers instead of asking the model to repeat the stub text and replace it? Because at this budget a model's own stub might not come back byte for byte, and an exact-match edit then fails. Matching the markers does not depend on what is between them.

If a write gets cut off anyway, Jiva's v0.3.44 notes say it detects the open tool call, injects a correction telling the model to switch to the skeleton approach, and carries on, instead of printing half a JSON object as the answer.

The price is more steps. Writing one file takes a skeleton plus one call per section. That costs time, and with a 40-request ceiling it costs more time still. I would rather pay in steps than in corrupted files.

## How do I set it up?

Install and run the wizard. Sarvam is the first provider it offers.

```bash
npm install -g jiva-core
jiva setup
```

The wizard fills in the endpoint, the model name and the reasoning strategy, and per the v0.3.50 notes it also sets the 40-per-minute rate limit. The relevant part of the resulting config looks like this:

```json
{
  "models": {
    "reasoning": {
      "endpoint": "https://api.sarvam.ai/v1/chat/completions",
      "apiKey": "your-sarvam-key",
      "model": "sarvam-105b",
      "type": "reasoning",
      "reasoningEffortStrategy": "api_param",
      "defaultMaxTokens": 4096
    }
  }
}
```

Keep `defaultMaxTokens` at 4096. The same release notes record a bug where the command-line client silently dropped that setting, so an old install could be sending no limit at all. If replies come back empty, check your version first.

Then start code mode in a project:

```bash
jiva chat --code
```

Add `--plan` if you want a written plan to approve before anything is changed. The plan gate is the cheapest control you can add to a model you are still learning to trust.

Install a language server for your stack too. After each file edit Jiva tells the language server and appends any compiler errors to the result, so the model sees its own mistake on the next step. With a small output budget, cheap early feedback matters more, not less.

## How do I know it works on my machine?

Run the benchmark. Do not trust a demo.

```bash
jiva benchmark
```

Per the README and the benchmark guide, this runs a baseline suite of eight coding tasks that build on each other, from writing a new function to a multi-file refactor to a cross-module debugging task. Each task runs in a throwaway workspace and is scored by Node's built-in test runner, with no model acting as judge. Every test file is hashed before the agent starts, so an agent that edits a test to make it pass fails with `tests-modified`. A healthy setup passes all eight.

A second suite, `microcrm`, asks the agent to build a small REST API on SQLite and then add harder features, and scores the share of 51 spec tests it passes. When a task fails because the model ran out of output tokens, the report marks it `[output-limited]`, which separates "the model reasoned badly" from "the cap got in the way."

I have not run these suites and I'm not going to quote scores I did not produce. The useful thing is that the check exists and fits in CI, because the process exits non-zero when a task fails. This is the same idea as [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/): decide how you will score it before you rely on it.

## What are the limits?

Plenty, and they are the honest part of the answer.

**A 4096-token cap is a ceiling on single outputs.** Jiva's README says tasks needing a larger single output are limited by it, and a higher plan limit raises that ceiling without changing the habit of writing in sections. Sectioned edits get around the file size problem. They don't help if one function genuinely needs more than 4096 tokens of code.

**Slower by construction.** More calls per file, a rate limit, and a reasoning model that thinks before every call. Expect a patient tool, not a fast one.

**A passing benchmark is not parity.** I am not claiming Sarvam-105B matches a frontier model on hard engineering. I have no evidence either way and the repo does not claim it. The case for it is different: an open model you can point at your own infrastructure or at an Indian provider, driven by an agent that knows its limits.

**This is a snapshot.** I read Jiva at version 0.3.53 and the integration notes from March. The Sarvam limits could change. Check their docs before you plan around any number here.

## Where does this leave you?

If you want a coding agent on Sarvam-105B, the tool has to be built for the cap from the start. Bolting a long-output agent onto a short-output model is how you get half-written files and a bill. Jiva is built for it, which is why it is where Gritsa starts. If you want help putting an agent like this into production on your own code and data, that's what [our AI agents work](/services/ai-agents/) is for.
