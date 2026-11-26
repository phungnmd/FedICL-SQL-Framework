# Bibliography: sources by section and how they were verified

`references.bib` holds 55 entries, built on 2026-11-26 from the papers
of `LITERATURE.md`, `DPO_RESEARCH.md`, `JOURNAL_BAR.md` and
`RESEARCH_STATE.md` (section 3.6), with the works the setup names.

## 1. Verification

- Each entry was written from a bibliographic record fetched that day,
  never from memory. The record is named in the comment above the entry
  in `references.bib`: the arXiv API, Crossref, the ACL Anthology, and
  the proceedings pages of NeurIPS, PMLR and MLSys.
- A second pass by the main session compared every entry again: all 50
  arXiv ids against the arXiv API and all 35 DOIs against Crossref
  (title, first author, number of authors, year, pages). Every id and
  DOI resolves. The only differences are the five listed in section 4,
  where the published record and the arXiv record disagree.
- The published version is preferred over the preprint; the arXiv id
  stays in `eprint`.
- All 55 entries compile with `sn-basic.bst` in the class of the
  manuscript without a warning. Set in that style they take 5.6 pages
  (the plan allowed 2.8 for 45 to 55 entries).

## 2. Sources by section

What each paper did, as the project's notes record it.

| Section | Key | What the paper did |
|---|---|---|
| 1 | li2024codes, li2025omnisql, mcmahan2017fedavg, ye2024openfedllm, zhang2023fl4sp, tao2024codelutra | framing: small open Text-to-SQL models, FedAvg, federated DPO, the earlier federated Text-to-SQL work, the closest centralized loop (rows below) |
| 2.1 | li2024codes | StarCoderBase pre-trained further on 21.5 GB of SQL-centric data, then full SFT; CodeS-1B Spider dev EX 77.9, TS 72.2 (Table 5) |
| 2.1 | li2025omnisql | SynSQL-2.5M; Qwen2.5-Coder-7B greedy Spider test: base 82.2, gold Spider + BIRD SFT 80.7, CoT SFT 86.6 (Table 5) |
| 2.1 | sheng2025slmsql | Qwen2.5-Coder 0.5B and 1.5B: SFT on 916K CoT rows, then GRPO on BIRD train; 1.5B Spider test SC@16 78.42 (Table 3) |
| 2.1 | zhang2025spftsql | verified synthesis plus self-play; Qwen2.5-Coder-1.5B Spider test EX: zero-shot 72.3, LoRA SFT 78.0, method 82.3 (Table 1) |
| 2.1 | papicchio2025think2sql | GRPO on BIRD train; 1.5B BIRD dev 27.5 to 44.2 (gold tables, temperature 0.7) |
| 2.1 | pourreza2025reasoningsql | GRPO with SQL partial rewards; 3B BIRD dev SFT 55.9 to 58.67 (Table 3) |
| 2.1 | yao2026arctic | GRPO with an execution-match reward; 7B BIRD dev 68.9, Spider test 88.8; drops training rows with empty gold results |
| 2.1 | zhong2024kid | knowledge distillation for Text-to-SQL into TinyLLaMA-1.1B; average of 5 sets: SFT 46.9, KID 51.8 |
| 2.1 | gao2024dailsql, pourreza2023dinsql, li2023resdsql | prompting with GPT-4 (DAIL-SQL, DIN-SQL) and schema ranking before skeleton decoding (RESDSQL); abstracts, DAIL-SQL section 3.1 |
| 2.1 | tritto2026gradesql | JIIS: execution-labelled outcome reward models rank SQL candidates; Spider test 87.47 against 85.47 for majority vote at N = 32 (RQ3); McNemar with Bonferroni, fixed seed |
| 2.1 | yi2025sktsql | JIIS: schema selection, SQL skeleton and T5 slot filling for small models (abstract) |
| 2.1, 4.5 | chang2023prompt | prompt formats for Text-to-SQL: CREATE TABLE text with example rows (sections 3 to 5, appendix A.1) |
| 2.2, 3.4 | rafailov2023dpo | the DPO loss; the reference model kept close to the distribution of the pairs |
| 2.2, 3.4 | tao2024codelutra | on-policy loop: 10 samples at temperature 1.0, execution labels, DPO + SFT (beta 0.1, lambda 1), LoRA r 8, 4 iterations; Spider 59.3 to 76.6, BIRD 22.3 to 43.1 (Table 1); DPO term alone 17.2 (Table 2); non-executable BIRD errors 40% to 11% (section 6) |
| 2.2, 3.4, 6 | pang2024irpo | self-sampled pairs labelled by correctness, DPO + NLL, gold added as chosen when no sample is correct; GSM8K 73.1 to 81.6 over four rounds, 61.8 without NLL (Table 1) |
| 2.2 | liu2025cotdpo | execution-labelled DPO on BIRD for 10 models of 6.7B to 15B; SQL-only DPO lowers EX for 6 of 10 (Table 1) |
| 2.2 | zhai2025excot | one off-policy and two on-policy DPO rounds; 70B BIRD dev 58.1 to 68.5 (Tables 1 and 2) |
| 2.2 | yang2024sense | GPT-4 synthetic SFT data, then DPO on pairs from a weak model; the DPO step adds 0.2 to 0.9 on Spider dev (Table 5) |
| 2.2 | zhang2025exesql | execution success against failure as preference pairs for SQL dialects (Table 9) |
| 2.2 | zhang2025codedpo | self-generated code and tests ranked for preference training (abstract) |
| 2.2 | prasad2025scpo | pairs from vote counts, DPO + NLL; GSM8K 63.91 without labels against 64.29 with gold (Table 1) |
| 2.2, 6 | miao2024aligning | DPO on the model's own samples beats SFT on correct samples; pairs from another model end below the start (Table 1) |
| 2.2, 3.4 | lanchantin2025bridging | semi-online DPO (sampler synchronised every s steps); Math500 offline 53.7, s = 100 58.9, online 58.7 (Table 1) |
| 2.2 | ni2023lever, shi2022mbrexec | execution at inference: a learned verifier, Spider dev 75.3 to 81.9 (LEVER, Table 2); execution-result MBR (abstract) |
| 2.3, 3, 4.4 | mcmahan2017fedavg | FedAvg |
| 2.3, 4.5 | hu2022lora | LoRA |
| 2.3 | zhang2024fedit | federated instruction tuning with LoRA (not read) |
| 2.3 | kuang2024fsllm | LoRA package for federated learning; Fed-CodeAlpaca HumanEval: centralized 13.54, FedAvg 13.29, local 10.99 |
| 2.3, 4.4 | ye2024openfedllm | FedDPO inside FedAvg with fixed pairs and a fixed reference (section 3); code HumanEval FedAvg 0.165, local 0.116 |
| 2.3 | ye2024fedllmbench, gao2025flowertune | federated LLM benchmarks: FedAvg 5.51 against FedProx 5.49 (Fed-ChatbotIT); coding average FedAvg 45.25, FedProx 44.65 (FlowerTune, Tables 7 and 8) |
| 2.3 | wu2025fedbiscuit | clients train preference selectors and the server runs DPO; FedDPO is its baseline |
| 2.3 | nayak2026pubswap, guo2026fedgrpo | verifier-driven federated RL: federated GRPO with public prompts, Qwen3-1.7B FedAvg-GRPO 50.7 to 55.8; reward-weighted aggregation, math average FedAvg 37.10, Fed-GRPO 39.06 (Table 4) |
| 2.3 | wu2026fedsurvey | survey; lists BIRD among the code benchmarks for federated evaluation |
| 2.4, 4.2 | zhang2023fl4sp | eight single-domain datasets as clients, T5-base; macro-average EM: centralized 70.3, FedAvg 40.0, FedOPT + Lorar 62.6 |
| 2.4 | xu2024kgrfl | federated BART parser (question to SPARQL) with RL-based fusion of client models (abstract) |
| 4.1 | li2023bird, yu2018spider | the BIRD and Spider datasets |
| 4.1 | gan2021spidersyn, deng2021realistic, gan2021spiderdk | Spider-Syn, Spider-Realistic, Spider-DK |
| 4.1, 7 | zhong2020testsuite | test-suite accuracy; EX on one database has a mean false-positive rate of 6.5% over 21 Spider-dev submissions (Table 2) |
| 4.2 | hsu2019noniid | the Dirichlet partition by label |
| 4.2 | li2022niidbench | the label-distribution-skew partition our split follows (per label, client proportions from a Dirichlet); added 2026-11-26 from Crossref and the arXiv API |
| 4.3 | hui2024qwen25coder, guo2024deepseekcoder | Qwen2.5-Coder (1.5B and 0.5B) and DeepSeek-Coder-1.3B |
| 4.4 | li2020fedprox | FedProx |
| 4.5 | loshchilov2019adamw, kwon2023vllm | AdamW; vLLM for decoding |
| 4.6 | mcnemar1947note, dietterich1998tests | McNemar's test; its use on the paired predictions of two learners |
| 4.6 | holm1979simple | the Holm correction |

