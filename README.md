This repo contains the source for my CV:

+ [generate.py](generate.py) creates a [website](http://bamos.github.io)
  and [PDF](http://bamos.github.io/data/cv.pdf)
  from a shared [YAML source](cv.yaml)
  by using Jinja templates.
+ The publications are rendered from a single
  [BibTeX](publications/all.bib) file.
  The abstracts are displayed in the website output
  and the selected publications here are highlighted.
+ The [YAML source](cv.yaml) links to all author websites,
  which will automatically be added to the
  publication lists in the website and PDF.
+ GitHub stars are automatically scraped and cached on disk.


# Building and running
Dependencies are included in `requirements.txt` and can be installed
using `pip` with `pip3 install -r requirements.txt`.
`make` will call [generate.py](generate.py) and
build the LaTeX documents with `latexmk` and `biber`.
The Makefile can also:

1. Stage to my website with `make stage`,
2. Start a local jekyll server of my website with updated
  documents with `make jekyll`, and
3. Push updated documents to my website with `make push`.

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

# Other people using this code
You are welcome to use this code with or without attribution in the
documents you produce, and add a link back here if you want!

![](./images/websites.png)

+ [Alessandro Checco](https://alessandrochecco.github.io/)
+ [Alex Sludds](https://alexsludds.github.io/)
+ [Amara Dinesh Kumar](https://dineshresearch.github.io/)
+ [Boyo Chen](https://boyochen.github.io/)
+ [Chaitanya Ahuja](https://chahuja.com/) ([code](https://github.com/chahuja/cv))
+ [Chaitanya Bapat](https://chaibapchya.github.io/about)
+ [Chieh Hubert Lin (林杰)](https://hubert0527.github.io/)
+ [Colin Clement](http://www.cbclement.com/cv/) ([code](https://github.com/colinclement/cv))
+ [Daniel Schaefer](https://github.com/JohnAZoidberg/cv)
+ [David B. Lindell](https://davidlindell.com/) ([code](https://github.com/davelindell/cv))
+ [Emir Ceyani](https://ceyani.io/) ([code](https://github.com/emirceyani/cv))
+ [Franziska Meier](https://fmeier.github.io/)
+ [Guojin Chen](https://dekura.github.io/)
+ [Jean Nassar](https://github.com/masasin/resume)
+ [Joan Cano](https://joancano.github.io/)
+ [Juan Martín Loyola](https://jmloyola.github.io/cv/) ([code](https://github.com/jmloyola/cv))
+ [Jun Xiong](https://suredream.github.io/)
+ [Jérémie Lumbroso](https://github.com/jlumbroso/cv)
+ [Krishnaditya Kancharla](https://krishnakancharla.github.io/about)
+ [Lamin Juwara](https://laminjuwara.github.io) ([code](https://github.com/LaminJuwara/laminjuwara.github.io))
+ [Lizeth Joseline Fuentes Pérez](https://lizonly.github.io/cv/) ([code](https://github.com/lizOnly/cv))
+ [Marco Piccirilli](https://mpicci.github.io/)
+ [Matthew L. Bendall](https://github.com/mlbendall/cv)
+ [Murali Koppula](https://murali-koppula.github.io/)
+ [Nathan P. Lawrence]( https://nplawrence.com/cv/) ([code](https://github.com/NPLawrence/CV))
+ [Nazim Coskun](https://github.com/nazimcoskun/cv)
+ [Nicholas J. Loman](https://github.com/nickloman/cv)
+ [Nikos Doulaveras](https://github.com/niveras/BlogCV)
+ [Norman Kabir](https://github.com/nkabir/cv)
+ [Nurpeiis Baimukan](https://nurpeiis.github.io/)
+ [Olalekan Ogunmolu](https://scriptedonachip.com/)
+ [Pieter Vanderpol](https://github.com/petevdp/cv)
+ [Prachi Sudrik](https://prachisudrik.github.io/about)
+ [Pınar Demetçi](https://pinardemetci.github.io/)
+ [Qian Ge](https://conan7882.github.io/)
+ [Renan Souza](https://renansouza.org/) ([code](https://github.com/renan-souza/cv))
+ [Stefan Doerr](https://github.com/stefdoerr/cv)
+ [Steve T.K. Jan](https://stevetkjan.github.io/)
+ [Swaminathan Gurumurthy](https://swami1995.github.io/)
+ [Vinayakumar Ravi](https://vinayakumarr.github.io/)
+ [Wen-Yen Chang](https://jwy-leo.github.io/)
+ [Wilka Carvalho](https://github.com/wcarvalho/cv)
+ [Yann-Aël Le Borgne](https://yannael.github.io/)
+ [You-Feng Wu](https://lilyo.github.io/)
