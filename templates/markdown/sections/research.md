{% extends "section.md" %}

{% block body %}
{% for r in items %}
+ {{ r.title }}, {{ r.place }}, {{ r.dates }}
    + **Advisor**: {{ r.advisor }}
    + **Area**: {{ r.area }}
  {% for detail in r.details %}
    + {{ detail }}
  {% endfor %}
{% endfor %}

{% endblock body %}
