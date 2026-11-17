# Federated data setup for Text-to-SQL on Spider: what the papers do and a setup

Written 2026-11-17 from the papers only. It was not checked against the
other notes, the current split in the code, or our own results. Section 6
lists which facts were read in the paper text and which were not. The DPO
stage itself is covered in `DPO_RESEARCH.md`.

## 1. Short answers

- Only one paper trains a Text-to-SQL model with federated learning (Zhang
  et al., ACL 2023), and it does not use Spider. No paper splits Spider or
  BIRD across clients. The setup has to rest on that one paper, on how
  Spider has been split in continual learning and compositional
  generalisation work, and on the partition recipes of federated learning.
- The database is the unit: every database belongs to one client. This is
  the story (each organisation owns its databases), it has precedent, and
  the DPO stage needs it because clients label by running SQL on their own
  databases.
- A split by database alone is close to IID for Spider test. The test uses
  unseen databases, so schema knowledge of a client does not carry over;
  what carries over is SQL skill, and that is spread evenly over Spider's
  databases. The skew that the test can see is in SQL structure.
- Proposed split: databases are assigned whole, by a Dirichlet over a
  database-level complexity label (four tiers). Main setting 5 clients,
  alpha 0.1. With that, the largest client holds about 37% of the databases,
  the smallest about 7%, and a client lacks about 2 of the 4 tiers.
- "Dirichlet alpha 0.1" has two published recipes with opposite outcomes,
  so the paper has to say which one it uses and over which label.
- Runs for the paper: 14 on the main setting, 4 for alpha, 2 for the client
  count. One seed with a paired test meets what the target journals print.

## 2. What the papers show

### 2.1 Federated Text-to-SQL

Zhang et al. (ACL 2023, T5-base, full fine-tuning) is the only one found.
Eight clients, one single-domain dataset each (Advising, ATIS, GeoQuery,
Restaurants, Scholar, Academic, IMDB, Yelp), from 78 to 4,347 training
examples. All clients join every round. They argue for natural clients
against synthetic Dirichlet splits of classification data. Each client is
tested on its own test split; results are exact match as macro and micro
averages.

| Row | Macro | Micro |
|---|---|---|
| Local fine-tuning | 62.78 | 71.47 |
| Centralized | 70.32 | 74.21 |
| FedAvg | 40.03 | 57.89 |
| FedProx | 41.67 | 58.84 |
| FedOPT | 58.32 | 68.49 |
| FedAvg + Lorar | 60.16 | 63.91 |
| FedOPT + Lorar | 62.55 | 69.39 |

Plain FedAvg is below local training on every client, most on the small
ones. Lorar weights a client by its size times its loss reduction in the
round.

Other work that matches "federated" and "SQL" is not federated training of
a Text-to-SQL model: query federation over databases, privacy at inference
time (MaskSQL, SafeNLIDB), a multi-agent system over a split schema (CSMA,
tables of one database divided between 2 to 4 agents, prompting only), and
federated learning on relational tables.

### 2.2 What Spider offers for a split

- Train: 8,659 questions on 146 databases. 7,000 are Spider's own; 1,659
  come from six earlier datasets (Restaurants, GeoQuery, Scholar, Academic,
  IMDB, Yelp). These six are also six of Zhang's eight clients.
- Dev: 1,034 questions on 20 databases. Test: 2,147 questions on 40
  databases. No database is shared between splits.
- 20 to 50 questions were written per database. Most of the 138 domains
  have one database.
- Hardness of the 7,000 training questions: easy 24.20%, medium 39.67%,
  hard 20.87%, extra hard 15.26%. The levels are defined by the number of
  SQL components, selections and conditions, and the official evaluator
  reports results by level.
- The Spider paper does not say that a domain label per database is
  published.

### 2.3 How Spider has been split into groups

