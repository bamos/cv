{% extends "section.md" %}

{% block body %}
*{{ total_stars }} GitHub stars across all repositories.*

<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td>
    <span class='cvdate'>{{ item.year }}</span>
    <a href="{{ item.repo_url }}">{{ item.name }}</a>
    <span style="white-space: nowrap">
    | <i class="fa fas fa-star"></i>&nbsp;{{ item.stars }}
    </span>
    {% if item.desc %} <em style="color: gray;">&mdash; {{ item.desc }}</em>{% endif %}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
