---
layout: post
title: "An agent's settings live in three places, and they disagree"
date: 2026-07-09 18:53:38 +0000
last_modified_at: 2026-10-17 17:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Agent infrastructure
  - Configuration
excerpt: "Ask where an agent's configuration lives and the answer is never one file. Jiva reads settings from a config file, from environment variables and from the request, and the order they win in has consequences for key rotation, defaults and debugging."
description: "How Jiva resolves configuration across its CLI config file, server environment variables, per-tenant stored config and per-session overrides, and what that means for key rotation, defaults and silent overrides."
keywords: "agent configuration, AI agent deployment, environment variables, secrets rotation, multi-tenant agents, MCP defaults, Jiva"
featured_image: "/assets/img/posts/2026-07-10-agentic-ai-infrastructure-from-code-releases-to-cloud-platforms.jpg"
---
# An agent's settings live in three places, and they disagree

*Updated 17 October 2026. This post first appeared in July 2026 as a roundup of releases and funding rounds, ending on the idea that agents need their own kind of cloud. I kept the question about infrastructure and dropped the roundup. What follows is what I found when I read how Jiva, our open-source agent framework, decides what an agent is allowed to be.*

Ask where an agent's configuration lives and you will usually be told "in the config file". For a framework that runs both on a laptop and on a server, that answer is wrong in an instructive way. Jiva has three sources of settings, they follow different rules, and the interesting part is what happens when they disagree.

I read the code to find out. None of what follows is exotic. It is what any agent framework drifts into once it has to run in two places.

## What is the laptop path?

On the command line, settings live in one JSON file at `~/.jiva/config.json`, managed by `ConfigManager` in `src/core/config.ts`. Older installs kept it in a platform-specific folder, and a one-time migration copies it across on first run and prints a message saying so. That is good manners: a move that is announced is a move you can debug.

Two details matter more than the migration.

The first is where validation happens. Every setter (`setReasoningModel`, `addMCPServer` and the rest) parses its input through a schema before writing. Reading does not. A full schema for the whole file exists in the source, but it is used only to generate types; the store itself is opened with no schema. Edit the file by hand and nothing checks your work until something downstream trips on it. Even the startup check is thin: `validateConfig()` confirms that a reasoning model exists and has either an API key or cloud credentials. It does not confirm that the endpoint answers or the model name exists.

The second is the tool defaults. The setup wizard registers two MCP servers and enables both: a filesystem server rooted at `/Users` on macOS or `/home` on Linux, and a shell server. Both are launched with `npx -y`, which downloads the package at startup if it is not already there. A new agent therefore begins life able to read every home directory on the machine and run commands, using code fetched at launch. That is a fair default for a developer's own laptop. It is a bad one to carry anywhere else, and the HTTP path knows it.

## What is the server path?

The server reads environment variables. `JIVA_MODEL_BASE_URL`, `JIVA_MODEL_API_KEY`, `JIVA_MODEL_NAME`, `MCP_FILESYSTEM_ALLOWED_PATHS` and a handful of others set the defaults, and a comment in `src/interfaces/http/session-manager.ts` calls them exactly that: server-level defaults.

Here is the sentence in that file I would underline. Per-tenant stored config takes full precedence, and the environment is applied only when a tenant has no stored config yet. On a tenant's first session, the code builds a model config from the environment, API key included, and writes it to that tenant's storage. From then on the environment is not consulted for the reasoning model. The comment says it plainly: to change a tenant's model, edit their `config.json` in the bucket directly.

Think about what that does to an ordinary operations task. You rotate the model API key in your deployment settings and redeploy. New tenants get the new key. Every existing tenant keeps the old one, in their own stored file, until someone edits each file. Nothing errors until the old key is revoked. The stale copy is not a bug in the usual sense. It is a design that was reasonable for bootstrapping and has no story for rotation.

It gets odder with the second model. The tool-calling model is read from the environment on every session, never from the tenant's file. So one session can run a reasoning model from stored config and a tool-calling model from this morning's deployment. The evaluator behind the chat route (the part that checks the agent's work) builds its model from the environment only, with a default endpoint and model name written into the source. Its comment says it uses the same configuration as the main agent. For a tenant whose stored config differs from the environment, it does not.

## What is the per-session path?

The third source is a request body. A caller can send an `agentConfig` object when creating a session, and it overrides the server defaults for that session only: the model name, the tool-calling model, the MCP server list, code mode, iteration limits, a workspace directory. It is never written to storage, and secrets are deliberately not part of it. The endpoint and key still come from the tenant.

I like most of this design. A caller can narrow an agent for one job without touching anything persistent, and an empty `mcpServers` list means no tools at all for that session, which is the safest configuration there is.

It has three sharp edges.

If the session already exists, `agentConfig` is logged as a warning and ignored. The caller gets a working agent that is not the one they asked for, and no error in the response.

The type allows stdio servers (`command`, `args`, `env`), but the validator requires a `url` on every server entry. A per-session stdio server is rejected before it starts.

And the `systemPrompt` field is accepted, validated and not wired to anything. The source says so: reserved for future use.

## What would I do with this?

Whatever framework you run, ask the same four questions of it.

Which source wins when two disagree? Write the order down. If the answer needs a code read, your operations team will find out the hard way.

Where is each secret stored, and how many copies are there? If the answer is "one per tenant", rotation is a migration, not a setting.

What does a caller get back when its override is ignored? Silence is the wrong answer.

And what does a new agent start out allowed to do? Defaults are policy. The ones that suit a laptop are rarely the ones that suit production, and the same code often ships both. The [MCP production guide](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/) covers the tool side of that in more detail, and the [storage post](/blog/2026/07/08/storage-gets-a-promotion-why-agentic-ai-is-redefining-infrastructure/) covers what happens when the storage layer underneath fails quietly.

Infrastructure for agents is mostly this: not new clouds, but old questions about configuration, asked of software that can act. If you want a second pair of eyes on how your agents are set up to run, [the Gritsa team](https://gritsa.com/contact/) does that work, and [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read it yourself.
