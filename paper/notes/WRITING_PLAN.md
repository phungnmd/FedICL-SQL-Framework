# FedLS-SQL: writing plan

Written 2026-11-26. How the manuscript is written: format, tools, the
structure of the paper, its tables and figures, and the steps in order.
What the paper claims and which rows exist is in `RESEARCH_STATE.md`
(sections 3.1, 3.4, 5.0); this file does not repeat it.

## 1. Fixed choices

| Part | Choice |
|---|---|
| Format | LaTeX, written to the JIIS shape first (25 pages, the tighter of the two). Section bodies live in `sections/*.tex` with no class-specific command, so a CMC version is a second main file, not a rewrite (section 9) |
| Class | Springer Nature `sn-jnl` (December 2024 package), `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`, BibTeX with `sn-basic.bst` |
| Place | `paper/manuscript/` in the paper repository; one commit per section |
| Who writes | the main session drafts every section, so the paper has one voice. Subagents (Opus) build the bibliography, audit claims and read the PDF cold |
| Numbers | no result number is typed. A script writes macros and tables from the committed evaluations (section 5) |
| Names | the method is `\method` and the paper says "the model", so the title can change without touching the text |
| What a writer reads | `CLAIMS.md` (step W3), the notes section named for its section in section 4, the generated tables. Not `LAB_LOG.md` |

Three things to check by hand before step W5; they could not be read
on 2026-11-26 because Springer sends automated requests to a login page:

1. The JIIS submission guidelines: the class it names (`JOURNAL_BAR.md`
   records the older Springer macro with `smallcondensed`; Springer's
   LaTeX page says `sn-jnl` serves every Springer Nature journal), the
   page format the 25 pages are counted in, and whether the manuscript
   is anonymised.
2. Springer Nature's rule on figures made with AI tools, for Fig. 1.
3. Which journal goes first. This plan assumes JIIS.

## 2. Tools

| Tool | Use | On the Mac |
|---|---|---|
| `pdflatex`, `bibtex` (TeX Live 2026 basic) | build; Springer requires that the source compiles with pdflatex | installed |
| TeX packages `sttools`, `threeparttable`, `appendix`, `ncctools`, `algorithms` | needed by `sn-jnl.cls` and its template (the template stops at `cuted.sty` today) | missing |
| `make` | `make` (pdflatex, bibtex, pdflatex twice), `make numbers`, `make lint`; `latexmk` is not needed | installed |
| `paper/notes/tools/overview_results.py` | `build()` returns every committed run (EX, difficulty levels, execution errors, wrong results, result commit) and every McNemar test; the paper's script imports it | exists |
| `paper/figures/render.py`, `STYLE.md` | diagrams (Fig. 1 exists) | exists |
| matplotlib | result charts, drawn at 119 mm in Arial 8 pt from the same data | installed with Python 3.11 |
| `pdftotext` | page and word counts, text for the cold reader | installed |
| `/ars-citation-check` | reference metadata against DOI and arXiv | installed |
| `/ars-reviewer` | cold read of the PDF as a journal reviewer | installed |
| `/ars-disclosure` | the AI-use statement | installed |
| `humanizer` | last pass on the prose | installed |

Install, not yet run:

```
tlmgr --usermode install sttools threeparttable appendix ncctools algorithms
```

Not used: `/ars-full` and `/ars-plan` (they start from a literature
search and a dialogue and know nothing of the committed results), Word,
Overleaf.

## 3. Folder

```
paper/manuscript/
  main.tex              JIIS wrapper: class, title, abstract, \input of the sections
  sections/             01_intro 02_related 03_method 04_setup 05_results
                        06_ablation 07_discussion 08_conclusion 90_declarations
                        A_prompt B_settings
  generated/            numbers.tex, tab_*.tex, missing.txt (written by the script, committed)
  figures/              fig_*.pdf (copied from paper/figures and the chart script)
  references.bib
  sn-jnl.cls  sn-basic.bst
  CLAIMS.md             thesis, contributions, claims with their keys, terms and notation
  tools/paper_numbers.py  tools/charts.py  tools/lint.py
  Makefile
```

## 4. Structure of the paper

Budget for 25 pages in `sn-jnl`, references included; it is measured on
the first build with empty tables in place and corrected then. Results
follow research questions and the ablations have their own section, as
in the JIIS papers read (`JOURNAL_BAR.md`).

