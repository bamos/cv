{% extends "section.md" %}

{% block body %}
{% for item in items %}
+ {{ item.title }}: {{ item.details }}
{% endfor %}
{% endblock body %}
