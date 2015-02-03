{% extends "section.md" %}

{% block body %}
{% for item in items %}
**{{ item.employer }}{% if item.location %}, {{ item.location }}{% endif %}** - _{{ item.about }}_ - {{ item.date }}

{% for note in item.notes %}
  - {{ note | wordwrap(width=76, wrapstring='\n    ') }}
{% endfor %}

{% endfor %}
{% endblock body %}
