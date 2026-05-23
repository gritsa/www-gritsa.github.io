---
layout: post
title: "Jiva v0.3.47: Multimodal Fixes and Vertex AI Enhancements"
date: 2026-05-19 00:00:00 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, multimodal, Vertex AI, Google ADC, Jiva"
excerpt: "Jiva 0.3.47 resolves multimodal image bugs, fixes Harmony tool calls on Vertex AI, and adds Google ADC support for seamless Cloud Run deployments."
description: "Discover how Jiva 0.3.47 resolves multimodal image bugs, fixes Harmony tool calls on Vertex AI, and adds Google ADC support for seamless Cloud Run deployments."
keywords: "Jiva 0.3.47, multimodal AI, Vertex AI, Google ADC, autonomous agents, LLM orchestration"
featured_image: "/assets/img/posts/2026-05-19-jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements.png"
---

## Introduction

The AI landscape moves at breakneck speed, and staying ahead means constantly polishing the underlying tooling. Today we’re excited to ship **Jiva 0.3.47**, a focused release that eliminates critical bugs in multimodal image handling, restores reliable tool‑call sequences on Vertex AI MaaS, and introduces **Google Application Default Credentials (ADC)** support—making Cloud Run deployments frictionless.

## What’s New in 0.3.47

### 1. Robust Multimodal Image Analysis

Previously, image‑analysis requests via `filesystem__read_media_file` triggered a cascade of 400 errors from the Groq API. The root cause was an empty `text` field in the tool result. Jiva now falls back to a descriptive placeholder (`"[Image content returned]"`) whenever a tool returns images without accompanying text, keeping the conversation flowing without breaking the model.

### 2. Fixed Harmony Tool‑Call Sequences on Vertex AI

Vertex AI MaaS uses a distinct Harmony dialect for tool calls. Earlier releases dropped these calls, causing endless loops. The update adds a **Vertex AI dialect parser** and ensures the raw Harmony tokens are retained in conversation history, so the model can correctly correlate a tool call with its result.

### 3. Cleaner Manager Synthesis

The Manager’s final reply was sometimes emitted as raw JSON because the synthesis prompt unintentionally included a “Respond ONLY with valid JSON” instruction from earlier planning steps. By isolating synthesis to a fresh context, the output is now plain, readable text with a safety fallback that extracts JSON if it slips through.

### 4. Model Field Support in CLI

A small but annoying bug prevented the newer `model` field from being used in CLI configurations, forcing the CLI to fall back to the default model. The fix now respects `model || defaultModel`, aligning the CLI with the latest config schema.

## New Features

### Google Application Default Credentials (ADC)

Running Jiva on Cloud Run previously required a static API key for Vertex AI. With **Google ADC**, Jiva automatically fetches short‑lived OAuth2 tokens from the GCP metadata server (or the `google-auth-library` when you’re developing locally). Simply set `useGoogleADC: true` in your model configuration:

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

No more hard‑coded keys, and token caching keeps the overhead to a single metadata call per hour.

### Increased Sub‑Agent Iteration Limit

Tasks that need back‑and‑forth tool usage (e.g., multi‑file edits, research loops) now benefit from a higher default `maxIterations` (20 instead of 10). This reduces premature termination for complex workflows.

## Impact for Developers

- **Reliability:** Image‑analysis and tool‑call bugs are gone, so production pipelines that rely on multimodal inputs can run without manual workarounds.
- **Security:** ADC eliminates the need to store long‑lived API keys in environment variables, aligning with best‑practice secret management.
- **Developer Experience:** The CLI now respects the modern `model` field, and the higher iteration ceiling means fewer “max‑iterations reached” errors during debugging.

## Conclusion

Jiva 0.3.47 is a concise but powerful update that tightens the core engine, adds essential cloud‑native credentials support, and expands the capabilities of autonomous agents. Whether you’re orchestrating multimodal workflows or scaling on Cloud Run, this release gives you the stability and security you need to ship AI‑driven products faster.

Explore the full release notes on GitHub and try it out today:

- [Jiva GitHub repository](https://github.com/KarmaloopAI/Jiva)
- [Documentation & guides](https://www.gritsa.com)

---

*Stay tuned for more advances in agentic AI. Follow us at [Gritsa Technologies](/) to keep up with the latest. Interested in deploying [autonomous AI agents](/services/ai-agents/) for your business? [Get in touch](/contact/).*