| # | Section | Pages | Content | Notes to read | Can be written |
|---|---|---:|---|---|---|
| | Title, abstract, keywords | 0.7 | title as "Name: mechanism for the task in the setting"; abstract of 150 to 250 words with one number (the gain on BIRD); 4 to 6 keywords | `JOURNAL_BAR.md` 3 | last |
| 1 | Introduction | 1.8 | small models for Text-to-SQL where data cannot be pooled; FedAvg SFT learns from one gold SQL and never uses the databases, federated DPO as published keeps its first pairs and reference; execution is available only at the client; the method in three sentences; headline results; a sentence that "federated Text-to-SQL" here means training, not querying federated databases; 4 contribution bullets, the last the released code, splits and predictions | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 | after 5 and 6 |
| 2 | Related work | 2.0 | 2.1 small models for Text-to-SQL; 2.2 preference optimization and execution feedback for SQL and code; 2.3 federated fine-tuning of language models, federated DPO; 2.4 federated semantic parsing and Text-to-SQL; Table 1 | `LITERATURE.md` 1.2, 1.3, 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6 | now |
| 3 | Method | 4.0 | 3.1 setting and notation (clients, databases, questions, what leaves a client); 3.2 overview, Fig. 1; 3.3 SFT warm-up rounds; 3.4 a preference round: sampling, execution labels, pairs, the DPO + NLL loss with the round's global model as reference, aggregation; Algorithm 1; 3.5 what it costs a client | `RESEARCH_STATE.md` 3.2, 3.3 (settings), 3.8; `DPO_RESEARCH.md` 3.1 to 3.4 | now |
| 4 | Experimental setup | 2.5 | datasets and metrics; federated setups, Table 2; models; the six baselines; implementation (prompt, LoRA, rates, rounds, sampling, decoding, seed, serving); McNemar test with Holm correction | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4 | now |
| 5 | Results | 6.0 | RQ1 against the baselines (Table 3, Fig. 2); RQ2 other models and federated setups (Tables 4, 5); RQ3 perturbed questions and test-suite accuracy (Table 6); RQ4 what changes in the errors and what it costs (Fig. 3, Table 7) | `RESEARCH_STATE.md` 5.0; generated tables | each part when its rows are in |
| 6 | Ablation study | 2.0 | on-policy rounds, the NLL term, the preference term, the number of warm-up rounds, aggregation weights, pooled clients (Table 8) | `RESEARCH_STATE.md` 5.0, second table | when its rows are in |
| 7 | Discussion and limitations | 1.3 | why the two kinds of round differ in the errors they remove; limits: clients need gold SQL and databases that can be queried, full participation and 5 to 10 clients, isolation of data and not differential privacy, added client compute | `RESEARCH_STATE.md` 3.1, 5.0 | after 5 and 6 |
| 8 | Conclusion | 0.4 | | | last |
| | Declarations | 0.4 | funding, competing interests, data availability, code availability, author contributions, use of AI tools | `JOURNAL_BAR.md` 1 | last |
| | References | 3.0 | 45 to 55 entries | | grows with the text |
| A, B | Appendix | 1.0 | A the prompt as the model saw it; B all settings in one table | `LITERATURE.md` 1.19 | now |

Supplementary file (outside the 25 pages): every McNemar test with its
adjusted p, pairs per client and round, cosine of the client updates,
the per-client statistics of the five splits, EX by round of every line.

## 5. Tables and figures

`tools/paper_numbers.py` imports `build()`, writes one macro per cell
(`\ex{bird}{k2}{4}`, `\gain{...}`, `\pval{...}`) and one `tab_*.tex` per
table, prints `--` for a row that is not committed and lists those rows
in `generated/missing.txt`. The Holm correction runs over the tests the
paper prints. A row enters a table by one line in `ARMS` of
`overview_results.py`, as for the overview page.

| Item | Content | Rows still missing (2026-11-26) |
|---|---|---|
| Fig. 1 | method overview | none (`paper/figures/fig_method_overview.svg`) |
| Algorithm 1 | the method: k warm-up rounds, then preference rounds | none |
| Table 1 | closest work by property: federated, execution labels, on-policy pairs, NLL term, model size (FL4SP, OpenFedLLM, CodeLutra, ExCoT, ours) | none |
| Table 2 | the five federated setups: clients, split, questions and databases per client | none, read from the split files |
| Table 3 | main: BIRD dev and Spider test; no training, local SFT, centralized SFT, FedAvg SFT, FedProx SFT, federated DPO as published, the method; EX, difficulty levels, gain and p against FedAvg SFT | BIRD: local SFT, centralized SFT, FedProx, federated DPO, second seed of two rows. Spider: local SFT, FedProx, federated DPO round 2 |
| Fig. 2 | EX by round, FedAvg SFT (to round 5) and the method, both datasets | none |
| Table 4 | three models on Spider, DeepSeek-Coder-1.3B on BIRD | DeepSeek rounds on Spider; all of BIRD |
| Table 5 | FedAvg SFT and the method in the five setups | IID, alpha 0.5 with 5 clients, alpha 0.5 with 10 clients |
| Table 6 | Spider-Syn, Realistic, DK; test-suite accuracy | the test-suite numbers are not committed |
| Fig. 3 | wrong answers by round split into execution errors and wrong results, FedAvg SFT and the method | none |
| Table 7 | client time per round (sampling, labels, training) and megabytes sent | none, read from the logs (`scripts/log_times.py`) |
| Table 8 | ablations at 4 rounds, BIRD and Spider | BIRD: without the preference term round 2, without NLL, k = 0 rounds 3 and 4, k = 3. Spider: without the preference term round 2, pooled clients |

