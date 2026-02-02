---
title: Roboracer Rules
layout: page
section: race
---
<style>
{% capture style %}{% include roboracer_rules/style.css %}{% endcapture %}{{ style | replace: "h4", "h5" | replace: "h3", "h4" | replace: "h2", "h3" | replace: "h1", "h2" }}
</style>

These rules are prepared for the _27th International RoboRacer Autonomous Racing Competition_. Rules are subject to change.

{% comment %}
<style>
ol#markdown-toc  li {
  margin-left: 1rem;
}
</style>
**Table of Contents**
1. ToC
{:toc}
{::options toc_levels="2..2" /}
{% endcomment %}

{% capture rules %}
{% include roboracer_rules/rules_v3.md %}
{% endcapture %}

{{ rules | replace: "# RoboRacer Rules", "" | markdownify | replace: "h4", "h3" | replace: "h5", "h4" | replace: "h6", "h5" }}
{% comment %}
/* This creates the rules again, but also populates the toc above. */
{{ rules | toc }}
{% endcomment %}

{% capture version %}
{% include_relative .git/modules/roboracer_rules/HEAD %}
{% endcapture %}

<p style="text-align: right; font-size: 0.6rem">
<i>Version: {{ version | slice: 0, 9 }}</i>
</p>
