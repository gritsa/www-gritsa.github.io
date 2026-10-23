---
layout: post
title: "Agent design patterns: the one that matters is what the model does not do"
date: 2026-05-26 22:31:36 +0000
last_modified_at: 2026-10-15 20:30:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - - AI agents
  - Agent architecture
  - Design patterns
excerpt: "Reflection, tool use, planning and multi-agent are the patterns everyone lists. The one that decides whether an agent survives production is the line you draw around the model."
description: "Agent design patterns (reflection, tool use, planning, multi-agent) and the pattern that matters most: keep deterministic work out of the model. With the three-layer pipeline from Gritsa's open-source agent framework, Jiva."
keywords: "agent design patterns, agentic AI patterns, reflection, tool use, planning, multi-agent, deterministic pipeline, AI agent architecture"
featured_image: "/assets/img/posts/2026-05-26-agentic-ai-design-patterns-2026-architecting-autonomous-systems.jpg"
---

# Agent design patterns: the one that matters is what the model does not do

*Updated 15 October 2026. This post was first published in May 2026 as a list of four patterns with a "30 to 40%" claim I could not source. I removed the claim and rewrote the post around the design guidance in Jiva, our open-source agent framework.*

The most useful agent design pattern is a boundary: give the model the work that needs judgment, and keep everything with a right answer in plain code. The usual list of patterns (reflection, tool use, planning, multi-agent) describes how to arrange a model. This one decides how much of the job the model gets at all.

## What are the four standard agent patterns?

Briefly, and with the cost of each:

- **Reflection.** The agent checks its own output and tries again. It costs an extra model call per pass, and it only helps when the agent can tell what "wrong" looks like.
- **Tool use.** The agent calls functions, APIs and databases instead of answering from memory. This is where most real value comes from, and where most real failures start.
- **Planning.** The agent breaks a goal into steps before acting. It helps when steps depend on each other. It hurts when the plan splits work that should stay together (more on that below).
- **Multi-agent.** Several agents with different roles hand work to each other. Every hand-off is a place for information to get lost. I wrote about [when two agents beat one](/blog/2026/05/25/agentic-ai-in-production-multi-agent-architectures-and-the-rise-of-the-sandbox/) separately.

None of these is wrong. All of them assume you have already decided the model should be doing the task.

## Which work should the model not do?

Anything where a junior developer could write the code in ten minutes. That is the rule of thumb in Jiva's own [agentic pipeline playbook](https://github.com/KarmaloopAI/Jiva/blob/main/docs/guides/agentic-pipeline-playbook.md), and I think it is the right one.

The playbook describes a three-layer pipeline:

1. **Deterministic data collection.** Scripts call the APIs and query the databases and write one structured file. No model involved.
2. **Bounded model work.** An agent reads that one file and writes one other file. Its only tools are reading and writing files. It does not search the web or query anything.
3. **Deterministic output.** A script reads both files and builds the report, payload or email.

The layers talk through files, never through the agent's memory. The model contributes what code cannot: narrative from numbers, patterns across data points, scoring with judgment, flagging what looks unusual and why. A database query, a REST call, a file conversion and a percentage stay in code.

## Why draw the line there?

Because of the failures the playbook lists, which are predictable:

- An agent calls its tools correctly, then writes the result from memory instead of from what the tools returned. The output is an empty template or a plausible invented number.
- A planner splits "gather the data" and "write the file" into two subtasks. The second worker has no memory of what the first one found.
- An agent asked to produce a formatted file end to end writes a stub script and never runs it. The output file is 0 bytes.
- A script fails, an API rate-limits, an agent times out, and with no recovery path the whole pipeline stops.

Look at what those have in common. None is a reasoning failure. They are what happens when a model is handed a job that has a deterministic answer, or a task that was split in the wrong place. Moving the job into code removes the failure instead of managing it.

## Where do reflection and planning fit then?

Smaller than the diagrams suggest.

The playbook's one reflection-like loop is for scripts, not answers. When a deterministic script fails, the error goes to a file, a code agent is asked to fix the script (and told not to run it), and the orchestrator retries. The playbook caps it at two attempts, and three at most before you abort and alert, because an unbounded retry loop burns credits and hides the root cause.

The model's step in the middle is also allowed to fail. If it produces nothing or malformed output, the final script renders the data without the narrative. The playbook says this is correct: a report with accurate numbers and no commentary beats no report.

That is a different attitude from "make the agent smarter." It assumes the model will sometimes fail and designs so that nothing important depends on it succeeding.

## What should you do with this?

1. **List the steps of the job, then label each one "judgment" or "right answer".** Only the first kind goes to a model.
2. **Give the model one input and one output.** If you want it to do more than read, reason and write, split it into two passes or move a step into code.
3. **Pass data between steps as files or tables, not as the agent's memory.** You can inspect a file.
4. **Cap every retry loop.** Two or three attempts, then stop and alert a person.
5. **Make the model step non-fatal.** Decide in advance what the output looks like if it fails.
6. **Write the test before the agent.** If you cannot say what a correct run looks like, [write that down first](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/), and make sure the data it reads has been [audited before it is published](/blog/2026/10/13/write-audit-publish-for-agents/).

The playbook is written for pipelines that run unattended and produce a document. It is not a theory of all agents. A coding assistant or an open-ended research agent needs more freedom than a one-file-in, one-file-out step. But even there, I would start from the same question: what in this job has a right answer, and why is a model computing it?

If you are deciding where an agent belongs in a process, and where it does not, [our AI agents service](/services/ai-agents/) is where that conversation starts.