| Paper | Split by | Detail |
|---|---|---|
| Chen et al., AAAI 2023 (continual learning) | domain of the database | 10 tasks, databases disjoint between tasks, most tasks under 500 labelled examples; mean over tasks and a pooled test set |
| C3, NeurIPS 2023 (Combined-stream) | database and SQL structure | 7 tasks from Spider and WikiSQL, to change both the table domain and the SQL structure |
| Shaw et al., ACL 2021 (Spider-SSP) | SQL structure | only the 51 training databases with more than 50 examples; databases shared between train and test; random, template, length and TMCD splits |
| CSMA, 2024 | tables inside a database | no training |

Shaw et al. measure what a shift in SQL structure costs (exact match on
their Spider splits):

| Model | Random | Template | Length | TMCD |
|---|---|---|---|---|
| T5-Base | 82.0 | 59.3 | 49.0 | 60.9 |
| T5-3B | 85.6 | 64.8 | 56.7 | 69.6 |

### 2.4 Partition recipes in federated learning

NIID-Bench (ICDE 2022) names three kinds of skew and gives recipes:

- Label skew: each client gets k labels; or, for each label, the shares of
  the clients are drawn from Dir(beta) and that label's examples are split
  accordingly.
- Feature skew: added noise; a synthetic set; or a natural one, where the
  writers of FEMNIST are assigned randomly and equally to the clients.
- Quantity skew: the client sizes are drawn from Dir(beta).

It states that label skew is harder than quantity skew, and that studies
should use more than one partition strategy.

Two recipes go by "Dirichlet alpha":

- NIID-Bench: per label, split across clients. Client sizes differ.
- Hsu et al. 2019 and FedNLP: per client, draw a label distribution
  q ~ Dir(alpha p) and sample that many examples. Client sizes are equal.

For tasks without a class label, FedNLP clusters sentence embeddings with
K-Means and uses the cluster as the label (Gigaword, alpha 0.1, 100
clients). For QA it uses a natural split, one sub-dataset per client (6
clients). Its quantity recipe is z ~ Dir(beta) over the client sizes.

Clients built from groups of natural ids: Flower's
`GroupedNaturalIdPartitioner` ("an organization of x users"), and
FederatedScope-LLM's meta-information splitter (one programming language
or one task category per client). Flower's Dirichlet partitioner draws
again when a client falls under a minimum size.

A simulation of the two readings of "alpha 0.1" for 146 databases and 5
clients:

| Reading | Largest client | Smallest client |
|---|---|---|
| Client sizes drawn from Dir(0.1) | 81% of the data | near 0%; 2.85 of 5 clients under 2% |
| Each database split across clients by Dir(0.1) | 24% | 17%; a database keeps 81% of its questions at one client, the rest leak to others |

### 2.5 Setups of the federated LLM benchmarks

| Paper | Model | Clients (per round) | How clients are formed | Rounds, local work | Baselines | Seeds |
|---|---|---|---|---|---|---|
| OpenFedLLM | 7B, LoRA r 32 (r 8 for alignment) | 20 (2), code 10 (2), alignment 5 (2) | random split, or one dataset per client | 100 to 200 rounds, 10 steps | local, 7 FL optimizers; no centralized | none |
| FedLLM-Bench | 7B, LoRA r 16 | 38 to 747 (4 to 10) | by annotator, user or IP; small clients filtered out | 50 to 200 rounds, 5 or 10 steps | local, 7 FL optimizers | none |
| FS-LLM | 7B and 2.7B | code 9, Dolly 8, math 3 | by programming language, by task category, IID | 500 rounds, 30 steps | global, federated, local | 3 |
| FedIT | 7B, LoRA r 8 | 100 (5) | quantity skew | 20 rounds, 1 epoch | local, centralized | none |
| FedNLP | DistilBERT, BART-base | 6 to 100 | Dirichlet over labels or clusters; natural for QA | 13 to 22 rounds, 1 epoch | FedAvg, FedProx, FedOPT | not found |
| FedPDPO | 82M and 1.1B, LoRA r 8 | 3 to 11, all join | by language, by reward margin, one dataset per client | 10 to 20 rounds, 1 epoch | FedAvg + DPO and others | 5 |
| Zhang et al. | T5-base, full | 8, all join | one dataset per client | 60 rounds, 6 or 12 epochs | local, centralized, FedAvg, FedProx, FedOPT | none |

