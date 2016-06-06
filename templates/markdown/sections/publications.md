{% extends "section.md" %}

{% block body %}

<a href="https://scholar.google.com/citations?user=CZwrwHAAAAAJ" class="btn btn-primary" style="padding: 0.3em;">
  <i class="ai ai-google-scholar"></i> Google Scholar
</a>

{% for p in items %}

### {{ p.title }} <a href="https://github.com/bamos/cv/blob/master/publications/{{ p.file }}"><i class="fa fa-code-fork" aria-hidden="true"></i></a>

<table class="table table-hover">
{{ p.details }}
</table>

{% endfor %}
{% endblock body %}
