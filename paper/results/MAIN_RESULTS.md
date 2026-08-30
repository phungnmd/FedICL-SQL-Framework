# FedLS-SQL — canonical paper result tables

> Updated 2026-08-26. This file is the single source of truth for paper-facing
> values. Stable artifact IDs resolve through
> `../notes/RESULT_REGISTRY.md`. Values are percentages unless stated
> otherwise. `PENDING:<task>` is an evidence gap, not a zero or a missing-value
> invitation.

The August 19 PDF is the advisor-provided planning input, not a fixed
experimental contract. The evidence-backed manuscript structure is
`../notes/PAPER_OUTLINE_TARGET.md`; the validated method and adaptive gates in
`../notes/PAPER_EVIDENCE_PLAN.md` determine which proposed experiments and
claims are retained.

## 1. Model and method scope

Keep model families in separate result blocks. Full-vocabulary reverse KL is
valid only inside a pair whose complete token-to-ID mappings have been checked
for equality.

| Track | Student family/model | Teacher family/model | Server transfer | Paper label | Status |
|---|---|---|---|---|---|
| Primary | Qwen2.5 / `Qwen/Qwen2.5-1.5B-Instruct` | Qwen2.5 / `Qwen/Qwen2.5-Coder-7B-Instruct` | teacher-target CE + token-level reverse KL | FedLS-SQL | canonical |
| Second family | Gemma 2 / `google/gemma-2-2b-it` | Gemma 2 / `google/gemma-2-9b-it` | regenerated teacher-target CE + token-level reverse KL | FedLS-SQL | canonical T1 portability endpoint; RKL increment is not independently significant |

## 2. Overall NL-to-SQL performance

Supports the current overall-performance claim and the draft outline's §4.2.
This is the headline final-model table. All current values use training seed 0,
greedy decoding, and no ICL.

### 2.1 Primary Qwen2.5 track

| Stable ID | Method | Spider EX | Spider EM | Exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX | Evidence status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `qwen.central.standard3.s0` | Centralized-standard-3ep | 67.31 | 64.41 | 14.31 | 55.91 | 54.06 | **53.27** | 13.04 | canonical official recipe |
| `qwen.fl.t3.s0` | Pure FL, T3 | 64.31 | 57.45 | 18.67 | 56.10 | 51.93 | 46.73 | 12.91 | canonical independent FL |
| `qwen.fedprox.t3.s0` | FedProx-LoRA (`mu=0.01`), T3 | 62.77 | 56.00 | 18.76 | — | — | — | — | closed negative optimizer baseline |
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

The fixed FedProx-LoRA reviewer baseline is negative on the primary endpoint.
Against the same-split pure-FL T3 checkpoint it changes 22 wrong rows to
correct but regresses 38 correct rows: `-1.55` Spider EX, exact paired McNemar
`p=0.0519`, and 194 versus 193 execution errors. It is also `-4.55` EX below
centralized-standard (`p=0.00112`) and `-6.77` below FedLS-SQL
(`p=6.37e-7`). This supports retaining FedAvg for the current method; it does
not claim that FedProx is universally ineffective.

### 2.2 Second-family portability track

This table replicates the matched mechanism ladder within Gemma. Its teacher
targets and logits are regenerated with Gemma 2 9B; no Qwen target/cache may be
reused. Gemma generates all 9,428 BIRD training rows and is independently
filtered by the fixed 8-second quick-execution stage and the official EX scorer
to obtain `N_gemma`; the three server-treated arms use exactly those rows. The
Qwen-specific count 3,873 is not imposed on this track.

The independent 60-second gold audit finds 9,056/9,428 executable rows. Of the
372 invalid outcomes, 350 are missing-table/column failures, 21 are timeouts,
and one is a disk-full failure; 330 are concentrated in `retail_world`. On the
common valid mask, Qwen retains 3,869 matches (`42.72%`) and Gemma retains
2,487 (`27.46%`), with 2,019 in common. Every Gemma-selected row is audit-valid.
These figures characterize the concrete teacher pipelines and local data
snapshot; they do not isolate model-family or parameter-count effects.

