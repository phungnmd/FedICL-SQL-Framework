# FedLS-SQL — canonical paper result tables

> Updated 2026-08-20. This file is the single source of truth for paper-facing
> values. Stable artifact IDs resolve through
> `../notes/RESULT_REGISTRY.md`. Values are percentages unless stated
> otherwise. `PENDING:<task>` is an evidence gap, not a zero or a missing-value
> invitation.

The August 19 PDF outline is a draft planning input, not a fixed experimental
contract. Table structure and priorities may change when new evidence changes
the paper's claims. The research question, validated method, and evidence gates
in `../notes/PAPER_EVIDENCE_PLAN.md` take precedence.

## 1. Model and method scope

Keep model families in separate result blocks. Full-vocabulary reverse KL is
valid only inside a pair whose complete token-to-ID mappings have been checked
for equality.

| Track | Student family/model | Teacher family/model | Server transfer | Paper label | Status |
|---|---|---|---|---|---|
| Primary | Qwen2.5 / `Qwen/Qwen2.5-1.5B-Instruct` | Qwen2.5 / `Qwen/Qwen2.5-Coder-7B-Instruct` | teacher-target CE + token-level reverse KL | FedLS-SQL | canonical |
| Second family | Gemma 2 / `google/gemma-2-2b-it` | Gemma 2 / `google/gemma-2-9b-it` | regenerated teacher-target CE + token-level reverse KL | FedLS-SQL | `PENDING:P0.7` |

## 2. Overall NL-to-SQL performance

Supports the current overall-performance claim and the draft outline's §4.2.
This is the headline final-model table. All current values use training seed 0,
greedy decoding, and no ICL.

### 2.1 Primary Qwen2.5 track

| Stable ID | Method | Spider EX | Spider EM | Exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX | Evidence status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `qwen.central.standard3.s0` | Centralized-standard-3ep | 67.31 | 64.41 | 14.31 | 55.91 | 54.06 | **53.27** | 13.04 | canonical official recipe |
| `qwen.fl.t3.s0` | Pure FL, T3 | 64.31 | 57.45 | 18.67 | 56.10 | 51.93 | 46.73 | 12.91 | canonical independent FL |
| `qwen.fedls.t3.s0` | FedLS-SQL, T3 | **69.54** | 38.59 | **9.77** | **59.65** | **55.51** | **52.71** | **21.58** | canonical full method |

FedLS-SQL exceeds pure FL by `+5.23`, `+3.55`, `+3.58`, `+5.98`, and
`+8.67` EX on Spider, Realistic, Syn, DK, and BIRD. Exact paired McNemar tests
are significant on Spider (`p=0.0001`), Syn (`p=0.0094`), DK (`p=0.0002`), and
BIRD (`p<1e-19`), but not Realistic (`p=0.095`). The `+2.22` Spider EX margin
over centralized-standard is not significant (`p=0.0865`) and is not a claim of
superiority to centralized training.

The official centralized OOD suite is now complete. Relative to centralized,
FedLS-SQL is `+3.74` EX on Realistic (`p=0.081`), `+1.45` on Syn (`p=0.337`),
`-0.56` on DK (`p=0.842`), and `+8.54` on BIRD (`p<1e-17`). Thus the current
evidence supports competitiveness with centralized training, not uniform OOD
superiority. BIRD remains a public-domain-adjacent cross-corpus diagnostic.

### 2.2 Second-family portability track

This table replicates the matched mechanism ladder within Gemma. Its teacher
targets and logits are regenerated with Gemma 2 9B; no Qwen target/cache may be
reused. Gemma generates all 9,428 BIRD training rows and is independently
execution-filtered to `N_gemma`; the three server-treated arms use exactly
those rows. The Qwen-specific count 3,873 is not imposed on this track.

