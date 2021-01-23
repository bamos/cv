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
      {{ school.school }} | {{ school.location }}
      {% if school.details %}
        <p style='margin-top:-1em;margin-bottom:0em' markdown='1'>
        {% for detail in school.details %}
        <br> {{ detail }}
        {% endfor %}
        </p>
      {% endif %}
    </td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