Sections 3.5 and 8 and the declarations need no source.

## 3. How far the notes read each paper

A sentence about a cited paper is limited to what was read.

| Read | Keys |
|---|---|
| In full | tao2024codelutra (figures not read), li2024codes, li2025omnisql, ye2024openfedllm, kuang2024fsllm, tritto2026gradesql, pang2024irpo, ye2024fedllmbench, liu2025cotdpo (Spider appendix not read), yang2024sense, sheng2025slmsql, zhong2020testsuite, zhang2023fl4sp, zhong2024kid, prasad2025scpo, wu2025fedbiscuit, zhai2025excot, yao2026arctic, papicchio2025think2sql, pourreza2025reasoningsql, nayak2026pubswap, guo2026fedgrpo |
| In part | rafailov2023dpo (the passage on the reference model), gao2024dailsql (section 3.1), gao2025flowertune (sections 2 to 4.3, Tables 1, 2, 7, 8), zhang2025spftsql (sections 3 and 4, Table 1, appendix A.3 and A.4), zhang2025exesql (section 3.4, appendix A.3 and A.4, Table 9), ni2023lever (sections 2 to 4, Table 2), wu2026fedsurvey (the benchmark section and table), lanchantin2025bridging (Table 1, abstract), miao2024aligning (Table 1), hui2024qwen25coder (section 7.4), chang2023prompt (sections 3 to 5, appendix A.1) |
| Abstract | pourreza2023dinsql, li2023resdsql, yi2025sktsql, xu2024kgrfl, shi2022mbrexec, zhang2025codedpo |
| Not read (cited as the source of a dataset, model, method or test) | mcmahan2017fedavg, hu2022lora, loshchilov2019adamw, li2023bird, zhang2024fedit, kwon2023vllm, mcnemar1947note, dietterich1998tests, holm1979simple, deng2021realistic, yu2018spider, gan2021spidersyn, gan2021spiderdk, li2020fedprox, hsu2019noniid, guo2024deepseekcoder |

