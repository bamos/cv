{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td style='padding-right:0;'>
<p markdown="1" style='margin: 0'>
{%- if i.title -%}
<strong>{{ i.title }}</strong>, <em>{{ i.place }}</em>
{%- else -%}
<strong>{{ i.place}}</strong>
{%- endif -%}
{% if i.location %}
, {{ i.location }}
{% endif %}
{% if i.inline_detail %}
<span markdown="1" style="color:grey;font-size:1.3rem;margin: 0">
({{ i.inline_detail }})
</span>
{%- endif -%}
</p>
  </td>
  <td class='col-md-2' style='text-align:right; padding-left:0;'>{{ i.dates }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