| Stable ID | Student | Method | Transfer objective | Round | Seed | Spider EX | Spider EM | Exec. errors | Error rate | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `gemma.base.s0` | Gemma 2 2B | Untouched base | none | 0 | 0 | 52.22 | 22.44 | 162 | 15.67 | canonical pretrained anchor |
| `gemma.fl.t1.s0` | Gemma 2 2B | Pure FL | none | 1 | 0 | 57.16 | **49.52** | 212 | 20.50 | canonical pre-server endpoint |
| `gemma.goldce.t1.s0` | Gemma 2 2B | Matched public CE | BIRD gold SQL | 1 | 0 | 41.68 | 23.60 | 303 | 29.30 | same Gemma-selected `N_gemma=2,487` identities |
| `gemma.seqkd.t1.s0` | Gemma 2 2B | FedLS-SeqKD | Gemma 9B teacher-target CE | 1 | 0 | 61.22 | 32.98 | **119** | **11.51** | matched hard-target ablation |
| `gemma.fedls.t1.s0` | Gemma 2 2B | FedLS-SQL | Gemma 9B target CE + reverse KL | 1 | 0 | **61.41** | 33.85 | 137 | 13.25 | canonical full endpoint |

Pure FL improves over the untouched Gemma base by `+4.94` EX (141 paired gains,
90 losses, exact McNemar `p=0.00096`). Teacher-target CE then improves over FL
by `+4.06` EX (137/95, `p=0.00698`) and full FedLS-SQL improves over FL by
`+4.25` EX (132/88, `p=0.00365`). Full FedLS-SQL is the numerical maximum, but
its `+0.19` EX over teacher-target CE is only two net questions (46/44,
`p=0.916`); its `+0.87` EM increment is also not significant (`p=0.281`). The
second family therefore supports the complete endpoint and, more strongly,
the hard teacher-target mechanism, but not a family-independent standalone RKL
gain.

Matched BIRD-gold CE falls `15.48` EX below FL and raises execution errors to
303. Because gold CE and both teacher-guided arms use the same 2,487 source
identities, selection count does not explain this contrast. The target form,
SQL style/complexity, and cross-corpus supervision mismatch require a focused
audit before causal wording is finalized. EX remains primary: teacher-guided
arms lower EM relative to FL while increasing execution accuracy, consistent
with semantically correct but non-canonical SQL generation.

Do not merge this block with §2.1. The endpoint gate is positive, but the RKL
increment is not material; do not extend Gemma to T3/OOD automatically.

### 2.3 Outline headline accuracy-efficiency table

This is the current candidate for the draft outline's
`Method–EM–EX–Trainable Params–Latency` table, not a frozen paper table.
Accuracy is Spider. Artifact-derived parameter counts are closed for the
audited T3 FL/FedLS adapters. Controlled latency is closed only for the
deployed T3 FedLS adapter and the 4-bit teacher reference on the fixed P1.1b
32-row inference subset; other latency cells remain unmeasured.

| Model family | Method | Spider EM | Spider EX | Trainable parameters | Inference latency | Inclusion status |
|---|---|---:|---:|---:|---:|---|
| Qwen2.5 1.5B | Centralized-standard-3ep | 64.41 | 67.31 | `PENDING:P1.1` | `PENDING:P1.1` | main baseline |
| Qwen2.5 1.5B | Pure FL, T3 | 57.45 | 64.31 | 18,464,768 | `PENDING:P1.1` | main baseline |
| Qwen2.5 1.5B | FedLS-SQL, T3 | 38.59 | **69.54** | 18,464,768 | 0.7873 s/query (IQR 0.0671) | proposed method; P1.1b fixed 32-row scope |
| Qwen2.5 1.5B | FedProx-LoRA, T3 | 56.00 | 62.77 | 18,464,768 | N/A | matched negative optimizer baseline; T1/T2 diagnostic pending |
| Qwen2.5-Coder 7B | Federated LLM | `NOT RUN` | `NOT RUN` | `NOT RUN` | `NOT RUN` | excluded from default evidence; no claim |
| Qwen2.5-Coder 7B | Teacher zero-shot | `NOT MEASURED` | `NOT MEASURED` | N/A | 1.6460 s/query (IQR 0.0100) | 4-bit resource reference only; accuracy not scored in P1.1b |
| Gemma 2 2B | FedLS-SQL (Gemma 9B teacher), T1 | 33.85 | 61.41 | `PENDING:P1.1` | `PENDING:P1.1` | second-family portability endpoint |

