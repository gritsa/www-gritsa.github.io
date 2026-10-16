---
layout: post
title: "An old instruction in your agent's history will be obeyed later"
date: 2026-05-19 00:00:00 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, prompt design, agent debugging, Jiva"
excerpt: "Jiva's final answers came back as raw JSON because a planning instruction was still in the conversation. The fix is a rule about context, not a better prompt."
description: "Why an agent's final answer came back as raw JSON: a Respond ONLY with valid JSON instruction from the planning step stayed in history. How Jiva v0.3.47 fixed it."
keywords: "agent final answer JSON, agent context management, planning and synthesis, Jiva, agent debugging"
featured_image: "/assets/img/posts/2026-05-19-jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements.png"
---

Updated 2026-10-16: rewritten around one bug from the Jiva v0.3.47 release notes. The full changelog is in [the release post](/blog/2026/05/31/jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements/).

Here is a bug that looks like the model misbehaving and is not. Jiva's manager agent finished a task and replied to the user with this:

```json
{"response": "...", "reasoning": "..."}
```

The user wanted a readable answer. The model had done exactly what it was told.

## What happened

Jiva's manager works in two steps. It plans the work, then synthesizes the results into a reply. The planning prompt contains the line "Respond ONLY with valid JSON", which is the right instruction for a step whose output a program will parse. The synthesis call then reused the entire planning conversation as its history, so that line was still sitting in it. The model followed the most explicit formatting instruction it could find. Nothing was wrong with the model.

## The fix is a context rule

The v0.3.47 fix did not add a sentence like "ignore the earlier JSON instruction". Synthesis now starts from a fresh context: the system messages and the synthesis prompt, and nothing from planning. As a backstop, if JSON still arrives, the code extracts the `response` or `content` field.

My view is that the rule generalizes. Every step of an agent should be handed the context it needs and no more. History is not free. An instruction written for step one is still an instruction at step five, and models weight explicit formatting commands heavily. If you find yourself writing a prompt that says "disregard the earlier instruction", the earlier instruction should not be there.

## A check you can run on your own agent

Take each step that produces output for a human, print the exact messages it receives, and read them top to bottom as if you were the model. Look for three things: formatting commands from other steps, tool schemas the step never uses, and role-play framing meant for a different task. Any of them is a candidate for the same bug.

The same release fixed three other bugs, including empty tool content that Groq rejects and a Vertex AI tool-call dialect that was silently dropped. Those are in [the full release note](/blog/2026/05/31/jiva-v0-3-47-multimodal-fixes-and-vertex-ai-enhancements/). The design reasoning behind keeping planning and execution apart is in [Agent design patterns: the one that matters is what the model does not do](/blog/2026/05/26/agentic-ai-design-patterns-2026-architecting-autonomous-systems/).
