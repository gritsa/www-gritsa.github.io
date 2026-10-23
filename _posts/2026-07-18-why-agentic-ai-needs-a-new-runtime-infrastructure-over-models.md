---
layout: post
title: "An agent runtime is the part that still works when the model doesn't"
date: 2026-07-17 18:32:57 +0000
last_modified_at: 2026-10-16 14:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - - AI agents
  - Agent runtime
  - Guardrails
excerpt: "Better models do not make agents safe to run. The controls that do are the ones the runtime enforces whether or not the model behaves. Here are the ones Jiva ships, and the one it deliberately leaves to you."
description: "What an AI agent runtime is, and which controls belong in it: iteration budgets, loop detection, read-only planning, approval gates, tool scoping. Concrete examples from Jiva, Gritsa's open-source agent framework, including its honest limits."
keywords: "agent runtime, AI agent guardrails, agent loop detection, plan and approve, iteration budget, agent infrastructure, Jiva"
featured_image: "/assets/img/posts/2026-07-18-why-agentic-ai-needs-a-new-runtime-infrastructure-over-models.jpg"
---

# An agent runtime is the part that still works when the model doesn't

*Updated 16 October 2026. This post was first published in July 2026 as a roundup of model announcements and included claims I could not source, plus a product preview I cannot find in Jiva's repository. I removed all of it and rewrote the post around what Jiva's code actually does.*

An agent runtime is the code that wraps a model and decides what it may do, how long it may keep doing it, and when a person gets a vote. The model proposes. The runtime disposes. Everything in the runtime works the same whether the model is brilliant or having a bad afternoon, and that is the whole reason to build it there instead of in the prompt.

A prompt is a request. A runtime is a rule. If a safety property depends on the model remembering an instruction at step 38 of a long task, you have a hope, not a control.

## What does a runtime actually control?

I read the code of [Jiva](https://github.com/KarmaloopAI/Jiva), our open-source agent framework, to find out what it enforces without asking the model. Its code mode (the single loop used for software tasks) has five controls worth copying.

**A budget on the loop.** The agent gets 50 iterations by default. Near the end the runtime changes behavior in stages: at 85% of the budget it injects a nudge to finish in-flight work, and at 95% it removes the tools entirely and asks for a final answer. The model cannot talk its way past this. Out of tools, the only move left is to say what it has.

**Loop detection.** If the model makes the same call with the same arguments three times in a row, the runtime skips the call and tells the model to stop and rethink. Models do get stuck in this pattern, and the cost of a stuck agent is real money in tokens. Three identical calls in a row is rarely progress, and a counter is cheaper than a post-mortem.

**A read-only first phase.** With the plan flag on, the first pass can only read files and search them. Editing, writing and shell commands are not available, and attempts return an error. The agent produces a plan, a person approves or rejects it, and only then does the full tool set switch on. The plan is not a courtesy. It is a gate.

**Tools that are off until you turn them on.** In code mode Jiva exposes no MCP servers by default. Each one is opt-in. Its documentation says why: too many tools bloat the context for no benefit. There is a second benefit I care about more. A tool the agent does not have is a tool it cannot misuse.

**A depth limit on delegation.** An agent can spawn a child agent for a focused task, but a child cannot spawn a grandchild. Two levels, then an error. Recursion without a ceiling is how a small mistake becomes a large bill.

None of these needs the model to be smart. That is the point.

## What does Jiva leave to you?

Isolation. By default, Jiva's filesystem tool is allowed to reach the user directories on the machine (`/Users` on macOS, `/home` on Linux, `C:\Users` on Windows), bounded by operating system permissions. The workspace is a default working area, not a fence. Its own documentation says not to run it as root.

I'd rather say this plainly than imply a sandbox that isn't there. If you want an agent to work only inside one project, the boundary has to come from where you run it: a container, a separate user account, a disposable machine. The runtime's controls limit how the agent behaves. They do not replace deciding where it is allowed to stand.

That split is the useful way to think about the whole category. Controls on behavior (budgets, loop checks, approval gates, tool scoping) belong in the runtime. Controls on blast radius (what files, networks and credentials exist at all) belong in the environment. When an agent does damage, I would look first for a missing control on one of those two lists.

## What should you ask before you deploy an agent?

Four questions, in the order I'd ask them:

1. What stops it if it loops? Look for a hard iteration or cost ceiling, enforced outside the prompt.
2. Where does a human approve something? Not "can they", but where exactly, and what the agent cannot do before that point.
3. Which tools does it have on day one? Fewer is better. Add them as the work demands.
4. What is the worst thing it can reach? Answer that for the machine and the credentials, not the prompt.

If a vendor answers any of these with "the model is trained not to," ask the question again.

## Where this fits

Runtime controls are one layer. The design of the pipeline decides how much the model is asked to do in the first place (I wrote about that in [agent design patterns](/blog/2026/05/26/agentic-ai-design-patterns-2026-architecting-autonomous-systems/)), and an evaluation decides whether it does it well ([write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/)). The tools it calls through [MCP](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/) have their own failure modes.

If you are moving an agent from a demo into something that touches real systems, [our AI agents service](/services/ai-agents/) is where I'd start the conversation.

The model will keep getting better. The runtime is what you can still trust on the day it isn't.
