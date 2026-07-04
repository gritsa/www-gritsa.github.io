---
layout: post
title: "Jiva v0.3.48: A Benchmark Suite for Code‑Mode AI"
date: 2026-07-04 10:42:38 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, LLM"
excerpt: "Jiva’s latest release adds a deterministic benchmark suite that measures how well models perform in code‑mode, exposing hidden limits and fixing critical tool‑call bugs."
description: "Explore Jiva v0.3.48's new benchmark suite, its impact on code‑mode reliability, and the fixes that make multi‑step coding tasks measurable."
keywords: "Jiva, code‑mode benchmark, autonomous agents, LLM, tool‑call fixes"
featured_image: "/assets/img/posts/2026-07-04-jiva-v0-3-48-a-benchmark-suite-for-code-mode-ai.png"
---

I’ve been watching the code‑mode experiments in Jiva for months. The `--code` flag works beautifully with `gpt-oss-120b`, but the moment you switch to a shorter‑output model like Sarvam‑105b or a rate‑limited service like Krutrim, the results start to wobble. Tasks that need larger writes, multi‑file refactors, or long‑horizon debugging simply fall apart, and we had no objective way to tell *why*.

That changed with **Jiva v0.3.48**, released on June 29, 2026. The update ships a built‑in, TDD‑style benchmark suite that drives a `CodeAgent` through a ladder of coding challenges, scoring each with Node’s native test runner. No external judges, no network calls—just deterministic pass/fail plus rich diagnostics (iterations, tokens, wall‑time, and whether the iteration cap was hit).

### What the suite actually does

The benchmark is organized into two suites:

* **`taskstore`** – a baseline, eight‑tier suite that builds a tiny task‑management library from scratch. Each tier adds a new feature or bug‑fix, and the tests are cumulative, so a refactor that breaks an earlier tier is caught immediately.
* **`microcrm`** – a scored suite that constructs a full‑stack CRM API using only Node built‑ins (`node:http` + `node:sqlite`). It runs 51 spec tests across five tasks, reporting a pass‑rate instead of a binary result.

Both suites are runnable from the CLI (`jiva benchmark`) or via HTTP endpoints (`/api/benchmark/*`). The CLI prints a tidy table, the highest tier passed, and any diagnostic notes. The HTTP API streams progress via Server‑Sent Events, making it easy to embed the benchmark in CI pipelines.

### Why this matters

Before v0.3.48 we were flying blind. A model could appear to “work” on a single‑file script but crumble when asked to split modules, handle edge‑case sorting, or serialize JSON. The new suite surfaces those exact failure points, turning vague “model is weak” feedback into concrete, reproducible data.

The release also ships two critical fixes that the benchmark immediately exposed:

1. **`write_file` / `edit_file` now accept `path` as an alias for `file_path`.** Many models emit the more natural `path` argument; the previous schema rejected it, wasting iterations.
2. **Schema errors are no longer mistaken for output‑token truncation.** The handler now distinguishes a malformed payload from a genuinely cut‑off response, giving the model the right corrective hint.

Additionally, the Sarvam‑105b preset’s token budget was corrected from 8192 to the actual 4096‑token cap, and the CLI now offers a graceful “continue?” prompt when the iteration limit is reached.

### How to try it

```bash
# Run the first three tiers against your current model
jiva benchmark --max-tier 3

# Get a full JSON report for CI
jiva benchmark --output report.json

# Stream progress over HTTP
curl -X POST https://your‑jiva‑host/api/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{"maxTier":5,"suite":"microcrm"}'
```

The benchmark reuses whatever model stack you already have configured—no extra setup required.

### The bigger picture

Having a deterministic, reproducible benchmark for code‑mode is a game‑changer for anyone building autonomous agents that write, refactor, or debug code. It turns “does the model work?” into “how far can the model go before it breaks, and why?” That clarity lets teams make informed decisions about model selection, token budgets, and iteration limits.

For us at Gritsa, this release is a step toward truly reliable AI‑augmented development. When agents can be measured as rigorously as unit tests, we can trust them to handle larger, more complex software tasks without constant human oversight.

If you’re experimenting with code‑mode agents, give the new benchmark a spin. The data you collect will help shape the next wave of autonomous coding tools—tools that don’t just suggest snippets, but actually ship production‑grade features.

---

*Read the full release notes on GitHub: [Jiva v0.3.48 – Code‑Mode Benchmark Suite](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.48).*