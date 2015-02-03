{% extends "section.md" %}

{% block body %}
{% for school in items %}
+ {{ school.degree }},
  {{ school.school }},
  {{ school.dates }}
  {% if school.overallGPA %}
    ({{ school.overallGPA }})
  {% endif %}
{% endfor %}
{% endblock body %}
