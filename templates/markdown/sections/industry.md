{% extends "section.md" %}

{% block body %}
{% for i in items %}
+ {{ i.title }}, {{ i.place }}, {{ i.dates }}
  {#
  {% for detail in i.details %}
    + {{ detail }}
  {% endfor %}
  #}
{% endfor %}
{% endblock body %}
