---
layout: post
title: "Jiva v0.3.47: Multimodal Fixes and Vertex AI Enhancements"
date: 2026-05-19 12:00:00 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, multimodal, Vertex AI, Google ADC, Jiva"
excerpt: "Jiva v0.3.47 resolves multimodal image bugs, fixes Harmony tool calls on Vertex AI, and adds Google ADC support for seamless deployment."
description: "Explore the latest Jiva release, its bug fixes for multimodal image analysis, improved Harmony tool-call handling on Vertex AI, and new Google Application Default Credentials support."
keywords: "Jiva, multimodal, Vertex AI, Google ADC, agentic AI, autonomous agents, LLM, Jiva release"
featured_image: "/assets/img/posts/2026-05-20-jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements.png"
---

## Introduction

The AI landscape is moving fast, and production teams need frameworks that keep pace. Today, we’re excited to announce **Jiva v0.3.47**, a release packed with critical fixes and new capabilities that make autonomous agents more reliable and easier to deploy on Google Cloud. This update tackles long‑standing bugs in multimodal image handling, restores proper Harmony tool‑call sequences on Vertex AI MaaS, and introduces **Google Application Default Credentials (ADC)** so you no longer need static API keys when running on Cloud Run.

---

## 1. Multimodal Image Bugs Fixed

### The Problem
Previously, asking a Jiva agent to analyse an image (e.g., via `filesystem__read_media_file`) would trigger a cascade of 400 errors from the underlying Groq API:

```
body.messages.5.tool.content : String should have at least 1 character
```

The Worker would retry up to 20 times and ultimately fail. The root cause was that the tool returned an empty `text` field alongside image data, and the Worker stored that empty string as the tool result, violating Groq’s requirement that every message contain at least one character.

### The Fix
In `src/core/worker-agent.ts` we added a fallback: when a tool returns images but no accompanying text, `toolResultText` now defaults to `'[Image content returned]'`. The image itself is still passed to the multimodal model via the existing `pendingImages` pipeline, so the analysis proceeds without error.

### Why It Matters
Multimodal agents are increasingly used for visual QA, document parsing, and content moderation. A single API error can halt an entire pipeline. By guaranteeing that every tool result contains a non‑empty string, Jiva now delivers **stable, production‑grade image analysis** out of the box.

---

## 2. Harmony Tool‑Call Sequences on Vertex AI MaaS

### The Problem
When using the Harmony format for tool calls, Jiva’s second‑turn tool invocations on Vertex AI MaaS would either be ignored or repeat endlessly. Two issues caused this:

1. **History format mismatch** – the Worker stored only the cleaned `response.content`, stripping the raw Harmony tokens (`<|call|>`, `<|return|>`, `<|channel|>`). Vertex AI expects those tokens to remain in the conversation history.
2. **Vertex AI dialect** – the platform emits tool calls using a slightly different Harmony dialect (`<|channel|>commentary to=TOOL_NAME <|constrain|>json<|message|>JSON_ARGS<|call|>`) that the existing parser didn’t understand.

### The Fix
* **Raw token preservation** – `ModelResponse` now includes a `rawHarmonyContent` field. When `useHarmonyFormat` is true, the Worker stores this raw string as the assistant message, preserving the necessary tokens.
* **Dialect parser** – added `vertexChannelRegex` in `src/models/harmony.ts` to correctly extract tool names and arguments from Vertex AI’s dialect, stripping the `functions.` prefix so they map to registered MCP tools.
* **Robust extraction** – `extractAssistantMessage()` now cleans both Krutrim and Vertex AI Harmony tokens from visible content and gracefully handles malformed `<|return|>` tags.

### Why It Matters
Harmony is the lingua franca for many LLM providers, and Vertex AI MaaS is a popular backend for large‑scale deployments. Restoring proper tool‑call sequences means **agents can now orchestrate multi‑step workflows** (e.g., fetch data, run analysis, and produce a report) without dead‑locking.

---

## 3. Manager Final Response Formatting

### The Problem
After completing a task, the Manager agent would sometimes return raw JSON instead of a human‑readable markdown answer, breaking downstream UI components that expect plain text.

### The Fix
The synthesis step now uses a **fresh context** containing only the system messages and the synthesis prompt, excluding the planning history that mistakenly contained a “Respond ONLY with valid JSON” instruction. A safety fallback also extracts the `response`/`content` field if the model still returns JSON.

### Why It Matters
Consistent output formatting is essential for **integrating agents into existing chat UIs or automation pipelines**. This fix eliminates surprise JSON payloads and keeps the user experience smooth.

---

## 4. Google Application Default Credentials (ADC) for Vertex AI MaaS

### The Problem
Deploying Jiva on Cloud Run or GKE required embedding a static API key in the model configuration, which is a security risk and complicates rotation.

### The Solution
A new module, `src/models/google-adc.ts`, automatically fetches short‑lived OAuth2 tokens from the GCP metadata server or via the `google-auth-library`. Tokens are cached and refreshed five minutes before expiry, limiting outbound calls to at most one per hour.

**Configuration example**

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

When `useGoogleADC` is true, the `apiKey` field is ignored, removing the need for manual key management.

### Why It Matters
**Zero‑trust deployment** becomes trivial. Teams can spin up Jiva agents on any GCP service that supports ADC (Cloud Run, GCE, GKE) without handling secrets, dramatically simplifying CI/CD pipelines and reducing the attack surface.

---

## 5. Sub‑Agent Iteration Limit Increased

The default `maxIterations` for sub‑agents spawned via `AgentSpawner` has been raised from **10 to 20**. Tasks that require many back‑and‑forth tool calls—such as multi‑file refactors or deep research—no longer hit the iteration wall prematurely.

---

## 6. CLI and Configuration Improvements

* The CLI now respects the newer `model` field (fallback to `defaultModel` if missing) when constructing model clients.
* Validation messages have been clarified, making troubleshooting faster.
* Dockerfile now includes `bash`, required by the `@mkusaka/mcp-shell-server` dependency.
* `cloud-run-deploy.yaml` updated the storage provider to the canonical `gcp-bucket`.

---

## 7. How to Upgrade

```bash
npm install -g jiva-core@0.3.47
```

No breaking changes. Existing configurations continue to work unchanged, and you can start using the new features immediately.

---

## Conclusion

Jiva v0.3.47 is more than a patch release—it’s a **stability and usability milestone** for anyone building production‑grade autonomous agents. By fixing multimodal image bugs, restoring Harmony tool‑call sequences on Vertex AI, delivering zero‑trust Google ADC support, and expanding iteration limits, we’re giving developers the confidence to ship AI‑driven workflows at scale.

If you’re ready to see these improvements in action, check out the [Jiva GitHub repo](https://github.com/KarmaloopAI/Jiva) and start building smarter, faster, and safer agents today.

---

*Stay tuned for more updates from Gritsa Technologies, where we turn cutting‑edge research into practical tools for the AI community.*