Client counts seen in cross-silo work: 3 (FFA-LoRA, FedSA-LoRA), 4 (FedMKT,
FedCoLLM, LESFT), 5 (OpenFedLLM alignment), 6 (FedNLP MRQA), 8 (Zhang,
FS-LLM), 9 (FS-LLM code), 10 (FLoRA, FedDF, FedCO).

Alpha values seen: 0.1 (FedNLP, FedDF, FedCO), 0.5 (FlexLoRA, FedSA-LoRA),
1 (FedNLP 20News, FedDF). Sweeps: FedDF over 100, 1, 0.5, 0.1, 0.01;
FedSA-LoRA over IID, 1, 0.5 and over 10, 20, 100 clients; FedCO over
alpha, 10 / 20 / 30 clients and local epochs.

Plain FedAvg of the LoRA matrices A and B (FedIT) is the reference every
LoRA aggregation paper compares with.

### 2.6 Public data at the server, and the privacy wording

- FedBiOT: "Assume there is a public dataset D_public available on the
  server".
- FedCoLLM: "The server owns an auxiliary dataset"; the server is
  semi-honest; raw private data "should not be directly uploaded".
- FedMKT: a shared public dataset; "without disclosing any private data",
  with a limitation sentence that there is no theoretical guarantee.
- FedDF, FedMD: unlabeled or public data at the server.
- Nguyen et al. and Chen et al. (both ICLR 2023): a pre-trained start
  reduces the effect of heterogeneity. This supports a server stage before
  the rounds, and it also means our split will look milder than the same
  split would from a cold start.

No paper has a teacher that runs once at the server before FedAvg; the
ones above keep the large model in every round.

### 2.7 What papers in the target journals contain

CMC has two federated NLP or LLM papers that could be read (LESFT 2026,
FLAT-ERP 2023) and JIIS has none; JIIS has Text-to-SQL papers (GradeSQL
2026 was readable).

- LESFT: 3 datasets, Qwen2.5 0.5B to 3B with LoRA r 8, 4 clients, baselines
  including centralized and FedAvg, six ablations with a client-count
  sweep, a cost table, no seeds.
- FLAT-ERP: 3 datasets, 8 clients, sweep over 8 / 16 / 32 clients, no seeds.
- FedCO (CMC 2026, vision): 10 clients, alpha 0.05 to 1, 8 baselines,
  ablations over clients and local epochs, a time table, no seeds.
- GradeSQL (JIIS): Spider dev, Spider test and BIRD dev by execution
  accuracy; one seed, with McNemar tests.

## 3. The split

### 3.1 Recipe

1. Every database goes whole to one client.
2. Label each of the 146 training databases with one of four complexity
   tiers, by its share of hard and extra hard questions (quartiles).
3. For each tier, draw the clients' shares from Dir(alpha) and assign the
   tier's databases to clients by those shares.
4. If a client ends with fewer than 5 databases (3 when there are 10
   clients), draw again.
5. The centralized run trains on the union of what the clients hold. The
   IID setting assigns databases at random in equal numbers.

### 3.2 What it gives

Simulation with four equal tiers, counting databases:

| Setting | Largest client | Smallest client | Share of a client's databases from one tier | Tiers a client lacks |
|---|---|---|---|---|
| 5 clients, alpha 0.1 | 37% | 7% | 81% | 2.05 of 4 |
| 5 clients, alpha 0.5 | 35% | 8% | 59% | 0.83 of 4 |
| 5 clients, alpha 1.0 | 32% | 10% | 51% | 0.39 of 4 |
| 5 clients, alpha 100 | 25% | 16% | 34% | 0 |
| 10 clients, alpha 0.5 | 22% | 3% | 64% | 1.23 of 4 |

With 10 clients, alpha 0.1 needs about 77 draws before every client has 3
databases, so the client-count sweep uses alpha 0.5.

### 3.3 Why this one

