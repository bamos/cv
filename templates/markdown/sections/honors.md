{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for award in items %}
<tr>
  <td class='col-md-2'>{{ award.year }}</td>
  <td>
    {{ award.title }}
    {% if award.descr %}
    <br><p style="color:grey;font-size:1.2rem">{{ award.descr }}</p>
    {% endif %}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
