# Makefile to build PDF, Markdown, and plaintext CV from YAML.
#
# Brandon Amos <http://bamos.io>

BLOG_DIR=$(HOME)/repos/blog

all: gen/cv.pdf gen/cv.md

gen/cv.tex gen/cv.md: cv.yaml generate.py publications.bib \
	tmpl/cv-section.tmpl.tex tmpl/cv.tmpl.tex \
	tmpl/cv-section.tmpl.md tmpl/cv.tmpl.md
	./generate.py

gen/cv.pdf: gen/cv.tex publications.bib
	cd gen && \
	pdflatex --halt-on-error cv && \
	rm -rf `biber --cache` && \
	biber cv && \
	pdflatex --halt-on-error cv && \
	rm -rf __pycache__ gen/cv.{aux,bcf,blg,log,out,run.xml}

.PHONY: stage
stage: gen/cv.pdf gen/cv.md
	cp gen/cv.pdf $(BLOG_DIR)/data
	cp gen/cv.md $(BLOG_DIR)

.PHONY: jekyll
jekyll: stage
	cd $(BLOG_DIR) && jekyll server

push: stage
	git -C $(BLOG_DIR) add $(BLOG_DIR)/data/cv.pdf
	git -C $(BLOG_DIR) add $(BLOG_DIR)/cv.md
	git -C $(BLOG_DIR) commit -m "Update vitae."
	git -C $(BLOG_DIR) push

.PHONY: clean
clean:
	rm -rf *.aux *.out *.log gen/* __pycache__
