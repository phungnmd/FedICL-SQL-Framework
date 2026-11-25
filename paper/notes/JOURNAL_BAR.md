# FedLS-SQL: what the two target journals require and publish

Read 2026-11-19. Journal facts come from the journals' own pages; the
bar comes from recent papers of each journal closest to ours. CMC: 7
papers, all read in full. JIIS: 4 read in full (open access), 5 by
abstract only (paywalled); statements about seeds, tests and structure at
JIIS rest on the 4. The key facts of the two closest papers (LESFT at
CMC, GradeSQL at JIIS) were read a second time from the source. The full
tables with quotes and links are in section 4.

## 1. Journal facts

| | CMC (Computers, Materials & Continua) | JIIS (Journal of Intelligent Information Systems) |
|---|---|---|
| Publisher | Tech Science Press, open access | Springer, hybrid |
| Scope | computer networks, AI, big data, software engineering, security, IoT, materials | "integration of artificial intelligence and database technologies"; query languages and interfaces are a listed topic |
| Impact factor (publisher page, 2025) | 2.4 | 3.5 |
| Quartile | Scimago 2025: Q2 (SJR 0.513, Computer Science Applications). JCR: Q3 on Peeref (JCR 2024). Read 2026-11-20 from search results, pages not opened | Scimago 2025: Q2 (SJR 0.775, Information Systems; Q2 since 2017). JCR: Q3 on Peeref (JCR 2023), Q2 on LetPub. Same reading |
| Length | no limit; the fee covers 15 pages | 25 pages at submission, with references, tables and figures |
| Format | Word or LaTeX template | LaTeX only (Springer macro, `smallcondensed`) |
| Abstract, keywords | 200 to 400 words; 3 to 10 keywords | 150 to 250 words; 4 to 6 keywords |
| Cost | USD 1,600 up to 15 pages, USD 100 per page above; USD 1,800 base for submissions from 2027-01-01 | none on the subscription route; USD 3,590 for open access |
| Review | single blind, at least two reviewers; 25 days to first decision and 71 days to acceptance on average (journal figures, 2025); acceptance rate 25% | "first decision response in three months"; blind model and acceptance rate not stated |
| Received to accepted in the papers read | 61 to 116 days | 88 to 209 days |
| Required statements | availability of data and materials, ethics, funding, author contributions, conflicts | data availability, competing interests, funding |
| Use of AI tools | must be disclosed (tool and purpose) in Methods or Acknowledgement; spelling and grammar checks are exempt | use of an LLM documented in Methods; AI-assisted copy editing is exempt |
| References | numbered, Vancouver style | numbered, Springer basic style |

Neither journal requires highlights, a limitations section or released
code.

## 2. What the read papers have

| | CMC (7 full texts) | JIIS (4 full texts) |
|---|---|---|
| Kind of contribution | known mechanisms combined and adapted to a setting in 5 of 7 | the same in 3 of 4; GradeSQL adapts a published mechanism to Text-to-SQL |
| Datasets | 2 to 5 public benchmarks | Text-to-SQL papers: Spider and/or BIRD only |
| Models | at least 3 models or sizes in every language-model paper | GradeSQL 7, one paper 3, one paper 1 |
| Baselines | 4 to 5 in language-model papers; 8 to 12 in classical federated papers | 2 close ones in GradeSQL; 11 in the one federated paper |
| Seeds | stated in 1 of 7 (3 seeds, mean and std) | one fixed seed in GradeSQL; mean of 5 runs in two papers; no std in any |
| Significance tests | none | GradeSQL: McNemar with Bonferroni correction |
| Gain over the strongest baseline | +0.9 to +19.5 points | +0.9 to +4.3 EX points in GradeSQL; 3 to 6 points in other Text-to-SQL papers |
| Federated settings | each federated paper varies clients or Dirichlet alpha and reports cost or communication; privacy is data isolation | the one federated paper has a cost section and a local-DP section |
| Limitations | no section; folded into discussion or future work | an explicit part in 3 of 4 |
| Code | released in 3 of 7 | released in all 4 |
| Length | 15 to 32 pages | 24 to 37 published pages |

The two closest papers:

- LESFT (CMC 2026): split federated LoRA fine-tuning with a changed loss.
  Qwen2.5-0.5B, 1.5B and 3B; 3 datasets; 4 clients, 1 to 5 varied; no
  non-IID test; baselines centralized SFT, FedAvg, split learning,
  SplitLoRA, SplitFrozen; a table of latency and communication; no seed,
  std or test stated.
- GradeSQL (JIIS 2026): candidates sampled from the model, labelled by
  execution, used to fine-tune a scorer. BIRD dev (1,534), Spider dev
  (1,034), Spider test (2,147); 7 models from 1B to 8B, among them
  Qwen2.5-1.5B-Instruct; "Runs used a fixed seed of 42"; McNemar with
  Bonferroni; gains of +0.93 to +4.33 EX; code, data and models released.

## 3. What this means for our paper

Already at the level of what both publish:

- Spider test and BIRD dev with execution accuracy.
- One seed with per-question McNemar tests: the protocol of GradeSQL,
  and more than any CMC paper read reports.
- A gain of 3.3 to 3.5 EX over the federated baseline at equal rounds.
- An ablation per part of the method.
- A non-IID split (alpha 0.1), privacy as data isolation.

Not there yet, by how often the read papers have it:

