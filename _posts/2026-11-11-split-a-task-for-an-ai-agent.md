---
layout: post
title: "How to split a task for an AI agent without losing the data in the gap"
date: 2026-11-11 09:00:00 -0500
author: "Amy Loomis"
categories: "AI Agents"
tags:
  - AI agents
  - Agent design
  - Task decomposition
excerpt: "Where you cut a task into steps decides whether an agent finishes it. Cut along data, not along topics."
description: "How to break a task into steps for an AI agent: why gather-then-write gives an empty file, how many steps to allow, and what a cheap result check misses."
keywords: "how to break down tasks for AI agents, agent task decomposition, planner worker agent, AI agent retries"
featured_image: "/assets/img/posts/2026-11-11-split-a-task-for-an-ai-agent.jpg"
---

Split a task for an AI agent along its data dependencies, not along its topics. If step two needs something step one found, and nothing saves it between them, put both in one step or write the result somewhere durable first. Most "the agent did every step and the output is empty" failures come from a cut in the wrong place.

I haven't run agent projects for a client and won't pretend to. This guide comes from the planner prompts and the execution loop in Jiva, Gritsa's open-source agent framework, which I read in the source. One of its prompts describes this exact failure, in capital letters.

## What does a planner actually hand to a worker?

In Jiva's general mode, a Manager agent turns a request into a short list of subtasks. A Worker agent runs them one at a time with the tools it has been given: files, a browser, a shell. If you want the case for having two agents at all, I wrote it up in [when two agents beat one](/blog/2026/05/25/agentic-ai-in-production-multi-agent-architectures-and-the-rise-of-the-sandbox/). This guide is about the next question: once you have a planner, where does it cut?

The detail that decides everything is in the execution loop. For each subtask, the Worker is called with two things: the instruction text and a shared context block. It is not handed the previous subtask's output. Whatever step one learned is gone when step two starts, unless step one wrote it to a file, a database or some other place step two can read.

That is not a bug in Jiva. It is how most multi-step agents behave, and it is the property the cut has to respect.

## What goes wrong when you cut in the wrong place?

The Manager's planning prompt contains a labeled bad example. Paraphrased: subtask one gathers data from the APIs and databases, subtask two compiles the results and writes them to `output.json`. The prompt says this will fail, because the second Worker has no data and the file will be empty.

The plan reads well. Each step is sensible, each step has a clear name, and a human reviewing the plan would approve it. It fails because the plan describes the work by topic ("collect", then "write up") when the real structure is a dependency: the write needs the thing that was collected, and the thing only exists inside one step's working memory.

The fix in the prompt is plain. Gather the data and write the complete results to the file in one subtask, before returning.

You can test any plan with one question per boundary: **what does the next step need that only this step knows?** If the answer is anything, either merge the steps or add an explicit save.

## How many steps should an agent get?

Fewer than you think. Jiva's planning prompt asks for one to three subtasks for code and file work and one to two for information gathering. It lists the failures it wants to avoid: five micro-steps such as "create the HTML structure", "add CSS", "add JS", "test", where one step ("create the calculator application as calc.html") would do. It also says not to create separate test or verify steps, because the Worker checks its own work as it goes.

I agree with the first two points and have doubts about the third, which I'll come back to. The reasoning behind the first two is simple. Every boundary is a place where context is lost, a model call that costs money, and a step whose output someone has to review. Fewer boundaries mean fewer places to lose the plot.

The framework also puts a ceiling on the plan. The execution loop takes the first N subtasks from the plan, where N defaults to 10 in the dual-agent class, and the agent spawner configures 20 for sub-agents it creates. A runaway plan cannot grow without limit. If you build your own, put a number there on day one.

## How does an agent check its own result?

Cheaply, and you should know exactly how cheap.

After each subtask the Manager decides whether to accept the Worker's output. In Jiva that decision is mostly a rule, not a model call:

| Situation | What the code does |
|---|---|
| Tools were used and the result is 100 characters or more | Accept without further review |
| No tools were used at all | Reject, and tell the Worker not to fabricate: use the tools |
| Tools were used but the result is under 100 characters | Ask a model to judge it: accept, or reject with one sentence on what is missing |

The middle row is the one I like most. A Worker that answers a data question without touching a single tool has produced text from memory, and the code treats that as the failure it is. It costs nothing to check and it catches a whole class of confident nonsense.

The first row is the one to understand before you copy the idea. "Used a tool and wrote a decent amount" says the agent did something. It does not say the thing is right. A 400-character answer built on the wrong table passes. So does a summary of a query that returned an error page. The third row raises its own question: the model that judges does not have to be the model that worked. I wrote about [giving each job its own model](/blog/2026/11/16/pick-a-model-for-each-job/).

That is the answer to my doubt about "don't create verify steps". A fast-path check is fine as a floor. It is not a verifier. For anything that matters, the check has to be something you can compute: row counts that match, a total that reconciles, a file that parses. I made the argument at length in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/), and this is the place it bites. The planner's review is a tripwire for the lazy failure. It will not find the subtle one.

## What happens when a step fails?

The loop allows one retry per subtask. When the review rejects a result, the code inserts a corrected instruction right after it, stating what was missing, and runs that. If the retry is also rejected, or the queue is full, the code accepts the partial result and moves on.

Then comes the part I'd copy into any agent. When the Manager writes the final answer, it is told to be honest about what was and was not accomplished, and failed subtasks are passed in under their own heading, "Subtasks That Could Not Be Completed", with the Worker's output beside them. The prompt says not to claim results for a subtask listed as failed.

One retry and an honest report is a defensible policy. Five silent retries followed by a cheerful summary is how a bad run turns into a bad email to a customer.

A small, real detail from the same file: the final answer is written in a fresh context, not the planning conversation. A code comment explains why. The planning prompt says "respond only with valid JSON", and when that history was included, the model could format the final reply as JSON too. The instruction you give a model for one step leaks into the next if the conversation carries it forward. Another hand-off to design on purpose.

## A short checklist for cutting a task

1. **List what each step produces and what the next step needs.** Draw the arrows. A step that consumes something only the earlier step knew is a bad boundary.
2. **Merge any gather-then-write pair.** Or write to disk or a database in the first step and say so in the instruction.
3. **Aim for the fewest steps that still have a clear owner.** If you wrote ten, ask which seven are really one.
4. **Cap the plan, and cap retries.** Pick the numbers before the first run, not after the first invoice.
5. **Check with something computable.** Row counts, reconciled totals, parsed output. Treat "the agent says it's done" as a signal, never as proof.
6. **Make the final report say what failed.** A summary that hides a failed step is worse than the failure.

None of this needs a particular framework. It needs someone to draw the arrows before the build, which is a scoping job and not an engineering one. If you're about to approve an agent that works through several steps, [our AI agents service](/services/ai-agents/) starts there, and [how to scope an agent like a hire](/blog/2026/10/21/how-to-scope-an-ai-agent/) covers the job description that comes first.

The best plan I can imagine for an agent is the one that looks slightly too simple. If you can't see why it would fail, check what step two is holding when step one is gone.
