# Build from repo root: make -C latex
# Requires: latexmk, TeX Live (or MacTeX) with tcolorbox, biblatex, etc.

PDF := main.pdf

all: $(PDF)

$(PDF): main.tex references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	latexmk -C
	rm -f $(PDF)

.PHONY: all clean
