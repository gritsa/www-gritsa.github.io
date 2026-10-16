---
layout: post
title: "Jiva v0.3.47: Multimodal Fixes and Vertex AI Enhancements"
date: 2026-05-31 06:31:35 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, Jiva"
excerpt: "Jiva v0.3.47 fixes four bugs that broke image analysis, tool calls on Vertex AI and the final answer format, and adds Google Application Default Credentials."
description: "What changed in Jiva v0.3.47: the Groq empty-content error on image tools, Vertex AI tool-call parsing, JSON leaking into the final answer, a CLI model field bug, Google ADC and a higher sub-agent iteration limit."
keywords: "Jiva, autonomous agents, multimodal AI, Vertex AI, Google ADC, open-source AI"
featured_image: "/assets/img/posts/2026-05-31-jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements.png"
---

Updated 2026-10-16: rewritten from the v0.3.47 release notes. The original post repeated the changelog with marketing language.

Jiva v0.3.47 was released on May 19, 2026. It is mostly bug fixes, and three of the four fixes share a cause: one part of the system handed the model something it was not meant to see, or took something away that it needed. The release also adds one feature that matters if you run on Google Cloud, which is Application Default Credentials.

## The four fixes

**1. Image tools failed with a 400 from Groq.** Tools such as `filesystem__read_media_file` return an empty text body plus the image bytes. The worker stored that empty string as the tool message, and Groq rejects any message with no content (`String should have at least 1 character`). The worker retried up to 20 times and failed each time. Now, when a tool returns images with no text, the content falls back to `[Image content returned]`, and the image still reaches the multimodal model through the same path as before.

**2. The final answer came back as raw JSON.** The manager's synthesis step reused the whole planning conversation, and that history contained the instruction "Respond ONLY with valid JSON" from the planning phase. The model obeyed it. Synthesis now starts from a fresh context made of the system messages and the synthesis prompt only. If the model still returns JSON, the code pulls out the `response` or `content` field.

**3. Tool calls broke from the second turn on Vertex AI.** Two causes. First, the worker stored the cleaned assistant message (Harmony tokens stripped) in history, but Harmony models need to see their own markers such as `<|call|>` and `<|channel|>` to connect a call to its result. History now keeps the raw content. Second, Vertex AI MaaS uses a different dialect (`<|channel|>commentary to=TOOL_NAME <|constrain|>json<|message|>JSON_ARGS<|call|>`) that was not parsed, so its tool calls were silently dropped. A new parser in `src/models/harmony.ts` handles it and strips the `functions.` prefix so names match the registered tool.

**4. The `model` config field was ignored in the CLI.** An entry using `model` instead of `defaultModel` passed `undefined` to the client, which fell back to its default model. The CLI now uses `model || defaultModel`.

## Google Application Default Credentials

A new module, `src/models/google-adc.ts`, fetches short-lived OAuth2 tokens so a Vertex AI MaaS deployment on Cloud Run no longer needs a static API key. It tries the GCP metadata server first, by IP address because musl libc (the node:20-alpine image) cannot resolve `metadata.google.internal`, and falls back to `google-auth-library` for local development. Tokens are cached and refreshed five minutes before expiry. Turn it on in the model entry:

```json
{
  "models": {
    "reasoning": {
      "endpoint": "https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/endpoints/{ENDPOINT_ID}/chat/completions",
      "useGoogleADC": true,
      "useHarmonyFormat": true,
      "model": "gpt-oss-120b-maas"
    }
  }
}
```

With `useGoogleADC` on, `apiKey` is optional.

## One more change

The default `maxIterations` for sub-agents started through `AgentSpawner` went from 10 to 20, so longer tool-use loops such as multi-file edits no longer stop at the old limit.

## Upgrade

```bash
npm install -g jiva-core@0.3.47
```

The release notes list no breaking changes. Existing configs keep working. The source is on [GitHub](https://github.com/KarmaloopAI/Jiva).

The second fix has its own short write-up: [why a planning instruction can leak into the final answer](/blog/2026/05/19/jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements/). For how Jiva separates planning from execution, see [Agent design patterns: the one that matters is what the model does not do](/blog/2026/05/26/agentic-ai-design-patterns-2026-architecting-autonomous-systems/).
