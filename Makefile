# Makefile to build PDF, Markdown, and plaintext CV from YAML.
#
# Brandon Amos <http://bamos.io>

BLOG_DIR=$(HOME)/repos/blog

all: gen/cv.pdf gen/cv.md

gen/cv.tex gen/cv.md: cv.yaml generate.py tmpl/cv-section.tmpl.tex tmpl/cv.tmpl.tex
	./generate.py

gen/cv.pdf: gen/cv.tex
	rubber --pdf gen/cv.tex
	rm -rf *.aux *.out *.log __pycache__
	mv cv.pdf gen

push: gen/cv.pdf gen/cv.md
	cp gen/cv.pdf $(BLOG_DIR)/data
	cp gen/cv.md $(BLOG_DIR)
	git -C $(BLOG_DIR) add $(BLOG_DIR)/data/cv.pdf
	git -C $(BLOG_DIR) add $(BLOG_DIR)/cv.md
	git -C $(BLOG_DIR) commit -m "Update vitae."
	git -C $(BLOG_DIR) push

.PHONY: clean
clean:
	rm -rf *.aux *.out *.log gen/* __pycache__
