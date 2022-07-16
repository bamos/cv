{% extends "section.md" %}

{% block body %}
Slides for my major presentations are open-sourced with a CC-BY license at
[bamos/presentations](https://github.com/bamos/presentations).

<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td style='padding-right:0;'>
    <span class='cvdate'>{{ item.year }}</span>
     <em>{{ item.title }}</em>,
    {% if item.url %}
        <a href="{{ item.url }}">{{ item.location }}</a>
    {% else %}
        {{ item.location }}
    {% endif %}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
