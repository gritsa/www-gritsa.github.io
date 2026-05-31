---
layout: post
title: "Jiva v0.3.47: Multimodal Fixes and Vertex AI Enhancements"
date: 2026-05-31 06:31:35 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, Jiva"
excerpt: "New Jiva release resolves multimodal bugs, adds Google ADC support, and boosts sub‑agent iteration limits."
description: "Jiva v0.3.47 delivers critical multimodal image handling fixes, Harmony tool‑call support for Vertex AI, Google Application Default Credentials, and higher sub‑agent iteration limits for production AI teams."
keywords: "Jiva, autonomous agents, multimodal AI, Vertex AI, Google ADC, open-source AI"
featured_image: "/assets/img/posts/2026-05-31-jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements.png"
---

## Introduction

The AI landscape moves fast, and production‑grade autonomous agents need rock‑solid reliability. Today we’re excited to announce **Jiva v0.3.47**, a focused release that squashes long‑standing multimodal bugs, brings full Harmony tool‑call compatibility to Vertex AI, adds seamless Google Application Default Credentials (ADC) support, and raises the sub‑agent iteration ceiling. For teams building scalable, multi‑tenant AI services, these upgrades translate directly into fewer failures, smoother deployments, and faster iteration cycles.

## What’s New in v0.3.47

### 1. Multimodal Image Handling Fix

Previously, requesting an image analysis via `filesystem__read_media_file` would trigger a cascade of `400` errors from Groq because the tool returned an empty text payload. The worker stored an empty string as the tool’s content, violating Groq’s requirement that every message contain at least one character.

**Fix:** The worker now falls back to a placeholder text (`[Image content returned]`) when a tool returns images without accompanying text, while still passing the raw image bytes to the multimodal model. This eliminates the error loop and restores reliable image‑based reasoning.

### 2. Harmony Tool‑Call Sequences on Vertex AI

Vertex AI MaaS emits tool calls in a distinct Harmony dialect (`<|channel|>commentary to=TOOL_NAME <|constrain|>json<|message|>JSON_ARGS<|call|>`). Earlier versions could not parse this format, causing tool calls to be dropped after the first turn.

**Fix:** Added a `vertexChannelRegex` parser in `src/models/harmony.ts` that normalises the Vertex AI dialect to the standard Harmony token set. The worker now stores the raw Harmony content in history, preserving the call‑return chain across multiple turns.

### 3. Google Application Default Credentials (ADC)

Deploying Jiva on Google Cloud Run or GKE previously required a static API key. The new `src/models/google-adc.ts` module automatically fetches short‑lived OAuth2 tokens from the metadata server, with a fallback to the `google-auth-library` for local development.

**Configuration:**
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
When `useGoogleADC` is true, the `apiKey` field becomes optional, simplifying CI/CD pipelines and improving security.

### 4. Sub‑agent Iteration Limit Increased

The default `maxIterations` for sub‑agents spawned via `AgentSpawner` has been raised from 10 to 20. This change benefits workflows that require deeper tool‑use loops, such as multi‑file refactors or extensive research tasks, without hitting the previous iteration ceiling.

## Why It Matters for Teams

- **Reliability:** Multimodal bugs are a common source of silent failures in production agents. The fix ensures image‑based reasoning works out‑of‑the‑box.
- **Enterprise Compatibility:** Harmony support on Vertex AI opens the door for large‑scale deployments on Google’s managed AI platform, leveraging existing IAM and VPC setups.
- **Security & Ops:** ADC removes the need to embed long‑lived API keys, aligning with zero‑trust best practices.
- **Scalability:** Higher iteration limits let agents perform more complex, multi‑step tasks without manual intervention.

## Upgrade

```bash
npm install -g jiva-core@0.3.47
```

All existing configurations remain compatible; simply add `useGoogleADC: true` where you want token‑based authentication.

---

*Ready to put these improvements to work? Explore the full release notes on GitHub and start building more resilient autonomous agents with **[Jiva](https://github.com/KarmaloopAI/Jiva)**.*

*For more insights on agentic AI and production‑ready solutions, visit **[Gritsa Technologies](https://www.gritsa.com)**.*