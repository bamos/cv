# Makefile to build PDF and Markdown cv from YAML.
#
# Brandon Amos <http://bamos.github.io> and
# Ellis Michael <http://ellismichael.com>

WEBSITE_DIR=$(HOME)/repos/website

TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
TEX=$(BUILD_DIR)/cv.tex
PDF=$(BUILD_DIR)/cv.pdf
MD=$(BUILD_DIR)/cv.md

ifneq ("$(wildcard cv.hidden.yaml)","")
	YAML_FILES = cv.yaml cv.hidden.yaml
else
	YAML_FILES = cv.yaml
endif

.PHONY: all public viewpdf stage jekyll push clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py cv.yaml

$(TEX) $(MD): $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)

$(PDF): $(TEX)
	latexmk -pdf -cd- -jobname=$(BUILD_DIR)/cv $(BUILD_DIR)/cv
	latexmk -c -cd $(BUILD_DIR)/cv

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(MD)
	cp $(PDF) $(WEBSITE_DIR)/data/cv.pdf
	cp $(MD) $(WEBSITE_DIR)/cv.md

jekyll: stage
	cd $(WEBSITE_DIR) && jekyll server

push: stage
	git -C $(WEBSITE_DIR) add $(WEBSITE_DIR)/data/cv.pdf
	git -C $(WEBSITE_DIR) add $(WEBSITE_DIR)/cv.md
	git -C $(WEBSITE_DIR) commit -m "Update cv."
	git -C $(WEBSITE_DIR) push

clean:
	rm -rf $(BUILD_DIR)/cv*
