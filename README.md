## About.
This repo contains code to generate my [my curriculum vitae](http://bamos.io/cv).
The data is contained in the YAML file [cv.yaml][cv.yaml]
and the scripts output the Markdown and LaTeX code to produce
the webpage and PDF on my website.

The scripts [blog-info.py][blog-info.py] and
[github-info.py][github-info.py] are Python 3 scripts that
produce statistics about my blog and github account to include in my CV.

## How to run.
[generate.py][generate.py] is a Python 3 script that reads
from [cv.yaml][cv.yaml] and outputs a LaTeX produced PDF and
Markdown file in the `gen` directory.
The dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.

[generate.py]: https://github.com/bamos/cv/blob/master/generate.py
[cv.yaml]: https://github.com/bamos/cv/blob/master/cv.yaml
[blog-info.py]: https://github.com/bamos/cv/blob/master/blog-info.py
[github-info.py]: https://github.com/bamos/cv/blob/master/github-info.py
[Requirements.txt]: https://github.com/bamos/cv/blob/master/Requirements.txt
