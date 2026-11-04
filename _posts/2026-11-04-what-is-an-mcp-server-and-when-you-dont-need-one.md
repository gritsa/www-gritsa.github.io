---
layout: post
title: "What is an MCP server, and when you don't need one"
date: 2026-11-04 08:15:00 -0500
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - MCP
  - AI agents
  - Integration
excerpt: "An MCP server lets a model discover and call your tools. If your own code makes the call, you may not need one."
description: "What an MCP server is, what it adds over a plain API, and the questions that tell you whether your project needs one at all."
keywords: "what is an MCP server, MCP vs API, when to use MCP, MCP server explained, Model Context Protocol"
featured_image: "/assets/img/posts/2026-11-04-what-is-an-mcp-server.jpg"
---

# What is an MCP server, and when you don't need one

An MCP server is a program that tells an AI application what it can do and then does it on request. It publishes a list of tools, each with a name, a plain-language description and a schema for its inputs, so a model can pick one and call it without anyone writing glue code for that pairing. MCP stands for Model Context Protocol, and the protocol is the standard way to have that conversation.

That is the whole idea. Here is the part that gets lost: the standard covers the conversation, not what is said in it. If the thing calling your system is code you wrote, one that always makes the same three calls in the same order, you do not need an MCP server. You need an API call.

## What is an MCP server, in plain words?

Three roles, and the spec names them. The **host** is the AI application the person is using. The host creates one **client** for each server it connects to, and each client keeps a dedicated connection to its **server**. The server, in the spec's words, is "a program that provides context to MCP clients."

Servers can offer three kinds of thing. Tools are functions the model can invoke, like querying a database. Resources are data it can read, like a schema or a file. Prompts are reusable templates. Most of the conversation about MCP is really about tools, so I will stay there.

Where the server runs is a separate question. A local server talks to the host over standard input and output on the same machine. A remote server talks over HTTP and can serve many clients. Same protocol, very different risk, which is a topic for [the last MCP post I wrote](/blog/2026/10/07/mcp-servers-in-production-what-breaks-first/).

## What does MCP add over a normal API?

Two things, and both only matter when the caller is a model.

**Discovery at runtime.** A client sends `tools/list` and gets back every tool with its description and input schema. The model reads those descriptions and decides which to use. Nobody had to hard-code "when the user asks about invoices, call this endpoint." The spec calls tools "model-controlled," meaning the model can discover and invoke them based on the conversation. A server can also say its list has changed, and the client asks again.

**Reuse across hosts.** The project's own introduction calls it "build once and integrate everywhere." If three different AI applications in your company need the same ticketing system, one server serves all of them, rather than three custom integrations.

Now what it does not add. It does not make the tool safe: the spec lists what servers must do, such as validate inputs and rate limit calls, and says plainly that these are the server's job. It does not make the model choose well. And it does not say anything about how the host uses the model. The architecture page states that MCP "does not dictate how AI applications use LLMs or manage the provided context."

The project describes MCP as a USB-C port for AI applications. I like the picture and want to push on it. A USB-C port tells you the plug fits. It says nothing about what you plugged in.

## When don't you need an MCP server?

My position, and it is a position: more teams are building servers than need them. Here are the cases where I would skip it.

**The workflow is fixed.** Picture a nightly job that pulls yesterday's orders, checks them against a rule set and writes a summary. Your code decides every step. The model, if there is one, only writes the summary. Discovery has nothing to discover, because the list of tools never changes and the model never chooses. Call the order system's API directly and hand the model the data.

**One app, one integration, and you own both ends.** If you control the application and the system it calls, a function the model can call, defined in your own code, does the same job with less to run and less to secure. A server is a second program with its own deployment, credentials and logs.

**The tool you would expose is "run anything."** A single tool that accepts a free-text query or shell command is not an integration, it is a hole with a protocol around it. Fix the tool before you wrap it.

## When does an MCP server earn its place?

When the caller really is a model deciding at runtime, and at least one of these is true.

Many tools, owned by different teams, and a model that has to pick among them. Picture an internal catalog where finance, support and operations each publish their own tools and any AI application in the company can use them. That is the shape MCP was built for.

More than one host needs the same capability. This is the "build once" case, and it is the strongest argument.

The set of tools changes depending on who is asking or what state the system is in. The listing mechanism handles that without a redeploy of every client.

Even then, there is a cost people forget. Every tool's name, description and schema is text the model has to read before it does anything. The spec's own architecture guide mentions "progressive tool discovery" for clients that connect to many servers, rather than loading every tool up front. [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build with, takes a similar line in its code mode: it does not load all MCP servers by default because, in its README's words, too many tools bloat the context. You opt in to the servers a task needs.

## Four questions to ask before anyone builds one

1. Who is the caller: your code, or a model choosing at runtime? If it is your code, stop here.
2. Will a second application want the same tools within a year? If not, a plain function may be enough.
3. Can you describe each tool in one sentence a model could not misread? If you cannot, the tool is too broad.
4. Who is accountable when the model calls it wrongly? Name a person, and decide where the human approval step sits.

## A note on versions

The spec ships in dated versions, and it has moved. I read the tools page from the 2025-06-18 version and the architecture and base-protocol pages from 2026-07-28. The newer version is explicit that the protocol is stateless: every request carries what the server needs, and anything that spans requests has to be an identifier the client passes back. If you are evaluating an SDK or a vendor's server, ask which version it speaks. "Supports MCP" is not one answer.

## Where this leaves you

Most of the value in an AI agent project sits in what the tools do and who is allowed to call them, not in the plumbing between the model and the tool. MCP makes the plumbing cheaper. That is useful, and it is also the reason to be suspicious of any plan whose first milestone is "stand up an MCP server."

If you are deciding what an agent should be able to touch, and which of those things deserve a server, that is the question our [AI agents service](/services/ai-agents/) is built around: agents scoped to a job function, with defined decision boundaries for what they may do alone and what needs approval, connected to your systems through their APIs.

The better question was never whether you have an MCP server. It is whether you could say, in one sentence, what the model is allowed to do with it.

*Sources: the Model Context Protocol [introduction](https://modelcontextprotocol.io/docs/getting-started/intro), [architecture guide](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) and [specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), read in full and re-checked 2026-11-04 (latest version 2026-07-28), and the Jiva README. The two examples above are hypotheticals, not client stories.*
