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
Also, I chase YAML over JSON because YAML better supports
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
wrapping every section in a `miniipage` environment
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