| Stable ID | Student | Method | Transfer objective | Round | Seed | Spider EX | Spider EM | Status |
|---|---|---|---|---:|---:|---:|---:|---|
| `gemma.base.s0` | Gemma 2 2B | Untouched base | none | 0 | 0 | `PENDING:P0.7` | `PENDING:P0.7` | pretrained anchor; no adapter |
| `gemma.fl.t1.s0` | Gemma 2 2B | Pure FL | none | 1 | 0 | `PENDING:P0.7` | `PENDING:P0.7` | active matched gate |
| `gemma.goldce.t1.s0` | Gemma 2 2B | Matched public CE | BIRD gold SQL | 1 | 0 | `PENDING:P0.7` | `PENDING:P0.7` | Gemma-selected `N_gemma` rows |
| `gemma.seqkd.t1.s0` | Gemma 2 2B | FedLS-SeqKD | Gemma 9B teacher-target CE | 1 | 0 | `PENDING:P0.7` | `PENDING:P0.7` | matched sequence-KD ablation |
| `gemma.fedls.t1.s0` | Gemma 2 2B | FedLS-SQL | Gemma 9B target CE + reverse KL | 1 | 0 | `PENDING:P0.7` | `PENDING:P0.7` | requires exact tokenizer compatibility |

Do not merge this block with §2.1. Extend it to T3 or OOD only if the T1 gate
is positive and material.

### 2.3 Outline headline accuracy-efficiency table

This is the current candidate for the draft outline's
`Method–EM–EX–Trainable Params–Latency` table, not a frozen paper table.
Accuracy is Spider; resource cells remain pending until measured under the
controlled protocol.

| Model family | Method | Spider EM | Spider EX | Trainable parameters | Inference latency | Inclusion status |
|---|---|---:|---:|---:|---:|---|
| Qwen2.5 1.5B | Centralized-standard-3ep | 64.41 | 67.31 | `PENDING:P1.1` | `PENDING:P1.1` | main baseline |
| Qwen2.5 1.5B | Pure FL, T3 | 57.45 | 64.31 | `PENDING:P1.1` | `PENDING:P1.1` | main baseline |
| Qwen2.5 1.5B | FedLS-SQL, T3 | 38.59 | **69.54** | `PENDING:P1.1` | `PENDING:P1.1` | proposed method |
| Qwen2.5 1.5B | FedProx-LoRA | `NOT RUN` | `NOT RUN` | `NOT RUN` | N/A | conditional baseline |
| Qwen2.5-Coder 7B | Federated LLM | `NOT RUN` | `NOT RUN` | `NOT RUN` | `NOT RUN` | excluded from default evidence; no claim |
| Qwen2.5-Coder 7B | Teacher zero-shot | `PENDING:P1.1` | `PENDING:P1.1` | N/A | `PENDING:P1.1` | resource/accuracy reference only |
| Gemma 2 2B | FedLS-SQL (Gemma 9B teacher), T1 | `PENDING:P0.7` | `PENDING:P0.7` | `PENDING:P0.7` | `PENDING` | second-family table, not main endpoint |

Few-shot LLM prompting and ICL are not silently promoted from legacy runs.
They may appear as a closed negative/diagnostic ablation only if the manuscript
needs them; they are not part of the canonical deployment method.

## 3. Convergence and generalization

Supports the convergence and non-IID claims currently proposed in draft §4.2.
The split is the fixed `K=5`, grouped-domain Dirichlet `alpha=0.5` setting.

### 3.1 Spider trajectory, Qwen2.5, seed 0

| Round | Independent pure FL EX | Mixed-lineage pre-server EX | FedLS-SQL endpoint EX |
|---:|---:|---:|---:|
| 1 | 56.67 | 57.35 | 63.35 |
| 2 | 62.19 | 64.02 | 66.15 |
| 3 | 64.31 | 66.05 | **69.54** |

The mixed-lineage pre-server column is diagnostic only: T2/T3 inherit earlier
KD and must never be labeled pure FL. FedLS-SQL improves `+6.19` EX from T1 to
T3 (`p<1e-4`). At matched two passes over private data, `T=2, E=1` exceeds
`T=1, E=2` by `+2.61` EX (`p=0.0067`), supporting repeated
communication/aggregation/distillation rather than local duration alone.

### 3.2 FedLS-SQL robustness trajectory, Qwen2.5, seed 0

| Dataset | T1 EX | T2 EX | T3 EX | T1→T3 | Paired `p` |
|---|---:|---:|---:|---:|---:|
| Spider | 63.35 | 66.15 | **69.54** | +6.19 | <1e-4 |
| Spider-Realistic | 52.95 | 56.30 | **59.65** | +6.69 | <1e-4 |
| Spider-Syn | 49.61 | 52.03 | **55.51** | +5.90 | <1e-4 |
| Spider-DK | 47.85 | 50.47 | **52.71** | +4.86 | 0.0007 |

