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
contents = yaml.load(f)
f.close()

body = ""
for section in contents['order']:
  body += env.get_template("cv-section.tmpl.tex").render(
    name = section[1].title(),
    contents = contents[section[0]]
  )

f_cv = open("gen-src/cv.tex", 'w')
f_cv.write(env.get_template("cv.tmpl.tex").render(
  name = contents['name'],
  phone = contents['phone'],
  email = contents['email'],
  url = contents['url'],
  body = body
))
f_cv.close()
