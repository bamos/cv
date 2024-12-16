# About
This repo contains the source I use to automatically generate
my curriculum vitae as a
[PDF](https://natolambert.com/cv)
from YAML and BibTeX input.
[generate.py](generate.py) reads from [cv.yaml](cv.yaml) and
[publications](publications) and outputs LaTeX and Markdown
by using Jinja templates.

**Credit: ** this is just a lowly fork, of the awesome code built by my colleague Brandon Amos.
The notable addition I added is getting stars for 🤗 HuggingFace models, datasets, and spaces.

# Building and running
Dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.
`make` will call [generate.py](generate.py) and
build the LaTeX documents with `latexmk` and `biber`. (install with `sudo tlmgr install latexmk` with latex installed, e.g. `brew install --cask basictex` and `sudo tlmgr update --self`)
The Makefile can also:

1. Stage to my website with `make stage`,
2. Start a local jekyll server of my website with updated
  documents with `make jekyll`, and
3. Push updated documents to my website with `make push`.

Note: I needed to install `pyyaml` with conda:
```
conda install pyyaml=5.4.1
```

Note: If errors with:
```
! LaTeX Error: File `moderncv.cls' not found.
```
Install `moderncv` with:
```
sudo tlmgr update --self
sudo tlmgr install moderncv
sudo tlmgr install mathabx
```

**Python env**:

1. Create and activate a conda environment:
```bash
conda create -n YOUR_ENV_NAME python=3.10
conda activate YOUR_ENV_NAME
```
2. Install required packages (see above)
3. Modify the `.env` file with `YOUR_ENV_NAME`



# What to modify
Change the content in `cv.yaml`.
You should also look through the template files to make sure there isn't any
special-case code that needs to be modified.
The `Makefile` can also start a Jekyll server and push the
new documents to another repository with `make jekyll` and `make push`.

## Warnings
1. Strings in `cv.yaml` should be LaTeX (though, the actual LaTeX formatting
   should be in the left in the templates as much as possible).
2. If you do include any new LaTeX commands, make sure that one of the
   `REPLACEMENTS` in `generate.py` converts them properly.
3. The LaTeX templates use modified Jinja delimiters to avoid overlaps with
   normal LaTeX. See `generate.py` for details.
