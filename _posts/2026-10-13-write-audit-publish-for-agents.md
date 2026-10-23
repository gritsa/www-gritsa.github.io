---
layout: post
title: "Write-Audit-Publish: how to stop bad data reaching your agents"
date: 2026-10-13 09:00:00 +0530
author: "Amy Loomis"
categories: "Data Foundations"
tags:
  - - Data engineering
  - AI agents
  - Data quality
excerpt: "An agent will use whatever number you give it. Audit the data before it can see it."
description: "Write-Audit-Publish explained for AI agent pipelines: stage data, audit it with automated checks, publish only when it passes. Includes what to check."
keywords: "write audit publish, data quality for AI agents, AI ready data, WAP pattern, Iceberg audit branch"
featured_image: "/assets/img/posts/2026-10-14-write-audit-publish-for-agents.jpg"
---

# Write-Audit-Publish: how to stop bad data reaching your agents

Write-Audit-Publish is a pipeline pattern with three steps: write new data somewhere consumers can't see it, run automated checks against it, and only then make it visible. If the checks fail, nothing was ever published. For pipelines that feed AI agents it matters more than it did for dashboards, because an agent won't squint at a number and say "that looks off." It will use it.

I haven't built this pattern for a client and I won't pretend otherwise. This guide is built from the Apache Iceberg documentation, which describes the mechanics precisely, plus my own opinion about where it belongs in an agent project.

## Why do agents make bad data more expensive?

A human reading a dashboard is an unreliable but real quality gate. Revenue dropped 90% overnight, and someone says "that's wrong" before the meeting ends. An agent reading the same table has no such instinct. It will quote the figure to a customer, reorder stock against it, or write it into a report that another agent reads tomorrow.

That is the whole argument. The reviewer you never budgeted for was the person looking at the screen, and the agent removes them. If you remove the reviewer, the check has to become code.

## What is the Write-Audit-Publish pattern?

Three steps, in order.

1. **Write.** The new batch lands in a staging area. Production consumers keep reading the last good version.
2. **Audit.** Checks run against the staged data: row counts, nulls in required columns, values in range, keys unique, totals that reconcile with the source.
3. **Publish.** If every check passes, staged data becomes the production version in one step. If any fails, you stop, alert someone, and production is untouched.

The point is the ordering. The common alternative is load first, check later, which means the bad batch is live for as long as it takes someone to notice. For a dashboard that is an embarrassment. For an agent that acts, it is an incident.

## How does it work in practice?

The pattern is a design, not a product, so there are several ways to build it. One of the cleanest comes from Apache Iceberg, an open table format. Its documentation describes an "audit branch": a named, independent line of table history that you can write to without touching the main table.

The steps in the Iceberg docs, lightly trimmed, look like this in Spark SQL:

```sql
ALTER TABLE db.table SET TBLPROPERTIES ('write.wap.enabled'='true');

ALTER TABLE db.table CREATE BRANCH `audit-branch` RETAIN 7 DAYS;

SET spark.wap.branch = audit-branch;
INSERT INTO prod.db.table VALUES (3, 'c');

-- run validation against audit-branch, then:
CALL catalog_name.system.fast_forward('prod.db.table', 'main', 'audit-branch');
```

The docs put it plainly: writes happen on a separate branch, "a validation workflow can validate (e.g. data quality) the state of audit-branch," and after validation the main branch is fast-forwarded to the head of the audit branch. Readers of the main table see the old data until that last call, then the new data, with nothing in between. The branch reference is removed when snapshot expiry runs a week later.

If you are not on Iceberg, the same shape works elsewhere: a staging schema and a swap, a partition exchange, a view that repoints. What matters is that publishing is one cheap, atomic move, and that nothing reads from staging.

## What should the audit step actually check?

Start with the checks that would have caught your last three data incidents. That list is better than any framework's defaults.

| Check | Catches | Example |
|---|---|---|
| Volume | Partial loads, empty extracts | Today's row count within a band of the trailing average |
| Completeness | Upstream field renamed or dropped | Required columns are non-null above a threshold |
| Validity | Unit changes, bad parsing | Prices positive, dates not in the future |
| Uniqueness | Duplicate loads | Primary key has no repeats |
| Reconciliation | Silent drops and double counts | Total in the table matches the total in the source system |

Two rules I would hold to. First, checks must be deterministic. A model judging whether data "looks right" is a fine alert and a poor gate. Second, every check needs a named owner and a decision attached: block, or warn and publish. A check nobody will act on is decoration.

This is the same principle as [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/). If you can't score it automatically, you can't delegate it. That goes for the data going in as much as the answers coming out.

## What if the audit fails at 2 a.m.?

Decide before it happens. There are only three sensible answers.

- **Hold the line.** Production keeps the last good data and the pipeline pages someone. The agent works from yesterday, which is almost always better than working from garbage.
- **Degrade the agent.** Tell the agent, through a flag or a note in its context, that its data is stale, so it can say so to users instead of presenting old figures as current.
- **Publish with a warning.** For low-stakes tables only, and only by explicit choice.

Holding the line has a cost: staleness. Whether stale beats wrong is a business question. For an agent quoting prices, wrong costs money. For an agent summarizing last week's support tickets, stale costs nothing. Ask the owner of the process, not the data engineer.

## Does the agent's own tool access need this too?

Yes, and this is where it connects to the rest of the stack. If your agent reads through an MCP server, as I wrote in [what breaks first in production](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/), point the tools at the published tables only. Never give an agent a tool that can read staging. The audit gate is worthless if there is a side door.

## Where this fits

I hold a position that the model is the least defensible part of an AI stack, and the data under it is the most. Write-Audit-Publish is a small, boring piece of that. It won't appear in a demo. It is the reason the second month of an agent's life is as good as the first.

If you are building agents on top of pipelines that have no gate, that is usually where we start: the [data engineering work](/services/data-engineering/) comes before the [agent](/services/ai-agents/), because the agent is only as good as what it reads.

A pipeline that publishes unchecked data to a reader that never doubts it is an accident with a schedule.
