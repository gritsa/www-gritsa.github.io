---
layout: post
title: "Why AI pilots never end"
date: 2026-11-10 09:00:00 -0500
author: "Amy Loomis"
categories: "AI Strategy"
tags:
  - AI pilots
  - AI strategy
  - Business AI
excerpt: "A pilot with no number and no date is not an experiment. It is a standing line item."
description: "Why AI pilots drag on for a year without a verdict, and the two sentences to write before kickoff so yours ends in a decision."
keywords: "why AI pilots fail, AI pilot success criteria, AI proof of concept"
featured_image: "/assets/img/posts/2026-11-09-ai-pilot-with-no-end-date.jpg"
---

An experiment is a thing that can fail. That is what separates it from a hobby with a budget.

Most AI pilots are written so they can't. Nobody names the number the pilot has to hit. Nobody sets the date it has to hit it by. So the pilot never fails, which means it never succeeds either. It just continues. Six months in, it has a steering committee, a Slack channel and a monthly demo. What it doesn't have is a verdict.

I think this is the real reason pilots stall, and it has little to do with the model. A pilot with no end date is a standing line item that happens to be called innovation.

## How a pilot gets immortal

Picture a support team piloting an assistant that drafts replies. The kickoff goal says "evaluate whether AI can improve support quality." Every word in that sentence can be defended and none can be measured. Improve against what? Quality according to whom? Evaluate for how long?

Three months later the drafts are decent on easy tickets and odd on hard ones. Some agents love it. Some never open it. That is a perfectly ordinary result, and it settles nothing, because there was no line it was supposed to cross. The pilot gets extended "to gather more data." The data it gathers is more of the same.

Meanwhile the people who would have to rebuild a workflow around it can't plan, because they don't know if it's real. The people who'd pay for production can't approve, because they've been shown a demo and not a result. Everyone is being reasonable. The project is stuck anyway.

## The two sentences

Before kickoff, write down two sentences and have the person who owns the budget sign them.

The first: **"If it does X by date Y, we put it in production and fund it."** X is a number from today's work, measured the way you already measure it. Tickets resolved without a human edit. Invoices matched without a touch. Hours from request to first draft. Pick one, write today's baseline next to it, and make it a number a skeptic would accept.

The second: **"If it doesn't, we stop on date Y."** Stop means stop. The team goes back to its day job, and the pilot's tools get switched off, not parked.

The second sentence is the hard one, because it admits the pilot might not work. That admission is the point. A pilot that is allowed to fail is the only kind whose success anyone will believe.

Software that runs agents already works this way. [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build on, will not loop on a task until someone steps in. Its manager plans a capped number of subtasks, a subtask that fails review gets one retry, and after that it stops retrying and carries on with what it has. Somebody picked those limits before the first run. Your pilot deserves the same courtesy.

## Where the number comes from

You can't write sentence one without a way to score the output, and that's work most teams skip. I made the case for it in [write the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/): if you can't score a result without arguing about it, you can't hand the job over. A pilot goal like "improve quality" is that same gap, one level up, and it is the same one that turns an AI strategy into [a procurement plan](/blog/2026/10/19/most-ai-strategy-is-a-procurement-plan/). The scope has the same problem: if nobody wrote the agent's [job description first](/blog/2026/10/21/how-to-scope-an-ai-agent/), nobody can say what "done" looks like for the pilot either. And if you haven't chosen the pilot's job yet, choose the one whose mistakes are cheapest to undo, as I argued in [Automate the job you can undo](/blog/2026/11/23/automate-the-job-you-can-undo/).

It also helps to decide, before the pilot, what production would cost. If nobody will fund the production version at the price you can already estimate, the pilot is theater, and it's cheaper to learn that in week one than in month nine.

## The objection

"Some things take longer than a quarter to judge." True. Then write the longer date. A twelve-month pilot with a number and a stop date is fine. A three-month pilot that quietly turns into twelve is not the same thing.

If you're staring at a pilot right now, ask whoever runs it one question: what result would make us shut this down? If the answer takes more than a sentence, you've found the problem. When you want help turning an agent pilot into something with a verdict, [that's the work we do on the AI agents side at Gritsa](/services/ai-agents/).

The best thing a pilot can give you is an answer. Even the no.
