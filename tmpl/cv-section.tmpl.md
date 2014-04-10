# {{ name }}

{% if name == "Education" %}
{% for school in contents %}
__{{ school.school }}__.  {{ school.degree }}.

+ {{ school.location }} &#124; {{ school.dates }}
{%- if school.majorGPA %}
+ Major GPA: {{ school.majorGPA }} &#124; Overall GPA: {{ school.overallGPA }}
{%- endif %}
{% endfor %}

{% elif name == "Research Experience" %}
{% for lab in contents %}

__{{ lab.lab }}__.  {{ lab.title }}.

+ {{ lab.location }} &#124; Advisor: {{ lab.advisor }} &#124; {{ lab.dates }}
{%- if lab.details -%}
{%- for detail in lab.details %}
+ {{ detail }}
{%- endfor %}
{%- endif -%}
{% endfor %}

{% elif name == "Industry Experience" %}
{% for company in contents %}

__{{ company.company }}__.  {{ company.title }}.

+ {{ company.location }} &#124; {{ company.dates }}
{%- if company.details -%}
{%- for detail in company.details %}
+ {{ detail }}
{%- endfor %}
{% endif %}
{% endfor %}

{% elif name == "Teaching Experience" %}
{% for university in contents %}

__{{ university.university }}__.  {{ university.title }}.

+ {{ university.location }} &#123; {{ university.dates }}
{%- for detail in university.details %}
+ {{ detail }}
{%- endfor %}
{% endfor %}

{% elif name == "Publications" %}
{% for type in contents %}

__{{ type['title'] }}.__

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
## [{{ v['name']}}]({{ v['url'] }})

{%- for detail in v['details'] %}
+ {{ detail }}
{%- endfor %}
{% endfor %}

{% elif name == "Activities" %}
{%- for activity in contents %}
+ {{ activity }}
{%- endfor %}

{% elif name == "Skills" %}
{%- for skill in contents %}
+ __{{ skill['title'] }}:__ {{ skill['details'] }}
{%- endfor %}

{% else %}
{{ contents }}
{% endif %}

