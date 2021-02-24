{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for item in items %}
<tr>
  <td>
    <a href="{{ item.repo_url }}">{{ item.name }}</a> |
    <i class="fa fas fa-star"></i> {{ item.stars }} |
    <em>{{ item.desc }}</em>
    <!-- {% if item.url %} -->
    <!--     <a href="{{ item.url }}">{{ item.name }}</a> {{ item.details }} -->
    <!-- {% else %} -->
    <!--     {{ item.name }} {{item.details }} -->
    <!-- {% endif %} -->
  </td>
  <td class='col-md-1' style='text-align:right;'>{{ item.year }}</td>
</tr>
{% endfor %}
</table>
{% endblock body %}
