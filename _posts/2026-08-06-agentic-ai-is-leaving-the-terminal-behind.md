---
layout: post
title: "Agent memory is whatever survives the summary"
date: 2026-08-05 18:32:32 +0000
last_modified_at: 2026-10-17 15:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - - AI agents
  - Agent memory
  - Context engineering
excerpt: "People ask for agents with memory. Open the code of a working agent and the memory is a summary, written by a model, from evidence it was only shown part of. What Jiva keeps, what it drops, and what to do about it."
description: "How context compaction works in Jiva: what is kept verbatim, what is summarized, how tool results are truncated before the summarizer sees them, and what that means for any agent you run in production."
keywords: "agent memory, context compaction, conversation summarization, context window, AI agents, Jiva, context engineering"
featured_image: "/assets/img/posts/2026-08-06-agentic-ai-is-leaving-the-terminal-behind.jpg"
---

# Agent memory is whatever survives the summary

*Updated 17 October 2026. This post first appeared in August 2026 as a news roundup that ended on the claim that the winning agents would be the ones that remember. I kept that question and dropped the roundup. What follows is what I found when I read how Jiva, our open-source agent framework, actually remembers.*

When someone asks for an agent "with memory", they usually picture a notebook the agent writes in and reads later. That is not what most agents have. What they have is a context window that fills up, and a rule for what to do when it does.

In Jiva that rule is compaction. Once a conversation gets long, a model writes a summary of the middle, the old messages are replaced by that summary, and the agent carries on. Whatever the summary leaves out is gone. That is the memory.

I read the code to see exactly what that means. It is more specific, and more fragile, than the word "memory" suggests.

## What does the agent keep verbatim?

It depends on which agent you are running, because Jiva has two paths.

The chat agent counts messages. `ConversationManager.condenseConversation()` in `src/core/conversation-manager.ts` keeps the first two messages (the system and developer prompts) and the last ten. The default trigger is 30 messages, set in `src/core/agent.ts`. Everything between is summarized.

The code agent counts tokens. In `src/code/agent.ts`, compaction fires when a response reports more than 100,000 prompt tokens, which the source comments describe as roughly 78% of a 128K window. It keeps the system prompt and the last five rounds, where a round is one message plus the tool results that answer it. The grouping lives in `src/code/rounds.ts`, and the comment explains why: cut in the wrong place and a tool call gets summarized away while its result survives, or the reverse.

The chat path slices the last ten messages by count and I found no equivalent grouping there. A cut that lands between a tool call and its result is possible. I have not reproduced it, so I will leave it at that: the two paths made different safety choices.

## What does the summarizer actually see?

This is the part that changed how I think about it. Before the summarizing model sees the middle of the conversation, long tool results are cut. In the chat path to 300 characters each. In the code path to 200 for tool results and 300 for other messages.

So the summary is written from a truncated record. A 5,000 character query result, a long error trace, a whole file the agent read: the summarizer sees the first few lines. If the detail that matters sits on line 40, it was never in front of the thing deciding what to remember.

The summary itself is capped at 1,500 tokens and follows a fixed template: Goal, Instructions, Discoveries, Accomplished, Relevant files. That is a good template for a coding session. It has no slot for "the customer's exact figure" or "the rule the user stated once, early, and never repeated". Those survive only if the summarizer judges them a Discovery or an Instruction.

Jiva does one thing to help. If the workspace has a directive, it is placed ahead of the conversation with the instruction to prioritize context that supports it. That is the right instinct. It also means the quality of your memory depends on how well you wrote the directive.

## What happens when the summary fails?

Both paths have a fallback, and both are blunt. The chat path trims to the most recent messages. The code path keeps the middle but cuts each tool result to its first line. The agent keeps working with less than it had. The failure is logged, but nothing in the conversation tells the user.

## Is anything remembered across sessions?

Conversations are saved through a storage provider (local disk or a cloud bucket) and can be reloaded, with a generated title and token totals. That persists the transcript. I looked for a store of facts the agent learns, retrieves later and updates, and did not find one in the source. Sub-agents have a stricter version of the same limit: the manager's planning prompt tells it that workers share no memory between subtasks, so data gathered in one is gone when the next starts.

None of that is a criticism. It is what a working agent framework looks like today. The mistake would be to read "memory" in a feature list and assume it means more than this.

## What I would do with this

Treat the summary as a lossy cache, never as a record. Three habits follow, and none of them needs a new framework.

Put the facts that must not be lost somewhere the compactor cannot touch. A file the agent writes and rereads, a database row, the directive. If losing a sentence would cost you money, it should not live only in the conversation.

Test your agent past the compaction line. Most demos end well before it. Run a task long enough to cross the threshold, then ask about something said in the first twenty messages. That answer tells you more than any benchmark.

And when you hear that an agent "remembers", ask who writes the summary, what they were shown, and what happens when it fails. The people selling agents rarely volunteer that. The code, if you can read it, always answers.

If you are deciding what an agent in your business should hold on to, [the Gritsa team](https://gritsa.com/contact/) designs that layer, and [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read it yourself.
