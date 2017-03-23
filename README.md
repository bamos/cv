[![Linux Build Status](https://travis-ci.org/bamos/cv.svg?branch=master)](https://travis-ci.org/bamos/cv)
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/l06od9i143im059m?svg=true)](https://ci.appveyor.com/project/bamos/cv)
[![Python Dependency Status](https://gemnasium.com/bamos/cv.svg)](https://gemnasium.com/bamos/cv)

# About
This repo contains the source I use to automatically generate
my curriculum vitae as a
[webpage](http://bamos.github.io)
and
[PDF](http://bamos.github.io/data/cv.pdf)
from YAML and BibTeX input.

[generate.py](generate.py) reads from [cv.yaml](cv.yaml) and
[publications](publications) and outputs LaTeX and Markdown
by using Jinja templates.

# Building and running
This requires a Python 3 installation,
and the hashbang of `generate.py` assumes an executable named
`python3` is available on the path.
Dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.
On Mac or Linux, `make` will call [generate.py](generate.py) and
build the LaTeX documents with `latexmk` and `biber`.

The Makefile will also:

1. Stage to my website with `make stage`,
2. Start a local jekyll server of my website with updated
  documents with `make jekyll`, and
3. Push updated documents to my website with `make push`.

# What to modify
Change the content in `cv.yaml`.
You should also look through the template files to make sure there isn't any
special-case code that needs to be modified.
The `Makefile` can also start a Jekyll server and push the
new documents to another repository.
To use the Jekyll integration,
review the `BLOG_DIR` variable and the `jekyll` and `push` targets.

## Warnings
1. Strings in `cv.yaml` should be LaTeX (though, the actual LaTeX formatting
   should be in the left in the templates as much as possible).
2. If you do include any new LaTeX commands, make sure that one of the
   `REPLACEMENTS` in `generate.py` converts them properly.
3. The LaTeX templates use modified Jinja delimiters to avoid overlaps with
   normal LaTeX. See `generate.py` for details.

## Publications
All publications are stored as BibTeX in [publications](publications).
The entries can be obtained from Google Scholar.
The order in the BibTeX file will be the order in
the output files.

BibTeX is built for integration with LaTeX, but producing
Markdown is not traditionally done from BibTeX files.
This repository uses [BibtexParser][bibtexparser] to load the
bibliography into a map.
The data is manually formatted to mimic the LaTeX
IEEE bibliography style.

[bibtexparser]: https://bibtexparser.readthedocs.org/en/latest/index.html

# Licensing
This work is distributed under the MIT license (`LICENSE-bamos.mit`)
with portions copyright Ellis Michael from
[emichael/resume](https://github.com/emichael/resume).
Ellis' portions are also distributed under the MIT license
(`LICENSE-emichael.mit`) and include
a re-write of `generate.py` and template restructuring.

# Similar Projects
There are many approaches to managing a resume or CV in git,
and this project uses unique Markdown and LaTeX templates.
The following list shows a short sampling of projects,
and I'm happy to merge pull requests of other projects.

<!--
To generate the following list, install https://github.com/jacquev6/PyGithub
and download the `github-repo-summary.py` script from
https://github.com/bamos/python-scripts/blob/master/python3/github-repo-summary.py.
Please add projects to the list in the comment and in the table below.

github-repo-summary.py \
  ajn123/CV \
  cies/resume \
  divad12/resume \
  emichael/resume \
  icco/Resume \
  jsonresume/resume-schema \
  kaeluka/cv \
  masasin/resume \
  mwhite/resume \
  prat0318/json_resume \
  qutebits/resume_42 \
  raphink/CV \
  sc932/resume \
  terro/CV \
  there4/markdown-resume \
  zellux/resume \
  Maples7/barn
-->

Name | Stargazers | Description
----|----|----
[ajn123/CV](https://github.com/ajn123/CV) | 13 | My resume in Latex
[cies/resume](https://github.com/cies/resume) | 261 | My resume as a PDF including the well commented LaTeX source and build instructions.
[divad12/resume](https://github.com/divad12/resume) | 40 | Yaml resume compiled into multiple formats (such as LaTeX, HTML (TODO), etc.)
[emichael/resume](https://github.com/emichael/resume) | 2 | Generate LaTeX and Markdown resume from YAML with Python.
[icco/Resume](https://github.com/icco/Resume) | 258 | A markdown port of my resume
[jsonresume/resume-schema](https://github.com/jsonresume/resume-schema) | 644 | JSON-Schema is used here to define and validate our proposed resume json
[kaeluka/cv](https://github.com/kaeluka/cv) | 68 | My CV.
[masasin/resume](https://github.com/masasin/resume) | 2 | Automatically generate your résumé and various cover letters from YAML files.
[mwhite/resume](https://github.com/mwhite/resume) | 707 | Markdown -> PDF/HTML resumé generator
[prat0318/json_resume](https://github.com/prat0318/json_resume) | 1123 | Generates pretty HTML, LaTeX, markdown, with biodata feeded as input in JSON
[QuteBits/resume_42](https://github.com/QuteBits/resume_42) | 14 | Python script that generates a beautiful resume from YAML data
[raphink/CV](https://github.com/raphink/CV) | 77 | My CV
[sc932/resume](https://github.com/sc932/resume) | 337 | My CV/resume in LaTeX.
[terro/CV](https://github.com/terro/CV) | 27 | My cv template
[there4/markdown-resume](https://github.com/there4/markdown-resume) | 749 | Generate a responsive CSS3 and HTML5 resume with Markdown, with optional PDF output.
[zellux/resume](https://github.com/zellux/resume) | 134 | My resume, generated with moderncv
[Maples7/barn](https://github.com/Maples7/barn) | 10 | A resume/CV generator, parsing information from YAML file to generate a static website which you can deploy on the Github Pages. Exactly like resume-version Hexo.
