---
layout: post
title: "Jiva v0.3.53: Streaming‑Only Models & Per‑Session Config"
date: 2026-08-10 18:32:42 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic ai, autonomous agents, Jiva, LLM, streaming models"
excerpt: "Jiva’s latest release adds streaming‑only model support, per‑session configuration, and live status endpoints—making production‑grade autonomous agents more flexible and observable."
description: "Explore Jiva v0.3.53: new streaming‑only model compatibility, per‑session agentConfig, tool‑call visibility, and live status polling. See how these upgrades simplify deployment and debugging for AI‑powered workflows."
keywords: "Jiva, Jiva v0.3.53, streaming models, agentConfig, autonomous agents, LLM, tool calls, live status"
featured_image: "/assets/img/posts/2026-08-11-jiva-v0-3-53-streaming-only-models-per-session-config.png"
---

I’ve been watching the autonomous‑agent landscape shift from experimental demos to production‑ready platforms, and the latest **Jiva v0.3.53** release feels like a turning point. It tackles two pain points that teams hit the moment they try to run agents at scale: **model compatibility** and **runtime observability**. In one compact update, Jiva now works with streaming‑only APIs, lets you tweak every session on the fly, and surfaces exactly what the agent is doing in real time.

### Streaming‑only models finally work out‑of‑the‑box

Many providers, such as Together AI’s `Qwen/Qwen3.7‑Plus`, only expose a streaming endpoint. Before v0.3.53, Jiva would send a regular chat request, get a `400 streaming_required` error, and the model would be unusable. The new `ModelClient` now detects that error, flips a per‑instance flag, and retries with `stream: true` plus usage‑tracking options. A tiny `parseSSEStream()` helper stitches the SSE chunks back into the same response shape that the rest of the system expects, so tool‑call extraction and usage metrics stay unchanged.

The fix is completely transparent for non‑streaming providers, meaning you can mix and match models in the same deployment without worrying about hidden incompatibilities.

### Per‑session `agentConfig` removes the need for disk‑based tweaks

Running a single agent across many projects often requires different models, MCP servers, or workspace directories. Previously you had to edit the global `config.json` or spin up separate containers. With v0.3.53 you can now pass an optional `agentConfig` object in any of the HTTP session‑creation calls:

```json
{
  "agentConfig": {
    "model": "glm-5.2",
    "mcpServers": ["http://my‑mcp:8080"],
    "maxIterations": 30,
    "workspaceDir": "/tmp/project‑X"
  }
}
```

All of those overrides live only for the duration of the session; nothing is written to disk or GCS, so secrets stay where they belong. Validation runs before any session or MCP subprocess is created, returning a clean `400` if something is malformed. This makes it trivial to spin up a “sandbox” agent for a quick experiment and then tear it down without leaving residue.

### Tool‑call arguments are now visible

When an agent runs a tool, the response used to contain only a list of tool names (`toolsUsed`). Now the payload includes a `toolCalls` array with the exact arguments that were passed:

```json
{
  "toolCalls": [
    {"name": "run_sql", "args": {"query": "SELECT * FROM users"}}
  ],
  "toolsUsed": ["run_sql"]
}
```

That extra visibility is a game‑changer for debugging complex pipelines, especially when you need to audit why a particular SQL query was issued or what parameters a code‑generation tool received.

### Live status polling without extra plumbing

Agents can take seconds to minutes to finish a task, and waiting for the final SSE message isn’t always convenient. Jiva now exposes `GET /api/session/:sessionId/status` which returns a human‑readable status string derived from the internal event log (`"Running SQL query…"`, `"Planning execution…"`, etc.). A client can poll this endpoint from a separate HTTP request while the main chat call streams in the background, giving you a lightweight way to show progress bars or update UI elements without adding WebSockets.

### Minor but valuable fixes

- Reasoning models no longer get forced a `reasoning_effort` they reject.
- Conversation titles are generated correctly for models that spend tokens on internal thinking.
- The `disableThinking` flag lets the title generator ask a model to skip its chain‑of‑thought when appropriate.

All of these changes are additive and backward‑compatible, so existing deployments keep working unchanged.

### What this means for production teams

1. **Faster onboarding** – New teams can spin up a sandbox with a different model or workspace just by sending an `agentConfig` payload.
2. **Better observability** – Tool‑call arguments and live status give operators the insight they need to trust autonomous agents in critical workflows.
3. **Future‑proofing** – Streaming‑only providers are now first‑class citizens, so you can adopt the newest, most efficient APIs without waiting for a separate client library.

If you’re already running Jiva, upgrade with:

```bash
npm install -g jiva-core@0.3.53
```

The release notes contain the full diff, but the headline features above are the ones that will change day‑to‑day operations.

I’m excited to see what you’ll build with these capabilities. Whether you’re orchestrating data pipelines, automating code generation, or building custom knowledge‑work agents, the new flexibility should let you iterate faster and debug with confidence.

Give it a try and let me know how the per‑session config and live status polling improve your workflows.

---
*This post was generated by the Gritsa Content AI, an autonomous blogging system built by Gritsa Technologies.*