## 6. Steps

Each step ends at its gate. Times are the owner's and the machine's,
estimates.

| Step | What | Gate | Time |
|---|---|---|---|
| W0 | the three checks of section 1 | answers written into section 1 | owner, 15 min |
| W1 | TeX packages, the folder of section 3, `main.tex` with empty sections | `make` gives a PDF | a few minutes of install |
| W2 | `paper_numbers.py`, the eight table files, `charts.py` for Fig. 2 and 3 | every cell equals the overview page; `missing.txt` equals the missing rows of section 5 | none |
| W3 | `CLAIMS.md`: the thesis in one sentence, 4 contributions, each claim with the macros that carry it and the sets it is stated for, the terms and the notation | owner approves | owner, 30 min |
| W4 | `references.bib`: a subagent takes the papers of `LITERATURE.md` and `DPO_RESEARCH.md` section 7 that the outline cites, fetches each entry from its DOI or arXiv id, prefers the published version, and records how far the paper was read (full or abstract) | `/ars-citation-check` clean; no entry typed by hand | none |
| W5 | Method, Algorithm 1, Experimental setup, appendix A and B | per-section loop below | owner, 30 min each |
| W6 | Related work, Table 1 | same | owner, 30 min |
| W7 | Results, part by part as `missing.txt` empties; Ablation study | same; a part is not written around `--` cells | waits for the GPU rows |
| W8 | Discussion and limitations, Conclusion, Introduction, abstract, title, keywords | same | owner, 1 h |
| W9 | whole paper: cold read of the PDF (`/ars-reviewer`), claim audit of the full text, `humanizer`, page count against 25 | owner and advisor read | advisor's time |
| W10 | declarations, AI-use statement (`/ars-disclosure`), public repository with code, splits and predictions, cover letter | submission files compile from a clean copy | owner, 1 h |

W1 to W6 need no result that is missing and can start now. When an
evaluation is committed later: one line in `ARMS`, `make numbers`,
`make`, and the claim audit runs again for the claims that use that row.

Per-section loop (W5 to W8):

1. Draft from `CLAIMS.md`, the notes of section 4 and the generated
   tables.
2. `make` and `make lint`.
3. Claim audit: a subagent with all the notes (`RESEARCH_STATE.md`,
   `LAB_LOG.md`) looks for a committed result that contradicts each
   sentence. It reports false or overstated sentences only; it does not
   ask for caveats or for the story of how a value was chosen.
4. Fix, owner reads, commit.

## 7. Rules for the text

- The setup is given as values. How a seed, a round, k or a setting was
  picked is not told. No sentence is false: a number chosen on Spider
  test is not called held-out, and the BIRD rows are BIRD dev.
- A claim names the set it holds on. Example: on-policy rounds are
  above fixed pairs on BIRD; on Spider test the two are level, so the
  paper does not say "on both datasets".
- "The model", never "the student"; no arm names, queue names, dates or
  "we first tried".
- A statement about another paper comes from a section of
  `LITERATURE.md` or `DPO_RESEARCH.md`; a paper read by abstract is
  cited only for what its abstract states. External result rows name
  their prompt, decoding and training data, or are left out.
- Numbered citations; an acronym is defined at first use in the
  abstract and again in the text; no em dash.

## 8. Checks

| Check | Tool | Fails on |
|---|---|---|
| Build | `make` | undefined reference or citation, overfull table |
| Numbers | `tools/lint.py` | a digit with a decimal point or a percent sign in sections 5 to 7 that is not a macro |
| Words | `tools/lint.py` | student, owner, queued, held-out, arm names, em dash |
| Bibliography | `tools/lint.py`, `/ars-citation-check` | entry without DOI or arXiv id, uncited entry, citation of a preprint that has a published version |
| Claims | subagent, section 6 | a sentence a committed result contradicts |
| Reader | `/ars-reviewer` on the PDF alone | reported to the owner; a comment is acted on when the paper gets better, not because it was made |
| Length | `pdftotext`, page count | more than 25 pages; abstract outside 150 to 250 words |

## 9. A CMC version

Same sections and tables, a second wrapper `main_cmc.tex` on the Tech
Science Press class (`TSP-Latex.zip`: `tsp.cls`, `vancouver.bst`):

- abstract of 200 to 400 words ending with the main numbers; 3 to 10
  keywords;
- statements as the class commands (acknowledgement, funding, author
  contributions, availability of data and materials, ethics approval,
  conflicts of interest); appendices before the references;
- figures at most 16.51 cm wide, labels in Arial or Helvetica of 8 pt
  or more (the figure standard already meets this);
- no page limit; the fee covers 15 pages, so the supplementary tables
  may move into the appendix only if the pages are paid for;
- use of AI tools that changes wording or structure is disclosed in the
  acknowledgement, and the caption of a diagram prepared with an AI
  tool names the tool and its version (author instructions, read
  2026-11-26);
- the class needs `CJKutf8`, `verse`, `bbm` and `mathcomp`, not
  installed.
