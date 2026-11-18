---
layout: post
title: "How to give an AI agent a metric instead of a table"
date: 2026-11-18 08:00:00 -0500
author: "Amy Loomis"
categories: "Data Engineering"
tags:
  - Data foundations
  - Semantic layer
  - AI agents
  - MCP
excerpt: "An agent handed tables writes its own definitions. Hand it named metrics and it can only pick from the ones you signed."
description: "How to give an AI agent a governed metric instead of a raw table: the six things a metric must record, a semantic layer example, the tools an agent gets, and what it does when no metric exists."
keywords: "semantic layer for AI agents, governed metrics for LLMs, AI agent text to SQL accuracy, dbt MCP server, AI ready data"
featured_image: "/assets/img/posts/2026-11-18-give-an-agent-a-metric.jpg"
---

Give an AI agent named metrics, not tables. A metric is a definition someone signed: what is counted, at what grain, with which filters, on which date. An agent that queries a table writes its own definition on every question. An agent that queries a metric can only choose between definitions you have already agreed.

I haven't built this for a client, and I haven't run the tooling below. This guide comes from reading dbt's documentation for its Semantic Layer and its MCP server, plus the reasoning that follows from how agents answer questions. Treat the YAML as a shape to adapt, not a file to paste.

## Why is a table the wrong thing to hand an agent?

A table has no opinion. It holds rows, and a `customers` table with a `status` column will happily support five different counts of "active customers." A person asking that question fills in the missing context from the meeting they are in. An agent fills it in from whatever the schema suggests, and then reports the answer in the same flat tone it uses for facts.

I made the longer case for this in [what is an active customer](/blog/2026/11/02/what-is-an-active-customer/): the work is writing the definition down, and it is a decision, not a cleaning job. This guide covers the next step. Once the definition exists, where does it live so the agent cannot route around it?

The answer is a layer between the agent and the warehouse that exposes metrics instead of rows. The agent asks for `active_customers` by month. It does not decide what active means.

## What must a metric record before an agent can use it?

Six things. If any is missing, the agent supplies a guess and you will not know which.

| Field | The question it answers | Example of a gap |
|---|---|---|
| Name | What do we call it, exactly? | "Revenue" that could be booked, billed or recognized |
| Definition | In one sentence, what is counted? | "Customers who paid us in the last 12 months" |
| Grain | One row per what? | Per customer, per contract or per invoice line |
| Filters | What is always excluded? | Test accounts, internal users, refunded orders |
| Time basis | Which date decides the period? | Order date versus payment date |
| Owner | Who can change it, and who signed it? | Nobody, so it drifts |

The owner row matters more than it looks. A definition without a named owner is a draft. The first time two teams disagree, the agent has no way to know which one wins, and neither do you.

## What does a metric look like in a semantic layer?

dbt's Semantic Layer is one concrete form. Metrics are written in YAML inside the project, next to the models they read. A simple metric, in dbt's words, points "directly to a single column expression within a semantic model." The documented keys include a name, a description, a type, an aggregation and an expression. A sketch using only those keys:

```yaml
models:
  - name: customers_paid_12m
    description: One row per customer who paid us in the last 12 months.
      Excludes test accounts and internal users. Owner: finance.
    semantic_model:
      enabled: true
      name: customers_paid_12m
    columns:
      - name: customer_id
    metrics:
      - name: active_customers
        description: Customers who paid us in the last 12 months.
        type: simple
        label: Active customers
        agg: count_distinct
        expr: customer_id
```

Notice where the rule lives. "Paid in the last 12 months, test accounts removed" is not in the metric block. It is in the model the metric reads, which means the filter is ordinary SQL that your pipeline tests can check. The metric block then says only how to count. That split keeps the contested part, the definition, in one reviewable place.

One caution from the docs themselves: the page's example places `metrics` beside `columns`, while its parameter text says they belong under `semantic_model`. Check the spec for your version before you copy anything.

## What does the agent actually get?

dbt publishes an MCP server, which is the standard way to hand an agent a set of tools. Its Semantic Layer tools, as listed in the project's README, are:

- `list_metrics`: retrieve all defined metrics
- `get_dimensions` and `get_entities`: what you can group or join by, for a given metric
- `get_dimension_values`: the distinct values of a dimension
- `query_metrics`: run a metric query with filtering and grouping
- `get_metrics_compiled_sql`: show the SQL for a metric without running it
- `list_saved_queries`: the questions someone already blessed

Two of those do most of the governance work. `list_metrics` means the agent can see the menu before it orders, so it can tell "we have no metric for that" from "I could not find the table." And `get_metrics_compiled_sql` means a person, or an evaluator agent, can read the exact SQL behind any answer without taking the agent's word for it.

There is a catch in the same documentation. The server also has a `text_to_sql` tool, which generates SQL from a question, and the docs list "Full access to dbt commands" for the self-hosted server. The README warns that enabling dbt commands through MCP "could modify your data models, sources, and warehouse objects." If your goal is governed answers, expose the Semantic Layer tools only. An agent with both a metric tool and a free SQL tool will use whichever is easier on a bad day. I would want to know from the logs which one it used.

## What should the agent do when no metric exists?

This is the part teams skip, and it decides whether the layer survives contact with real users. People will ask questions no metric covers. The agent has three honest options:

1. **Say there is no metric for that**, name the closest one, and stop.
2. **Answer from raw tables, labeled as exploratory**: "This is not a governed number. Here is the query I used."
3. **File a request** for a new metric, with the question attached.

Pick the first for anything that goes in a board deck, the second for anything an analyst will review, and build the third in from the start, because the list of questions the agent could not answer is the best roadmap for your next ten metrics.

What the agent must not do is the fourth option, the one that happens by default: quietly answer from the tables with no label at all.

## How do you know it works?

Before launch, write twenty questions whose answers you already know, including five that no metric covers. Run them. For the fifteen covered ones, the agent's number should match yours and the compiled SQL should show the definition you signed. For the five uncovered ones, the correct output is a refusal or a labeled exploratory answer. If it returns a confident number for those, your layer has a leak.

That test is the same idea as [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/). Keep it in version control and re-run it whenever a metric changes. The other half of the safety net sits upstream: a pipeline that refuses to publish a table that breaks its own rules, which is what [write-audit-publish](/blog/2026/10/13/write-audit-publish-for-agents/) is for.

## What does this cost, and when is it not worth it?

It costs the definition work, which is mostly meetings, and the engineering is ordinary after that. It also only covers what someone has defined. For a company with five core metrics and one analyst, a handful of saved queries may be all you need, and a semantic layer is more machinery than the problem deserves. For a company where finance and sales already argue over the revenue number, it is cheaper than the argument.

On the agent side, connecting is the small part. [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build on, takes any stdio or HTTP MCP server as an entry in its config, so a metrics server is a few lines of setup. I have not run that pairing myself and I will not pretend the plumbing is the hard bit. The hard bit is the list of definitions behind the server.

If you are at the point of deciding which metrics an agent may answer from, that is the work our [data engineering team](/services/data-engineering/) does, and the agent side sits with the [AI agents practice](/services/ai-agents/).

The simplest version of the idea fits on one line. Do not ask the agent to be careful with your definitions. Give it a place where the careless answer is not available.
