{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for item in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td style='padding-right:0;'>
    {% if item.url %}
        <a href="{{ item.url }}">{{ item.name }}</a> {{ item.details }}
    {% else %}
        {{ item.name }} {{item.details }}
    {% endif %}
  </td>
  <td class='col-md-2' style='text-align:right; padding-left:0;'>{{ item.year }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
