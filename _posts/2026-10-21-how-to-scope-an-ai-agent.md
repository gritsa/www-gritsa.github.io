---
layout: post
title: "How to scope an AI agent: write the job description first"
date: 2026-10-21 09:00:00 +0530
author: "Amy Loomis"
categories: "AI Agents"
tags:
  - AI agents
  - Agent design
  - Business AI
excerpt: "An agent project fails at scoping before it fails at engineering. Write the one-page job description first."
description: "How to scope an AI agent: a one-page job description with purpose, tasks, constraints and context, plus why a rule on the page is not a lock."
keywords: "how to scope an AI agent, AI agent job description, AI agent guardrails, what is an AI agent for business"
featured_image: "/assets/img/posts/2026-10-21-scope-an-ai-agent.jpg"
---

# How to scope an AI agent: write the job description first

To scope an AI agent, write it a one-page job description before anyone chooses a framework: one purpose, a short list of tasks, a list of things it must never do, and the context it needs. If you can't fit the job on a page, you don't have an agent. You have a hope.

I haven't run a scoping workshop for a client and I won't invent one. This is built from how directive files work in Jiva, Gritsa's open agent framework, plus my own view of where agent projects go wrong.

## Why does scoping matter more than the model?

Because the model will try to be helpful about anything you leave open. A person hired into a vague role asks questions. An agent in a vague role fills the gap with its best guess, at machine speed, using whatever tools you handed it.

Take the classic kickoff-deck sentence: "an assistant that helps with operations." Helps with what? Allowed to touch what? Judged by whom? Nobody answers, so the agent answers for them.

## What goes in the job description?

Four parts. Jiva's directive file uses exactly these four headings, and I think that's the right skeleton for any agent, whatever you build it with.

| Section | The question it answers | Weak version | Strong version |
|---|---|---|---|
| Purpose | Why does this agent exist? | "Help the finance team" | "Reconcile supplier invoices against purchase orders" |
| Tasks | What does it actually do? | "Handle exceptions" | "Flag invoices where the amount differs from the PO by more than a set tolerance" |
| Constraints | What must it never do? | (missing) | "Never pay, approve or edit. Read only." |
| Context | What does it need to know? | "Our systems" | "Which tables hold POs, who owns them, what the tolerance is" |

Here is the shape in Jiva's own format, trimmed from its README example for a code review agent:

```markdown
# Purpose
Code review assistant for a Django web application.

# Tasks
- Scan for security vulnerabilities (SQLi, XSS, CSRF)

# Constraints
- Only analyze .py files
- Do not modify files without explicit approval

# Context
PostgreSQL backend, GDPR-sensitive user data.
```

Notice what the constraints do. They don't describe the job. They fence it. "Only analyze .py files" removes a whole category of surprise. "Do not modify files without explicit approval" turns an agent that acts into an agent that proposes.

## How do you decide what the agent may do alone?

Sort every task into one of three bins before you build anything.

1. **Read and report.** The agent looks at things and tells a person. Cheapest to get wrong.
2. **Propose.** The agent drafts a change and a person approves it.
3. **Act.** The agent changes something with no one in the loop.

Start every task in bin one or two. Move a task to bin three only when you can measure the agent's output against a test you wrote in advance. That test is its own subject; I made the case in [Write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/). The short version: if you can't score the work, you can't delegate the work.

## What should the constraints cover?

Write constraints as things a stranger could check. "Be careful with customer data" is a mood. These are rules:

- **Scope of data.** Which tables, folders or APIs it can reach. Everything else is invisible to it.
- **Scope of action.** Read, draft, write, delete. Name the verbs.
- **Money and messages.** Whether it can spend, send an email or contact a customer. Default to no.
- **Stopping conditions.** When it must hand back to a person: low confidence, a missing field, an amount over a limit.

The data scope is also where upstream quality shows up. If the agent reads a table, that table needs checks before the agent sees it, which is the argument in [Write-Audit-Publish](/blog/2026/10/13/write-audit-publish-for-agents/). If it calls tools, each tool is a permission, which is what breaks first in [MCP servers in production](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/).

## Does writing a constraint actually enforce it?

Not by itself, and this is the part most scoping guides skip. In Jiva, I read the code that loads the directive. The file is parsed into purpose, tasks, constraints and context, but what the model receives is the raw text, placed in the system prompt under "You are operating with the following directive." So a line like "Do not modify files without explicit approval" is an instruction the model is asked to follow. It is not a lock.

That is how most agent setups work, not a flaw in one framework. A constraint on the page tells the agent what you want. A permission on the tool decides what it can do. If the page says "read only" and the agent holds a credential that can write, you have a policy and no control.

So write the constraint on the page, then make it true somewhere else: a read-only database role, a folder the agent can't leave, an approval step before anything is sent. The page is the spec. The permissions are the enforcement. You need both, and a reviewer should be able to tick each constraint against a real setting.

## How do you know the job description is good enough?

Hand it to someone who wasn't in the room and ask three questions.

- What would this agent do if it received an email it has never seen a pattern for?
- What is the worst thing it could do with the access listed?
- Who gets told when it stops?

If any answer is "it depends" or a shrug, the description isn't finished. Fix the page, not the prompt.

## What do you do with the finished page?

Three things. Put it in the repo next to the agent so it gets reviewed like code. Give one named person ownership of it, the way a manager owns a role. And revisit it when the agent's tools change, because a new tool is a new permission and the page should say so.

Frameworks come after that, and they matter less than people think. Whether you use Jiva or something else, the page is what makes the agent safe to run.

If you're about to approve a first agent project and want a second pair of eyes on the scope, that is the work on our [AI agents service page](/services/ai-agents/).