Few-shot LLM prompting and ICL are not silently promoted from legacy runs.
They may appear as a closed negative/diagnostic ablation only if the manuscript
needs them; they are not part of the canonical deployment method.

## 3. Convergence and generalization

Supports the convergence and non-IID claims currently proposed in draft §4.2.
The split is the fixed `K=5`, grouped-domain Dirichlet `alpha=0.5` setting.

### 3.1 Spider trajectory, Qwen2.5, seed 0

| Round | Independent pure FL EX | FedProx-LoRA EX | Mixed-lineage pre-server EX | FedLS-SQL endpoint EX |
|---:|---:|---:|---:|---:|
| 1 | 56.67 | 55.80 | 57.35 | 63.35 |
| 2 | 62.19 | 59.96 | 64.02 | 66.15 |
| 3 | 64.31 | 62.77 | 66.05 | **69.54** |

FedProx is below round-matched pure FL by `0.87`, `2.22`, and `1.55` EX at
T1/T2/T3. The T2 paired comparison has 19 corrections versus 42 regressions
(`p=0.00444`); T1 has 26/35 (`p=0.306`) and T3 has 22/38 (`p=0.0519`). This
closes the proposed FedLS-FedProx interaction screen: there is no observed
early-round FedProx advantage to promote. The mixed-lineage pre-server column
is diagnostic only: T2/T3 inherit earlier KD and must never be labeled pure
FL. FedLS-SQL improves `+6.19` EX from T1 to
T3 (`p<1e-4`). At matched two passes over private data, `T=2, E=1` exceeds
`T=1, E=2` by `+2.61` EX (`p=0.0067`), supporting repeated
communication/aggregation/distillation rather than local duration alone.

### 3.2 Spider trajectory replication, Qwen2.5, seed 1

| Round | Independent pure FL EX / errors | Mixed-lineage pre-server EX / errors | FedLS-SQL endpoint EX / errors | FedLS − pure FL |
|---:|---:|---:|---:|---:|
| 1 | 57.45 / 247 | 57.45 / 247 | 62.48 / 139 | **+5.03** |
| 2 | 61.70 / 213 | 63.25 / 195 | 64.22 / 121 | +2.51 |
| 3 | 61.99 / 213 | 64.70 / 156 | **65.76 / 126** | **+3.77** |

FedLS-SQL rises `+3.29` EX from T1 to T3 (78/44 paired wins/losses,
`p=0.00266`), whereas independent pure FL gains only `+0.29` from T2 to T3
(`p=0.810`). Earlier server knowledge survives subsequent private training and
aggregation: before the new server step, the mixed lineage exceeds pure FL by
`+1.55` at T2 (`p=0.152`) and `+2.71` at T3 (`p=0.0193`). The individual T2
and T3 server steps add `+0.97` and `+1.06` EX but are not independently
significant (`p=0.498`, `p=0.413`); they reduce execution errors from 195 to
121 and from 156 to 126. Thus the replication supports cumulative recurring
transfer and retained knowledge, not a claim that every server step must yield
a separately significant EX increment. “Seed 1” denotes training seed; the
older T1 ladder stored evaluation RNG seed 0, which does not alter greedy
`k=0` decoding.

### 3.3 FedLS-SQL robustness trajectory, Qwen2.5, seed 0

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
provisional. Final T3 seed reliability is reported separately below; seed 2
remains `PENDING:P0.8b` and is intentionally deferred while higher-value
evidence gaps are reviewed.

### 4.3 Final T3 training-seed reliability, Qwen2.5

