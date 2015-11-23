{% extends "section.md" %}

{% block body %}
{% for school in items %}
+ {% if school.degree -%}
    {{ school.degree }},
  {% endif %}
  {{ school.school }},
  {{ school.dates }}
  {% if school.overallGPA %}
    ({{ school.overallGPA }})
  {% endif %}
{% endfor %}
{% endblock body %}
