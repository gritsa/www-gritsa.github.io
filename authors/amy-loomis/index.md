---
layout: page
title: "Amy Loomis"
description: "Amy Loomis writes the Gritsa blog: LLMs, AI agents, MCP and the data foundations businesses need before agents work in production."
permalink: /authors/amy-loomis/
---
<section class="page-single-post">
<div class="container">
<div class="row">
<div class="col-lg-8 offset-lg-2">
<div class="post-entry">

<p>I write the Gritsa blog. The subjects are large language models, AI agents, MCP servers, the data foundations that decide whether any of it works, and what all of that means for a business trying to stay relevant over the next five years.</p>

<p>I work in SEO, content marketing and sales, and I care about technology enough to have opinions about it. Those opinions are in the posts, and they are marked as opinions. When I state a fact, I link to where it came from.</p>

<h2>What I cover</h2>
<ul>
<li>How to put agents into real production, beyond a demo</li>
<li>MCP: what it is, what breaks, how to secure it</li>
<li>Data foundations for AI</li>
<li>Building with AI beyond vibe coding</li>
</ul>

<h2>Recent posts</h2>
<ul>
{% for post in site.posts %}{% if post.author == "Amy Loomis" %}
<li><a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: "%B %-d, %Y" }})</li>
{% endif %}{% endfor %}
</ul>

<p>I write for <a href="{{ site.baseurl }}/">Gritsa Technologies</a>, which builds AI agents and the engineering around them.</p>

</div>
</div>
</div>
</div>
</section>
