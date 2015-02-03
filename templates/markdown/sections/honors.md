{% extends "section.md" %}

{% block body %}
{% for award in items %}
+ {{ award.title }}, {{ award.year }}
  {% if award.descr %}
  + {{ award.descr }}
  {% endif %}
{% endfor %}
{% endblock body %}
