{% extends "section.md" %}

{% block body %}

<table class="table table-hover">
{% for school in items %}
  <tr>
    <td>
      <strong>{{ school.degree }}</strong>, {{ school.school }}
      {% if school.overallGPA %}
        ({{ school.overallGPA }})
      {% endif %}
      <br>
      {% if school.details %}
        <p style='margin-top:-1em;margin-bottom:0em' markdown='1'>
        {% for detail in school.details %}
        <br> {{ detail }}
        {% endfor %}
        </p>
      {% endif %}
    </td>
    <td class="col-md-2" style='text-align:right;'>{{ school.dates }}</td>
  </tr>
{% endfor %}
</table>
{% endblock body %}
