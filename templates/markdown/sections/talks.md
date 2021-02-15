{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for item in items %}
<tr>
  <td class='col-md-1'>{{ item.year }}</td>
  <td>
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
