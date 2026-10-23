---
layout: post
title: "A sub-agent is a function call with a briefing problem"
date: 2026-07-15 18:32:44 +0000
last_modified_at: 2026-10-16 16:30:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Multi-agent systems
  - Agent architecture
excerpt: "When a manager agent delegates to a specialist, the specialist knows only what the manager wrote down. How Jiva's spawn_agent works, what it hands over, and what it leaks."
description: "How delegation works in a multi-agent system: Jiva's spawn_agent tool, the depth limit, what a sub-agent receives, why the brief is the real design problem, and where persona scoping stops."
keywords: "multi-agent orchestration, sub-agent, spawn agent, agent delegation, manager worker agents, Jiva"
featured_image: "/assets/img/posts/2026-07-16-from-tool-calling-loops-to-multi-agent-orchestrations-the-new-agentic-ai-landscape.jpg"
---

# A sub-agent is a function call with a briefing problem

*Updated 16 October 2026. This post was first published in July 2026 as a summary of other people's articles about multi-agent trends. I removed the borrowed quotes and rewrote it around the delegation code in Jiva, our open-source agent framework, because that is the part I can vouch for.*

Most diagrams of a multi-agent system show boxes and arrows. A manager on top, three specialists below, results flowing back up. The diagram makes delegation look like organization. It is closer to a function call.

In [Jiva](https://github.com/KarmaloopAI/Jiva), a manager agent delegates through one tool, `spawn_agent`. It takes a persona name, a task, optional context and an optional iteration cap. It returns a string. While the sub-agent works, the manager waits. Nothing else happens in parallel, and the result lands in the manager's conversation as one tool result, the same as a file read.

That is a useful way to think about multi-agent design. The hard part is not the org chart. It is what you put in the arguments.

## What does a sub-agent know when it starts?

Only what the manager wrote. Reading `src/core/agent-spawner.ts`, the sub-agent's first message is built from three things: the project root path, the optional `context` string, and the `task`. It does not receive the conversation so far, the user's original request, or the manager's directive. A comment in the source says as much: the convention is that the manager includes the relevant constraints and a short summary in `context`, and a later phase might pass structured parent context along.

So a delegation is only as good as the briefing. "Check the code and see if anything looks wrong" produces a sub-agent that guesses what you meant. "Review `src/auth/` for SQL injection, this system uses JWT, tokens reportedly expire too early" produces a review. Jiva's own spawning guide makes this exact point with the same two examples, and the system prompt tells the manager to put constraints and a conversation summary in the context field.

If you have ever handed work to a contractor with a one-line email, you know the failure. The difference is that a contractor writes back with questions. A sub-agent that is run once, with no channel back to the manager mid-task, does not. It makes its best guess and returns something confident.

## How deep can the tree go?

Not deep by default. The guide in Jiva's repository says the default depth is three levels. The code says one: `maxAgentDepth` defaults to 1 in `dual-agent.ts`, with a comment that only the manager can spawn. When the limit is reached, the `spawn_agent` tool is not offered to the model at all, so a leaf agent cannot even try. I trust the code over the guide, and I would flag the mismatch to the people who maintain the guide, which is us.

Depth one is a reasonable default. Every extra level multiplies cost, because each sub-agent is a full agent with its own loop, and it multiplies the ways a vague brief can degrade as it is paraphrased downward.

## What does a persona actually scope?

A persona gives the sub-agent a role, a prompt and, if the persona defines them, extra MCP tool servers. That sounds like isolation. It is less than it sounds.

The sub-agent shares the manager's workspace and the same MCP server manager. When a persona brings its own tool servers, the spawner adds them to that shared manager. In the spawner file I found no code that removes them when the sub-agent finishes. The comment on the add call even says that a server already existing is fine. In practice that means a persona is a prompt boundary, not a permission boundary. If you need a reviewer that cannot write files, the persona text asking it not to is a request, not a control.

This is the same lesson as with the controls in my other Jiva posts. [The runtime enforces; the prompt asks](/blog/2026/07/17/why-agentic-ai-needs-a-new-runtime-infrastructure-over-models/). And the manager's job of checking a worker's output against what it really did is the subject of [the receipts guardrail](/blog/2026/08/08/when-agents-go-rogue-guardrails-for-the-new-ai-workforce/).

## When is it worth splitting at all?

Jiva's guide has a short list I agree with. Delegate when the task needs a different kind of expertise, when you want a second set of eyes on your own work, or when the pieces are independent. Do not delegate trivial file operations, steps where the context is the whole point, or information gathering that a tool call would answer.

I would add one test. Can you write the brief in four sentences? If you cannot say what the sub-agent needs to know, the task is not separable yet, and a second agent will only spread the confusion across two context windows.

## What I would build first

Before a second agent, write the brief template: the goal, the constraints, the files in scope, what "done" looks like, what to return. Make the manager fill it in every time. Then add one check on the way back, the same way you would review a pull request from someone new: did the result address the task, and does the tool record support what it claims?

That is most of orchestration. The rest is boxes and arrows.

If you are weighing a manager and specialists design for real work, [our AI agents service](/services/ai-agents/) is where I would start the conversation. And before you build it, [write the test for the finished job](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/).
