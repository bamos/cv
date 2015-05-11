{% extends "section.md" %}

{% block body %}
{% for course in items %}
+ {{ course.name }}, {{ course.instructor}}, {{ course.semester }}
{% endfor %}
{% endblock body %}
