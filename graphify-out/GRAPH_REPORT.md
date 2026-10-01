# Graph Report - FedICL-SQL  (2026-10-02)

## Corpus Check
- 170 files · ~836,694 words
- Verdict: corpus is large enough that graph structure adds value.
- Scope: This root scan followed `.gitignore`, so it excluded the separate `fedicl-sql/` code repository. The sole detected code file, `.claude/settings.local.json`, produced no AST nodes. This graph covers root and `paper/` documentation, references, and images.

## Summary
- 393 nodes · 368 edges · 77 communities (41 shown, 36 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output
- Token accounting: Agent usage was unavailable to the graph builder. The zeros above mean untracked usage, not a zero-cost extraction.
- Graph health: The incremental extraction had no missing endpoints, self-loops, or new undirected edge collapse. The initial full build collapsed 6 edge pairs in undirected mode.
- Incremental update: 4 changed `paper/notes/` files produced 33 new nodes and 51 new edges; 12 old nodes and 21 old edges were replaced or removed.
- Benchmark note: `graphify benchmark` used a 19,650-word estimate and reported 21.8x fewer tokens per query; this estimate does not cover the detector's 836,694-word corpus.

## Community Hubs (Navigation)
- Methods and SeqKD Gates
- Current Experiment Matrix
- KD Evidence and Retention
- Federated Architecture Diagram
- Training Pass Results
- Archived Evidence Planning
- Federated Benchmark Results
- Data Isolation Architecture
- Current Experiment Queue
- Text to SQL Methods
- Historical KD and ICL
- Experiment Results Screenshot
- Protocol V2 Method Design
- Early Federated Runbooks
- Federated In Context Learning
- Federated Teacher Student Transfer
- SQL Benchmarks and Parsing
- ICL Prompt Methods
- Execution Guided Distillation
- BIRD Baseline Audit
- Transfer and Consolidation Reviews
- Related Work Novelty
- Communication and Secure Sum
- No ICL Ablation
- Early Server KD Method
- ICL Comparison Emails
- Early Paper Outlines
- Archived Manuscript Evidence
- Superseded Method Screens
- Manuscript and Figures
- Structured Knowledge Distillation
- Federated BART and QLoRA
- Few Shot Learning Surveys
- Federated ICL Methods
- Federated Mutual Transfer
- Text to SQL Distillation
- Interactive SQL Disambiguation
- LLM SQL Adaptation
- Prompting Method Surveys
- SQL Prompt Evaluation
- SQL Evaluation Datasets
- Seed One Trajectory
- Forward KL Runbooks
- Verified Teacher Targets
- Architecture Figure Source
- Interactive Architecture Figure
- Early KD Research
- Protocol V1 Claim Gates
- Archived Method Outline
- Protocol V1 Lab Log
- Protocol V1 Results
- Superseded Struct SQL
- Result Provenance Registry
- Federated NLP Thesis
- Embedding and Search
- Expected Information Gain
- Text to Text Parsing
- LLM Technical Reports
- Phi Four Report
- Prompt Engineering Survey
- Federated BART Study
- Federated NLP Experiments
- RESDSQL Parsing Method
- Chinese Embedding Resources
- GPU Similarity Search
- CodeS SQL Models
- Adversarial SQL Robustness
- T5 Transfer Learning
- Large Language Model Survey
- GPT Four Report
- Phi Four Model
- GPT Three Few Shot
- DAIL SQL Evaluation
- Manuscript Formatting Template
- FedProx Trajectory Diagnostic
- GKD Run Cancellation
- QLoRA Fine Tuning

## God Nodes (most connected - your core abstractions)
1. `Experimental results comparison table` - 12 edges
2. `Comparison of Base, Federated and Centralized FT evaluation results` - 10 edges
3. `Client or Organization` - 10 edges
4. `FedLS-SQL run queue` - 10 edges
5. `FedLS-SQL experiment matrix` - 7 edges
6. `Federated Coordination Server` - 6 edges
7. `FedLS-SQL lab log` - 6 edges
8. `FedLS-SQL system architecture` - 6 edges
9. `FedLS-SQL paper workspace guide` - 5 edges
10. `FedLS-SQL research project convention` - 5 edges

## Surprising Connections (you probably didn't know these)
- `FedLS-SQL paper workspace guide` --conceptually_related_to--> `Early FedLS-SQL paper outline`  [INFERRED]
  CLAUDE.MD → paper/2-[outline]-FedLS-SQL_A Novel Federated L-SLMs Framework for NL2SQL-Aug19.pdf
- `Federated LLM-SLM with schema-aware ICL PDF` --semantically_similar_to--> `Federated LLM-SLM with schema-aware ICL Markdown`  [INFERRED] [semantically similar]
  paper/archive/pre_fedls_2026-08/old_outlines/fedicl_sql_outline.pdf → paper/archive/pre_fedls_2026-08/old_outlines/fedicl_sql_outline.md
- `DAIL-SQL` --semantically_similar_to--> `DAIL-SQL`  [INFERRED] [semantically similar]
  paper/references/md/[9]-DAIL-SQL.md → paper/references/pdf/DAIL-SQL.PDF
- `Terminal private consolidation A>K>A` --conceptually_related_to--> `Lightweight adapters for server LLM and client SLM co-tuning`  [INFERRED]
  paper/results/MAIN_RESULTS.md → paper/references/pdf/[8]-2024-Fedcollm A parameter-efficient federated co-tuning framework for large and small language models.pdf
- `FedLS-SQL agent instructions` --references--> `FedLS-SQL research project convention`  [EXTRACTED]
  AGENTS.md → CONVENTION.MD

## Hyperedges (group relationships)
- **Data pass 1 comparison** — paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_fedavg_pre_kd_pass_1_5_clients_ex_57_35_em_50_58_execution_error_22_82, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_server_kd_pass_1_5_clients_ex_63_35_em_31_53_execution_error_12_86, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_centralized_ft_pass_1_ex_62_19_em_57_16_execution_error_20_41 [EXTRACTED 1.00]
- **Data pass 2 comparison** — paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_fedavg_pre_kd_pass_2_5_clients_ex_64_02_em_56_96_execution_error_18_38, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_server_kd_pass_2_5_clients_ex_66_15_em_33_56_execution_error_11_99, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_centralized_ft_pass_2_ex_67_02_em_62_57_execution_error_16_05 [EXTRACTED 1.00]
- **Data pass 3 comparison** — paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_fedavg_pre_kd_pass_3_5_clients_ex_66_05_em_60_15_execution_error_17_21, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_federated_post_server_kd_pass_3_5_clients_ex_69_54_em_38_59_execution_error_9_77, paper_archive_pre_fedls_2026_08_old_emails_screenshot_2026_08_19_at_10_10_21_centralized_ft_pass_3_ex_67_60_em_62_67_execution_error_15_76 [EXTRACTED 1.00]
- **Client Text-to-SQL Pipeline** — paper_archive_pre_fedls_2026_08_old_outlines_figures_fig_architecture_source_schema_encoder, paper_archive_pre_fedls_2026_08_old_outlines_figures_fig_architecture_source_retrieval_module, paper_archive_pre_fedls_2026_08_old_outlines_figures_fig_architecture_source_icl_prompt_constructor, paper_archive_pre_fedls_2026_08_old_outlines_figures_fig_architecture_source_local_slm, paper_archive_pre_fedls_2026_08_old_outlines_figures_fig_architecture_source_local_training [EXTRACTED 1.00]
- **Protocol V1 evidence map** — paper_archive_protocol_v1_no_bird_evidence_experiment_matrix_v1_protocol_v1_claim_gates, paper_archive_protocol_v1_no_bird_evidence_lab_log_v1_protocol_v1_evidence_and_limits, paper_archive_protocol_v1_no_bird_evidence_main_results_v1_protocol_v1_paper_results [INFERRED 0.85]
- **Fixed AKA teacher CoT comparison** — paper_notes_experiment_matrix_fixed_aka_teacher_cot_method_gate, paper_notes_pipeline_next_october_2_fixed_aka_cot_gate, paper_notes_pipeline_next_p2_11_auxiliary_plan_recipe, paper_notes_pipeline_next_full_gold_plus_teacher_plan_proposal [EXTRACTED 1.00]

## Communities (77 total, 36 thin omitted)

### Community 0 - "Methods and SeqKD Gates"
Cohesion: 0.09
Nodes (26): FedLS-SQL agent instructions, FedLS-SQL paper workspace guide, Server-side knowledge transfer, Experiment provenance contract, FedLS-SQL research project convention, Structural data isolation, Early FedLS-SQL paper outline, Federated large-small model architecture (+18 more)

### Community 1 - "Current Experiment Matrix"
Cohesion: 0.14
Nodes (21): A3 matched consolidation depth, FedLS-SQL experiment matrix, Fixed AKA teacher CoT method gate, P2.10 stopped QP-CoT recipe, P2.11 auxiliary teacher plan screen, Paper closure controls, Pipeline and teacher attribution ladder, Proposed full-gold plus plan contrast (+13 more)

### Community 2 - "KD Evidence and Retention"
Cohesion: 0.13
Nodes (16): Protocol v2 lab log, Row-matched SeqKD public edge, Terminal private-stage erosion of teacher edge, Execution-gated on-policy distillation, KD method review, Post-K terminal retention, Historical KD candidate review, Historical KD candidate set (+8 more)

### Community 3 - "Federated Architecture Diagram"
Cohesion: 0.23
Nodes (16): Federated Aggregation Engine, FedICL-SQL architecture diagram, Client or Organization, Federated Coordination Server, Global SLM Student Model, Global LLM Teacher, In-Context Learning Hub, ICL Prompt Constructor (+8 more)

### Community 4 - "Training Pass Results"
Cohesion: 0.14
Nodes (14): Base (zero-shot), Base (zero-shot), Eval k=0: EX 50,00; EM 21,08; Exec. error 25,92%, Base (zero-shot), Eval k=3: EX 52,22; EM 29,30; Exec. error 23,98%, Centralized FT, Centralized FT, Train k=0, Eval k=0: EX 62,19; EM 57,16; Exec. error 20,41%, Centralized FT, Train k=0, Eval k=3: EX 61,32; EM 56,00; Exec. error 21,08%, Centralized FT, Train k=3, Eval k=0: EX 64,02; EM 58,22; Exec. error 17,79%, Centralized FT, Train k=3, Eval k=3: EX 58,61; EM 50,77; Exec. error 20,12% (+6 more)

### Community 5 - "Archived Evidence Planning"
Cohesion: 0.18
Nodes (14): Archived evidence plan, Protocol v1 evidence gate, Archived next-task dashboard, Protocol v1 task status, Archived target outline, Protocol v1 research questions, Archived paper TODO, Protocol v1 adaptive backlog (+6 more)

### Community 6 - "Federated Benchmark Results"
Cohesion: 0.15
Nodes (13): Base, BIRD dev, Centralized 3 epoch, DK, Federated r1, post-KD, Federated r1, pre-KD, Federated r3, post-KD, Federated r3, pre-KD (+5 more)

### Community 7 - "Data Isolation Architecture"
Cohesion: 0.24
Nodes (12): Client-private Spider shards and local LoRA CE, FedLS-SQL architecture and data-isolation boundary, Execution verification (QuickExec 8 s and official result-equivalent EX), Frozen LLM teacher (zero-shot SQL generation), Global SLM adapter, LoRA tensor-only upload and broadcast, Structural locality, optional Secure Sum, no differential-privacy guarantee, Public BIRD train (question, schema, gold SQL) (+4 more)

### Community 8 - "Current Experiment Queue"
Cohesion: 0.30
Nodes (12): A1 four-arm merge screen, A2 interleaving proposal, A3 matched-depth proposal, FedLS-SQL run queue, Full-gold plus teacher-plan proposal, Local STaR-SQL-style alternative, October 2 fixed AKA CoT gate, P2.10 do not rerun (+4 more)

### Community 9 - "Text to SQL Methods"
Cohesion: 0.21
Nodes (12): Light-SQL, Light-SQL: Small Language Model with In-Context Learning, DAIL-SQL, Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation, DIN-SQL, DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction, DAIL-SQL, Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation (+4 more)

### Community 10 - "Historical KD and ICL"
Cohesion: 0.20
Nodes (11): Historical reverse KL and KID directions, Historical RKD and KID plan, KID and related KD critical review, True KID imperfect-sequence rewriting, ICL evaluation report, Negative matched ICL outcome, ICL versus no-ICL evaluation, Non-ICL federated KD ablation (+3 more)

### Community 11 - "Experiment Results Screenshot"
Cohesion: 0.18
Nodes (11): Base zero-shot, pass 0: EX 50,00; EM 21,08; execution error 25,92%, Centralized FT, pass 1: EX 62,19; EM 57,16; execution error 20,41%, Centralized FT, pass 2: EX 67,02; EM 62,57; execution error 16,05%, Centralized FT, pass 3: EX 67,60; EM 62,67; execution error 15,76%, Comparison of Base, Federated and Centralized FT evaluation results, Federated post-FedAvg pre-KD, pass 1, 5 clients: EX 57,35; EM 50,58; execution error 22,82%, Federated post-FedAvg pre-KD, pass 2, 5 clients: EX 64,02; EM 56,96; execution error 18,38%, Federated post-FedAvg pre-KD, pass 3, 5 clients: EX 66,05; EM 60,15; execution error 17,21% (+3 more)

### Community 12 - "Protocol V2 Method Design"
Cohesion: 0.25
Nodes (9): Evidence-aware dataset profiles, Private LoRA FedAvg public KD reference, Protocol v2 architecture, Role-independent public and private transfer, FedLS-SQL method placeholder, Operator dashboard, Adaptive protocol v2 TODO, Factor-wise LoRA averaging cross-term bias (+1 more)

### Community 13 - "Early Federated Runbooks"
Cohesion: 0.25
Nodes (8): Block K Archived Queue, Pure FL through T3 causal control, Pre-FedLS Next Runs, Round scaling evidence and missing control, Centralized FL FL-KD comparison HTML, Centralized FL FL-KD comparison Markdown, Final Comparison Email HTML, Final Comparison Email Markdown

### Community 14 - "Federated In Context Learning"
Cohesion: 0.25
Nodes (8): A Survey on In-context Learning, In-context learning with demonstrations and frozen model parameters, Light-SQL, Semantic retrieval of few-shot NL-to-SQL examples, Iterative client-server context refinement, Federated In-Context Learning (Fed-ICL), Implicit Federated In-Context Learning (IFed-ICL), Implicit client context vectors injected into residual streams

### Community 15 - "Federated Teacher Student Transfer"
Cohesion: 0.25
Nodes (8): FedMKT federated mutual knowledge transfer, Minimum edit distance token alignment for mutual transfer, Lightweight adapters for server LLM and client SLM co-tuning, FedCoLLM federated co-tuning, FedLS-SQL protocol-v2 main accuracy results, Terminal private consolidation A>K>A, Paper results source-of-truth and update contract, Stable result IDs and immutable artifact lineage

### Community 16 - "SQL Benchmarks and Parsing"
Cohesion: 0.32
Nodes (8): ScienceBenchmark: A Complex Real-World Benchmark for Evaluating Natural Language to SQL Systems, ScienceBenchmark, SmBoP: Semi-autoregressive Bottom-up Semantic Parsing, SmBoP, RESDSQL: Decoupling Schema Linking and Skeleton Parsing for Text-to-SQL, RESDSQL, ScienceBenchmark: A Complex Real-World Benchmark for Evaluating Natural Language to SQL Systems, ScienceBenchmark

### Community 17 - "ICL Prompt Methods"
Cohesion: 0.29
Nodes (7): CodeS prompt and retrieval method, DAIL-SQL retrieval and prompt method, DAIL-SQL versus CodeS methods, Four-axis ICL taxonomy, ICL methods survey, Client DAIL-weighted ICL training, Federated ICL pipeline

### Community 18 - "Execution Guided Distillation"
Cohesion: 0.33
Nodes (6): BIRD KD Effect Report, Matched Spider FT2 control, Execution-anchored on-policy distillation, Fed-ICKD V2 Historical Proposal, Execution-anchored on-policy GKD, Post-BIRD KD Research Directions

### Community 19 - "BIRD Baseline Audit"
Cohesion: 0.33
Nodes (6): Protocol v1 archive notice, Protocol v1 BIRD evidence omission, BIRD prompt truncation failure, BIRD baseline audit, Valid results and adapters ledger, Protocol v2 lineage filter

### Community 20 - "Transfer and Consolidation Reviews"
Cohesion: 0.40
Nodes (6): P2.2 transfer review, Public transfer trade-off, P2.3 terminal consolidation review, Terminal private consolidation, P2.4 teacher-signal review, Soft logits unproven

### Community 21 - "Related Work Novelty"
Cohesion: 0.33
Nodes (6): Related papers key references, FedLS-SQL novelty boundary, Rationale-augmented SeqKD, Struct-SQL review, RESDSQL schema linking and skeleton parsing, CodeS open-source Text-to-SQL models

### Community 22 - "Communication and Secure Sum"
Cohesion: 0.50
Nodes (4): Logical FP32 communication payload, P1.4a communication audit, P1.8a Secure Sum compatibility replay, Secure Sum compatibility

### Community 23 - "No ICL Ablation"
Cohesion: 0.50
Nodes (4): Non-ICL Full Pipeline Ablation, Private FT FedAvg Server KD, Matched no-ICL and ICL evaluation, No-ICL Federated Runbook

### Community 24 - "Early Server KD Method"
Cohesion: 0.50
Nodes (4): July 2026 Progress Report, Server-side public BIRD distillation, Protocol V1 Method Draft, Server-side large-to-small transfer

### Community 25 - "ICL Comparison Emails"
Cohesion: 0.50
Nodes (4): ICL versus No-ICL Email HTML, ICL versus No-ICL Email Markdown, No-ICL paper pipeline HTML, No-ICL paper pipeline Markdown

### Community 26 - "Early Paper Outlines"
Cohesion: 0.50
Nodes (4): Federated LLM-SLM with schema-aware ICL Markdown, Federated LLM-SLM with schema-aware ICL PDF, FedICL-SQL Paper Outline Markdown, FedICL-SQL Paper Outline PDF

### Community 27 - "Archived Manuscript Evidence"
Cohesion: 0.50
Nodes (4): Archived manuscript skeleton, Protocol v1 manuscript claims, Archived result registry, Protocol v1 artifact lineage

### Community 28 - "Superseded Method Screens"
Cohesion: 0.50
Nodes (4): Superseded P2.7 screen, P2.7 three-arm screen, Deferred P2.8 gate, P2.8 matched gold gate

### Community 29 - "Manuscript and Figures"
Cohesion: 0.50
Nodes (4): Current manuscript outline, Protocol v2 paper requirements, Active figures notice, Protocol v2 figure requirement

### Community 30 - "Structured Knowledge Distillation"
Cohesion: 0.50
Nodes (4): KID, Learning from Imperfect Data: KID for Text-to-SQL, Knowledge Distillation with Structured Chain-of-Thought for Text-to-SQL, Struct-SQL

### Community 31 - "Federated BART and QLoRA"
Cohesion: 0.50
Nodes (4): FedAvgBART, Federated Learning with Pre-trained BART for Classification and Generation, QLoRA, QLoRA: Efficient Finetuning of Quantized LLMs

### Community 32 - "Few Shot Learning Surveys"
Cohesion: 0.50
Nodes (4): A Survey on In-Context Learning, In-Context Learning, GPT-3 Few-Shot Learning, Language Models are Few-Shot Learners

### Community 33 - "Federated ICL Methods"
Cohesion: 0.50
Nodes (4): Fed-ICL, Federated In-Context Learning: Iterative Refinement, IFed-ICL, Implicit Federated In-Context Learning for Task-Specific LLM Fine-Tuning

### Community 34 - "Federated Mutual Transfer"
Cohesion: 0.50
Nodes (4): FedMKT, FedMKT: Federated Mutual Knowledge Transfer, FedCoLLM, FedCoLLM: Federated Co-tuning for Large and Small Language Models

### Community 35 - "Text to SQL Distillation"
Cohesion: 0.50
Nodes (4): KID knowledge distillation, Learning from Imperfect Data: Towards Efficient Knowledge Distillation of Autoregressive Language Models for Text-to-SQL, Knowledge Distillation with Structured Chain-of-Thought for Text-to-SQL, Struct-SQL

### Community 36 - "Interactive SQL Disambiguation"
Cohesion: 0.50
Nodes (4): Expected Information Gain clarification, Interactive Text-to-SQL via Expected Information Gain for Disambiguation, Expected Information Gain clarification, Interactive Text-to-SQL via Expected Information Gain for Disambiguation

### Community 37 - "LLM SQL Adaptation"
Cohesion: 0.50
Nodes (4): SQL-PaLM: Improved Large Language Model Adaptation for Text-to-SQL, SQL-PaLM, DIN-SQL, DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction

### Community 38 - "Prompting Method Surveys"
Cohesion: 0.50
Nodes (4): Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing, Prompt-based learning taxonomy, Prompt Engineering and In-Context Learning: A Comprehensive Survey of Techniques, Applications, and Future Directions, Prompt engineering and ICL taxonomy

### Community 39 - "SQL Prompt Evaluation"
Cohesion: 0.67
Nodes (3): DAIL-SQL benchmark evaluation, SQL-PaLM Text-to-SQL adaptation, Pre-train Prompt and Predict survey

### Community 40 - "SQL Evaluation Datasets"
Cohesion: 0.67
Nodes (3): Spider cross-domain Text-to-SQL dataset, ADVETA adversarial table perturbation benchmark, ScienceBenchmark real-world NL-to-SQL benchmark

## Knowledge Gaps
- **186 isolated node(s):** `Protocol v1 archive notice`, `BIRD baseline audit`, `P2.2 transfer review`, `Valid results and adapters ledger`, `Superseded P2.10 runbook` (+181 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 206 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `P2.10 do not rerun` connect `Current Experiment Queue` to `Current Experiment Matrix`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `P2.10 stopped QP-CoT recipe` connect `Current Experiment Matrix` to `Current Experiment Queue`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `Protocol v1 archive notice`, `BIRD baseline audit`, `P2.2 transfer review` to the rest of the system?**
  _186 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Methods and SeqKD Gates` be split into smaller, more focused modules?**
  _Cohesion score 0.08615384615384615 - nodes in this community are weakly interconnected._
- **Should `Current Experiment Matrix` be split into smaller, more focused modules?**
  _Cohesion score 0.1380952380952381 - nodes in this community are weakly interconnected._
- **Should `KD Evidence and Retention` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `Training Pass Results` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
