{% if name.lower() != "none" %}
<h2 id="-{{ home_id }}"><i class="fa fa-chevron-right" style="font-size: 0.9em;"></i> {{ name }}</h2>
{% endif %}
{% if legend %}
{{ legend }}

{% endif %}
{% block body %}
{{ data }}

{% endblock body %}