| Training seed | Pure FL EX | FedLS-SQL EX | Delta | FedLS wins/losses | Exact McNemar `p` | FL/FedLS exec. errors |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 64.31 | 69.54 | **+5.23** | 121/67 | 0.0001002 | 193/101 |
| 1 | 61.99 | 65.76 | **+3.77** | 111/72 | 0.00483 | 213/126 |
| 2 | `PENDING:P0.8b` | `PENDING:P0.8b` | `PENDING:P0.8b` | `PENDING:P0.8b` | `PENDING:P0.8b` | `PENDING:P0.8b` |
| Mean over completed seeds | 63.15 | 67.65 | **+4.50** | N/A | N/A | N/A |

Across the two completed training seeds, the EX-delta sample SD is `1.03`
points. At seed 1, the paired bootstrap 95% interval is approximately
`[+1.26,+6.38]` points, and FedLS-SQL improves every Spider hardness stratum.
The two positive seeds establish enough replication for the current direction
decision but are not reported as a final three-seed uncertainty result; P0.8b
closes that cell when reactivated. Question-level McNemar
tests characterize paired test-row evidence and are not substitutes for
training-seed uncertainty.

### 4.4 P0.9b execution-guided selection screen (negative)

This method-selection screen starts both 256-row arms from
`qwen.fl.shared.t1.s0` and matches row count, 256 micro-steps, 16 optimizer
updates, seed, and all training flags. The full uniform arm is approximately
15 times larger and is context only.

| Stable ID | Server treatment | Spider EX | Spider EM | Exec. errors | Role |
|---|---|---:|---:|---:|---|
| `qwen.fl.shared.t1.s0` | none | 57.35 | **50.58** | 236 | shared initialization |
| `qwen.seqkd.random256.t1.s0` | random 256 teacher targets | **58.70** | 35.88 | **222** | matched primary control |
| `qwen.seqkd.globalerror256.t1.s0` | 192 global-error-prioritized + 64 uniform-remainder targets | 56.67 | 30.66 | 240 | rejected selector |
| `qwen.seqkd.t1.s0` | full uniform 3,873 targets | 61.32 | 30.27 | 161 | larger-budget context |

Global-error selection is `-2.03` EX versus random256 (47 paired gains, 68
losses, exact McNemar `p=0.0617`), `-5.22` EM (`p=5.15e-9`), and adds 18
execution errors. It fails the preregistered `+1.0` EX/no-error-increase gate
and is not part of FedLS-SQL. Training resource measurements are ineligible:
the arms ran concurrently and the random arm had a failed OOM attempt before a
fresh successful rerun.

### 4.5 Outline sensitivity matrix

| Outline item | Current evidence | Paper treatment |
|---|---|---|
| Remove LLM guidance | complete: pure FL vs FedLS-SQL | main ablation |
| Remove knowledge distillation | complete via matched ladder | main ablation |
| Structural distillation | not implemented | remove from claims/tables |
| Teacher families/sizes | Qwen 7B canonical; Gemma 9B T1 replication complete | family replication, not a controlled size sweep |
| Student families/sizes | Qwen 1.5B canonical; Gemma 2B T1 replication complete | family replication, not a controlled size sweep |
| LoRA ranks 4/8/16/32 | only r=16 canonical | optional |
| Clients 5/10/20 | only K=5 canonical | optional |
| FedProx | not implemented/run | conditional baseline |
| Federated 7B LLM | not run | do not claim comparison |
| ICL | matched negative evidence: -2.90 train-side EX, -3.87 inference-demo EX, 2.35x client time | closed negative appendix/limitation only |

### 4.6 Centralized schedule sensitivity, Qwen2.5, seed 0

| Stable ID | Recipe | Spider EX | Spider EM | Exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX | Role |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `qwen.central.standard3.s0` | one continuous three-epoch schedule | 67.31 | 64.41 | 14.31 | 55.91 | 54.06 | 53.27 | 13.04 | official methodology |
| `qwen.central.restart3.s0` | three independently scheduled passes | 67.60 | 62.67 | 15.76 | 57.87 | 53.19 | 52.52 | 12.91 | historical sensitivity only |

The paired Spider EX difference is `0.29` points (`p=0.863`). Never attach the
restart OOD values to the standard row.

