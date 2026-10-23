---
layout: post
title: "Jiva v0.3.53: Streaming-Only Models and Per-Session Config"
date: 2026-08-10 18:32:42 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, Jiva, LLM, streaming models"
excerpt: "Jiva v0.3.53 lets a request override the model, MCP servers and workspace for one session without writing anything to disk, shows the arguments of every tool call, and adds a status endpoint for polling progress."
description: "What changed in Jiva v0.3.53: streaming-only model support, per-session agentConfig that never touches disk, toolCalls arguments in chat responses, the live session status endpoint, and fixes for empty titles and Windows console windows."
keywords: "Jiva, agentConfig, per-session configuration, streaming models, tool call audit, session status, AI agent framework"
featured_image: "/assets/img/posts/2026-08-11-jiva-v0-3-53-streaming-only-models-per-session-config.jpg"
---

Updated 2026-10-16: rewritten from the v0.3.53 release notes. The original was a tour of features in marketing language, and it carried a sample config the notes do not document.

Jiva v0.3.53 was released on August 5, 2026. All of it is additive and backward compatible, and the notes say sessions that omit the new fields behave exactly as before. The theme running through it is that a session should be able to carry its own settings, and an operator should be able to see what the agent is doing while it does it.

## Per-session `agentConfig`

Before this release, running one Jiva server for several projects meant editing the stored configuration or starting separate containers. Now `POST /api/session`, `POST /api/chat` and `POST /api/chat/stream` accept an optional `agentConfig` object that overrides settings for that session only:

- `model` and `toolCallingModel`, the reasoning and tool-calling model names
- `mcpServers`, which replaces the MCP server list for the session
- `codeModeEnabled` and `codeLsp`
- `maxIterations`, the per-agent iteration cap
- `workspaceDir`, a session-scoped workspace
- `systemPrompt`, accepted but reserved for future use

The design choice that matters is what does not happen. Per-session config is never written through the storage provider, so secrets in it never touch disk or Google Cloud Storage. Validation runs before any session or MCP subprocess is created and returns a 400 with descriptive errors. For the streaming route it runs before the server-sent-event headers go out, so a bad config gets a clean JSON error instead of a failure halfway through a stream. If you send `agentConfig` for a session that already exists or is being created, it is logged and ignored: the existing session's config wins.

The notes also add a per-session skills directory. When `workspaceDir` is set, `${workspaceDir}/skills` is scanned alongside the user-level skills folder, and a missing folder is not an error.

This is the multi-tenant lesson from [v0.3.46](/blog/2026/05/20/jiva-v0-3-46-fixes-multi-tenant-concurrency-bugs/) applied to configuration: state that belongs to one session should live with that session.

## Tool-call arguments in the response

The chat response used to list only the names of the tools the agent used, in `toolsUsed`. It now also returns `toolCalls`, an array of objects with the tool `name` and its `args`. The notes give the example of seeing the actual SQL query a tool ran, not just that a SQL tool ran. `toolsUsed` is unchanged. The field is filled by the worker and passed up through the dual-agent, and it is not populated in code mode.

If you are asked to explain why an agent did something, the arguments are the evidence. A list of tool names is not.

## Live session status

`OrchestrationLogger` now keeps a `currentStatus` string, derived from the structured events it already writes. Examples in the notes are "Running SQL query…", "Planning execution…" and "Synthesizing results…". `GET /api/session/:sessionId/status` returns `200` with `{ status }` if the session exists and `404` with `{ error: 'Session not found' }` otherwise, which the notes call an expected outcome of polling, not an error. A client can poll it from a second request while `POST /api/chat` is in flight, with no WebSocket or event-stream plumbing.

## Streaming-only models

Some providers only accept streaming requests. The notes name Together AI's `Qwen/Qwen3.7-Plus`. Jiva used to send a normal request and get `400 streaming_required` on every call. `ModelClient` now detects that error, flips a flag on the instance and retries with `stream: true` and usage reporting on. A new `parseSSEStream()` reassembles the stream into the same shape as a normal response, so tool-call extraction and usage tracking are unchanged. Providers that support normal requests are not affected.

## Smaller fixes

- **A forced `reasoning_effort`.** `createSession` always passed `medium` when building the tool-calling model client, and plain tool-calling models such as Groq's `llama-3.3-70b-versatile` rejected it with a 400. The catalog value is now passed through as is, so non-reasoning models send nothing.
- **Empty conversation titles.** Title generation had a hard-coded 200-token limit. Reasoning models such as GLM-5.2, DeepSeek, Qwen3, gpt-oss and Sarvam spend tokens on thinking first, so the budget could be gone before the title appeared. A new `disableThinking` option sends both flags the model families read (`thinking: false` and `enable_thinking: false`), models that cannot turn thinking off get `reasoningEffort: 'low'`, and the hard-coded limit is gone in favor of each model's configured default. This is the same family of bug as the one in the [v0.3.50 token-budget post](/blog/2026/07/16/jiva-v0-3-50-unified-config-vision-code-mode-boost/).
- **Console windows on Windows.** Code mode's `bash` tool and the LSP launcher never set `windowsHide`, so every command flashed a console window. Both now set it, and it does nothing on macOS or Linux.

The notes also mention that `compactionThreshold` can now be edited through `jiva config --compaction-threshold` and applies to both chat and code modes, with a suggestion to set it to roughly 70 to 80 percent of the model's context length.

## Upgrade

```bash
npm install -g jiva-core@0.3.53
```

No breaking changes. Source and notes are in the [Jiva repository](https://github.com/KarmaloopAI/Jiva). If you want help running agents with this kind of per-session control and an audit trail, see Gritsa's [AI agent services](/services/ai-agents/).
