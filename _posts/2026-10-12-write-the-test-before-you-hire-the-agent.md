---
layout: post
title: "Write the test before you hire the agent"
date: 2026-10-12 09:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - AI evaluation
  - Future readiness
excerpt: "If you can't score an agent's output automatically, you can't hand the job over. The eval is the job description."
description: "How to evaluate AI agents before you build them: why a pilot that can't be scored never graduates, and how an answer key turns opinion into a number."
keywords: "how to evaluate AI agents, AI pilot stuck, AI agent testing, agent evals, AI agent delegation"
featured_image: "/assets/img/posts/2026-10-12-write-the-test-before-you-hire-the-agent.jpg"
---

# Write the test before you hire the agent

Most AI pilots run forever because nobody can say what "good enough" means, whatever the model can do. If you can't score an agent's output automatically, you can't delegate the job to it, because every run needs a person to look at the result. That person is the cost you were trying to remove.

Think about how you'd hand a job to a new employee. You'd say what done looks like. Invoices are coded to the right account. Support tickets get the correct category. The migration script leaves row counts matching. Then you'd check the first few, relax, and check a sample after that. Delegation is the moment checking gets cheaper than doing.

With agents, teams skip the first step. They build the agent, watch it work on a handful of examples, and say "that looks right." Looks right is a feeling. It doesn't survive the second person who reviews it, or the model upgrade in March, or the Tuesday when an input arrives with a field renamed. Nobody can tell whether a change made things better or worse, so nobody changes anything, and the pilot stays a pilot.

The fix is unfashionable. Write the test first.

Take a job like "categorize inbound support tickets." Pull a few hundred tickets that a person already categorized. That is your answer key. Run the agent over them, compare, and you have a number. Now every decision has a price. Swap in a cheaper model and see what the number does. Change the prompt and see. Add a tool and see. The argument about whether the agent is good turns into a chart that goes up or down.

Some jobs don't have an answer key, and this is where it gets interesting. If you can't define a right answer for a job, you've learned something before spending any money: either the job isn't well specified, or it needs a person. Both are useful findings. Writing code that has to pass a test is easy to score, which is why coding agents improved first. Writing a persuasive proposal is hard to score, so I'd keep a human on it for now and not pretend otherwise.

One warning about scoring with another model. It's tempting, and it's fine for a first look, but a judge model that shares blind spots with the agent will happily agree with it. Where you can, score with something that cannot be charmed: a test suite, a schema check, a row count, a lookup against the system of record. The benchmark that ships with [Jiva](https://github.com/KarmaloopAI/Jiva), our open-source agent framework, works this way. Tasks run in throwaway workspaces and are checked by Node's test runner, with no model judging another model.

This also changes who should be in the room at the start. The evaluation is a business document. It says which mistakes are tolerable and which are not, and an engineer shouldn't decide that alone. A miscategorized ticket costs a minute. A wrong refund costs money. The test encodes that difference, and the people who own the outcome should write it.

So before the next agent project, skip the demo. Ask for the answer key. If the team can produce one in a week, you have a project. If they can't, you have a meeting about what the job actually is, and that meeting is cheaper now than in month four.

If you're stuck at that point, [our AI agents service](/services/ai-agents/) is where I'd start the conversation. The same habit applies when the agent talks to your systems through [MCP servers](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/): decide what a correct call looks like before you connect anything. The same logic applies to the data underneath: [Write-Audit-Publish](/blog/2026/10/13/write-audit-publish-for-agents/) is the answer key for what an agent is allowed to read.

This is also where an AI plan usually goes wrong one level up: [most AI strategy is a procurement plan](/blog/2026/10/19/most-ai-strategy-is-a-procurement-plan/), a list of tools with no jobs and no measures behind it.

The test only makes sense once the job is written down. [How to scope an AI agent](/blog/2026/10/21/how-to-scope-an-ai-agent/) covers the one-page job description that comes before the answer key.
