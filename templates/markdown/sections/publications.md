{% extends "section.md" %}

{% block body %}
{% for p in items %}

### {{ p.title }}
{{ p.details }}
{% endfor %}
{% endblock body %}
