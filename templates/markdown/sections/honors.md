{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for award in items %}
<tr>
  <td class='col-md-2'>{{ award.year }}</td>
  <td>
    {{ award.title }}
    <!-- {% if award.descr %} -->
    <!-- <ul><li>{{ award.descr }}</li></ul> -->
    <!-- {% endif %} -->
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
