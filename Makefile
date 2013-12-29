# Makefile to build PDF, Markdown, and plaintext CV from YAML.
#
# Brandon Amos <http://bamos.io>

all: cv.pdf

cv.pdf: cv.yaml generate.py tmpl/cv-section.tmpl.tex tmpl/cv.tmpl.tex
	./generate.py
	rubber --pdf gen/cv.tex
	rm -rf *.aux *.out *.log __pycache__
	mv cv.pdf gen

.PHONY: clean
clean:
	rm -rf *.aux *.out *.log *.pdf __pycache__
