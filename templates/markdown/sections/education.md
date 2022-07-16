{% extends "section.md" %}

{% block body %}

<table class="table table-hover">
{% for school in items %}
  <tr>
    <td>
      <span class='cvdate'>{{ school.dates }}</span>
      <strong>{{ school.degree }}</strong>, <em>{{ school.school }}</em>
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
  </tr>
{% endfor %}
</table>
{% endblock body %}
