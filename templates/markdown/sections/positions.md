{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td>
<p markdown="1" style='margin: 0'>
{%- if i.title -%}
<strong>{{ i.title }}</strong>, {{ i.place }}
{%- else -%}
<strong>{{ i.place}}</strong>
{%- endif -%}
{% if i.location %}
, {{ i.location }}
{% endif %}
{% if i.inline_detail %}
 ({{ i.inline_detail }})
{% endif %}
</p>
  </td>
  <td class='col-md-2' style='text-align:right;'>{{ i.dates }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
