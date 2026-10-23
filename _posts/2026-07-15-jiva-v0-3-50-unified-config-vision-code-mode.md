---
layout: post
title: "Jiva v0.3.50: one config file, proactive rate limits and native vision"
date: 2026-07-14 18:32:12 +0000
author: "Gritsa"
categories: "AI Technology"
tags:
  - agentic AI
  - autonomous agents
  - Jiva
excerpt: "Jiva v0.3.50 moves the CLI and the HTTP interface onto one config file, waits before it hits a provider's rate limit, and lets a single model handle both reasoning and images."
description: "What changed in Jiva v0.3.50: one config file at ~/.jiva/config.json, proactive rate limiting with Retry-After, vision detection in setup, native vision for reasoning models and a skeleton-first code mode."
keywords: "Jiva, autonomous agents, rate limiting, vision models, code mode, configuration, open source"
featured_image: "/assets/img/posts/2026-07-15-jiva-v0-3-50-unified-config-vision-code-mode.jpg"
---

Updated 2026-10-16: rewritten from the v0.3.50 release notes. The original post restated the changelog in marketing language and glossed over what each change fixes.

Jiva v0.3.50 was released on July 14, 2026. The thread through it is providers that are more constrained than the defaults assume: a hard request ceiling, a small output budget, a single model that also reads images. Most of the release is Jiva adjusting to that. Three other fixes from the same release, the ones that share a cause, have [their own write-up](/blog/2026/07/16/jiva-v0-3-50-unified-config-vision-code-mode-boost/).

## The CLI and the HTTP interface now share one config file

Until this release, the CLI kept its config in a platform-specific place chosen by the `conf` package: `~/Library/Preferences/jiva-nodejs` on macOS, `%APPDATA%/jiva-nodejs/Config` on Windows, `~/.config/jiva-nodejs` on Linux. The local HTTP interface had always used `~/.jiva/config.json`, next to its conversations and logs. They were different files, so a change made through one did not reach the other, and nothing said so.

`ConfigManager` now pins the CLI to `~/.jiva`, so both read and write the same file. The first time it starts, `migrateLegacyConfigIfNeeded()` copies a legacy config over if the new file does not exist yet. If something is already at the new path when the copy happens, it is backed up to `config-backup.json` first rather than overwritten. After that, `~/.jiva/config.json` is authoritative and the migration never runs again. The CLI prints the result on the next `jiva` invocation, and the HTTP interface logs it as a warning at startup.

## Rate limiting that waits instead of reacting

A new `maxRequestsPerMinute` setting on the model client makes it keep its own request timestamps in a trailing 60-second window and wait before sending a request that would break the limit. Before, Jiva reacted to a 429 after it happened. The release was motivated by Sarvam-105B, which allows 40 requests a minute and 4096 output tokens, and the Sarvam preset in the setup wizard now sets 40 for you. The setting works for any provider with a known ceiling.

When a 429 does arrive, Jiva reads the standard `Retry-After` header first (RFC 6585). It parses provider-specific wording out of the error body, such as Groq's "Please try again in 8.53s.", only when the header is missing.

## One model for reasoning and images

Some providers offer a single model that reasons and sees images. Groq's `llama-4-maverick` is one example the notes give. For those setups, the separate `multimodal` model and its caption-then-forward detour are wasted work.

A new `hasVision` flag lets any configured model declare native vision support, whatever its type. When an image arrives, the routing order is:

1. a dedicated multimodal model, if one is configured (unchanged legacy behavior)
2. the reasoning model, if it has `hasVision`
3. the tool-calling model, if it has `hasVision`
4. the legacy passthrough

Existing setups with a `multimodal` model behave as before. The two agent types, `DualAgent` and `CodeAgent`, needed no change because both send every model call through the orchestrator.

The setup wizard now asks "Does this model support vision (image input)?" right after you enter the model name. A new `src/utils/vision-detection.ts` matches the name against known vision-capable families and uses the result only as the default answer, with the reason shown, for example "Llama 4 Maverick supports vision". You can override it. `jiva config --show` also prints a `Vision: Yes/No` line. Before this release the flag could only be set by editing `config.json` by hand.

## A skeleton-first workflow for small output budgets

When a reasoning model's `defaultMaxTokens` is 8192 or less, code mode's system prompt now requires the model to scaffold every new file as `### section-<name>` and `### endsection` blocks and fill them one at a time, and it states the exact token budget. Before, that advice applied only to large files. To make this dependable, `edit_file` gained a `use_regex` mode: `old_string` is compiled as a regex, so a whole section can be replaced by matching its markers without reproducing the stub inside.

## More metadata on code-mode conversations

Saved code-task conversations now record which MCP servers were enabled and the iteration budget, plus a free-form field for the run mode. Values saved earlier persist across later auto-saves that do not repeat them. The type for this metadata also existed twice, with the copies drifting apart. It now lives once, in `storage/types.ts`.

## The bug fixes

- **A directive became a second system message.** `ManagerAgent` appended it as an extra message, and strict providers answered `400 System message must be at the beginning`. The notes name Qwen3.6 on Krutrim as one that rejected it. The directive is now merged into the single system message.
- **Code mode stopped after about ten iterations with `maxIterations` at 100.** Context compaction only ran when the last response had tool calls, so once the model began returning empty responses the bloated prompt was resent unchanged and failed the same way each time. Compaction now runs whenever the prompt is over the threshold.
- **The CLI ignored `defaultMaxTokens` and `reasoningEffortStrategy`.** All four places that build a model client dropped both settings, so a 4096-token cap for Sarvam never reached the request.
- **Conversation titles were snippets or leaked reasoning.** The next post covers this one with the two above.

## Upgrade

```bash
npm install -g jiva-core@0.3.50
```

The release notes list no breaking changes, and existing configs keep working. If you run on Sarvam and have not run `jiva config` since before this release, running it picks up the new rate limit default. The source and full notes are on [GitHub](https://github.com/KarmaloopAI/Jiva/releases/tag/v0.3.50).
