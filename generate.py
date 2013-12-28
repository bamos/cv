#!/usr/bin/python3.3
#
# Generates LaTeX, markdown, and plaintext copies of my CV.
#
# Brandon Amos <http://bamos.io>
# 2013.12.28

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("tmpl"))

import yaml

f = open("cv.yaml", 'r')
yaml_contents = yaml.load(f)
f.close()

body = ""
for section in yaml_contents['order']:
  body += env.get_template("cv-section.tmpl.tex").render(
    name = section[1].title(),
    contents = yaml_contents[section[0]]
  )

f_cv = open("gen/cv.tex", 'w')
f_cv.write(env.get_template("cv.tmpl.tex").render(
  name = yaml_contents['name'],
  phone = yaml_contents['phone'],
  email = yaml_contents['email'],
  url = yaml_contents['url'],
  body = body
))
f_cv.close()
