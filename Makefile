# Makefile to build PDF and Markdown cv from YAML.
#
# Brandon Amos <http://bamos.github.io> and
# Ellis Michael <http://ellismichael.com>

WEBSITE_DIR=$(HOME)/repos/website
WEBSITE_PDF=$(WEBSITE_DIR)/cv.pdf
WEBSITE_MD=$(WEBSITE_DIR)/index.md

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

.PHONY: all public viewpdf stage jekyll check-pushed push clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py cv.yaml

$(TEX) $(MD): $(TEMPLATES) $(YAML_FILES) generate.py publications/*.bib
	./generate.py $(YAML_FILES)

$(PDF): $(TEX)
	# TODO: Hack for biber on OSX.
	rm -rf /var/folders/8p/lzk2wkqj47g5wf8g8lfpsk4w0000gn/T/par-62616d6f73

	latexmk -pdf -cd- -jobname=$(BUILD_DIR)/cv -interaction=nonstopmode -halt-on-error $(BUILD_DIR)/cv
	latexmk -c -cd $(BUILD_DIR)/cv

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(MD)
	git -C $(WEBSITE_DIR) checkout $(WEBSITE_PDF) $(WEBSITE_MD)
	@if git -C $(WEBSITE_DIR) diff-index --quiet HEAD --; then \
		git -C $(WEBSITE_DIR) pull --rebase; \
	else \
		echo "Warning: $(WEBSITE_DIR) has uncommitted changes, skipping pull"; \
	fi
	cp $(PDF) $(WEBSITE_PDF)
	cp $(MD) $(WEBSITE_MD)

stage-md: $(MD)
	cp $(MD) $(WEBSITE_MD)

jekyll: stage
	cd $(WEBSITE_DIR) && bundle exec jekyll server

check-pushed:
	@set -eu; \
	status=$$(git status --porcelain --untracked-files=normal); \
	if [ -n "$$status" ]; then \
		echo "Commit all changes in the CV repository and push them before running make push." >&2; \
		exit 1; \
	fi; \
	if ! branch=$$(git symbolic-ref --quiet --short HEAD) || \
	   ! remote=$$(git config --get "branch.$$branch.remote") || \
	   ! upstream=$$(git config --get "branch.$$branch.merge") || \
	   [ "$$remote" = "." ]; then \
		echo "Push the current CV branch to a remote with git push -u before running make push." >&2; \
		exit 1; \
	fi; \
	git fetch --quiet "$$remote" "$$upstream"; \
	if ! git merge-base --is-ancestor HEAD FETCH_HEAD; then \
		echo "Push the current CV commit with git push before running make push." >&2; \
		exit 1; \
	fi

# Run staging only after the guard succeeds, including with parallel make.
push: check-pushed
	$(MAKE) stage
	git -C $(WEBSITE_DIR) add $(WEBSITE_PDF) $(WEBSITE_MD)
	git -C $(WEBSITE_DIR) commit -m "Update cv."
	git -C $(WEBSITE_DIR) push

clean:
	rm -rf *.db *.shelf $(BUILD_DIR)/cv*
