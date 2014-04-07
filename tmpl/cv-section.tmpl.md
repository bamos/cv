# {{ name }}

{% if name == "Education" %}
{% for school in contents %}
{{ school.degree|e }} {{ school.school|e }}.
+ {{ school.location|e }} | {{ school.dates|e }}
{%- if school.majorGPA -%}
+ Major GPA: {{ school.majorGPA|e }} | Overall GPA: {{ school.overallGPA|e }}
{%- endif -%}
{%- endfor %}

{% elif name == "Research Experience" %}
{% for lab in contents %}
## {{ lab.lab|e }}
### {{ lab.title|e }}
+ {{ lab.location|e }} | Advisor: {{ lab.advisor|e }} | {{ lab.dates|e }}
{%- if lab.details -%}
{%- for detail in lab.details %}
+ {{ detail }}
{%- endfor %}
{%- endif -%}
{% endfor %}

{% elif name == "Industry Experience" %}
{% for company in contents %}
## {{ company.company|e }}
### {{ company.title|e }}
+ {{ company.location|e }} | {{ company.dates|e }}
{%- if company.details -%}
{%- for detail in company.details %}
+ {{ detail }}
{%- endfor %}
{%- endif -%}
{% endfor %}

{% elif name == "Teaching Experience" %}
{% for university in contents %}
## {{ university.university|e }}
### {{ university.title|e }}
+ {{ university.location|e }} | {{ university.dates|e }}
{%- for detail in university.details %}
+ {{ detail }}
{%- endfor %}
{% endfor %}

{% elif name == "Publications" %}
{% for type in contents %}
## {{ type['title'] }}

{%- for pub in type['details'] %}
{{ loop.index }}. {{ pub }}
{%- endfor %}
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