## 4. Where the records differ from the notes or from each other

- The four entries that were in `references.bib` are now the published
  versions: DPO (NeurIPS 36), CodeLutra (TMLR 2025; the key keeps
  2024), FedAvg (PMLR 54, pp. 1273 to 1282), LoRA (ICLR 2022).
- The notes say "venue not verified" for five papers that are
  published: OpenFedLLM and FederatedScope-LLM (KDD 2024), FedLLM-Bench
  (NeurIPS 2024, Datasets and Benchmarks), ExCoT (Findings of ACL 2025;
  the published title drops "ExCoT:"), Arctic-Text2SQL-R1 (Findings of
  ACL 2026).
- KGRFL: the notes say 2023; the issue is February 2024 (IEEE TCSS
  11(1)).
- Author lists that differ between arXiv and the published record; the
  entry follows the published record: BIRD (17 against 18 on arXiv),
  FedIT (8 against 9), Arctic-Text2SQL-R1 (9 against 10), DPO (Manning
  before Ermon), GradeSQL (Subramanian before Narducci, and a
  different title in the journal), FedAvg ("Brendan McMahan").
- Think2SQL: its arXiv comment points to a later paper in TMLR with
  another title; the entry is the preprint.

## 5. To check by eye

1. SLM-SQL (`sheng2025slmsql`). The ACL Anthology and Crossref give the
   second author as "Shuai, Xu Shuai"; arXiv gives "Shuai-Shuai Xu".
   The entry has "Xu, Shuai-Shuai". The Anthology also names the main
   proceedings as booktitle under a Findings id. Both on the PDF of the
   paper.
2. Holm (1979) has no Crossref record and its JSTOR DOI does not
   resolve. The entry is written from the OpenAlex record (title,
   author, journal, volume 6, pages 65 to 70; no issue number) and
   carries the stable address of JSTOR.
3. Six entries were checked on pages outside the planned sources,
   because DBLP and OpenReview answered with a browser challenge: LoRA,
   AdamW, FedBiscuit, CodeLutra and the federated survey on ML
   Anthology pages, FedProx on the MLSys proceedings page. Title,
   authors and year also agree with the arXiv record of each.
