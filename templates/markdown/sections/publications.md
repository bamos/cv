{% extends "section.md" %}

{% block body %}

<a href="https://scholar.google.com/citations?user=CZwrwHAAAAAJ" class="btn btn-primary" style="padding: 0.3em;">
  <i class="ai ai-google-scholar"></i> Google Scholar
</a>

{% for p in items %}

### {{ p.title }}

{:.table}
| | Title | Authors | Location |
|---|---|---|---|
{{ p.details }}

{% endfor %}
{% endblock body %}
