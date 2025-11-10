{% extends "section.md" %}

{% block body %}
*Slides for my major presentations are available
[here](https://bamos.github.io/presentations/)
under a CC-BY license.*

<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td style='padding-right:0;'>
    <span class='cvdate'>{{ item.year }}</span>
    {% if item.url %}
     <a href="{{ item.url }}"><em>{{ item.title }}</em></a>,
    {% else %}
     <em>{{ item.title }}</em>,
    {% endif %}
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
