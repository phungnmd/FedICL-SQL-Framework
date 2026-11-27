# FedLS-SQL manuscript. Run from paper/manuscript.
#   make            the PDF (build/main.pdf); stops on an undefined reference; a number that
#                   waits for its result prints as ?? (STRICT=1, used by submit, stops on it)
#                   and a guess written with \expect{value} prints as value?? and counts the same
#   make numbers    macros, tables and settings from the committed results and configs
#   make figures    the result charts (JOURNAL=cmc or jiis) and a copy of the method diagram
#                   (drawn in paper/figures, rendered there with render.py)
#   make floats     every table and figure on its own, for reading the cells
#   make pilot      a draft subsection on its own page (pilot/harness.tex)
#   make lint       the checks of tools/lint.py (JOURNAL=cmc or jiis)
#   make inventory  macros and \cite keys of every section, for a before/after diff
#   make submit     the flat one-directory source the journal asks for, compiled
# The target journal is CMC (owner, 2026-11-27): main.tex on the Tech Science Press class in
# Definitions/. JOURNAL=jiis builds the Springer wrapper, main_jiis.tex, into build/main_jiis.pdf.
JOURNAL ?= cmc
ifeq ($(JOURNAL),jiis)
MAIN    := main_jiis
STYLE   := sn-jnl.cls sn-basic.bst
else
MAIN    := main
STYLE   := $(wildcard Definitions/*)
endif
BUILD   := build
# STRICT=1 stops on a number without a committed result; a draft prints it as ??, or as
# value?? where \expect{value} gives a guess
STRICT  ?= 0
PYTHON  ?= python3
# matplotlib is not in the project environments; uv provides it for the charts
PLOT_PY ?= uv run --no-project --with matplotlib==3.10.8 python
# The LaTeX3 files of the distribution go first in the search path: a newer copy in a user
# tree does not match the format and stops the class (it loads expl3.sty through enotez).
TEXDIST := $(shell kpsewhich -var-value TEXMFDIST)
export TEXINPUTS := $(TEXDIST)/tex/latex/l3kernel//:$(TEXDIST)/tex/latex/l3packages//:$(TEXDIST)/tex/latex/l3backend//:$(TEXINPUTS)
LATEX   := pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
SOURCES := $(MAIN).tex macros.tex references.bib $(wildcard sections/*.tex) \
           $(wildcard generated/*.tex) $(wildcard figures/*.pdf) $(STYLE)

.PHONY: all pdf numbers figures floats pilot lint inventory submit clean

all: pdf

pdf: $(BUILD)/$(MAIN).pdf

$(BUILD)/$(MAIN).pdf: $(SOURCES)
	@mkdir -p $(BUILD)
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass1.out || (tail -30 $(BUILD)/pass1.out; exit 1)
	@if grep -q '\\citation' $(BUILD)/$(MAIN).aux; then bibtex $(BUILD)/$(MAIN) > $(BUILD)/bibtex.out || (cat $(BUILD)/bibtex.out; exit 1); fi
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass2.out || (tail -30 $(BUILD)/pass2.out; exit 1)
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass3.out || (tail -30 $(BUILD)/pass3.out; exit 1)
	@n=$$(grep -c "No committed number" $(BUILD)/$(MAIN).log); if [ "$$n" -gt 0 ]; then \
	   if [ "$(STRICT)" = "1" ]; then grep -n "No committed number" $(BUILD)/$(MAIN).log; \
	     echo "STOP: $$n numbers have no committed result"; exit 1; \
	   else echo "draft: $$n numbers wait for a committed result and print as ??"; fi; fi
	@if grep -n -E "Warning: (Reference|Citation) .* undefined" $(BUILD)/$(MAIN).log; then \
	   echo "STOP: undefined reference, citation or number (lines above)"; rm -f $@; exit 1; fi
	@$(PYTHON) tools/pages.py $(BUILD)/$(MAIN).log --journal $(JOURNAL)

numbers:
	$(PYTHON) tools/paper_numbers.py
	$(PYTHON) tools/paper_settings.py

figures:
	$(PLOT_PY) tools/charts.py --journal $(JOURNAL)
	cp ../figures/fig_method_overview.pdf figures/fig_method_overview.pdf

floats: 
	@mkdir -p $(BUILD)
	$(LATEX) -output-directory=$(BUILD) floats.tex > $(BUILD)/floats.stdout || (tail -30 $(BUILD)/floats.stdout; exit 1)
	$(LATEX) -output-directory=$(BUILD) floats.tex > $(BUILD)/floats.stdout || (tail -30 $(BUILD)/floats.stdout; exit 1)
	@echo "$(BUILD)/floats.pdf"

pilot:
	@mkdir -p $(BUILD)
	$(LATEX) -output-directory=$(BUILD) -jobname=pilot pilot/harness.tex > $(BUILD)/pilot.stdout || (tail -30 $(BUILD)/pilot.stdout; exit 1)
	bibtex $(BUILD)/pilot > $(BUILD)/pilot.bibtex || (cat $(BUILD)/pilot.bibtex; exit 1)
	$(LATEX) -output-directory=$(BUILD) -jobname=pilot pilot/harness.tex > $(BUILD)/pilot.stdout || (tail -30 $(BUILD)/pilot.stdout; exit 1)
	$(LATEX) -output-directory=$(BUILD) -jobname=pilot pilot/harness.tex > $(BUILD)/pilot.stdout || (tail -30 $(BUILD)/pilot.stdout; exit 1)
	@if grep -n -E "Warning: (Reference|Citation) .* undefined|No committed number" $(BUILD)/pilot.log; then \
	   echo "STOP: undefined reference, citation or number (lines above)"; exit 1; fi
	@echo "$(BUILD)/pilot.pdf"

lint:
	$(PYTHON) tools/lint.py --journal $(JOURNAL)

inventory:
	$(PYTHON) tools/lint.py --inventory > $(BUILD)/inventory.txt
	@echo "$(BUILD)/inventory.txt"

submit:
	$(MAKE) -B pdf STRICT=1
	$(PYTHON) tools/flatten.py --journal $(JOURNAL)

clean:
	rm -rf $(BUILD) submit
