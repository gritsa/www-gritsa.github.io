---
layout: post
title: "The security review for a coding agent starts at its shell"
date: 2026-07-10 18:34:20 +0000
last_modified_at: 2026-10-16 17:30:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - AI security
  - Coding agents
excerpt: "Before you ask whether the model is safe, ask what its shell can reach and what record it leaves. What Jiva's bash tool does, what it logs, and what the operator still owns."
description: "A practical security review of a coding agent, using Jiva's code mode as the example: how the bash tool runs, what environment it inherits, where approval happens, what gets logged and what the operator has to add."
keywords: "coding agent security, AI agent security, agent shell access, agent audit log, agent environment variables, Jiva"
---

# The security review for a coding agent starts at its shell

*Updated 16 October 2026. This post was first published in July 2026 as a roundup of other people's security taxonomies and benchmarks. I removed the borrowed claims and rewrote it around what Jiva, our open-source agent framework, actually does when it runs a command, because that is the part I can check.*

A coding agent is a language model with a shell. Most security talk is about the first half of that sentence: will the model be tricked, will it hallucinate a dependency, will it obey a hostile comment in a file. Those are real. They are also hard to measure, and they change every time the model does.

The second half is not hard to measure. You can read it. So I read it.

## What does Jiva's bash tool actually do?

In Jiva's code mode, the `bash` tool is a thin wrapper around Node's `exec`. Reading `src/code/tools/bash.ts`:

- The command runs with the workspace as its working directory. That is where it starts, not a fence. A command can `cd ..` or name an absolute path.
- It inherits the whole environment of the Jiva process (`env: { ...process.env }`). Whatever API keys and tokens are in the shell that launched the agent are visible to every command the agent runs.
- The tool itself applies no command filter. There is no list of forbidden commands in it.
- It does have limits on time and noise: a 30 second default timeout, a 5 minute ceiling, and output capped at 2,000 lines or 50 KB so the model's context does not flood.

None of this is a flaw. A coding agent that cannot run your tests is not a coding agent. But it means the safety of a command is decided by what the process is allowed to do, not by anything inside the tool.

## Where does a human get to say no?

At the plan, not at the command. Start code mode with `--plan` and Jiva generates an implementation plan and asks you to approve it before executing. After approval, the plan is injected as the approved instruction and the agent works. I found no per-command confirmation prompt in the CLI.

That is a sensible trade for speed. It also means approval covers intent, and nothing checks that each command stayed inside it. If your control is "a person read the plan", then what you are trusting is the model's loyalty to the plan. For the loop-level limits that do exist, such as the iteration budget and repeated-call detection, see [the runtime post](/blog/2026/07/17/why-agentic-ai-needs-a-new-runtime-infrastructure-over-models/). For a check that compares what the agent claims against what it did, see [the guardrails post](/blog/2026/08/08/when-agents-go-rogue-guardrails-for-the-new-ai-workforce/).

## What record does it leave?

Less than you would want. In code mode, each tool call is logged at info level as a line like `[CodeAgent] Tool: bash {"command":"..."}`. String arguments are truncated at 500 characters, and the line goes to the console. Unless you capture that output, there is no file.

The structured file log, `~/.jiva/logs/orchestration-<timestamp>.log`, belongs to the manager and worker path. It records each tool call with its arguments and each tool result as a success flag, not the output. In the HTTP mode it buffers per session and flushes to a storage provider.

So the record answers "what did the agent try", roughly. It does not answer "what did the command print", and neither path writes a diff. For a security investigation you would also want the output and the resulting change. Git gives you the second one for free if you insist the agent works on a branch.

## Four questions I would ask before giving any coding agent a shell

1. **What is in its environment?** List the variables the launching shell holds. If a production credential is among them, the agent has it. Start the agent from a shell that holds only what the task needs.
2. **What can its user account reach?** Jiva's Docker image runs as a non-root user, and that is the right default. The CLI runs as you, and its filesystem server is scoped to your user directories by default. Run it under an account, or in a container, that can see one project and not your home folder.
3. **Where does the record go, and is it complete enough?** Capture the console output, keep the output of commands if you need to reconstruct an incident, and treat the git history of the work branch as part of the log.
4. **What is the human approving?** A plan, a commit, a pull request? Pick the artifact that is easiest to inspect and make that the gate.

These are properties of the environment, and the environment is the part you control. I would rather hand a mediocre model a well-fenced shell than hand a brilliant one the keys to a laptop.

The model will be replaced twice before your next audit. The shell will still be there.
