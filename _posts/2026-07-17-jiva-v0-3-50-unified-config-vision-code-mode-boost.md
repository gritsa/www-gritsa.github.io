---
layout: post
title: "Three agent bugs with one cause: a reasoning model that ran out of tokens"
date: 2026-07-16 20:33:04 +0000
author: "Gritsa"
categories: "AI Technology"
tags:
  - agentic AI
  - autonomous agents
  - Jiva
excerpt: "A 20-token title call, a dropped max_tokens setting and a code agent that gave up early all traced back to the same thing: the model spent its budget thinking and never answered."
description: "Three bugs fixed in Jiva v0.3.50 that share one root cause: a reasoning model exhausting its completion budget before producing visible output, and how to guard against it."
keywords: "reasoning models, max tokens, finish_reason length, agent bugs, Jiva, autonomous agents"
featured_image: "/assets/img/posts/2026-07-17-jiva-v0-3-50-unified-config-vision-code-mode-boost.jpg"
---

Updated 2026-10-16: rewritten from the Jiva v0.3.50 release notes. The original post duplicated the [full release note](/blog/2026/07/14/jiva-v0-3-50-unified-config-vision-code-mode/); this one covers a single pattern from it.

A reasoning model spends part of its output budget thinking before it writes the answer. If the budget is too small, the thinking uses all of it, the response ends mid-thought, and nothing the user can read comes back. Three bugs fixed in Jiva v0.3.50 turned out to be that one failure arriving by different routes.

## 1. A 20-token budget for a title

Jiva asks the model for a short title for each conversation. `ConversationManager.generateTitle()` set `maxTokens` to 20. The orchestrator sends calls with no tools and no images to the reasoning model, and models such as GLM-5.2 emit an inline thinking block before the answer. Twenty tokens is barely enough for the thinking alone. The model often ran out mid-thought, so the response contained the start of its reasoning, no closing tag and no title.

The cleanup code then failed twice. The function that strips control tokens did not strip thinking blocks, so the reasoning survived into the content. The title cleanup (trim, remove quotes and punctuation, cut to 60 characters) did not remove it either, and the guard that rejects garbage titles checked for emptiness, under three characters and the word "untitled", not for 60 characters of leaked reasoning. Saved conversations in `~/.jiva/conversations/` therefore showed one of two wrong shapes: the first 40 characters of the user's first message, or text like `Okay, the user wants a short title for their mess...`.

The fix has four parts:

- A new `stripThinkingContent()` removes closed thinking blocks and also the truncated, unclosed ones.
- After stripping, the last non-empty line is taken as the title, since models sometimes add preamble.
- `maxTokens` went from 20 to 200, enough for thinking plus a title.
- The call sets `reasoningEffort: 'low'`, because a title is a trivial task.

The first-message snippet remains as the last resort.

## 2. A token cap that never reached the request

A reasoning model configured with `defaultMaxTokens: 4096`, which Sarvam-105B needs, had no effect through `jiva chat`. All four places in `src/interfaces/cli/index.ts` that build a model client dropped `defaultMaxTokens` and `reasoningEffortStrategy`, although both were in the config schema and written by the setup wizard. The request went out with no cap, the provider applied its own default, and the model could burn its completion budget on reasoning before producing anything visible. The fix passes both fields through at all four sites.

## 3. A code agent that quit with iterations to spare

Code mode stopped with `[No response content]` after about ten iterations even with `maxIterations` set to 100. Retrying the same request by hand usually worked. The cause was in compaction: it only ran when the last response included tool calls. Once a model starts returning genuinely empty responses, with no content and no tool calls, that condition can never be true again. The context never shrinks, the same oversized prompt is resent on each retry, and it fails the same way. The cap of four empty responses was the real limit, not the iteration budget.

Two changes fixed it. Compaction no longer requires tool calls. And Jiva now records the provider's `finish_reason`, which it used to throw away. An empty response with `finish_reason: 'length'` is direct evidence that the model ran out of completion budget mid-thought, so code mode forces a compaction immediately. The old behavior added another text nudge, which made the prompt heavier and the next attempt worse.

## What to take from it

If you run reasoning models in an agent, three habits would have caught all of these:

1. **Read `finish_reason`.** `length` with empty content is a budget problem, not a model problem. Retrying with the same prompt will not help.
2. **Give small utility calls room.** A title, a classification or a routing decision still pays the thinking cost on a reasoning model. Set the budget for thinking plus the answer, and turn the reasoning effort down.
3. **Check that settings arrive.** A config field that the setup wizard writes and the schema accepts can still be dropped between the file and the HTTP request. Test the request, not the config.

The rest of the release, including the single shared config file and the rate limiter, is in the [v0.3.50 release note](/blog/2026/07/14/jiva-v0-3-50-unified-config-vision-code-mode/). The source is on [GitHub](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.50).
