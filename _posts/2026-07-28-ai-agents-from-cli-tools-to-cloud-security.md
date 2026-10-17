---
layout: post
title: "Stopping an agent is a request, not a command"
date: 2026-07-27 18:33:30 +0000
last_modified_at: 2026-10-17 16:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Human in the loop
  - Agent controls
excerpt: "Every agent demo has a stop button. Read the code behind one and you find a flag that is checked between steps. What Jiva's terminal loop lets a person do, and what to ask before you give an agent real work."
description: "How the human controls in Jiva's interactive loop actually work: Ctrl+C as a cooperative stop flag, the step-limit prompt, and a plan-approval gate that is a single yes or no. What each one does and does not guarantee."
keywords: "AI agent controls, human in the loop, stop an AI agent, plan approval, agent step limit, Jiva, agent safety"
featured_image: "/assets/img/posts/2026-07-28-ai-agents-from-cli-tools-to-cloud-security.png"
---

# Stopping an agent is a request, not a command

*Updated 17 October 2026. This post first appeared in July 2026 as a roundup of three news items. I dropped the roundup and kept one idea from it: agents are software, and software needs controls that work. What follows is what I found when I read the interactive loop in Jiva, our open-source agent framework.*

Every agent has a way for a person to say "stop". It is usually Ctrl+C, or a button. People assume it behaves like killing a process. In Jiva it does not, and I think most agents are the same.

The terminal loop lives in `src/interfaces/cli/repl.ts`. It is 620 lines, and nearly all of it is about one question: what can the human still do once the agent is running?

## What does Ctrl+C actually do?

Two different things, depending on whether the agent is busy.

At the prompt, with nothing running, Ctrl+C exits. While a turn is in progress, the handler calls `agent.stop()` and changes the spinner to "Stopping after current step". That is a literal description. `stop()` sets a boolean. The agent's loop reads it at the top of each iteration and, if it is set, ends the turn with the message "[Task stopped by user]". The code agent does this in `src/code/agent.ts`; the multi-step chat agent checks the flag between subtasks in `src/core/dual-agent.ts`.

So a stop lands between steps, never inside one. If the current step is a model call that takes a minute, or a shell command that takes ten, it finishes first. Pressing Ctrl+C a second time does nothing extra. I found no force path in the loop.

One detail I liked: the flag is cleared at the start of every new turn, so a stray Ctrl+C at a prompt cannot poison the next request.

None of this is wrong. A cooperative stop is the only kind that leaves the conversation history in a state the agent can continue from. The point is what it means for you. "Stop" is a request that gets honored at the next safe boundary. If your agent can run a step that sends an email, deletes a file or spends money, the stop button does not protect that step. Only the permissions around it do. I wrote about that boundary in [the security review for a coding agent](/blog/2026/07/10/agentic-ai-takes-over-production-code-security-risks-rise/).

## What happens when the agent runs out of steps?

Every agent has a step budget. In code mode, when the agent hits it, the turn ends with a `stopReason` of `max-iterations`, and the loop shows a menu: "Jiva reached its step limit before finishing this task", with Continue or Stop. Choosing Continue sends a fixed message telling the agent to resume exactly where it left off.

That is a good design, because the alternative is an agent that quietly stops at 80% and reports success. It is also easy to miss that the menu exists only in the standard path. The evaluator-harness path, where a second agent checks the first one's work, does not look at `stopReason`, so the Continue menu never appears. Whether an exhausted run is caught in that mode depends on what your evaluator checks. I covered the budget itself in [the post on the agent runtime](/blog/2026/07/17/why-agentic-ai-needs-a-new-runtime-infrastructure-over-models/).

## Is the plan approval a real gate?

In code mode with the `--plan` flag, each request goes through a planning pass first. The planning pass is properly restricted. It is given three tools, `read_file`, `glob` and `grep`, and if the model asks for anything else the code returns a message saying the tool is not available during planning. It is limited to twelve iterations, and for the last two the tools are removed so the model has to write the plan. It runs in an isolated message thread and does not touch the conversation history.

Then the person sees the plan and answers one question: "Implement this plan?" Yes or no. If no, the request is cancelled and you are told to refine it and try again. If yes, the plan text is added to the message with the note that it was "reviewed and approved by the user" and should be implemented exactly as described.

Three things follow.

You cannot edit the plan, only accept or reject it. Fixing step four of seven means rewording the request and getting a new plan, which may differ in steps one to three.

The approval is of a description, not of actions. The agent that executes is not bound to the plan by anything but its instructions. The gate narrows what the agent is likely to do. It does not enforce it.

And the planning step does not see a skill you loaded with a slash command. The loop passes the raw request to planning, and adds the skill's instructions only to the message that executes. I read that from the code and did not run it, but it means a skill that changes how work should be done can be absent from the plan you approved.

## What I would ask before giving an agent real work

Four questions, each answerable by someone who can read the agent's code or docs.

When I say stop, at what boundary does it take effect, and what can happen before then?

When the agent runs out of budget, does it tell me, and can I tell finished from exhausted?

When I approve a plan, what binds the agent to it?

Which controls vanish when I switch to the mode that does more checking?

The people building the agent should answer in a sentence each. If they cannot, the controls are decoration.

If you are putting an agent in front of real work and want those answers designed in rather than discovered, [talk to the Gritsa team](https://gritsa.com/contact/). [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read the loop yourself.