This supports one non-IID partition at seed 0, not broad IID/quantity/SQL-skew
robustness. The latter settings remain conditional experiments. BIRD is a
cross-corpus diagnostic: within the FedLS lineage the server step adds `+8.28`
EX at T1 and `+3.91` at T3 (`p<1e-6`), but the public pool is also BIRD-derived,
so this is not the headline benchmark.

## 4. Ablation and causal evidence

Supports the causal evidence currently proposed in draft §4.3. Structural
distillation is omitted because it is not an implemented component. The matched
ladder changes only the server treatment after one shared Qwen T1 FedAvg
adapter.

### 4.1 Matched T1 supervision ladder, Qwen2.5, seed 0

| Stable ID | Server treatment | Spider EX | Spider EM | Exec. errors | Error rate |
|---|---|---:|---:|---:|---:|
| `qwen.fl.shared.t1.s0` | none | 57.35 | 50.58 | 236 | 22.82 |
| `qwen.goldce.t1.s0` | matched BIRD-gold CE | 57.83 | 23.89 | 195 | 18.86 |
| `qwen.seqkd.t1.s0` | teacher-target CE | 61.32 | 30.27 | 161 | 15.57 |
| `qwen.fedls.t1.s0` | teacher-target CE + reverse KL | **63.35** | 31.53 | **133** | **12.86** |

| Paired contrast | EX delta | Wins/losses | Approx. 95% CI | Exact McNemar `p` |
|---|---:|---:|---:|---:|
| public gold over FL | +0.48 | 127/122 | [-2.51, +3.48] | 0.800 |
| teacher target over public gold | **+3.48** | 86/50 | [+1.28, +5.68] | **0.0026** |
| reverse KL over teacher target | +2.03 | 59/38 | [+0.17, +3.89] | 0.0417 |
| full FedLS-SQL over public gold | **+5.51** | 93/36 | [+3.38, +7.64] | **<1e-6** |
| full FedLS-SQL over FL | **+6.00** | 145/83 | [+3.16, +8.84] | **<1e-4** |

Question-level tests at one training seed do not establish across-seed method
significance.

### 4.2 T1 training-seed evidence, Qwen2.5

| Stage | Seed 0 EX | Seed 1 EX | Seed 2 EX | Mean ± sample SD |
|---|---:|---:|---:|---:|
| FedAvg, pre-server | 57.35 | 57.45 | 59.77 | 58.19 ± 1.37 |
| + teacher-target CE | 61.32 | 62.28 | 59.48 | 61.03 ± 1.42 |
| + reverse KL, full endpoint | 63.35 | 62.48 | 62.38 | **62.74 ± 0.53** |

| Training-seed contrast | Mean delta | SD | `p` |
|---|---:|---:|---:|
| whole server stage over FedAvg | **+4.55** | 1.75 | **0.046** |
| reverse KL over teacher-target CE | +1.71 | 1.38 | 0.165 |
| full method over distillation-only | +1.39 | 1.12 | 0.165 |

The server stage as a whole is supported; standalone reverse KL remains
provisional. Final T3 seed-1/2 reliability is deferred as `PENDING:P0.8`.

### 4.3 Outline sensitivity matrix

| Outline item | Current evidence | Paper treatment |
|---|---|---|
| Remove LLM guidance | complete: pure FL vs FedLS-SQL | main ablation |
| Remove knowledge distillation | complete via matched ladder | main ablation |
| Structural distillation | not implemented | remove from claims/tables |
| Teacher sizes 7B/8B/14B | Qwen 7B canonical; Gemma 9B family replication pending | model-size sweep remains optional |
| Student sizes 0.5B/1.1B/1.5B/3B | Qwen 1.5B canonical; Gemma 2B family replication pending | family replication, not a controlled size sweep |
| LoRA ranks 4/8/16/32 | only r=16 canonical | optional |
| Clients 5/10/20 | only K=5 canonical | optional |
| FedProx | not implemented/run | conditional baseline |
| Federated 7B LLM | not run | do not claim comparison |
| ICL | matched negative evidence: -2.90 train-side EX, -3.87 inference-demo EX, 2.35x client time | closed negative appendix/limitation only |

