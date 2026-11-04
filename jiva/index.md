---
layout: page
title: Jiva, the open-source AI agent framework
description: Jiva is an MIT-licensed autonomous agent for the terminal and cloud. Any OpenAI-compatible model, MCP tools, a code mode, and Sarvam-105B support.
permalink: /jiva/
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "name": "Jiva",
      "url": "https://gritsa.com/jiva/",
      "description": "Jiva is an open-source (MIT) autonomous AI agent for the terminal and cloud. It works with any OpenAI-compatible model provider, uses MCP servers for tools, and has a general mode and a code mode.",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "macOS, Linux, Windows",
      "license": "https://opensource.org/licenses/MIT",
      "isAccessibleForFree": true,
      "sameAs": [
        "https://github.com/KarmaloopAI/Jiva",
        "https://www.npmjs.com/package/jiva-core"
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://gritsa.com/" },
        { "@type": "ListItem", "position": 2, "name": "Jiva", "item": "https://gritsa.com/jiva/" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is Jiva?",
          "acceptedAnswer": { "@type": "Answer", "text": "Jiva is an open-source (MIT) autonomous AI agent for the terminal and cloud. It works with any OpenAI-compatible model provider, uses MCP servers for tools, and runs in two modes: a general mode with a Manager agent and a Worker agent, and a code mode for software engineering." }
        },
        {
          "@type": "Question",
          "name": "Does Jiva work with Sarvam-105B?",
          "acceptedAnswer": { "@type": "Answer", "text": "Yes. Sarvam-105B has been supported as a reasoning model since Jiva v0.3.42, with a setup preset, handling of Sarvam's tool-call format, and recovery when a large file write hits Sarvam's 4096-token output cap. That cap still limits very large single writes." }
        },
        {
          "@type": "Question",
          "name": "Is Jiva free to use?",
          "acceptedAnswer": { "@type": "Answer", "text": "Jiva itself is free and MIT licensed. You pay your model provider for the tokens you use, and for anywhere you choose to host it." }
        },
        {
          "@type": "Question",
          "name": "Which models can Jiva use?",
          "acceptedAnswer": { "@type": "Answer", "text": "Any model behind an OpenAI-compatible API. The setup wizard has presets for Krutrim, Groq, Sarvam and OpenAI, and the documentation shows a local Ollama example." }
        },
        {
          "@type": "Question",
          "name": "How is Jiva different from a chatbot?",
          "acceptedAnswer": { "@type": "Answer", "text": "A chatbot answers. Jiva plans a task, calls tools such as the file system, a browser or a shell, checks the result, and keeps going until the job is done." }
        }
      ]
    }
  ]
}
</script>

<div class="container" style="padding: 60px 0; max-width: 860px;">

<p><strong>Jiva is an open-source (MIT) autonomous AI agent for the terminal and cloud.</strong> It works with any OpenAI-compatible model provider, uses MCP servers for its tools, and runs in two modes: a general mode for multi-step tasks and a code mode for software engineering. Gritsa builds its production agents on it.</p>

<p>Source: <a href="https://github.com/KarmaloopAI/Jiva">github.com/KarmaloopAI/Jiva</a>. Package: <a href="https://www.npmjs.com/package/jiva-core">jiva-core on npm</a>. This page was checked against Jiva v0.3.53 on 4 November 2026.</p>

<h2>Jiva at a glance</h2>
<table class="table">
<tbody>
<tr><th scope="row">What it is</th><td>An autonomous agent that plans a task, uses tools and checks its own work</td></tr>
<tr><th scope="row">License</th><td>MIT</td></tr>
<tr><th scope="row">Install</th><td><code>npm install -g jiva-core</code>, then <code>jiva setup</code> (Node 20 or newer)</td></tr>
<tr><th scope="row">Models</th><td>Any OpenAI-compatible endpoint. Setup presets for Krutrim, Groq, Sarvam and OpenAI</td></tr>
<tr><th scope="row">Tools</th><td>MCP servers. The file system server is on by default; browser automation and shell servers can be added</td></tr>
<tr><th scope="row">Modes</th><td>General mode (Manager and Worker) and code mode (<code>--code</code>)</td></tr>
<tr><th scope="row">Runs</th><td>In a terminal, from a TypeScript API, or as a service on Google Cloud Run</td></tr>
</tbody>
</table>

<h2>Two modes</h2>
<p><strong>General mode</strong> is a two-agent pipeline. A Manager agent plans the task and splits it into subtasks. A Worker agent carries them out with the configured MCP tools. The Manager then pulls the results into one answer. Simple conversational messages are answered directly, without subtasks. Tools arrive through MCP, the Model Context Protocol; if that is new to you, start with <a href="/blog/2026/11/04/what-is-an-mcp-server-and-when-you-dont-need-one/">what an MCP server is, and when you don't need one</a>.</p>
<p><strong>Code mode</strong> (<code>jiva chat --code</code>) is a single loop built for software engineering. The model is called with tool definitions, the tools run inside the Jiva process, and after every file edit Jiva asks the relevant language server for compiler errors and hands them back to the model. The edit tool tries nine matching strategies, so small indentation drift does not break an edit. A plan-then-approve flag (<code>--plan</code>) makes the agent show its plan before it touches files.</p>