- It gives a reason to federate. A client that lacks two tiers cannot
  learn the harder queries alone. With databases assigned at random every
  client sees every kind of query, and local training may come close to
  FedAvg.
- The test can see it: the skew is in SQL structure, which carries over to
  unseen databases (2.3), and the evaluator reports by hardness level.
- It is not degenerate: the smallest client keeps about 7% of the
  databases, against near 0% when the client sizes are drawn from Dir(0.1).
- Each piece is published: whole natural ids per client (Chen et al.,
  Flower, FEMNIST in NIID-Bench), a Dirichlet per label (NIID-Bench), the
  label from Spider's own hardness levels.

### 3.4 Weak points

- The pieces are published, the combination on Spider is not. The paper
  needs a paragraph and a table of the split.
- At the level of questions the skew is softer than the tier figures: a
  database of the hardest tier still has easy questions. The share of the
  four hardness levels per client has to be counted after the split.
- The six databases from the earlier datasets hold far more questions than
  the others (1,659 questions on six databases). The client that gets them
  grows in questions, not in databases.
- The server stage makes every split look milder (2.6).

## 4. Runs for the paper

### 4.1 Main setting

5 clients, alpha 0.1, all clients in every round, aggregation weights by
client size, plain FedAvg of the LoRA matrices.

| Row | Runs | Role |
|---|---|---|
| Student without training | 0 | starting point |
| Local training, each client | 5 | lower bound; mean, minimum and maximum |
| Centralized on the union | 1 | upper bound; the same run serves every split |
| FedAvg | 1 | main baseline |
| FedProx | 1 | baseline for non-IID data |
| FedAdam (FedOPT) | 1 | server optimizer baseline; far above FedAvg in Zhang et al. |
| Server stage only | 1 | the server stage without federated training; serves every split |
| Server stage + FedAvg SFT | 1 | the method without the DPO stage |
| The same, with as many extra rounds as the DPO stage has | 1 | so that the gain of the DPO stage is not longer training |
| FedAvg SFT + DPO, no server stage | 1 | the method without the server stage |
| Full method | 1 | |

14 runs. Ablations inside the DPO stage are added on this setting.

### 4.2 Sensitivity

Two rows per cell: FedAvg and the full method.

| Varied | Levels | Extra runs |
|---|---|---|
| alpha, 5 clients | 0.1 (main), 0.5, IID | 4 |
| clients, alpha 0.5 | 5 (already run), 10 | 2 |

### 4.3 Training values

Ranges are what the papers in 2.5 use. Where our current recipe is inside
the range, it stays.

| Item | Range in the papers | Value |
|---|---|---|
| Local work per round | 1 epoch, or 10 steps | 1 epoch |
| SFT rounds | 13 to 22, 20, 60 | 20, checkpoint chosen on Spider dev |
| DPO rounds | 4 iterations with the peak at 3 (CodeLutra), 2 (ScPO) | 4 |
| Centralized | the same number of passes over the data | up to 20 epochs, chosen on dev |
| LoRA rank | 8, 16, 32 | the current one |
| FedProx mu | 0.0001 (Zhang et al.) | 0.0001 |
| Seeds | none in CMC and JIIS; 3 in FS-LLM; 1 with McNemar in GradeSQL | 1, with a McNemar test between the method and FedAvg on the 2,147 test rows |

### 4.4 What the paper reports

- The split: one line per client with databases, questions and the share
  of each hardness level.
- Main table: execution accuracy on Spider test, with the four hardness
  levels as columns.
- Sensitivity over alpha and over the client count.
- Cost: adapter size sent per round, total communication, time, peak
  memory, all from the logs.
- One sentence that the public data shares no database with Spider test,
  and one limitation sentence that no formal privacy guarantee is claimed.

### 4.5 Count and options

Required: 14 + 4 + 2 = 20 runs, plus the ablations inside the DPO stage.

Options, by value for cost:

1. Three seeds for FedAvg and the full method on the main setting, with
   the split seed changed as well: 4 more runs.