### 4.4 Centralized schedule sensitivity, Qwen2.5, seed 0

| Stable ID | Recipe | Spider EX | Spider EM | Exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX | Role |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `qwen.central.standard3.s0` | one continuous three-epoch schedule | 67.31 | 64.41 | 14.31 | 55.91 | 54.06 | 53.27 | 13.04 | official methodology |
| `qwen.central.restart3.s0` | three independently scheduled passes | 67.60 | 62.67 | 15.76 | 57.87 | 53.19 | 52.52 | 12.91 | historical sensitivity only |

The paired Spider EX difference is `0.29` points (`p=0.863`). Never attach the
restart OOD values to the standard row.

## 5. Efficiency and trade-offs

Supports the communication/resource claims currently proposed in draft §4.2.

### 5.1 Communication payload

| Quantity | Bytes | MiB/GiB | Scope |
|---|---:|---:|---|
| One serialized global adapter | 73,911,080 | 70.487 MiB | weight payload only |
| Five client uploads per round | 369,555,560 | 352.436 MiB | five serialized adapters |
| Five client broadcasts per round | 369,555,400 | 352.435 MiB | five global adapters |
| Total per round | 739,110,960 | 704.871 MiB | upload + broadcast |
| Total through T3 | 2,217,332,880 | 2.065 GiB | three rounds |

Pure FL and FedLS-SQL have identical client-network payload because teacher
transfer is server-local. Counts exclude transport framing and protocol
metadata.

### 5.2 Accuracy-resource table

| Track/model | EX scope | Trainable parameters | Inference latency | Peak allocated/reserved VRAM | Process RSS | Status |
|---|---|---:|---:|---:|---:|---|
| FedLS-SQL / Qwen2.5-1.5B | Spider T3 | `PENDING:P1.1` | `PENDING:P1.1` | `PENDING:P1.1` | `PENDING:P1.1` | requires controlled warm-up benchmark |
| Teacher / Qwen2.5-Coder-7B | matched resource subset | N/A | `PENDING:P1.1` | `PENDING:P1.1` | `PENDING:P1.1` | cost reference, not federated-7B baseline |

Old shared-server timing is operational evidence only and must not fill this
table. Resource runs require fixed in-process warm-up, identical rows/decoding,
exclusive hardware, at least three fresh repetitions, and median plus
dispersion.

## 6. Error analysis

Supports the error analysis currently proposed in draft §4.4.

| Analysis | Available evidence | Status |
|---|---|---|
| Invalid/execution failures | per-row `exec_error` plus aggregate rates | ready for audit |
| EX=1, EM=0 equivalent SQL | 338 FedLS-T1 vs 101 FL-T1 cases | `PENDING:error-audit` |
| Spider hardness | easy/medium/hard/extra metrics logged | ready |
| JOIN/nested/aggregation/filtering constructs | predictions available; validated classifier absent | pending utility |
| Schema-linking errors | predictions available; validated extractor absent | do not claim yet |
| Federated-distribution errors | one `alpha=0.5` split only | insufficient for broad claim |
| LLM-SLM transfer failures | matched prediction rows available | ready for representative audit |

## 7. Adaptive evidence dashboard

| Current candidate paper evidence | Canonical section here | Coverage |
|---|---|---|
| Overall NL-to-SQL performance | §2 | seed-0 final-model table complete |
| Communication efficiency | §5.1 | complete for adapter payload |
| Resource efficiency | §5.2 | pending controlled benchmark |
| Non-IID robustness | §3.2 | scoped to one partition; broader settings pending |
| Convergence analysis | §3.1–§3.2 | seed 0 complete; final reliability deferred as P0.8 |
| Ablation and sensitivity | §4 | core causal ladder complete; broad sweeps optional |
| Error analysis | §6 | predictions available; structured audit pending |

This dashboard may be reordered, reduced, or extended after each evidence gate.
The draft outline is an experiment menu, not evidence that every proposed sweep
must be completed. Manuscript claims must follow validated results and the
adaptive gates in `../notes/PAPER_EVIDENCE_PLAN.md`.
