# {{ name }}

{% if name == "Education" %}
{% for school in contents %}
__<big>{{ school.school }}.</big>__  {{ school.degree }}.
{%- if school.overallGPA %}
GPA: {{ school.overallGPA }}
{%- endif %}

+ {{ school.location }}
&#124; {{ school.dates }}
{% endfor %}

{% elif name.endswith("Experience") %}
{% for n in contents %}

__<big>{{ n.place }}.</big>__  {{ n.title }}.

+ {{ n.location }}
{% if n.advisor -%}
  &#124; Advisor: {{ n.advisor }}
{% endif -%}
&#124; {{ n.dates }}
{%- if n.details -%}
{%- for detail in n.details %}
+ {{ detail }}
{%- endfor %}
{%- endif -%}
{% endfor %}

{% elif name == "Publications" %}
{% for type in contents %}

__<big>{{ type['title'] }}.</big>__

{% for pub in type['details'] %}
{{ loop.index }}. {{ pub }}
{% endfor %}
{% endfor %}

{% elif name == "Honors \\& Awards" or name == "Honors & Awards" %}
{%- for award in contents %}
  {%- if 'url' in award %}
+ [{{ award['title'] }}]({{ award['url'] }})
  {%- else %}
+ {{ award['title'] }}
  {%- endif %}
{%- if 'descr' in award %}
  + {{ award['descr'] }}
{%- endif %}
{%- endfor %}

{% elif name == "Projects" %}
{% for k,v in contents.items() %}

<big>[{{ v['name']}}]({{ v['url'] }})</big>

{% for detail in v['details'] %}
+ {{ detail }}
{%- endfor %}
{% endfor %}

{% elif name == "Activities" %}
{%- for activity in contents %}
+ {{ activity }}
{%- endfor %}

{% elif name == "Skills" %}
{%- for skill in contents %}
+ __{{ skill['title'] }}.__ {{ skill['details'] }}
{%- endfor %}

{% else %}
{{ contents }}
{% endif %}

