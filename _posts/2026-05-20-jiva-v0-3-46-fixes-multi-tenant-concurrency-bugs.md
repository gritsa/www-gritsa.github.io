---
layout: post
title: "Jiva v0.3.46 Fixes Multi-Tenant Concurrency Bugs"
date: 2026-05-20 08:00:00 +0000
author: "Gritsa"
categories: "AI Technology"
tags: "agentic AI, autonomous agents, Jiva"
excerpt: "Jiva v0.3.46 fixes six concurrency bugs in the HTTP and Cloud Run interface. One shared object, mutated across an await, let one tenant's requests write into another tenant's storage path."
description: "What changed in Jiva v0.3.46: the shared storage provider that corrupted cross-tenant GCS paths, a session race that leaked sub-processes, a logger singleton that mixed tenants, and the gcp alias that silently fell back to local storage."
keywords: "Jiva, multi-tenant, concurrency, Cloud Run, storage provider, session isolation, AI agent framework"
featured_image: "/assets/img/posts/2026-05-20-jiva-v0-3-46-fixes-multi-tenant-concurrency-bugs.png"
---

Updated 2026-10-16: rewritten from the v0.3.46 release notes. The original post summarized the changelog and added claims the notes do not make.

Jiva v0.3.46 was released on May 15, 2026. It fixes a set of concurrency bugs that made the HTTP and Cloud Run interface unsafe when several tenants used it at once. Most of them come from one mistake, and it is a mistake worth recognizing in your own agent code: an object created once at startup, shared by every session, and changed by each one.

## The root cause

At startup the server created one `GCPBucketProvider`. Every new HTTP session called `setContext()` on that same object to say which tenant and session it belonged to. Creating a session is async and makes several calls to Google Cloud Storage. If tenant B's session started while tenant A's was between two of those calls, tenant A's next read or write used tenant B's path.

The symptom was quiet. Data looked missing, or showed up in the wrong place. Nothing threw.

## The six fixes

**1. `JIVA_STORAGE_PROVIDER=gcp` fell through to local storage.** The canonical value is `gcp-bucket`, and the short form `gcp` matched no case in the factory, so it hit the default branch and used the container's ephemeral filesystem. Per-tenant MCP server lists, directives and conversation history were never read from GCS. The factory now maps `gcp` to `gcp-bucket` and `s3` or `aws` to `aws-s3`.

**2. The shared storage context.** The fix is a new method, `createSessionScoped(context)`, that returns a provider with a fixed context that never changes. The scoped provider shares the stateless pieces (the GCS bucket client and a config cache keyed by tenant ID) and owns the mutable ones (its context and its log buffer). The session manager now stores one scoped provider per session and sends every storage operation through it. The shared object's context is never mutated while serving requests.

**3. `setConfig()` read its context after an `await`.** It awaited the config cache first and only then looked up the tenant path, so a concurrent `setContext()` could redirect the write. It now captures the context and path before the first `await`.

**4. Duplicate sessions.** Two simultaneous requests for the same tenant and session on a cold start could each create a session, with two agents and two sets of MCP sub-processes. The second overwrote the first in the sessions map and the first one's sub-processes leaked. The session manager now keeps a map of pending creations, and a second caller awaits the same promise instead of starting its own. The pending entry is removed in a `finally` block whether creation succeeds or fails.

**5. Teardown wrote to the wrong tenant.** When a session was destroyed on idle timeout or shutdown, saving the conversation and flushing logs went through the shared provider, which held whichever context was set last. Teardown now uses the session's own provider.

**6. The orchestration logger mixed tenants.** It was a strict singleton, so every concurrent session's manager, worker and client events went to the most recently registered session's GCS path. Each session now gets its own logger. The command-line interface keeps the old singleton, so nothing changes there.

The release notes also point to the v0.3.45 notes for further small bug fixes.

## What to take from it

All six bugs have the same shape. State that belongs to one request lived in an object that belonged to all of them, and an `await` gave another request the chance to change it. Moving the mutable part into a per-session object removed the whole class. Locking the shared one would have worked only until the next engineer added a new field to it.

If you are building a multi-tenant agent service, check two things before anything else. Does any singleton hold a tenant ID, a path or a credential? And does any function read that value after an `await`? Both are cheap to find and expensive to find in production.

## Upgrade

```bash
npm install -g jiva-core@0.3.46
```

On Cloud Run, set the canonical value. `gcp` still works through the alias:

```yaml
- name: JIVA_STORAGE_PROVIDER
  value: gcp-bucket
```

The notes describe the changes as additive. The command-line mode and the public provider and agent interfaces are unchanged. Each tenant's configuration lives at `gs://{bucket}/{tenantId}/config.json` and is read from GCS at the start of every new session.

Jiva is open source: [github.com/KarmaloopAI/Jiva](https://github.com/KarmaloopAI/Jiva). If you want agents like this running in your own environment, see Gritsa's [AI agent services](/services/ai-agents/).
