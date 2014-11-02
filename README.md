## About.
This repo contains the source I use to automatically generate
[my curriculum vitae](http://bamos.io/cv) as a webpage and PDF
from YAML and BibTeX input.

[generate.py][generate.py] reads from [cv.yaml][cv.yaml] and
[publications.bib][publications.bib] and outputs LaTeX and Markdown
by using Jinja templates.
Statistics about my blog and github account are obtained
using [blog-info.py][blog-info.py] and [github-info.py][github-info.py].

### YAML.
I chose to use YAML because it can be easily written and maintained
by hand and it's easy to read into Python.
Also, I chose YAML over JSON because YAML better supports
comments, which I use a lot in my CV for experimental changes
and archiving outdated information.

### BibTeX.
I use BibTeX to manage publications because I can easily copy and
paste from Google Scholar and so I can use the `publications.bib` file
directly in new LaTeX papers.

### LaTeX.
I wrote the LaTeX template to be as minimal as possible because
I like making small changes.
The larger resume and templates I've seen are more difficult to modify.
I've also had problems with a multi-page CV when using other
templates, and I've added better support in these by
wrapping every section in a `minipage` environment
so the sections are intelligently put on correct pages.
This is working well for small sections, but I'm not sure how
it will work for sections that are larger than a page in length.

### Markdown.
I also added a Markdown template because an HTML CV blends better with my
personal website than embedding a PDF CV.

## How to run.
The dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.
On Mac or Linux, `make` will call [generate.py][generate.py] and build
the LaTeX documents with `pdflatex` and `biber`.

The Makefile will also:

1. Stage to my website with `make stage`,
2. Start a local jekyll server of my website with updated
  documents with `make jekyll`, and
3. Push updated documents to my website with `make push`.

## Further implementation and usage details.
### generate.py
1. Read `cv.yaml` into Python as a map and loop through the `order` vector,
   which maps a section key to the title to display.
   This is done so sections can be moved and hidden without
   deleting them.
2. Generate the LaTeX or Markdown content for every section by using the
   templates
   [cv-section.tmpl.tex][cv-section.tmpl.tex] and
   [cv-section.tmpl.md][cv-section.tmpl.md].
   The conditional statements make the sections a little messy,
   but using a template for each section lets the order be changed
   solely by the `order` vector.
3. Generate the entire LaTeX or Markdown document by using
   the templates [cv.tmpl.tex][cv.tmpl.tex] and [cv.tmpl.md][cv.tmpl.md].

### Publications.
Currently, all publications are stored as BibTeX in `publications.bib`.
These have to be in the order you want them to appear in the
output files.
Including this in LaTeX is straightforward,
but producing Markdown is slightly more complicated.
I use [BibtexParser][bibtexparser] to load the bibliography into
a map and manually format the data to mimic the LaTeX IEEE bibliography style.

# Similar Projects
There are many approaches to managing a resume or CV in git,
and this project uses unique Markdown and LaTeX templates.
The following list shows a short sampling of projects,
and I'm happy to merge pull requests of other projects.

<!--
To generate the following list, install v1 of https://github.com/jacquev6/PyGithub
and run the following command. Please add projects alphabetically to the list in
the comment and in the table below.

python3<<EOF
from github import Github
import time
github = Github()
repo_list = [
  "afriggeri/cv", "cies/resume", "deedydas/Deedy-Resume", "divad12/resume",
  "icco/Resume", "jsonresume/resume-schema", "kaeluka/cv",
  "mwhite/resume", "prat0318/json_resume", "QuteBits/resume_42", "raphink/CV",
  "sc932/resume", "terro/CV", "there4/markdown-resume", "zellux/resume"
]

print("Name | Stargazers ({}) | Description".format(time.strftime("%Y-%m-%d")))
print("|".join(["----"]*3))
for r_name in repo_list:
  r = github.get_repo(r_name)
  content = " | ".join([
    "[{}]({})".format(r.full_name,r.html_url),
    str(r.stargazers_count),
    r.description
  ])
  print(content)
EOF
-->

Name | Stargazers (2014-11-02) | Description
----|----|----
[afriggeri/cv](https://github.com/afriggeri/cv) | 749 | CV, typesetted in Helvetica Neue, using XeTeX, TikZ and Biblatex
[cies/resume](https://github.com/cies/resume) | 184 | My resume as a PDF including the well commented Latex sources and build instructions.
[deedydas/Deedy-Resume](https://github.com/deedydas/Deedy-Resume) | 464 | A one page , two asymmetric column resume template in XeTeX that caters to an undergraduate Computer Science student
[divad12/resume](https://github.com/divad12/resume) | 22 | Yaml resume compiled into multiple formats (such as LaTeX, HTML (TODO), etc.)
[icco/Resume](https://github.com/icco/Resume) | 212 | A markdown port of my resume
[jsonresume/resume-schema](https://github.com/jsonresume/resume-schema) | 303 | JSON-Schema is used here to define and validate our proposed resume json
[kaeluka/cv](https://github.com/kaeluka/cv) | 64 | My CV.
[mwhite/resume](https://github.com/mwhite/resume) | 527 | Markdown -> PDF/HTML resumé generator
[prat0318/json_resume](https://github.com/prat0318/json_resume) | 1002 | Generates pretty HTML, LaTeX, markdown, with biodata feeded as input in JSON
[QuteBits/resume_42](https://github.com/QuteBits/resume_42) | 2 | It generates a beautiful resume from yaml data
[raphink/CV](https://github.com/raphink/CV) | 45 | My CV
[sc932/resume](https://github.com/sc932/resume) | 294 | My CV/resume in LaTeX.
[terro/CV](https://github.com/terro/CV) | 17 | My cv template
[there4/markdown-resume](https://github.com/there4/markdown-resume) | 353 | Generate a responsive CSS3 and HTML5 resume with Markdown, with optional PDF output.
[zellux/resume](https://github.com/zellux/resume) | 88 | My resume, generated with moderncv

[generate.py]: https://github.com/bamos/cv/blob/master/generate.py
[publications.bib]: https://github.com/bamos/cv/blob/master/publications.bib
[cv.yaml]: https://github.com/bamos/cv/blob/master/cv.yaml
[blog-info.py]: https://github.com/bamos/cv/blob/master/blog-info.py
[github-info.py]: https://github.com/bamos/cv/blob/master/github-info.py
[Requirements.txt]: https://github.com/bamos/cv/blob/master/Requirements.txt
[cv-section.tmpl.tex]: https://github.com/bamos/cv/blob/master/tmpl/cv-section.tmpl.tex
[cv-section.tmpl.md]: https://github.com/bamos/cv/blob/master/tmpl/cv-section.tmpl.md
[cv.tmpl.tex]: https://github.com/bamos/cv/blob/master/tmpl/cv.tmpl.tex
[cv.tmpl.md]: https://github.com/bamos/cv/blob/master/tmpl/cv.tmpl.md
[bibtexparser]: https://bibtexparser.readthedocs.org/en/latest/index.html
