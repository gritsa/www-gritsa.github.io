---
layout: post
title: "MCP servers in production: what breaks first"
date: 2026-10-07 09:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - MCP
  - AI agents
  - AI governance
excerpt: "The protocol is rarely what fails. Tool sprawl, broad permissions and borrowed tokens are, usually in that order."
description: "MCP server best practices from the spec: what breaks first in production, from tool sprawl and broad scopes to token passthrough, and how to fix each."
keywords: "MCP server best practices, MCP security, MCP servers in production, what is an MCP server, MCP tool design"
featured_image: "/assets/img/posts/2026-10-07-mcp-servers-in-production.jpg"
---

An MCP server is a small program that exposes tools, data and prompts to an AI model through the Model Context Protocol, so an agent can query a database or file a ticket without custom glue code for each system. Connecting one takes an afternoon. Keeping one safe, cheap and understandable for a year is the actual project.

I haven't run a fleet of MCP servers for a client, and I won't pretend to. What follows is built from the protocol's own specification and security guidance, plus how [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build with, handles the same problems. The ordering, what breaks *first*, is my opinion. The failure modes themselves are documented.

## What breaks first when an MCP server meets real use?

In my reading, the order is: the model gets buried in tools, the tools are too broad, the credentials are borrowed, the errors don't help, and nobody can say afterward who did what. Each one is a design decision made in the first week and discovered in the fourth month.

## 1. Too many tools

Every tool you connect has a name, a description and a schema, and all of it lands in the model's context on every turn. Connect five servers with twenty tools each and you've handed the model a hundred-item menu before it reads the user's question.

Jiva's own documentation is blunt about this. Its code mode does not load every configured server by default, because, in the README's words, too many tools bloat the context. You opt servers in by name. That's a framework author telling you what they learned the hard way.

The fix is boring. Give each agent only the servers its one job needs. An agent that reconciles invoices does not need the browser server. If two servers both expose a tool called `search`, the spec says clients "SHOULD implement a disambiguation strategy such as prefixing tool names with a server identifier." Do it before the model has to guess.

## 2. Tools that are too broad

The fastest MCP server to write has one tool: `run_sql`. It also hands the agent every table, every column and every `DELETE` the database user is allowed to run.

Ten narrow tools beat one wide one. `get_invoice_status(invoice_id)` can be validated, rate limited and logged in a way a free-text query never can. The spec's security section is explicit that servers must validate all tool inputs, implement access controls, rate limit invocations and sanitize outputs. A single `run_sql` makes every one of those four close to impossible, because the input *is* the program.

Scopes have the same problem one level up. The spec's security guidance lists the usual mistakes: publishing every possible scope, using wildcards like `*` or `full-access`, and bundling unrelated privileges "to preempt future prompts." Its recommendation is a progressive model. Start with a minimal read-only scope and step up only when a privileged operation is first attempted. A stolen token with `db:*` on it is a much worse afternoon than one that could only read.

## 3. Borrowed credentials

This is the one I'd lose sleep over. The tempting design is a server that takes whatever token the agent's client presents and forwards it to the downstream API. It's easy, and the spec has a name for it: token passthrough, an anti-pattern it explicitly forbids. The rule is stated flatly: MCP servers "MUST NOT accept any tokens that were not explicitly issued for the MCP server."

The reason is practical, not bureaucratic. If the server forwards tokens untouched, rate limits and monitoring that depend on who the token was issued to are bypassed. The downstream logs show a different identity than the one actually calling. And a stolen token can use your server as a pipe.

If your server proxies a third-party API, there is a second trap, the confused deputy problem. A proxy that uses one static OAuth client ID, lets clients register dynamically, and relies on a consent cookie can be tricked into handing an authorization code to an attacker without the user ever seeing a consent screen. The spec's fix is per-client consent that the MCP server itself enforces, with exact-match redirect URIs. If you're buying or building an MCP server that fronts a SaaS product, ask the vendor how they handle this. A blank look is an answer.

## 4. Errors the model can't use

Agents recover from mistakes when the mistake is explained. The spec splits failures into two kinds. Protocol errors (unknown tool, malformed request) are things a model is unlikely to fix. Tool execution errors, such as a date in the wrong format or a value out of range, come back in the result with `isError: true`, and clients should pass them to the model so it can correct itself.

The spec's own example is a good standard: "Invalid departure date: must be in the future. Current date is 08/08/2025." That error tells the model what was wrong and what right looks like. Compare it to a stack trace, or a bare `500`. One teaches the agent. The other makes it retry the same call four times and burn your budget.

```json
{
  "isError": true,
  "content": [{
    "type": "text",
    "text": "invoice_id INV-2291 not found. IDs look like INV-0001 to INV-9999."
  }]
}
```

## 5. State that anyone can guess

The current version of the protocol has no sessions. If your tools need to remember something between calls, like a cart or an open workflow, you return a handle and the model passes it back as an argument. The spec's security page names the risk: state handle hijacking, where a guessed or leaked handle lets someone operate on another user's state.

Two rules from the spec cover most of it. Never treat possession of a handle as authentication, and bind each handle to the authenticated user on the server, keyed from the verified token rather than anything the client supplies. Make handles random and let them expire.

## 6. The local server nobody reviewed

Local MCP servers run on a person's machine with that person's privileges. The spec's example of a malicious startup command is not subtle: a package install chained to a `curl` that posts `~/.ssh/id_rsa` to a stranger's server. It requires clients to show the exact command before running a one-click install, and recommends sandboxing.

For a company, this is a policy question, not a technical one. Who is allowed to add an MCP server to a laptop that can reach production? If the answer is "anyone who finds one on a forum," you have a software supply chain with a chat interface on top.

## 7. Nobody can say who did what

The spec says clients should log tool usage for audit purposes and show users tool inputs before calling, so sensitive data doesn't leave by accident. It also says there should always be a human in the loop with the ability to deny tool invocations. Note the wording: *should*, not *must*. The protocol leaves the line to you.

My own position, and it's a position, not a finding: put the human at the edge of irreversibility, not in every loop. Let the agent read freely and draft freely. Require approval for money, deletion, anything a customer sees. That only works if the log can answer, for any action, which agent, on whose authority, with which arguments. Decide the format before the first incident, not during it.

One more caution from the spec: clients must treat tool annotations such as "read-only" or "destructive" as untrusted unless they come from a trusted server. A tool that calls itself harmless is making a claim, not providing a guarantee.

## A short checklist before you connect the next server

- Does the agent need this server for its one job? If not, leave it out.
- Is there a narrow tool for each action, or one tool that accepts a program?
- Are scopes minimal, and does the token carry only the audience it was issued for?
- Do errors say what was wrong and what right looks like?
- Are state handles random, expiring and bound to a user?
- Who approved this server, and can you see its exact startup command?
- Can you answer "who did what" from the logs alone?

None of this is exotic. It's the same discipline you'd apply to giving a new hire system access: decide the job, then grant the minimum. It's also the first conversation in every [production agent project we take on](/services/ai-agents/), before anyone writes a prompt, and it usually leads straight to the data underneath, which is where [the real work tends to be](/services/data-engineering/). If you read my [earlier piece on AI buyers](/blog/2026/10/06/your-next-b2b-buyer-might-be-an-ai-agent/), this is the other side of that table: once agents can act on your systems, the question stops being "can they reach us" and becomes "what should they touch."

*Sources: the Model Context Protocol specification (the [tools](https://modelcontextprotocol.io/specification/latest/server/tools) and [security best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) pages, read 2026-10-07), and the Jiva README.*
