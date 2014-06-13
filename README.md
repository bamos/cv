## About.
This repo contains code to generate my [my curriculum vitae](http://bamos.io/cv).
The data is stored in the YAML file [cv.yaml][cv.yaml] and
BibTeX file [publications.bib][publications.bib],
and the rest of the scripts and templates output Markdown and LaTeX
code to produce the webpage and PDF on my website.

[generate.py][generate.py] is a Python 3 script that reads
from [cv.yaml][cv.yaml] and outputs LaTeX and Markdown
by using Jinja templates.

The scripts [blog-info.py][blog-info.py] and
[github-info.py][github-info.py] are Python 3 scripts that
produce statistics about my blog and github account to include in my CV.

## How to run.
The dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.
On Linux, `make` will call [generate.py][generate.py] and build
the LaTeX documents.

The Makefile will also:

1. Stage to my website with `make stage`,
2. Start a local jekyll server of my website with updated
  documents with `make jekyll`, and
3. Push updated documents to my website with `make push`.

[generate.py]: https://github.com/bamos/cv/blob/master/generate.py
[publications.bib]: https://github.com/bamos/cv/blob/master/publications.bib
[cv.yaml]: https://github.com/bamos/cv/blob/master/cv.yaml
[blog-info.py]: https://github.com/bamos/cv/blob/master/blog-info.py
[github-info.py]: https://github.com/bamos/cv/blob/master/github-info.py
[Requirements.txt]: https://github.com/bamos/cv/blob/master/Requirements.txt
