---
layout: post
title: "What is an active customer?"
date: 2026-11-02 09:00:00 -0500
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - Data foundations
  - AI readiness
  - Future readiness
excerpt: "Before an agent can answer a question about your business, someone has to write down what your words mean."
description: "AI-ready data is less about clean tables than written definitions. Gartner says 63% of firms lack the practices. Start with one question: what is an active customer?"
keywords: "AI ready data, data readiness for AI agents, why AI projects fail data, business definitions, metadata"
featured_image: "/assets/img/posts/2026-11-02-what-is-an-active-customer.jpg"
---

# What is an active customer?

Before an AI agent can answer a question about your business, somebody has to write down what your words mean. That sounds like a small chore. It is the reason a large share of AI projects stall, and it has very little to do with how clean your data is.

Here is the test I would run before buying anything. Ask three people in your company how many active customers you have. Picture the answers: sales counts anyone with an open contract. Finance counts anyone invoiced in the last twelve months. Product counts anyone who logged in this quarter. Three numbers, each correct, each living in a different table, and nobody has ever needed them to agree because a human always knew which one they meant.

A person asks "how many active customers do we have?" and automatically adds the context. They know who is asking, what the meeting is about, which report the number is going into. An agent has none of that. It has the schema. It finds a table called `customers` and a column called `status`, and it answers in the same calm sentence it would use for something it knew. You get a wrong number with perfect manners, and nothing in the output tells you it was a choice.

Gartner has been saying a version of this for a while. In a February 2025 Q&A, one of its analysts reported that 63% of organizations either lack the right data management practices for AI or are not sure whether they have them (a survey of 1,203 data management leaders). The same piece predicts that through 2026, organizations will abandon 60% of AI projects that are not supported by AI-ready data. Its explanation is the interesting part. In traditional data management, it says, uses of data are not well documented, and organizations lack the practice and the metadata to judge whether data is ready for AI.

Metadata is the word to translate. It means the written answer to "what does this mean, who owns it, and where does it come from." Most companies carry those answers in people's heads. That works until you hire an agent whose entire job is to act without asking.

That is why "clean the data first" is such unsatisfying advice. You can deduplicate and normalize for a year and still have three customer counts. Cleaning fixes errors. It does not settle meaning. Meaning is a decision, and a decision needs a person with the authority to make it: finance and sales are going to have to agree, in writing, on one definition for each of the ten or twenty terms the business actually runs on. Revenue. Churn. Active. Qualified. On time.

That list is a smaller project than a data lake and a better predictor of success. It is also the part you can't outsource to a model or a vendor, because the answer is not in the data. It is in the room.

Once the definitions exist, the engineering is ordinary. Put them where the agent reads them, as a governed model or a documented view and not a slide. Make the pipeline refuse to publish a table that breaks its own definition, which is what [write-audit-publish](/blog/2026/10/13/write-audit-publish-for-agents/) is for. Test the agent against questions whose answers you already know. That is our [data engineering](/services/data-engineering/) work in a sentence, and the dull middle of most agent projects we get asked about.

[Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build on, shows how small the first step can be. It reads a plain markdown directive file from the project root, with sections for purpose, tasks, constraints and context. That file is a fine place for "active customer means invoiced in the last twelve months, and here is the table." It will not write the sentence for you. Nothing will.

So skip the readiness audit for a week and try the smaller experiment. Write one definition of "active customer" that sales, finance and product will all sign. If that takes a month, you have just learned how long the real project will take, and what your first agent would have been guessing.
