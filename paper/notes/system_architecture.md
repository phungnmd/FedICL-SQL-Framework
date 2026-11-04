# FedLS-SQL: system architecture

What this file is: the fixed setup, the data rules and the limits on what we
may claim. Findings are in `RESEARCH_STATE.md`, candidate directions in
`DIRECTION.md`, results in `LAB_LOG.md`, commands in `PIPELINE_NEXT.md`. The
executable contract is `fedicl-sql/docs/PROTOCOL_V2.md`. Previous versions:
[2026-11-04](../archive/directions_2026-11/system_architecture_2026-11-04.md),
[2026-09-24](../archive/method_reviews_2026-09/system_architecture_2026-09-24.md).

## 1. Goal

Train a small model (SLM) on private Text-to-SQL data held by several clients,
without moving that data. A large frozen teacher runs on the server, on public
data only. Deploy only the SLM.

## 2. Parts

| Part | Choice |
|---|---|
| Student | Qwen2.5-Coder-1.5B-Instruct, LoRA r16. Deployed alone. |
| Teacher | Qwen2.5-Coder-7B-Instruct, frozen, 4-bit, server only, public data only. |
| Clients | 5 clients, domain-cluster non-IID split `alpha_0.1/k5`. Private rows never leave a client. |
| Aggregation | Sample-weighted, factor-wise FedAvg of LoRA factors. Plaintext. |
| Communication | LoRA adapters; for replay, one-time public rows with compressed teacher targets (server to client). |
| Prompting | No ICL (k = 0) in training, teacher and evaluation. |
| Compute | Two RTX A5000 24 GB under WDDM (`fedicl-sql/docs/A5000_RUN_CONFIG.md`). |

Names: the paper is **FedLS-SQL**; the code package stays `fedicl_sql`. Old
run IDs and artifact paths never change.

## 3. Data

| Profile | Prompt | Use |
|---|---|---|
| `spider` | schema + question | Spider training and evaluation |
| `bird_with_evidence` | schema + evidence + question | BIRD public pool and BIRD dev |
| `bird_no_evidence` | schema + question | disclosed ablation only |

- BIRD public pool: all 9,428 training rows (gold CE, Hinton KD); 5,319
  execution-selected teacher targets (SeqKD); 1,266 checked teacher CoT
  solutions (P2.60 `cot1`). The 3,873-row pool is protocol-v1 history.
- Spider private: 8,659 training rows on the `k5` split; about 6,997 have a
  gold result that execution can check and enter RL rounds.
- Train and test never share a database. Test data never becomes training,
  retrieval or teacher data. BIRD training uses `max_len=7168` and fails on
  overflow.

## 4. Training building blocks

- `A`: one private round, each client trains one local epoch on its rows, then
  FedAvg. `K`: one public server epoch on BIRD; `K[ce]` gold CE,
  `K[fkl]` Hinton (0.5 CE + 0.5 T^2 KL, T = 2). A chain containing `K` is not
  pure FL; only all-`A` chains are FL controls.
- Client replay: each client mixes a public subset with the teacher's top-50
  targets into its private round (P2.47-P2.48).
- RL round (centralized so far, P2.58-P2.62): sample K = 8 outputs per
  question, check by execution, one chosen/rejected pair per mixed question,
  DPO (beta 0.1) plus NLL on chosen, lr 1e-5, reference = the round's start
  adapter. Fresh rounds of up to 1,200 questions, then retries on questions
  with no correct sample.
- Student loss: `--lm-loss target_fp32` with `logits_to_keep`.

## 5. Evaluation

- Spider EX on Spider dev (1,034) and Spider test (2,147), reported together.
  Test may inform choices and is then not called held-out. BIRD dev with
  evidence (1,534) and Spider-Realistic/SYN/DK only for finalized arms or on
  request. EM is a diagnostic.
- Scorers: `spider_result_eq_v1` (60 s budget); `bird_official_set_pair_timeout30_v2`.
- Greedy decoding, evaluation batch 16, seed 0 unless stated.
- One seed: exact McNemar on row-matched predictions. Pooled seeds: the
  question-clustered test (per-question mean over seeds, normal test across
  questions), never summed discordant pairs.

## 6. What we may claim

- Privacy is structural data isolation, not differential privacy or secure
  aggregation.
- Individual parts are not new (`LITERATURE.md` section 1). Claim the
  task-specific adaptation and its matched evidence.
- A pipeline beating FedAvg at equal private rounds shows the pipeline works at
  that budget; it does not isolate the teacher. Teacher claims need a matched
  gold or no-teacher contrast; CoT claims need the SQL-only route with the
  same rounds.
- A non-significant contrast is not an equivalence result.
- Protocol-v1 results never fill a protocol-v2 table.
