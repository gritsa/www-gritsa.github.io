---
layout: post
title: "Self-improving agents: the version I would put in production is a supervisor with a checklist"
date: 2026-07-04 18:32:13 +0000
last_modified_at: 2026-10-16 16:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Agent evaluation
  - Supervision
excerpt: "An agent is a model calling tools in a loop. The loop that improves it, in a way a business can accept, is a second agent that checks the work against a written definition of done and sends the first one back. Here is how Jiva's harness does it, with its limits."
description: "Self-improving AI agents, without the hype: a supervisor agent that checks work against a written directive, nudges the worker, and gives up after a fixed number of cycles. How Jiva's evaluator harness works and where it can fail."
keywords: "self-improving agents, agent supervision, evaluator agent, agent harness, tool-calling loop, definition of done, Jiva"
featured_image: "/assets/img/posts/2026-07-05-from-tool-calling-loops-to-self-improving-agents.jpg"
---

# Self-improving agents: the version I would put in production is a supervisor with a checklist

*Updated 16 October 2026. This post was first published in July 2026 as a summary of two outside articles about agent-generated training data and long-horizon models, with a prediction that agents would soon improve themselves. I could not stand behind the prediction, so I replaced the post with something I can show: a supervision loop that Jiva ships today.*

An AI agent, at its smallest, is a model calling tools in a loop until it decides it is done. The trouble sits in the last four words. The agent decides. Nothing outside the loop has an opinion about whether the work is finished.

"Self-improving" usually promises a fix for that: agents that get better on their own. The version that matters to a business is much less grand. It is a second agent, with a written definition of done, that checks the first one's work and sends it back.

## What is a supervisor agent?

A supervisor agent does not do the task. It reads what the worker produced, compares it with the requirements, and tells the worker what is missing. Then it checks again. The improvement happens inside one task, against a standard a person wrote down in advance. Nothing is trained and nothing carries over to the next run.

Jiva, our open-source agent framework, ships this as its evaluator harness. I read the source to see what it really does. You switch it on with `jiva chat --harness evaluator`.

## How Jiva's evaluator works

The main agent runs first and finishes its work as usual. Then the evaluator starts, and four design choices stand out.

**The definition of done is a file.** The evaluator takes the workspace's `jiva-directive.md` and wraps it in a fixed template, with no model call involved. The template tells the evaluator to treat the directive as the ground truth of "done", to read the actual files, and never to assume success. A task counts as complete only if its output exists and meets the stated requirement.

**The evaluator is told not to do the work.** Its instructions say it must instruct the worker, never perform the task itself. Its special tools are for oversight: it can list and read the worker's saved conversations and send the worker a message, which is how every correction is meant to happen. Note the wording, though. It also receives the same MCP tools as the worker, so the separation is an instruction, not a permission. I come back to that below.

**It has its own memory.** The evaluator gets its own model connection, its own message history and its own tool servers, pointed at the same workspace. It does not inherit the worker's reasoning, which is the point: it judges the files, not the worker's account of them.

**It gives up on a schedule.** By default the evaluator runs up to five cycles of check, nudge and re-check, with up to thirty model calls in each. If the worker cannot fix a gap after two nudges, the instructions say to report an unresolved gap rather than keep pushing. The verdict comes back as structured data: passed or not, the list of gaps, how many nudges were sent, how many cycles ran, and which files it inspected as evidence. Token use for the two agents is reported separately.

## Where it breaks

Reading the code, I found five limits you should know before relying on it.

The supervisor runs on the same model configuration as the worker. Two copies of one model share blind spots. If the worker misreads the directive in a particular way, the supervisor may read it the same way.

The supervisor is held back by instruction alone. Because it gets the worker's tool set, nothing in the code stops it from writing files itself. If you run this where that matters, limit what the supervisor can reach before you rely on it.

The verdict is parsed leniently. The evaluator is asked to answer with a JSON block. If it does not, the code falls back to scanning the text for phrases like "evaluation passed" or "work is complete". That is a pragmatic choice, and it also means a loose sentence can count as a pass. An answer under twenty characters is treated as inconclusive and fails.

It costs real money. Jiva's own harness guide says the evaluator typically adds two to three times the worker's token use and response time. That is a number from the documentation, not a measurement I made. Put it in the budget before you turn it on.

And it is only as good as the directive. A vague directive produces a supervisor that approves vague work. The harness guide says as much: be specific, include acceptance criteria.

## Why this beats waiting for self-improvement

You do not need an agent that improves itself. You need one whose work is checked by something other than its own confidence. That is a loop you can reason about: bounded, logged, with a stated stopping rule and a failure state a human can read.

It also moves the hard part somewhere useful. The quality of the result now depends on how clearly you wrote down what done means, which is a business skill and not a machine learning one. I argued the same thing from the buyer's side in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/). A supervisor is that test, run every time.

A supervisor checks the claim against the files. A different guardrail checks the claim against the tool log, which I covered in [the guardrail that checks the receipts](/blog/2026/08/08/when-agents-go-rogue-guardrails-for-the-new-ai-workforce/). They catch different failures and you may want both. If you are deciding where an agent can safely run without a person watching, [our AI agents service](/services/ai-agents/) is where I would start that conversation.

The agent that improves itself is a research topic. The agent that cannot say "done" until someone else has looked is a purchasing decision, and you can make it today.
