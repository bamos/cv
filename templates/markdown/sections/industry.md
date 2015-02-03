{% extends "section.md" %}

{% block body %}
{% for i in items %}
+ {{ i.title }},
  {{ i.place }},
  {{ i.dates }}
{% endfor %}
{% endblock body %}
