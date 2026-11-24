{% extends "section.md" %}

{% block body %}
*Slides for my major presentations are available
[here](https://github.com/bamos/presentations)
under a CC-BY license.*

<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td>
    <span class='cvdate'>{{ item.year }}</span>
    {% if item.url %}
     <a href="{{ item.url }}"><em>{{ item.title }}</em></a>
    {% else %}
     <em>{{ item.title }}</em>
    {% endif %}
    <span style="padding: 0 0.2em;">•</span>
    {% if item.location_url %}
        <a href="{{ item.location_url }}">{{ item.location }}</a>
    {% else %}
        {{ item.location }}
    {% endif %}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
