# FedLS-SQL manuscript. Run from paper/manuscript.
#   make            the PDF (build/main.pdf); stops on an undefined reference
#   make numbers    macros, tables and settings from the committed results and configs
#   make figures    the result charts (JOURNAL=jiis or cmc)
#   make floats     every table and figure on its own, for reading the cells
#   make lint       the checks of tools/lint.py (JOURNAL=jiis or cmc)
#   make inventory  macros and \cite keys of every section, for a before/after diff
#   make submit     the flat one-directory source the journal asks for, compiled
MAIN    := main
BUILD   := build
JOURNAL ?= jiis
PYTHON  ?= python3
# matplotlib is not in the project environments; uv provides it for the charts
PLOT_PY ?= uv run --no-project --with matplotlib==3.10.8 python
LATEX   := pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
SOURCES := $(MAIN).tex macros.tex references.bib $(wildcard sections/*.tex) \
           $(wildcard generated/*.tex) $(wildcard figures/*.pdf) sn-jnl.cls sn-basic.bst

.PHONY: all pdf numbers figures floats lint inventory submit clean

all: pdf

pdf: $(BUILD)/$(MAIN).pdf

$(BUILD)/$(MAIN).pdf: $(SOURCES)
	@mkdir -p $(BUILD)
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass1.out || (tail -30 $(BUILD)/pass1.out; exit 1)
	@if grep -q '\\citation' $(BUILD)/$(MAIN).aux; then bibtex $(BUILD)/$(MAIN) > $(BUILD)/bibtex.out || (cat $(BUILD)/bibtex.out; exit 1); fi
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass2.out || (tail -30 $(BUILD)/pass2.out; exit 1)
	$(LATEX) -output-directory=$(BUILD) $(MAIN).tex > $(BUILD)/pass3.out || (tail -30 $(BUILD)/pass3.out; exit 1)
	@if grep -n -E "Warning: (Reference|Citation) .* undefined|No committed number" $(BUILD)/$(MAIN).log; then \
	   echo "STOP: undefined reference, citation or number (lines above)"; rm -f $@; exit 1; fi
	@$(PYTHON) tools/pages.py $(BUILD)/$(MAIN).log

numbers:
	$(PYTHON) tools/paper_numbers.py
	$(PYTHON) tools/paper_settings.py

figures:
	$(PLOT_PY) tools/charts.py --journal $(JOURNAL)

floats: 
	@mkdir -p $(BUILD)
	$(LATEX) -output-directory=$(BUILD) floats.tex > $(BUILD)/floats.out || (tail -30 $(BUILD)/floats.out; exit 1)
	$(LATEX) -output-directory=$(BUILD) floats.tex > $(BUILD)/floats.out || (tail -30 $(BUILD)/floats.out; exit 1)
	@echo "$(BUILD)/floats.pdf"

lint:
	$(PYTHON) tools/lint.py --journal $(JOURNAL)

inventory:
	$(PYTHON) tools/lint.py --inventory > $(BUILD)/inventory.txt
	@echo "$(BUILD)/inventory.txt"

submit: pdf
	$(PYTHON) tools/flatten.py --journal $(JOURNAL)

clean:
	rm -rf $(BUILD) submit
