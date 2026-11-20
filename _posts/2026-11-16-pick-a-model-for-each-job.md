---
layout: post
title: "Pick a model for each job, not each agent"
date: 2026-11-16 07:58:00 -0500
author: "Amy Loomis"
categories: "AI Strategy"
tags:
  - LLM selection
  - AI agents
  - Model choice
excerpt: "The smartest model in your agent can still fail at the dullest step. Choose models by job."
description: "Why choosing one best LLM for an AI agent is the wrong question, and how giving each job its own model and fallback makes agents sturdier."
keywords: "choosing an LLM for AI agents, multi-model AI agents, which LLM for production agents"
featured_image: "/assets/img/posts/2026-11-16-pick-a-model-for-each-job.jpg"
---

Every agent project starts with the same meeting. Someone puts up a leaderboard and asks which model we should use.

It is the wrong unit of choice. An agent is not one task. It reads a request, decides what to do, writes a tool call, looks at a screenshot, drafts a reply, checks its own work. Those are different jobs, and one model does not have to do all of them. Pick models for the jobs, and let the agent hold more than one.

I think this is where the next year of sturdier agents comes from, and it has little to do with who tops the leaderboard.

## The dull step that breaks the clever model

Here is a failure that looks too silly to be real. A model reasons well. It plans the task, picks the right tool, knows what it wants. Then it writes the arguments for the tool call, and the JSON comes back malformed. The API rejects it with an error. The run dies on punctuation.

That failure is written into the code of Jiva, our open-source agent framework. [Jiva's model orchestrator](https://github.com/KarmaloopAI/Jiva) can hold three models at once: one to reason, one to read images, and one dedicated to making tool calls. The comment on that last slot says why it exists: for the times the reasoning model produces invalid JSON in its tool-call arguments and the call gets rejected. The framework's own description of the dedicated model is that it serializes those arguments reliably.

Models fail the boring part in different ways. Jiva's release notes record that Sarvam-105B emits its tool calls as XML inside the message text instead of in the structured field, so an agent that only reads the structured field sees a model that never uses its tools. I wrote up [what a coding agent has to do about that and about the model's output cap](/blog/2026/10/28/run-a-coding-agent-on-sarvam-105b/).

Nobody designs a slot like that because they enjoy complexity. Somebody watched a capable model trip on the boring part and decided the boring part deserved its own hire.

## Roles, not rankings

The image slot works the same way. If you configure a separate vision model, Jiva has it describe each image in words and hands the words to the other model. If your main model can already see, the newer code lets the images go straight through. Either way the question being asked is the one a manager asks about a team: who is best placed to do this step, and what happens when they can't?

That second half is where the value is. A single-model agent has no answer to "what happens when they can't". It retries the same model with the same input and hopes. An agent with roles can hand the step to someone else.

## What this changes in how you buy

If the unit is the job, a few things follow.

You evaluate by job. A score on a broad benchmark tells you little about whether a model writes clean tool arguments for your twelve tools. Test that, on your tools, with your inputs. I argued the general version in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/).

You stop treating the model as the foundation. It is a part, with a slot, and slots can be refilled. That is also what keeps you out of the trap I wrote about in the [lock-in essay](/blog/2026/10/26/llm-lock-in-is-not-where-you-think-it-is/): the more your system depends on one model's habits, the more it costs to swap that model when a better or cheaper one arrives.

And you plan for the step that fails, not only the step that impresses. The demo shows the reasoning. Tuesday shows the JSON.

## The objection

"More models, more moving parts." Yes. Every slot is something to configure, monitor and pay for, and a small project can reasonably start with one model and no fallback. But the day an agent starts doing real work, the cost of a rejected call is a stuck run and a person asking why. Adding a second model for one narrow job is often the cheapest fix in the whole system.

If you are choosing a model for an agent this quarter, write the list of jobs first. Then ask who should do each one. [That is how we scope agent projects at Gritsa](/services/ai-agents/), before anyone opens the leaderboard.

You are not hiring a genius. You are staffing a process.
