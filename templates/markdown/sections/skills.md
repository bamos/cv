{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for item in items %}
<tr>
  <td class='col-md-2'>{{ item.title }}</td>
  <td markdown="1">
{{ item.details }}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