## 5. Efficiency and trade-offs

Supports the communication/resource claims currently proposed in draft §4.2.

### 5.1 Communication payload

| Quantity | Logical tensor bytes | MiB/GiB | Scope |
|---|---:|---:|---|
| One global LoRA adapter | 73,859,072 | 70.438 MiB | 18,464,768 FP32 adapter parameters |
| Five client uploads per round | 369,295,360 | 352.188 MiB | five adapter tensor payloads |
| Five global broadcasts per round | 369,295,360 | 352.188 MiB | five post-server/global tensor payloads |
| Total per round | 738,590,720 | 704.375 MiB | upload + broadcast |
| Total through T3 | 2,215,772,160 | 2.064 GiB | three rounds |

Pure FL and FedLS-SQL have identical tensor payload because every client and
global adapter has the same 392-tensor schema and the teacher transfer is
server-local. The production audit at nested commit `147f455` independently
checks all six round records and reports the serialized-file accounting proxy:
`369,555,560` upload bytes, `369,555,400` aggregation-adapter broadcast bytes,
`739,110,960` bytes per round, and `2,217,332,880` through T3. That proxy
includes safetensors headers and records `fedavg_adapter`; the algorithm
broadcasts post-server `m_g` for FedLS. Their logical tensor payload is
identical, while the audited final serialized files differ by only 32 header
bytes. The paper therefore reports logical FP32 tensor bytes and excludes
serialization headers, transport framing, and protocol metadata.

### 5.1a Optional Secure Sum compatibility audit

| Audit | Parameters | Max/mean abs. error vs plaintext | Cosine | Time | Masked upload | Metadata | Comparable communication expansion |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen FL round 1, five clients | 18,464,768 | `3.7253e-9` / `1.4493e-10` | `0.9999999999999983` | 7.1147 s | 738,590,720 B | 1,401 B | about 49.93% |

This P1.8 result (`6c67e79`) validates an optional local pairwise-mask Secure
Sum wrapper over the same weighted aggregation. It is reported separately from
accuracy: headline FL/FedLS results retain their standard plaintext FedAvg
lineages. The audit is not an end-to-end MPC deployment or a DP guarantee.

### 5.2 Accuracy-resource table

| Track/model | EX scope | Trainable parameters | Inference latency | Peak allocated/reserved VRAM | Process RSS | Status |
|---|---|---:|---:|---:|---:|---|
| FedLS-SQL / Qwen2.5-1.5B BF16 | Spider T3 accuracy; fixed 32-row resource subset | 18,464,768 | 0.7873 s/query (IQR 0.0671) | 3,474.6 / 3,684.7 MB | 1,815.2 MB (IQR 1.3) | 5/5 fresh repetitions eligible |
| Teacher / Qwen2.5-Coder-7B 4-bit | fixed 32-row resource subset; accuracy not scored | N/A | 1.6460 s/query (IQR 0.0100) | 6,776.8 / 7,044.3 MB | 2,021.0 MB (IQR 2.4) | 5/5 fresh repetitions eligible; not a federated-7B baseline |

P1.1b used identical deterministic rows and decoding, two in-process warm-up
rows, batch size 4, five fresh independent repetitions per model, and excluded
model loading and SQL scoring from the timed region. The student is `2.09x`
faster by both latency and throughput and uses `48.73%` less peak allocated
VRAM, `47.69%` less reserved VRAM, and `10.18%` less process RSS than the
already-quantized 4-bit teacher. These are shared-server steady-state inference
measurements, not training, energy, concurrency, full-test, or federated-7B
evidence; hardware exclusivity is not claimed.

## 6. Error analysis

The canonical paired audit uses the independent pure-FL and FedLS-SQL T3
predictions on all 1,034 Spider rows. EX is primary; EM is retained only as a
SQL-form diagnostic.

### 6.1 Outcome-state transitions

| Outcome | Pure FL | FedLS-SQL | Change |
|---|---:|---:|---:|
| EX correct | 665 | **719** | +54 net |
| Executable but wrong | 176 | 214 | +38 |
| Execution error | 193 | **101** | -92 (-47.7%) |

