---
layout: post
title: "LLM lock-in is not where you think it is"
date: 2026-10-26 09:02:00 -0400
author: "Amy Loomis"
categories: "AI Technology"
tags:
  - LLM lock-in
  - Open models
  - AI evaluation
excerpt: "Swapping the model is a config change. Knowing the swap worked is the project."
description: "LLM vendor lock-in is rarely the API. It is the quirks your code absorbed and the test you never wrote. What a model-agnostic framework shows."
keywords: "LLM vendor lock-in, switch LLM provider, model agnostic AI"
featured_image: "/assets/img/posts/2026-10-26-llm-lock-in-quirks.jpg"
---

# LLM lock-in is not where you think it is

When someone says "we can always swap the model," they are usually right about the swap and wrong about the cost. Changing the model name in a config file takes a minute. Finding out whether everything around it still works is the project, and that is where lock-in actually lives: in the quirks your code quietly absorbed, and in the test you never wrote.

I find it useful to look at software that was built specifically to avoid lock-in, because the scar tissue shows. [Jiva](https://github.com/KarmaloopAI/Jiva), the open-source agent framework we build at Gritsa, talks to any provider that exposes an OpenAI-style chat endpoint. On paper, that is the whole story. Point it somewhere else and go.

Now open the model client's config. Besides the endpoint, key and model name, there are eight optional behavior settings. A flag for one provider's tool-call format, which has to be parsed out of text instead of read from a field. A setting for how to tell the model how hard to think, because one provider wants it as a request parameter, another strips unknown parameters and only honors a line in the system prompt, and for unknown providers the code does both. A token ceiling that has to be set explicitly, because a model that spends its output budget on reasoning returns an empty answer. A requests-per-minute limit, because a free tier has one.

Not one of those exists to pick a model. Each exists because a specific provider behaved differently from the others and someone had to make the difference stop mattering. That is what "model agnostic" looks like from the inside. It is a thin, honest layer of accumulated exceptions.

The retry loop tells the same story. It retries on 403, 429 and the usual server errors, up to four times. For a rate limit it reads the standard Retry-After header first, because some providers only send the header and others only put the wait time in the message body, so the code falls back to parsing "try again in 8 seconds" out of English prose, and only then to plain backoff. There is even a branch that notices a provider answering "this model only supports streaming" and flips itself into streaming mode for good. Nobody sat down and designed that. Production produced it.

Here is the part I care about. None of this is lock-in to a vendor. It is lock-in to your own accumulated workarounds, and it is invisible until you change something. Teams that build directly on one provider's SDK have the same pile, they just never see it as a pile. It reads as "how the app works." Then the day the price changes, or a better model appears, the swap fails somewhere three layers away from the config file.

So the portability you want is not "the API is the same." It is "I can tell, in an afternoon, whether the new setup is any good." That needs a test that does not care which model it is grading. Jiva ships one for this reason. Tasks run in throwaway workspaces and are scored by Node's test runner, with no model judging another model, and when a task fails because the provider capped the output at 4,096 tokens, the report labels it as output-limited instead of letting it pass for a reasoning failure. The label matters. It separates "this model is worse" from "this configuration is wrong," and those lead to opposite decisions. I walk through what that cap does in practice in [how to run a coding agent on Sarvam-105B](/blog/2026/10/28/run-a-coding-agent-on-sarvam-105b/).

If you are weighing the lock-in question for your own stack, skip the vendor comparison and ask two things. What would you have to change in your code if the provider disappeared on Friday? And if you changed it, what would tell you on Monday that the agent was still doing its job? The first answer is often shorter than you fear. The second is often "nothing," and that is the real dependency. It is the same gap I described in [writing the test before you hire the agent](/blog/2026/10/12/write-the-test-before-you-hire-the-agent/).

We start every [agent engagement](/services/ai-agents/) with that test, partly because it makes the model choice reversible. A model you can re-score in an afternoon is a model you rent. One you can't is a model you married.
