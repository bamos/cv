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
      <strong>{{ school.school }}</strong> | {{ school.location }}
      {% if school.details %}
        <p style='margin-top:-0.5em;margin-bottom:0em' markdown='1'>
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
