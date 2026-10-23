---
layout: post
title: "A skill is a routing rule, and the description is the whole rule"
date: 2026-07-13 20:34:12 +0000
last_modified_at: 2026-10-17 11:00:00 +0530
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - AI agents
  - Agent skills
  - Context engineering
excerpt: "An agent skill is a folder with one required file. What decides whether the agent ever uses it is a single line of metadata. How Jiva loads skills, and where the loading stops short."
description: "How agent skills work in Jiva: three layers of progressive disclosure, why the description field does the routing, what the validator enforces, and what allowed-tools does not."
keywords: "agent skills, SKILL.md, progressive disclosure, context window, agent personas, Jiva, skill routing"
featured_image: "/assets/img/posts/2026-07-14-ai-agents-take-over-from-code-to-web-apps.jpg"
---

# A skill is a routing rule, and the description is the whole rule

*Updated 17 October 2026. This post first appeared in July 2026 as a roundup of three tool releases and a personal anecdote about building a web app with an agent. I could not stand behind the anecdote or the borrowed quotes, so I removed them and rewrote the post around the skills code in Jiva, our open-source agent framework.*

A skill, in the sense most agent tools now use the word, is a folder with one required file. The file is called `SKILL.md`. It has a block of metadata at the top and instructions below. That is all.

The interesting part is not the file. It is how little of it the agent sees by default.

## What does the agent see before it uses a skill?

Three layers, and only the first is always in context. The Jiva persona guide calls it progressive disclosure, and the loader in `src/personas/skill-loader.ts` is built around it.

1. **Metadata.** The name and the description. At startup Jiva scans each skill folder and parses only the frontmatter. In `persona-manager.ts`, `generateSkillsPromptBlock()` turns every skill into a small XML entry with its name, description and the path to its `SKILL.md`, and that block goes into the system prompt.
2. **The body.** The instructions. They are not in the prompt. The prompt carries one sentence telling the model that when a request matches a skill's description, it should read that skill's file with the view tool.
3. **Resources.** Scripts, reference documents and templates in subfolders. The body is supposed to say when to open them.

So a skill costs a few dozen tokens until it matters, and then it costs the whole file. A hundred skills can sit in the prompt without crowding out the task.

## Who decides when a skill is used?

The model does, by reading the descriptions and judging a match. I looked for any code that does the matching and found none. `loadSkill()` exists on the persona manager and marks content as loaded, but nothing in the agent paths calls it. The body gets read because the model chose to open the file.

That makes the description the entire routing rule. There is no keyword table, no classifier and no second chance. If the description does not read like the user's request, the skill is invisible, however good the instructions below it are.

The persona guide says as much: it tells authors to write descriptions that are "pushy" and to include every trigger phrase. I agree with the direction. A description should name the situations that call for the skill, in the words a user would use, not summarize what the skill is.

The validator keeps the field honest in two ways. A description is required, it cannot exceed 1,024 characters, and it cannot contain angle brackets, which would break the XML block it is pasted into. Names must be lowercase letters, digits and hyphens, at most 64 characters. A body over 500 lines produces a warning, not an error, with the suggestion to move detail into `references/`.

## Where does the design stop short?

Two places, both worth knowing before you rely on it.

**Skills can be shadowed quietly.** Jiva also scans a standalone skills folder in the user's home directory, plus an optional per-session folder. When two folders hold skills with the same name, the later one is skipped without a warning. The home folder is scanned first, so a skill there beats a workspace skill of the same name. If yours is not firing, check for a twin.

**`allowed-tools` is a hint, not a fence.** A skill can declare which tools it may use. I searched the code for anywhere that list restricts tool access and found only one use: the dual-agent setup prints it into the context given to the validating agent, so the supervisor knows what the worker was expected to use. Nothing blocks a call. If you need a skill to be unable to run shell commands, the skill file is the wrong place to say so.

## What I would do with this

Write the description last, and test it as a search query. Take five real requests a user might make. For each, ask whether the description would make you open this file. If you would not, the model will not either.

Then keep the body short enough that opening it is cheap, and push anything bulky into references the body points at by name. The saving from progressive disclosure disappears the moment every skill is a 500 line wall of text that the model reads in full whenever it fires.

None of this is specific to Jiva. Any agent that ships skills as folders has the same shape: a cheap index in the prompt, an expensive body behind it, and a model deciding between them on the strength of a sentence. Whoever writes that sentence is doing the routing.

If you are working out how to give an agent reusable expertise without bloating its context, [the Gritsa team](https://gritsa.com/contact/) builds exactly this kind of setup, and [Jiva](https://github.com/KarmaloopAI/Jiva) is open source if you would rather read the code.
