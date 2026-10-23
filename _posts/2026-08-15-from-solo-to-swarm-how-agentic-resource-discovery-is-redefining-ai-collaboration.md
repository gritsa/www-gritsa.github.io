---
layout: post
title: "An agent's tool list is a snapshot taken at startup"
date: 2026-08-14 22:32:26 +0000
last_modified_at: 2026-10-17 17:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - - AI agents
  - MCP
  - Tool discovery
excerpt: "Talk of agents discovering tools suggests something live. In the code of a working agent, discovery is one call at startup, and the list never changes after that. What that means in practice."
description: "How tool discovery works in Jiva's MCP client: one listing per connection, a prefixed namespace, silent startup failures, a dropped error flag and inherited secrets. What to check in any agent you run."
keywords: "MCP tool discovery, MCP client, AI agent tools, tool namespacing, MCP error handling, Jiva, agent tool list"
featured_image: "/assets/img/posts/2026-08-15-from-solo-to-swarm-how-agentic-resource-discovery-is-redefining-ai-collaboration.jpg"
---

# An agent's tool list is a snapshot taken at startup

*Updated 17 October 2026. This post first appeared in August as a roundup about agents finding each other's tools through shared registries. I could not stand behind the roundup, so I replaced it with the part I can check: how Jiva, our open-source agent framework, discovers and calls tools today, read from the source.*

When people talk about agents discovering tools, they picture something live. The agent asks, a registry answers, a new capability appears. What most agent frameworks run today is plainer. The agent reads a list when it starts, and that list is its whole world.

I read Jiva's MCP client (`src/mcp/client.ts` and `src/mcp/server-manager.ts`, about 480 lines between them) to see what that list is, and what happens when reality stops matching it.

## When does the agent learn what tools exist?

Once per connection. When Jiva connects to an MCP server, it calls `listTools()`, converts the answer to its own tool format and stores it on the connection record. That is discovery.

The client does have a `refreshTools()` method that would read the list again. I searched the source and nothing calls it. If a server adds, renames or removes a tool after startup, the agent keeps the old list until someone disconnects and reconnects that server. A removed tool still gets offered to the model, which calls it and gets an error. A new tool is never offered at all.

## What does the model actually see?

Every tool from every enabled server, on every turn. In the chat agent's loop (`src/core/agent.ts`), `getAllTools()` runs at the top of each iteration and the full result goes out with the request.

Each name is prefixed with its server, as `server__tool`, and each description with `[server]`. That is a sensible answer to two servers that both expose a tool called `search`. It also means that connecting one more server adds its whole menu to every request, whether the task needs it or not. This is the "too many tools" problem from [what breaks first with MCP servers](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/), seen from inside the client.

Routing is a string split. `executeTool` cuts the name at the first double underscore: what comes before is the server, the rest is the tool. Tool names that contain `__` themselves are fine, because the remainder is rejoined. A server name with `__` in it, or one that ends in a single `_`, will route to a server that does not exist. Small, and easy to avoid once you know. Name servers with letters and hyphens.

## What happens when a server is down?

At startup, Jiva connects to all enabled servers in parallel. A failure is logged as a warning and the others carry on. If none connect, the log says the agent "will run without external tools", and it runs.

I found no retry in this code and no timeout on the connect call. The SDK underneath may impose its own, and I did not check. The consequence is the one to plan for: an agent that was supposed to have a database tool can start without one, with nothing stopping it from taking the task. An agent with no database tool can still write a fluent answer about your database.

## What does a failed tool call look like?

`executeTool` pulls the text and any images out of the result and returns them. It never reads `isError`.

MCP lets a server mark a result as a failure and explain why in the text, so the model can correct itself. Jiva's model still receives that text, so the self-correction path works. What disappears is the flag. To the code around the model, a failed call and a successful one come back as the same kind of value, and the chat loop logs `executed successfully` for both. Only exceptions, such as a dead connection, are turned into error messages. Content that is neither text nor image is dropped, unless nothing else came back, in which case the raw result is passed through.

That matters the moment you want to count failures, cap retries or audit what the agent did. Anything built on thrown exceptions will miss every failure the server reported politely.

## What do local servers inherit?

For stdio servers, Jiva starts the child process with the agent's entire environment and lays the configured variables on top. The code comment says why: without the inherited `PATH`, launchers like `npx` and `uvx` fail. It is the pragmatic choice. It also means every local MCP server starts with every secret the agent process holds.

The same file pipes each server's stderr and discards it, so startup noise never reaches the terminal. That keeps the screen clean. It also means a server that crashes on launch leaves no trace in the agent's output beyond "failed to connect".

## What I would do with this

None of this is a flaw unique to Jiva. It is what a first working MCP client looks like, and most clients I have seen described do some version of it. Four habits follow.

Treat the tool list as a deploy artifact. If you change what a server offers, restart the agent that uses it, and do not assume it noticed.

Check at startup that the tools the job requires are present, and refuse to run if they are not. A quiet fallback to "no tools" is the worst outcome, because the agent still answers.

Run the agent with a minimal environment, so what a local server can read is a decision and not an accident.

And if you write the servers, return failures with `isError` and a message a model can act on. If you write the client, keep the flag.

The idea behind agent registries is a good one. But an agent can only use a registry if it notices the list changed, and the one I read looks exactly once.

If you are deciding which tools an agent in your business should be allowed to see, [the Gritsa team](https://gritsa.com/contact/) designs that layer, and [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read it yourself.
