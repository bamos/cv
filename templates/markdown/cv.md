---
layout: index
title: {{ name.first }} {{ name.last }}
---

{% for section in sections if section.id == 'about' %}
<div id="about-intro" markdown="1">

{{ section.content }}

</div>
{% endfor %}

{% if about_formal %}
<div id="bio" class="home-bio-formal" hidden markdown="1">

{% raw %}{% comment %}Generated from about_formal in the CV YAML; bio.md also serves the standalone page.{% endcomment %}
{% capture formal_bio %}{% include_relative bio.md %}{% endcapture %}
{% assign bio_parts = formal_bio | split: '---' %}
{{ bio_parts | slice: 2, bio_parts.size | join: '---' | normalize_whitespace | markdownify }}{% endraw %}

</div>
{% endif %}

<div class="home-sections" markdown="1">

<div class="home-tabs-slot" markdown="0">
<div class="home-navigation">
<nav class="home-tabs" aria-label="Homepage sections">
{% for section in sections if section.id != 'about' %}
  <a id="tab-{{ section.id }}" href="#{{ section.id }}">{{ section.name }}</a>
{% endfor %}
</nav>
</div>
</div>

{% for section in sections if section.id != 'about' %}
<section id="{{ section.id }}" class="home-section" markdown="1">

{{ section.content }}

</section>

{% endfor %}
</div>

<p id="last-updated" style="font-size: 0.85em; color: #999;">Last updated on {{ today }}.</p>
