---
layout: post
title: "Automate the job you can undo"
date: 2026-11-23 07:58:00 -0500
author: "Amy Loomis"
categories: "AI Strategy"
tags:
  - AI automation
  - First AI agent
  - Future readiness
excerpt: "Pick your first agent job by how cheaply a mistake can be reversed, not by how big the prize looks."
description: "What to automate first with AI: rank candidate jobs by the cost of undoing a mistake, and why the reversible ones teach you the most."
keywords: "what to automate first with AI, first AI agent project, AI automation use cases"
featured_image: "/assets/img/posts/2026-11-23-automate-the-job-you-can-undo.jpg"
---

Most teams pick their first AI agent job the way they pick a restaurant for a big dinner: by how impressive it sounds. The biggest, most expensive process in the company wins, and the project starts with the highest stakes it will ever have.

I would pick the other way. Rank every candidate job by what it costs to undo a mistake, and start with the one where undoing is cheapest. The prize for the first project is not savings. It is learning how your agent fails, while failing is cheap.

## Undo cost is the number nobody writes down

Every automation business case has a column for hours saved. Almost none has a column for "what happens when it's wrong." Yet that is the property that decides how much supervision the job needs, and supervision is where the hours saved go to die.

Picture three jobs in the same finance team. The agent drafts the monthly variance commentary, a person reads it and edits it before it goes anywhere. The agent codes incoming invoices to general ledger accounts, and a wrong code gets caught at month-end review. The agent pays suppliers. All three are "automation." Their undo costs are nothing like each other. A bad draft costs a minute. A bad code costs a journal entry. A bad payment costs a phone call to a bank and, sometimes, a supplier who now trusts you a little less.

Same technology, three different projects. If you start with the third one, you will spend the first six months building approval gates, and the agent will be slower than the clerk it replaced.

## What the cheap jobs teach you

A reversible job gives you something an irreversible one can't: a lot of mistakes you can afford to look at. You learn which inputs confuse the agent. You learn whether the check you wrote actually catches the failure, which is the same lesson as [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/). You find out what your data looks like when something other than a patient colleague has to read it.

And you build the thing that makes the harder jobs possible later: a record of what the agent did and a habit of checking it. Nobody grants an agent authority over money because a slide said so. They grant it because last quarter's small jobs went well and the log shows why.

## Where I would not start

Anything public, anything that moves money, anything that deletes, anything a customer sees before a person does. Those jobs are not off limits forever. They are bad first jobs, because they ask you to trust a system you have not yet watched fail.

There is a second trap on the other side, and it is boredom. If the job is so low-stakes that nobody would notice if it vanished, you will learn nothing and prove nothing. The sweet spot is a job people do every day, that is tedious enough that they will be glad to lose it, and where a wrong answer is caught by a step that already exists.

Make a list of your candidates. Next to each, write one sentence: "If this is wrong, we find out when, and fix it how?" The jobs with a short, boring answer are your shortlist. When you [scope an agent like a hire](/services/ai-agents/), that sentence is the probation terms.

The ambitious project is still there. It just goes second, with a log behind it.
