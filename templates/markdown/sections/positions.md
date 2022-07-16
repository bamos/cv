{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for i in items %}
<tr>
  <td style='padding-right:0;'>
<span class='cvdate'>{{ i.dates }}</span>
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
</tr>
{% endfor %}
</table>
{% endblock body %}
