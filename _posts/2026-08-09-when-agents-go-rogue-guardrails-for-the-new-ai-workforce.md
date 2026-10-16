---
layout: post
title: "The guardrail that checks the receipts: auditing what an agent says it did"
date: 2026-08-08 18:31:57 +0000
last_modified_at: 2026-10-16 15:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Guardrails
  - Agent evaluation
excerpt: "Most agent guardrails watch what goes in and what comes out. The one I would add first checks the agent's claims against its own tool log. Here is how Jiva does it, and where that check fails open."
description: "A guardrail for AI agents that audits claims against the tool-call record: unjustified failure, results the tools do not support, missing required tools. How Jiva's client agent works, with its honest limits."
keywords: "AI agent guardrails, agent validation, hallucinated tool use, agent audit, claims versus tool calls, Jiva client agent"
featured_image: "/assets/img/posts/2026-08-09-when-agents-go-rogue-guardrails-for-the-new-ai-workforce.png"
---

# The guardrail that checks the receipts: auditing what an agent says it did

*Updated 16 October 2026. This post was first published in August 2026 as a roundup of an incident report and two product announcements, with figures I could not source and a roadmap promise I cannot find in Jiva's code. I removed all of it and rewrote the post around a guardrail Jiva actually ships.*

A guardrail for an AI agent is usually a filter. It reads the prompt going in, or the answer coming out, and blocks what looks unsafe. That is useful and it is not enough, because the failure that wastes the most money in agent work is not a toxic answer. It is a confident answer about work that was never done.

"I reviewed all the source files and found no bugs." Did it read any of them? Or did it list a directory, see the file names, and write a paragraph that sounds like a review?

The guardrail I would add first is one that asks for the receipts: compare what the agent says it did with the record of what it actually called.

## What does it mean to check the receipts?

Every tool call an agent makes is a fact. The agent's summary is a claim. A receipt check puts the two side by side and rejects the summary when the facts do not support it. It needs no opinion about whether the content is safe. It only needs to know what each tool can and cannot tell you.

Jiva, our open-source agent framework, has this built in. I read the source of its client agent (the part that validates the worker agent's output before the user sees it) to see what it enforces. There are three checks, run in this order.

**1. Giving up without trying.** If the worker says the task cannot be done, a separate model call asks whether it showed evidence: an error message, a permission failure, a concrete limit. The prompt is blunt about it. A worker that used zero tools and claims failure has no evidence. "I don't have the ability" and "this is outside my scope" are explicitly not evidence. The answer goes back with an instruction to actually attempt the task.

**2. Claims the tools cannot support.** A second call compares the worker's result with the list of tools it used, in order. The prompt spells out tool semantics: a directory listing shows names, not contents; only a read tool reads files. Its first listed pattern is exactly the one above, a worker that claims to have inspected code but only listed directories. Others: claiming to have run tests when no shell tool was used, and quoting line numbers from files it never opened.

**3. Required tools that were never used.** This one is plain code, no model call. Each requirement the client extracts from the request can carry a list of tools that must be used. If the worker finished without touching any of them, that is an issue. A task that needs real actions and finished with no tool calls at all is rejected at standard or thorough involvement, unless the tools themselves errored, in which case the failure is passed through as honest.

Any issue found makes the client reject the result and generate a correction instruction for the worker. Clean checks approve it.

## Why this beats a content filter for most business agents

A business agent's expensive mistakes are mostly false completions. The report that was never run. The file that was never written. The "verified" that verified nothing. A content classifier sees fluent, harmless text and passes it. A receipt check sees a claim with no matching call and does not.

It also gives you something to audit later. If every approved result has passed a comparison against the tool log, then the log is the thing you review when something goes wrong, not a transcript of reasoning.

## Where it breaks

I would be selling you the thing I am criticizing if I stopped there, so here are the limits, taken from the same file.

The first two checks are language-model judgments, not rules. They are only as good as the model doing the auditing, which can be wrong in both directions. And both are written to fail open: if the audit call errors or returns something unparsable, the code returns "coherent" and "no failure claim" and moves on. That is a sensible default for a product that should not stall on a flaky call. It is also a hole, and you should know it is there.

The tool-semantics list is tool-name based. A custom tool called something unhelpful gets judged by guesswork from its name. And the third check only works if the requirement extraction chose the right tools to demand.

None of this touches the other half of agent safety, which is what an agent can reach in the first place. That is the runtime's job, and I wrote about those controls separately in [an agent runtime is the part that still works when the model doesn't](/blog/2026/07/17/why-agentic-ai-needs-a-new-runtime-infrastructure-over-models/). A receipt check catches an agent that lies about its work. It does nothing about an agent that does exactly what it was told with too much access.

## What to ask a vendor

1. When your agent says it finished, what is that compared against?
2. Is the comparison a rule, a model call, or both? What happens when it errors?
3. Can I read the tool log for every approved result?

If the answer to the first question is "the agent's own summary," the guardrail is the thing it is supposed to be guarding.

If you are putting an agent in front of work that matters, [our AI agents service](/services/ai-agents/) is where I would start that conversation. And if you are writing the acceptance tests for one, [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/).

The agent that says "done" is not the evidence that it is done. The log is.
