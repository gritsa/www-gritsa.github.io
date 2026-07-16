---
layout: post
title: "Jiva v0.3.50: Unified Config, Vision & Code-Mode Boost"
date: 2026-07-16 20:33:04 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, LLM"
excerpt: "Jiva's latest release brings proactive rate limiting, vision detection, and smarter code-mode scaffolding."
description: "Explore Jiva v0.3.50's unified configuration, vision-capable model auto-detection, and skeleton-first workflow for low-output-budget models."
keywords: "Jiva, autonomous agents, LLM, vision detection, code-mode, rate limiting"
featured_image: "/assets/img/posts/2026-07-17-jiva-v0-3-50-unified-config-vision-code-mode-boost.png"
---

I’ve been watching the agentic AI space evolve, and the latest Jiva release feels like a quiet but powerful step forward. It’s not a flashy headline‑grabbing feature, but the changes underneath the hood make a real difference for anyone building production‑grade autonomous agents.

### Proactive rate limiting that actually works

Many of us have hit the dreaded 429 “Too Many Requests” wall when scaling agents against providers with strict caps—Sarvam‑105B, for example, caps at 40 requests per minute. Jiva v0.3.50 now tracks request timestamps in a rolling 60‑second window and **waits before sending** a request that would breach the limit, rather than reacting after the fact. It also respects the standard `Retry‑After` header and falls back to parsing provider‑specific messages when needed. The result? Fewer retries, smoother pipelines, and less surprise throttling in production.

### Vision detection baked into setup

Vision‑capable models have been proliferating—Llama 4 Maverick, Qwen, Kimi, Claude, GPT‑4+, Gemini, Pixtral, and more. Previously you had to edit `config.json` manually to tell Jiva a model could see images. The new `detectVisionCapability()` utility matches model names against a curated list and surfaces a clear reason (“Llama 4 Maverick supports vision”). During the CLI setup wizard you’re now asked “Does this model support vision?” and the answer is pre‑filled with the detection result, but still overridable. This tiny UX tweak removes a whole class of configuration errors.

### Skeleton‑first workflow for low‑output‑budget models

When a reasoning model’s `defaultMaxTokens` is ≤ 8192, code mode now **mandates** scaffolding every new file as `### section‑<name>` / `### endsection` blocks and filling them one at a time. The system prompt explicitly tells the model its token budget, preventing it from over‑committing and running out of space mid‑thought. The new `use_regex` mode for `edit_file` makes replacing whole sections reliable, even when the stub content changes.

### Unified configuration across CLI and HTTP

Previously the CLI and the local HTTP interface read/wrote different config files, leading to silent drift. Jiva now pins both to `~/.jiva/config.json`. A one‑time migration copies any legacy platform‑specific config into the new location, backing up the old file if something already exists. After this release, a single `jiva config --show` reflects the exact same settings whether you’re using the CLI or the HTTP API.

### Richer conversation metadata

`ConversationMetadata` now includes `mcpServers`, `maxIterations`, and a free‑form `harness` field. When you run a code task, Jiva records which MCP servers were enabled, the iteration budget you set, and the harness (e.g., `evaluator`). This metadata survives auto‑saves, giving you a clearer audit trail for debugging complex agent runs.

### Bug fixes that matter

- **Manager double system‑message crashes** – Fixed a bug where a directive was appended as a second system message, breaking strict providers like Qwen3.6.
- **CodeAgent empty‑response loop** – Added `finishReason` handling and forced compaction when the model runs out of tokens mid‑thought.
- **CLI config drop** – `defaultMaxTokens` and `reasoningEffortStrategy` are now correctly passed through all four CLI entry points.
- **Conversation titles** – Stripped thinking blocks, raised token budget, and set low reasoning effort, yielding clean, LLM‑generated titles.

### What this means for you

If you’re running agents on providers with tight rate limits, you’ll see fewer throttling hiccups. If you rely on vision‑enabled models, the setup wizard now guides you instead of leaving you to edit JSON by hand. And for code‑generation tasks with constrained token budgets, the skeleton‑first approach should dramatically reduce “out‑of‑tokens” failures.

All of this lands in a single, non‑breaking upgrade:

```bash
npm install -g jiva-core@0.3.50
```

Existing configurations continue to work unchanged, and the migration script ensures a smooth transition.

I’m excited to see how the community puts these improvements to work. The agentic AI landscape is moving fast, and Jiva keeps delivering the kind of pragmatic upgrades that let us focus on building, not on fighting the framework.

If you haven’t tried the new release yet, give it a spin and let us know how it changes your workflow.

---

*Read the full release notes on GitHub: [Jiva v0.3.50](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.50).*

*Gritsa Technologies builds autonomous AI agents with Jiva – open‑source, production‑ready, and constantly improving.*