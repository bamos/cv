{% extends "section.md" %}

{% block body %}
{% for item in items %}
+ {{ item.details }}, {{ item.university }},
  {{ item.course.number }}, {{ item.dates }}
{% endfor %}
{% endblock body %}
