{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td class='col-md-3'>{{ i.date }}</td>
  <td>{{ i.info }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
