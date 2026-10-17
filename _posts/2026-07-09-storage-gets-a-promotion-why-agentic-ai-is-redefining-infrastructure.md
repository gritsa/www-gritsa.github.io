---
layout: post
title: "When agent storage fails, it looks like an agent with no memory"
date: 2026-07-08 18:32:31 +0000
last_modified_at: 2026-10-17 18:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Agent infrastructure
  - Storage
excerpt: "The storage an agent needs is a handful of JSON files, and the way it fails is silent. Nothing crashes. The agent just forgets. Four places in Jiva's storage layer where that happens."
description: "How Jiva stores agent state: conversations, config, logs and snapshots behind one provider interface. Where a missing setting, a failed read or a skipped file turns into an agent that quietly forgets, and what to check in yours."
keywords: "AI agent storage, agent persistence, conversation storage, multi-tenant agents, silent failure, Jiva storage provider, agent state"
featured_image: "/assets/img/posts/2026-07-09-storage-gets-a-promotion-why-agentic-ai-is-redefining-infrastructure.png"
---

# When agent storage fails, it looks like an agent with no memory

*Updated 17 October 2026. This post first appeared in July as a roundup about storage hardware for long-context inference, and it ended with a performance claim about Jiva that I cannot support. I replaced it with the part I can check: how Jiva, our open-source agent framework, stores what an agent needs to remember, and how that fails. Read from the source (`src/storage`, about 1,300 lines) and from Jiva's own v0.3.46 release note.*

Most talk about storage for AI agents is about speed. Faster disks, bigger caches, memory close to the GPU. That matters if you run the model yourself. If you build agents on top of a hosted model, the storage you own is much smaller and much plainer, and it fails in a way that is easy to miss.

It fails by looking like emptiness.

## What does an agent actually need to store?

Five things, and Jiva puts all five behind one abstract class, `StorageProvider`.

- **Config**, per tenant: one `config.json` holding things like the list of tool servers an organization has switched on.
- **Conversations**: one JSON file per conversation, with every message and a metadata block (title, counts, token totals).
- **A directive** per workspace: the standing instructions the agent reads before it starts.
- **Logs**: buffered in memory, flushed to a file per session.
- **A state snapshot**, so a cloud function can hand a session to the next one.

That is the whole list. No database, no vector index. Two providers are implemented: the local filesystem for the command line, and a Google Cloud Storage bucket for hosted use. The class comment and the settings also name S3 and Redis. Ask the factory for either and it throws "not yet implemented". It is worth knowing which logos on a diagram are real.

Everything in a cloud deployment is addressed by tenant and session, both of which must come from the authenticated request. Locally, Jiva uses fixed defaults (`local` and `cli-session`) so the command line works without any login.

## Failure one: a setting that does not match falls back to local disk

The factory reads `JIVA_STORAGE_PROVIDER` and compares it to the provider names. Anything it does not recognize lands in the `default` branch, which creates the local filesystem provider.

That is not hypothetical. The v0.3.46 release note describes it happening: a Cloud Run service was configured with `gcp`, the real value was `gcp-bucket`, and the service ran on the container's own disk. Per-tenant tool lists, directives and conversation history were never read from the bucket. Nothing errored. The agent answered every question. It had simply never heard of anything a user had told it before.

The fix added aliases for `gcp`, `s3` and `aws`. The `default` branch is still there, so any other typo takes the same road. A deployment that asks for cloud storage and receives local disk should stop at startup. A fallback is the right behavior for a laptop and the wrong one for a server.

## Failure two: "not found" and "broke" are the same answer

Read a conversation from the bucket and the helper does the following: if the object does not exist, return `null`. If the download throws, log a warning and return `null`. The caller cannot tell a conversation that was never saved from one that could not be reached a moment ago.

One layer up, the conversation manager turns any failure, including this one, into `Conversation not found`. And when it saves, it first tries to load the existing conversation so it can keep the title. Its catch block says to ignore the error because it will "create new". A network blip during that read means the conversation is written back as if it were new.

The local provider is the same shape. It returns `null` for a missing file and for a file that no longer parses as JSON.

For a person, "I can't find that conversation" is a mild annoyance. For an agent resuming a task, it is a task that starts over with no warning that anything was lost. If your storage layer has one return value for "nothing there" and "couldn't look", you will eventually act on the first when the second is true.

## Failure three: the list quietly leaves things out

Listing conversations locally reads every file, and a file that fails to parse is skipped. The comment is "Skip invalid files." If the directory itself cannot be read, the result is an empty list.

On the bucket the shape is different but the cost is worse. To list conversations, the provider lists the object names under the tenant's prefix and then downloads every conversation in full, only to read the small metadata block at the top. A tenant with a few hundred long conversations pays for all of them every time the sidebar opens. I did not measure it, and I am not going to put a number on it. The pattern is enough: metadata that lives inside the big file can only be had by reading the big file.

The silent skip is the part that matters for trust. One corrupted file and the user's history is a conversation shorter than it should be, with no way to know.

## Failure four: an append that rewrites everything

The logging path has the same quiet quality. Locally, logs are appended to a file. On the bucket, an append is a read of the whole existing log, a string concatenation and a write of the whole thing back. Each flush costs the size of the log so far, and it is only safe because each session writes its own log. Two writers on the same key would overwrite each other's lines.

None of this is wrong for a first version. It works, and for one session at a time it works fine. It is the reason to know the shape of what you are running.

## What this changes about how you run an agent

You do not need faster storage to make an agent dependable. You need storage that can say no. A few habits cover most of it.

Write and read back a canary at startup. If the agent is supposed to use a bucket, put one small object in it and fetch it before accepting any work. A missing bucket, a bad credential or a mistyped setting then stops the deploy.

Make unknown configuration an error. Reject a provider name you do not recognize. Local disk is a fine default on a laptop, but a server should have to ask for it.

Keep "absent" and "failed" apart in the return type. A missing conversation is an answer. A failed read is an exception, and whoever called it should decide what to do.

Treat "fewer conversations than yesterday" as an alert. It is the cheapest test for the whole class of silent skips.

And test it the way you would test the agent's judgment: with a deliberately broken environment and a check that it refuses to run. That is the same idea as [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/), applied to the plumbing.

Storage also has a second, separate way to fail that I have left out here: two requests sharing one mutable piece of state. Jiva hit that one too, in a multi-tenant deployment, and I wrote about the pattern in [the v0.3.46 post](/blog/2026/05/20/jiva-v0-3-46-fixes-multi-tenant-concurrency-bugs/). And what happens to the contents of a conversation once it gets long is a different question, covered in [Agent memory is whatever survives the summary](/blog/2026/08/05/agentic-ai-is-leaving-the-terminal-behind/).

An agent that crashes gets fixed the same day. An agent that forgets can run for weeks. Build the storage so that forgetting is the loud failure.

If you are putting an agent into production and want the plumbing reviewed before a customer finds it, [the Gritsa team](https://gritsa.com/contact/) does that work, and [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read the code yourself.
