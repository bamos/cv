{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td class='col-md-3'>{{ i.dates }}</td>
  <td>
    <strong>{{ i.title }}</strong> | {{ i.place}} | {{ i.location }}
    {% if i.details %}
    {% for detail in i.details %}
        <p style='display:inline' markdown='1'>
            <br> {{ detail }}
        </p>
    {% endfor %}
    {% endif %}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
