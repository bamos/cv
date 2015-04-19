{% extends "section.md" %}

{% block body %}
{% for r in items %}
+ {{ r.title }}, {{ r.place }}, {{ r.dates }}
    + **Advisor**: {{ r.advisor }}
    + **Area**: {{ r.area }}
{% endfor %}

{% endblock body %}
