#!/usr/bin/python3
#
# Generates LaTeX, markdown, and plaintext copies of my CV.
#
# Brandon Amos <http://bamos.io>
# 2013.12.28

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("tmpl"))
import re
import yaml
from datetime import date

f = open("cv.yaml", 'r')
yaml_contents = yaml.load(f)
f.close()

def latexToMd(s):
  if isinstance(s,str):
    s = s.replace(r'\\', '\n\n')
    s = s.replace(r'\it', '')
    s = s.replace('--', '-')
    s = s.replace('``', '"')
    s = s.replace("''", '"')
    s = s.replace(r"\LaTeX", "LaTeX")
    s = s.replace(r"\#", "#")
    s = s.replace(r"\&", "&")
    s = re.sub(r'\\[hv]space\*?\{[^}]*\}', '', s)
    s = s.replace(r"*", "\*")
    s = re.sub(r'\{ *\\bf *([^\}]*)\}', r'**\1**', s)
    s = re.sub('\{([^\}]*)\}', r'\1', s)
  elif isinstance(s,dict):
    for k,v in s.items():
      s[k] = latexToMd(v)
  elif isinstance(s,list):
    for idx, item in enumerate(s):
      s[idx] = latexToMd(item)
  return s

def generate(ext):
  body = ""
  for section in yaml_contents['order']:
    if ext == "md":
      contents = latexToMd(yaml_contents[section[0]])
      name = latexToMd(section[1].title())
    else:
      contents = yaml_contents[section[0]]
      name = section[1].title()
    body += env.get_template("cv-section.tmpl." + ext).render(
      name = name,
      contents = contents
    )

  f_cv = open("gen/cv." + ext, 'w')
  f_cv.write(env.get_template("cv.tmpl." + ext).render(
    name = yaml_contents['name'],
    pdf = yaml_contents['pdf'],
    src = yaml_contents['src'],
    phone = yaml_contents['phone'],
    email = yaml_contents['email'],
    email_recaptcha = yaml_contents['email_recaptcha'],
    url = yaml_contents['url'],
    body = body,
    today = date.today().strftime("%B %d, %Y")
  ))
  f_cv.close()

generate("tex")
generate("md")