<h2>Give the agent a job description</h2>
<p>Jiva reads a directive file from your project root. In it you write the agent's purpose, tasks, constraints and context, in plain language. Jiva looks for <code>jiva-directive.md</code> first and falls back to <code>AGENTS.md</code> and <code>.jiva/directive.md</code>. The guide on <a href="/blog/2026/10/21/how-to-scope-an-ai-agent/">how to scope an AI agent</a> explains why this file does so much of the work.</p>

<h2>Jiva on Sarvam-105B</h2>
<p>Sarvam-105B is an Indian open reasoning model. Jiva has supported it as a first-class reasoning model since v0.3.42. In practice that means four things, all described in the Jiva documentation:</p>
<ul>
<li>a setup preset, so <code>jiva setup</code> fills in the endpoint, model name and reasoning settings;</li>
<li>transparent handling of Sarvam's XML-format tool calls;</li>
<li>fixes (v0.3.48) that stopped Sarvam rejecting file-edit calls, found by running Jiva's benchmark against it;</li>
<li>automatic recovery when a large file write hits Sarvam's output cap.</li>
</ul>
<p><strong>The limit, plainly:</strong> Sarvam's API caps output at 4096 tokens per response, so a very large single write is still limited. Jiva's benchmark flags those failures as <code>[output-limited]</code> so you can tell them from logic failures. We have not published benchmark scores comparing Jiva on Sarvam-105B with other agents or other models, and we do not claim parity with frontier models.</p>
<p>As far as we know, Jiva is the only autonomous agent with first-class coding capabilities that runs with Sarvam-105B. We have not found another that documents it. If you know of one, tell us and we will correct this page the same day. The step-by-step version is in <a href="/blog/2026/10/28/run-a-coding-agent-on-sarvam-105b/">How to run a coding agent on Sarvam-105B</a>.</p>

<h2>Measure the model, not the marketing</h2>
<p><code>jiva benchmark</code> runs a set of coding tasks against your own model and configuration, in throwaway workspaces, and scores them with Node's built-in test runner. There is no model acting as judge. One suite is a gate: a healthy setup passes every task. A second suite builds a small REST API against a specification and reports the percentage of spec tests that pass, which is how you compare two models or two settings. The same habit applies to any agent you plan to hire: <a href="/blog/2026/10/12/write-the-test-before-you-hire-the-agent/">write the test first</a>.</p>

<h2>Try it</h2>
<pre><code>npm install -g jiva-core
jiva setup        # pick a provider, paste your API key
jiva benchmark    # check your model and settings work in code mode
jiva chat --code  # start a coding session
jiva run "What changed in the last 5 commits?"</code></pre>
<p>Model choice is a configuration line, not a rewrite. That is deliberate. Why it matters is the subject of <a href="/blog/2026/10/26/llm-lock-in-is-not-where-you-think-it-is/">LLM lock-in is not where you think it is</a>.</p>

<h2>How Gritsa uses Jiva</h2>
<p>Gritsa builds agents for businesses on Jiva: agents that take over a job function instead of answering questions. Because Jiva is open source and model-agnostic, a client is not tied to one model or one vendor's runtime. If you want an agent built, start at <a href="/services/ai-agents/">Autonomous AI agents</a>. If you only want the framework, take it from GitHub.</p>

<h2>Questions</h2>

<h3>What is Jiva?</h3>
<p>Jiva is an open-source (MIT) autonomous AI agent for the terminal and cloud. It works with any OpenAI-compatible model provider, uses MCP servers for tools, and runs in a general mode and a code mode.</p>

<h3>Does Jiva work with Sarvam-105B?</h3>
<p>Yes. Sarvam-105B has been supported as a reasoning model since Jiva v0.3.42, with a setup preset, handling of Sarvam's tool-call format, and recovery when a large file write hits Sarvam's 4096-token output cap. That cap still limits very large single writes.</p>

<h3>Is Jiva free to use?</h3>
<p>Jiva itself is free and MIT licensed. You pay your model provider for the tokens you use, and for anywhere you choose to host it.</p>

<h3>Which models can Jiva use?</h3>
<p>Any model behind an OpenAI-compatible API. The setup wizard has presets for Krutrim, Groq, Sarvam and OpenAI, and the documentation shows a local Ollama example.</p>

<h3>How is Jiva different from a chatbot?</h3>
<p>A chatbot answers. Jiva plans a task, calls tools such as the file system, a browser or a shell, checks the result, and keeps going until the job is done.</p>

<p>Want an agent built on Jiva for a job in your business? <a href="/contact/">Talk to Gritsa</a>.</p>

</div>
