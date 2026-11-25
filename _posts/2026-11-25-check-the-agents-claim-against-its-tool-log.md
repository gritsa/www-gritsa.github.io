---
layout: post
title: "How to catch an AI agent that says it did work it didn't do"
date: 2026-11-25 07:50:00 -0500
author: "Amy Loomis"
categories: "AI Agents"
tags:
  - AI agents
  - Agent reliability
  - Verification
excerpt: "An agent's report is a claim. Check it against the log of what the agent actually did, before anyone acts on it."
description: "How to catch an AI agent that reports work it never did: compare the claim with the tool log, which claims a cheap check can settle, and what a model judge cannot."
keywords: "how to verify AI agent output, AI agent hallucination, agent says it ran tests, AI agent tool logging, AI agent reliability"
featured_image: "/assets/img/posts/2026-11-25-check-the-agents-claim.jpg"
---

Treat an agent's report as a claim, and check it against the record of what the agent actually did. If the report says "I reviewed every file and found no problems" and the log shows the agent listed a directory and never opened a file, you have your answer. The report was fluent. The work did not happen.

I haven't deployed agents for a client and won't pretend otherwise. This guide comes from reading how [Jiva](https://github.com/KarmaloopAI/Jiva), Gritsa's open-source agent framework, checks its own worker agent, including the places where that check is weak. The weak places are the useful part.

## Why does an agent report work it never did?

A model writes the report the same way it writes everything else: by producing the most plausible next words. "I have reviewed the codebase and found no issues" is a very plausible sentence at the end of a task called "review the codebase." Whether it is true depends on what happened in the middle, and the sentence itself carries no trace of that.

This is why the failure is hard to catch by reading. The report is well formed. The tone is right. Nothing in the prose marks the gap between "looked at the folder names" and "read the code."

So the fix has to come from somewhere other than the prose. Every agent that calls tools already produces a second record: the list of calls it made. That record was written by the framework, not by the model's sense of how the task should have gone. It is the only part of the output the model cannot embellish.

## What does Jiva compare the report against?

Jiva splits the work between a Worker, which does the task with tools, and a Client agent, which decides whether to accept the result. That is the same split I described in [how to split a task for an AI agent](/blog/2026/11/11/split-a-task-for-an-ai-agent/). Before the Client accepts anything, it runs what the source calls a result-versus-evidence coherence check.

The Client hands a model judge three things: the original request, the Worker's result, and the ordered list of tool names the Worker called. The prompt tells the judge what each family of tool can and cannot show. A directory listing shows names, not contents. A file-read tool shows contents. A shell tool runs commands, so what was run has to be inferred from the result.

Then it names the patterns to look for. I will paraphrase five, because they work as a checklist for any agent, framework aside:

1. The agent says it inspected or analyzed source code but only listed directories.
2. The agent says "no bugs found" or "the code is correct" without reading a source file.
3. The agent says it ran tests or a build, but no shell tool appears in the log.
4. The agent quotes line numbers, variable names or function logic from files it never opened.
5. The agent makes a firm statement about quality or behavior without having read the relevant code.

If the judge finds a claim the log does not support, the result is rejected with the unsupported claims listed, validation tightens, and the Worker gets a correction telling it which tool it should have used. The instruction in the source is concrete: read the files before claiming to have analyzed them.

## Which claims can you settle without a model?

Here is where I would push on the design. A judge reading a list of tool names is a second opinion. It is not proof. Some of the claims on that checklist you can settle with plain code.

"I ran the tests" is a log lookup. Was a shell tool called, and does the output the framework captured contain a test runner's summary line? That is a string match on a record you own, with no judgment involved.

"I wrote the report to this path" is a file check. Jiva does this one deterministically: its file-existence helper asks a read tool for the first line of the file, and falls back to a shell test if no read tool exists. Either the file is there or it is not.

"I read these forty files" is a count. If the log shows four read calls, the claim is wrong, and you did not need to ask anyone.

My rule of thumb: for every claim an agent can make that names a concrete action, ask whether the action leaves a mark in the log. If it does, check the mark in code. Save the model judge for claims that have no mark to check, such as "the logic here is sound."

## Where does the model judge fall short?

Three places, all visible in the source.

**It sees names, not arguments.** The judge is given which tools were called and in what order. It is not given what they were called with or what they returned. An agent that read the wrong file, or read the right file and got an error back, looks identical to one that did the job. Jiva does record each call's name and arguments in a parallel structure, so the data exists. The coherence prompt just doesn't use it. If you build something like this, pass the arguments and a trimmed output.

**It sees a slice of the report.** The result is cut to its first 1,000 characters before the judge reads it. A long report can make its unsupported claim in paragraph six. Hold that number in mind for your own setup: whatever you truncate, you are choosing not to check.

**It fails open.** If the judge's answer cannot be parsed, or the call throws an error, the code returns "coherent" and carries on. That is a reasonable choice for a framework that does not want one bad API call to stall a whole task. It is also a reminder that "the check passed" and "the check did not run" can look the same in a summary line. Log which one it was.

I have not run this check against real tasks or measured how often the judge is right, so I will not give you a rate. Treat it as a design to learn from.

## How do you build the log in the first place?

Two habits make everything above possible.

Record every tool call with its name, its arguments and its result, outside the model's control. If the only copy of "what the agent did" is the agent's own summary, you have nothing to check it against. Jiva keeps the name list and the name-and-arguments list side by side for exactly this reason.

And decide in advance which claims need evidence. That is the [job description](/blog/2026/10/21/how-to-scope-an-ai-agent/) doing its work: it says what "done" means, so you know what to look for in the log. Picture an agent asked to clean a customer list and report how many duplicates it removed. The count is a claim. The log should show a query or a script, and the number should be reproducible from the data before and after. (That is a hypothetical, not a case I have seen.) If the agent says 312 and the log shows no deletion step, you have found out in a minute rather than in next quarter's mailing.

## What should you do on Monday?

Start from the idea in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/): if you can't score the output, you can't hand the job over. Then pick the one agent task your team already trusts and read three of its reports next to their logs. Count the sentences that name an action. For each, find the line in the log. If you can't find it, you have found your first check to automate.

I would also stop asking agents to summarize their own work as the only output. Ask for the report and the evidence together, and let a boring piece of code compare them. If you want help building agents whose work you can audit, that is the kind of project Gritsa takes on: [AI agents](/services/ai-agents/).

An agent that can't show its work is asking you to take it on faith. That was never a good basis for delegating to anyone.
