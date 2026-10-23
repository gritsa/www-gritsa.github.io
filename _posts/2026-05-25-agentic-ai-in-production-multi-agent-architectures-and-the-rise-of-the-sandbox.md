---
layout: post
title: "Multi-agent architectures: when two agents beat one, and when one loop wins"
date: 2026-05-25 20:31:57 +0000
last_modified_at: 2026-10-15 16:30:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - - AI agents
  - Agent architecture
  - Multi-tenant
excerpt: "Splitting an agent in two is a cost you pay for a benefit. Here is when the benefit shows up, and the production bug that taught us where the real boundary sits."
description: "When a multi-agent architecture is worth it and when a single loop is better, using the manager and worker design in Jiva and a real multi-tenant isolation bug as the examples."
keywords: "multi-agent architecture, manager worker agents, single agent loop, agent isolation, multi-tenant AI agents"
featured_image: "/assets/img/posts/2026-05-25-agentic-ai-in-production-multi-agent-architectures-and-the-rise-of-the-sandbox.jpg"
---

# Multi-agent architectures: when two agents beat one, and when one loop wins

*Updated 15 October 2026. This post was first published in May 2026 as a survey of agent trends. I rewrote it around what we can actually verify: how Jiva, our open-source agent framework, is built, and one bug we shipped a fix for.*

A multi-agent architecture is worth its cost when the work splits into a planning step and an execution step that need different context. For a task that is one tight loop of "look, edit, check", a single agent is faster and easier to debug. Most teams reach for several agents because the diagram looks serious, and then pay for it in latency and in bugs that live between the agents.

Jiva ships both designs, which makes it a fair place to look at the trade.

## What are the two designs?

In general mode, [Jiva](https://github.com/KarmaloopAI/Jiva) runs a Manager agent and a Worker agent. The Manager plans, breaks the request into subtasks and writes the final answer. The Worker carries out each subtask using whatever tool servers are configured: files, a browser, a shell. A simple conversational message skips the pipeline and gets answered directly.

In code mode, there is one agent in a single loop. It calls the model, runs a tool, gets feedback from the language server after a file edit, and goes around again. The README says plainly why it exists: removing the hand-offs between agents reduces latency, and the file tools run inside the same process.

Same framework, same models, two shapes. The team that built it decided that coding is a tight loop and a research or operations task is not.

## When does splitting pay off?

Split when the two halves want different things.

- **Different context.** Planning needs the whole request and a view of what is possible. Execution needs one subtask and the tool output in front of it. Keeping them apart stops a long tool result from drowning the plan.
- **Different tools.** The planner does not need a shell. The worker does. Giving each only what it needs shrinks both the prompt and the blast radius.
- **A place to look when it goes wrong.** If the final answer is bad, you can ask whether the plan was wrong or the execution was. In a single loop those two failures tangle together.

Do not split for parallelism alone, or because the task feels big. Every hand-off is a place for information to get lost and a model call you pay for. Jiva's own code mode is the argument: where the work is one loop, the framework removes the seam.

## Where did the boundary actually matter?

Not between the agents. Between the customers.

Jiva release 0.3.46, from May 2026, fixed a set of bugs that made its cloud interface unsafe for several tenants at once. The root cause was one shared storage object whose context was overwritten each time a new session started. A request from one tenant could read or write another tenant's storage path. A second singleton, the orchestration logger, wrote every session's events to whichever session registered last.

Nothing about that was an agent-design problem. It was shared mutable state. The fix gave every session its own storage provider with a context that cannot change, and its own logger, and made concurrent requests for the same session wait on a single creation instead of starting two. The v0.3.46 release notes in the [Jiva repository](https://github.com/KarmaloopAI/Jiva) list each change.

I read that as the useful lesson of "sandboxing" for agents. People picture a box around the model. The failures that reach customers are quieter: two sessions sharing an object that was written for one.

## What should you do with this?

1. **Start with one agent.** Add a second only when you can name the context or the tools it should not share with the first.
2. **Give each session its own state.** Storage, logs, conversation history. If something is a singleton, ask what happens when two customers hit it in the same second.
3. **Write the test for concurrency before the second customer arrives.** Two sessions, interleaved, checking that neither sees the other's data.
4. **Keep the hand-offs few and inspectable.** Log what the planner asked for and what the worker returned, per session.

If you are weighing an agent project and want to know whether it needs one agent or several, [our AI agents service](/services/ai-agents/) is where that conversation starts. Before you build anything, [write the test](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/) that says what a correct run looks like, and read [what breaks first when agents talk to your systems](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/).
