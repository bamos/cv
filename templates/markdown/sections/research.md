{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for r in items %}
<tr>
  <td class='col-md-3'>{{ r.dates }}</td>
  <td>
    <strong>{{ r.place }}</strong>, {{ r.advisor }} <br>
    {{ r.area }}
  </td>
</tr>
{% endfor %}
</table>

{% endblock body %}