1. More than one model. Every CMC language-model paper has 3 or more;
   LESFT uses three Qwen2.5 sizes. At JIIS it is common but not general.
2. A cost or communication table (all federated papers read).
3. One federated factor varied: number of clients or alpha (all CMC
   federated papers; no evidence either way at JIIS).
4. Baselines: 2 federated ones now. Centralized SFT (queued) and a
   local-only line would give 4, the count of LESFT.
5. A correction for multiple comparisons where several McNemar tests are
   printed (GradeSQL).
6. For JIIS: a limitations part and released code and predictions.

Not needed by this evidence: standard deviations, differential privacy.

Seeds (revised 2026-11-26): GradeSQL has one fixed seed, and two of the
four JIIS full texts report the mean of 5 runs. A McNemar test measures
the test questions, not the difference between two training runs. The
paper runs a second training seed of the two main rows on BIRD
(`RESEARCH_STATE.md`, section 3.4); the other rows keep one seed.

Federated papers at JIIS, by title (Crossref, title search for
"federated" in ISSN 1573-7675, 2026-11-25): six from 2024 to 2026, four
on recommendation (FedRKG among them), one on intrusion detection in
vehicular networks, one on multi-source data analysis; none on a
language model. Their full texts were not read (Springer refused
automated requests), so their client counts and non-IID levels are not
known here. The setups of federated LoRA papers are in
`FEDERATED_DATA_SETUP.md`, section 2.5; the paper's five setups follow
its section 4.2 (`RESEARCH_STATE.md`, section 3.4).

Fit:

- JIIS is the closer home for the topic (at least 7 Text-to-SQL papers
  in 2025-2026, one with our evaluation protocol) and costs nothing. No
  paper on federated learning with language models was found there, so
  the paper would open on the database problem, and the limit is 25
  pages.
- CMC takes the kind of contribution (a known mechanism adapted to a
  setting), is faster and states its acceptance rate. Its language-model
  papers all run several models, and it has one Text-to-SQL paper, an
  evaluation study.

Writing conventions seen in both:

- Title: "Name: mechanism for the task in the setting".
- Introduction ends with 3 to 4 contribution bullets; at JIIS the last
  one is the released resources.
- Related work is section 2.
- JIIS: results ordered by research questions, a separate ablation
  section, a short limitations section, a paragraph with the seed and
  the serving setup, prompts in an appendix; abstract with at most one
  number.
- CMC: abstract of 200 to 400 words ending with the main numbers; limits
  of the work in the discussion or as future work.

Not verified: the JCR quartiles of both journals on Clarivate itself (the
Scimago quartiles come from search results of 2026-11-20); the JIIS blind
model and acceptance rate; everything beyond the abstract for the 5
paywalled JIIS papers. "Not stated" for seeds and tests in a paper rests
on a text search of the full text.

## 4. Papers read

CMC, all in full:

| Paper | Link | What it is |
|---|---|---|
| LESFT: sample-efficient split fine-tuning | https://www.techscience.com/cmc/v87n1/66082 | split federated LoRA, 3 Qwen2.5 sizes |
| FedCO: consistency optimization under non-IID data | https://www.techscience.com/cmc/v89n1/68400 | 3 vision sets, 8 baselines, 4 alpha values, +0.92 over the strongest |
| FedCCM: clustered client momentum | https://www.techscience.com/cmc/v86n3/65485 | 3 vision sets, 12 baselines, 100 clients |
| Open-source LLM agents for SQL generation | https://www.techscience.com/cmc/v88n2/67604 | evaluation study, Spider dev, no method |
| TinySecGPT | https://www.techscience.com/cmc/v87n2/66574 | LoRA tuning of 6 small models for a domain |
| Task-structured curriculum for multi-task distillation | https://www.techscience.com/cmc/v86n3/65435 | 5 datasets, 3 T5 sizes, 3 seeds, +1.7 to 2.6 |
| Activation steering and RL for compact models | https://www.techscience.com/cmc/v88n3/68139 | 3 models of 1.5B, one synthetic dataset |

JIIS:

| Paper | Link | Read |
|---|---|---|
| GradeSQL | https://link.springer.com/article/10.1007/s10844-026-01071-6 (arXiv 2509.01308) | full |
| FedRKG: personalized federated recommendation | https://link.springer.com/article/10.1007/s10844-026-01089-w | full |
| LLASP: fine-tuning LLMs for answer set programming | https://link.springer.com/article/10.1007/s10844-025-01017-4 | full |
| LLIMONIIE: Italian information extraction | https://link.springer.com/article/10.1007/s10844-025-00978-w | full |
| SKT-SQL | https://link.springer.com/article/10.1007/s10844-025-00963-3 | abstract |
| PPR-SQL | https://link.springer.com/article/10.1007/s10844-026-01049-4 | abstract |
| LU-SQL | https://link.springer.com/article/10.1007/s10844-026-01032-z | abstract |
| Self-refinement loop for Text-to-SQL | https://link.springer.com/article/10.1007/s10844-026-01050-x | abstract |
| FinSent-DistillQ | https://link.springer.com/article/10.1007/s10844-025-01020-9 | abstract |

Journal pages: https://www.techscience.com/cmc/info/journal_overview ,
https://www.techscience.com/cmc/info/auth_instru ,
https://www.techscience.com/cmc/info/article_charge ,
https://link.springer.com/journal/10844/aims-and-scope ,
https://link.springer.com/journal/10844/submission-guidelines .
