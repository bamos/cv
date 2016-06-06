{% extends "section.md" %}

{% block body %}

<table class="table table-hover">
{% for school in items %}
  <tr>
    <td class="col-md-3">{{ school.dates }}</td>
    <td>
      {% if school.degree %}
        <strong>{{ school.degree }}</strong>
        {% if school.overallGPA %}
          ({{ school.overallGPA }})
        {% endif %}
        <br>
      {% endif %}
      {{ school.school }}
    </td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
