{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
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
  <td class='col-md-2' style='text-align:right;'>{{ i.dates }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
