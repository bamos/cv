{% extends "section.md" %}

{% block body %}
Slides for my major presentations are open-sourced with a CC-BY license at
[bamos/presentations](https://github.com/bamos/presentations).

<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td style='padding-right:0;'>
     <em>{{ item.title }}</em>,
    {% if item.url %}
        <a href="{{ item.url }}">{{ item.location }}</a>
    {% else %}
        {{ item.location }}
    {% endif %}
  </td>
  <td class='col-md-2' style='text-align:right; padding-left:0;'>{{ item.year }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
