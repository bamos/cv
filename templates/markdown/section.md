{% if name.lower() != "none" %}
## <i class="fa fa-chevron-right" style='font-size: 0.9em;'></i> {{ name }}
{% endif %}
{% if legend %}
{{ legend }}

{% endif %}
{% block body %}
{{ data }}

{% endblock body %}
