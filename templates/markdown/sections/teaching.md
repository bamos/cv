{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td><strong>{{ i.name }}</strong> ({{ i.short }}), {{ i.position }}</td>
  <td class='col-md-2' style='text-align:right;'>{{ i.semester }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
