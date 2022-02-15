{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for item in items.main %}
<tr>
  <td>
  {% if item.url %}
     <a href="{{ item.url }}">{{ item.details }}</a>
  {% else %}
      {{item.details }}
  {% endif %}
  {% if item.sub_details %}
  <br><p style="color:grey;font-size:1.2rem">{{ item.sub_details }}</p>
  {% endif %}
  <td class='col-md-2' style='text-align:right;'>{{ item.year }}</td>
  </td>
</tr>
{% endfor %}
</table>

<!-- ### <i class="fa fa-chevron-right"></i> {{ name }} -->
### Reviewing
<table class="table table-hover">
{% for item in items.reviewing %}
<tr>
  <td>
      {{ item }}
  </td>
</tr>
{% endfor %}
</table>
{% endblock body %}
