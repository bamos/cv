{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td align='right' style='padding-right:0;padding-left:0;'>{{ loop.index }}.</td>
  <td style='padding-right:0'><strong>{{ i.name }}</strong> ({{ i.short }}), {{ i.position }}</td>
  <td class='col-md-2' style='text-align:right; padding-left:0;'>{{ i.semester }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
