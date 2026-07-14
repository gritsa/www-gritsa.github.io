---
layout: post
title: "Jiva v0.3.50: Unified Config, Vision & Code Mode"
date: 2026-07-14 18:32:12 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, LLM"
excerpt: "Jiva v0.3.50 brings unified configuration, native vision support, and smarter code‑mode scaffolding for constrained models."
description: "Discover the new Jiva v0.3.50 release: unified config across CLI and HTTP, auto‑detect vision models, proactive rate limiting, and skeleton‑first code generation for low‑budget LLMs."
keywords: "Jiva, autonomous agents, LLM, vision, code mode, rate limiting, configuration, open source"
featured_image: "/assets/img/posts/2026-07-15-jiva-v0-3-50-unified-config-vision-code-mode.png"
---

I’ve been watching the Jiva repo closely, and the latest release feels like a quiet but powerful upgrade. It’s not a flashy headline‑grabber, but it solves the friction points that show up when you try to run autonomous agents at scale.

### One config to rule them all

Previously the CLI and the local HTTP interface kept their own separate configuration files. That meant a change made in the CLI could silently disappear when you switched to the HTTP mode, and vice‑versa. v0.3.50 unifies the storage location to `~/.jiva/config.json`. The migration script copies any legacy platform‑specific file the first time the new manager starts, and it backs up anything unexpected before overwriting. Now the same JSON powers both entry points, so you can edit it once and have it apply everywhere.

### Proactive rate limiting

Many providers impose hard caps—Sarvam‑105B, for example, caps at 40 requests per minute. Earlier versions only reacted to 429 errors, which meant a burst could still hit the limit and cause failures. The new `maxRequestsPerMinute` field makes the client track its own request timestamps in a rolling 60‑second window and pause before sending a request that would exceed the ceiling. It also respects the standard `Retry‑After` header, falling back to provider‑specific wording only when needed. The Sarvam preset now sets this to 40 automatically, so you get safe defaults out of the box.

### Vision detection without extra wiring

Vision‑capable models have been supported under the hood for a while, but you had to flip a flag manually. v0.3.50 adds a small utility that matches model names against known vision families—Llama 4 Maverick/Scout, Qwen, Kimi, GLM, Claude, GPT‑4+, Gemini, Pixtral, Grok, Phi‑multimodal, and more. During setup the wizard now asks “Does this model support vision?” and shows the matched reason. The flag lives in the unified config, so both CLI and HTTP see it instantly. When `hasVision` is true, the orchestrator routes images directly to that model instead of routing them through a separate multimodal caption step.

### Skeleton‑first code generation for low‑budget models

When a reasoning model’s `defaultMaxTokens` is ≤ 8192, the system prompt now mandates a skeleton‑first workflow. Every new file is created with `### section‑<name>` / `### endsection` blocks, and the model fills them one at a time. This keeps the token budget predictable and prevents the model from overshooting its limit. The `edit_file` tool gained a `use_regex` mode, so a whole section can be replaced by matching its markers without reproducing the current stub content.

### Richer conversation metadata

The `ConversationMetadata` type now includes optional fields for `mcpServers`, `maxIterations`, and a free‑form `harness`. When you run a code task, the agent records which MCP servers were enabled, the iteration budget you set, and the harness (e.g., `jiva-core` evaluator or a UI feature like “deep‑run”). Those values survive across auto‑saves, giving you a clearer audit trail of what the agent was allowed to do.

### Bug fixes that matter

- **Manager double system‑message crashes** – Some strict providers reject more than one system message. The directive is now merged into the single system message, eliminating the 400 error.
- **CodeAgent giving up early** – Empty responses used to trigger a retry cap that stopped the agent after four tries, even when `maxIterations` was high. The fix removes the tool‑call requirement for in‑loop compaction and adds a `finishReason` check that forces compaction when the model runs out of tokens mid‑thought.
- **CLI dropping `defaultMaxTokens`** – The CLI now forwards the `defaultMaxTokens` and `reasoningEffortStrategy` fields from the config, so Sarvam‑105B respects its intended token ceiling.
- **Conversation titles leaking thinking** – The title generation now strips any `` thinking blocks, raises the token budget from 20 to 200, and sets `reasoningEffort: 'low'`. The result is a clean, LLM‑generated title instead of a snippet of the first user message.

### How to upgrade

```bash
npm install -g jiva-core@0.3.50
```

No breaking changes. Existing configurations continue to work, and the migration script will bring any legacy files into the new unified location automatically.

---

What excites me most is the combination of proactive rate limiting and native vision support. It means you can spin up a multi‑agent pipeline that ingests images, reasons about them, and writes code—all without hitting hidden provider caps or manually wiring vision flags. The skeleton‑first code mode also feels like a practical safeguard for teams that need to keep token usage predictable.

If you’re already running Jiva, give the upgrade a try and let me know how the new config feels in your workflow. For those just starting, the unified config and vision detection lower the barrier to building truly autonomous agents that can see, think, and code.

*Check out the full release notes on GitHub:* [Jiva v0.3.50 release](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.50)

---

*Gritsa Technologies* is building the future of autonomous AI. Our open‑source framework, **Jiva**, lets you orchestrate LLM‑powered agents with confidence. Visit [Gritsa Technologies](https://www.gritsa.com) to learn more.