2. 20 clients at alpha 0.5: 2 more runs.
3. A second set of clients from BIRD train, main rows only. The public data
   then has to be SynSQL and the teacher has to run on it. The CMC papers
   read use about three datasets, so a reviewer may ask; it is the most
   expensive option.

## 5. First checks, no training needed

1. Build the split and print the table of 4.4 (databases, questions and
   hardness shares per client). If the clients' hardness shares are close
   to each other, the tier label is too weak.
2. Then three training rows on the main setting: local, FedAvg,
   centralized. If the local model of a client that lacks the hard tiers is
   not below FedAvg on the hard and extra hard columns, the split does not
   pose a problem either, and smaller clients are the next thing to try,
   not more skew.

## 6. What was checked

Read in the paper text or the documentation page: Spider's counts, split
rule, the six earlier datasets and the hardness definition; the hardness
shares of Spider train (from arXiv 2312.06172, Table 2); Chen et al.'s 10
tasks by domain with disjoint databases; the descriptions of the two
streams in LECSP; Shaw et al.'s Spider splits and Table 3; Zhang et al.'s
Table 2 and the Lorar formula; the label and feature recipes of NIID-Bench;
FedNLP section 3.2 and Table 2; Hsu et al.'s recipe; the Flower partitioner
pages; CSMA's schema division; FS-LLM's two client datasets.

Read only through a tool that summarises long pages, so to be checked in
the PDF before it is cited: everything in 2.5 except the FedNLP and FS-LLM
client data, all of 2.6 and 2.7, Zhang et al.'s rounds and local epochs,
NIID-Bench's quantity recipe and its sentence that feature and quantity
skew barely affect FedAvg, the C3 citation.

Not found or not read: the number of databases and examples per task in
Chen et al. (in a figure) and where their domain labels come from; the SQL
atoms and compounds Shaw et al. use for TMCD; the venues of FedDF and
FS-LLM.

The search for federated Text-to-SQL covered the arXiv API, OpenAlex, the
citations of Zhang et al. on Semantic Scholar (9 papers), ACL Anthology and
web search with journal names. A paper outside those indexes would have
been missed.

## 7. References

- Zhang et al., Federated Learning for Semantic Parsing: arXiv 2305.17221
- Spider: arXiv 1809.08887
- Hardness shares of Spider: arXiv 2312.06172
- Chen et al., Learn from Yesterday (continual Text-to-SQL): arXiv 2211.11226
- LECSP: arXiv 2412.07246
- C3, Parameterizing Context (NeurIPS 2023)
- Shaw et al., Compositional Generalization and Natural Language Variation: arXiv 2010.12725
- CSMA: arXiv 2412.05850
- NIID-Bench: arXiv 2102.02079
- Hsu et al.: arXiv 1909.06335
- FedNLP: arXiv 2104.08815
- Flower Datasets partitioners: flower.ai/docs/datasets
- FederatedScope-LLM: arXiv 2309.00363
- OpenFedLLM: arXiv 2402.06954
- FedLLM-Bench: arXiv 2406.04845
- FedIT: arXiv 2305.05644
- FedPDPO: arXiv 2603.19741
- FlexLoRA: arXiv 2402.11505
- FFA-LoRA: arXiv 2403.12313
- FLoRA: arXiv 2409.05976
- FedSA-LoRA: arXiv 2410.01463
- FedBiOT: arXiv 2406.17706
- FedMKT: arXiv 2406.02224
- FedCoLLM: arXiv 2411.11707
- FedDF: arXiv 2006.07242
- FedMD: arXiv 1910.03581
- Nguyen et al., pre-trained initialization in FL: arXiv 2206.15387
- Chen et al., pre-training for FL: arXiv 2206.11488
- LESFT (CMC 2026): doi 10.32604/cmc.2025.074034
- FLAT-ERP (CMC 2023): doi 10.32604/cmc.2023.034439
- FedCO (CMC 2026): doi 10.32604/cmc.2026.083715
- GradeSQL (JIIS 2026): arXiv 2509.01308
