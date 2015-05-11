{% extends "section.md" %}

{% block body %}
{% for item in items %}
+ {{ item.name }}, {{ item.position }},
  {{ item.semester }}
{% endfor %}
{% endblock body %}