FedLS corrects 121 FL failures and regresses 67 FL-correct rows, reproducing the
headline `+5.22` EX difference (exact McNemar `p=0.0001002`). Of the 193 FL
execution errors, 72 become correct, 56 become executable-but-wrong, and 65
remain execution errors. Missing-column failures fall from 163 to 91 and
missing-table failures from 20 to 2.

### 6.2 Hardness and SQL-construct strata

| Stratum | n | FL EX | FedLS EX | Delta | Wins/losses | Paired `p` |
|---|---:|---:|---:|---:|---:|---:|
| Medium | 446 | 64.35 | **74.22** | +9.87 | 64/20 | <0.00001 |
| Aggregation | 551 | 67.15 | **73.14** | +5.99 | 62/29 | 0.00071 |
| GROUP BY | 277 | 61.37 | **68.59** | +7.22 | 38/18 | 0.0105 |
| JOIN | 408 | 46.57 | **51.96** | +5.39 | 56/34 | 0.0263 |
| ORDER BY | 237 | 59.49 | **71.31** | +11.81 | 40/12 | 0.00013 |
| LIMIT | 189 | 57.67 | **70.90** | +13.23 | 35/10 | 0.00025 |
| Hard | 174 | **55.17** | 54.60 | -0.57 | 19/20 | 1.000 |
| Nested query | 83 | 49.40 | **50.60** | +1.20 | 6/5 | 1.000 |
| Set operation | 80 | **50.00** | 31.25 | **-18.75** | 5/20 | 0.00408 |

All 1,034 gold queries parse under SQLGlot's SQLite dialect. Construct subsets
overlap and the displayed tests are exploratory, not adjusted for multiple
comparisons. The robust paper interpretation is that FedLS sharply reduces
invalid SQL and helps several common structures, while set operations remain a
specific limitation rather than a reason to change the frozen method.

FedLS T3 has 333 `EX=1, EM=0` rows. These pass the execution-result criterion
and are consistent with BIRD-to-Spider SQL-form variation; a deterministic
example file is retained for transparent qualitative inspection. EM is not an
optimization target.

| Analysis | Available evidence | Status |
|---|---|---|
| Invalid/execution failures | paired states and grouped SQLite errors | complete |
| EX=1, EM=0 SQL-form variation | 333 FedLS-T3 cases plus deterministic examples | complete as secondary diagnostic |
| Spider hardness | paired T3 audit | complete |
| JOIN/nested/aggregation/filtering constructs | SQLGlot parse coverage 1,034/1,034 | complete exploratory strata |
| Schema-linking errors | predictions available; validated extractor absent | do not claim yet |
| Federated-distribution errors | one `alpha=0.5` split only | insufficient for broad claim |
| LLM-SLM transfer failures | 121 corrections, 67 regressions, fixed-rule examples | complete descriptive audit |

## 7. Adaptive evidence dashboard

| Current candidate paper evidence | Canonical section here | Coverage |
|---|---|---|
| Overall NL-to-SQL performance | §2 | seed-0 final-model table complete |
| Communication efficiency | §5.1 | complete for adapter payload |
| Resource efficiency | §5.2 | complete for scoped deployment inference; training/federated-7B resources not measured |
| Non-IID robustness | §3.3 | scoped to one partition; broader settings pending |
| Convergence analysis | §3.1–§4.3 | complete trajectories at seeds 0/1; final T3 gain positive at both seeds |
| Ablation and sensitivity | §4 | core causal ladder complete; broad sweeps optional |
| Error analysis | §6 | paired EX-oriented T3 audit complete |
| Optimizer baseline breadth | §2.3/§4.5 | FedProx-LoRA recommended; design/run pending |
| Novelty positioning | related-work matrix | mandatory nearest-work audit pending |

This dashboard may be reordered, reduced, or extended after each evidence gate.
The draft outline is an experiment menu, not evidence that every proposed sweep
must be completed. Manuscript claims must follow validated results and the
adaptive gates in `../notes/PAPER_EVIDENCE_PLAN.md`.
