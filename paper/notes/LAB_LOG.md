# FedLS-SQL — active lab log

## Current state

- Active protocol: `v2`, dataset profiles explicit.
- Primary metric: execution accuracy (EX).
- Method status: open; FedAvg + verified-target SeqKD is the reference path,
  with canonical full-data Hinton forward KL as the primary token-level
  soft-logit baseline.
- P2.1q completed at `e9bde43`: scoring is stable, but P2.1 training
  checkpoints are diagnostic only because required BIRD context was truncated.
- P2.1R full-context Base/Centralized/FL computation is complete; official
  30-second BIRD rescore/publication remains.
- Next: close both public-teacher lanes, inspect teacher/pool quality, then run
  the matched T1 causal ladder in both directions.
- Historical record: `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`.

## 2026-09-10 — official BIRD timeout closure

Source audit found that BIRD's original and Mini-Dev EX evaluators assign one
30-second deadline to the combined prediction/gold execution. MAC-SQL likewise
uses 30 seconds for EX and 60 seconds only for VES. The previous live scorer
used 60 seconds independently for each SQL, although its set-of-row-tuples
comparison was correct. Nested commit `2178d5a` replaces it with
`bird_official_set_pair_timeout30_v2` and adds a fingerprinted, resumable CPU
rescorer for saved prediction CSVs. Training and generation remain valid; no
model inference needs repeating. The independent BIRD-train gold audit remains
at 60 seconds because it is a data-integrity diagnostic, not benchmark EX.

## 2026-09-03 — BIRD protocol reset

Audit confirmed that BIRD `evidence` existed in processed source rows but was
deliberately excluded by the common Spider prompt builder. Consequently the
teacher, target generation, student SFT/KD, and BIRD evaluation all operated in
a no-knowledge setting. BIRD officially allows this setting, so old numbers are
not fabricated; however, they cannot serve as the standard with-evidence BIRD
baseline or as canonical evidence for the revised paper without explicit
relabeling.

Observed selection evidence:

- evidence populated: 93.16% of BIRD source and 90.34% of the Qwen pool;
- selected examples have shorter evidence on average: 79.24 vs 95.96 chars;
- selection retention declines from 52.19% for 1–60 chars to 25.60% for at
  least 131 chars;
- evidence length and selection have Spearman `r=-0.2207`, `p=2.35e-104`;
- an existing 512-row diagnostic did not show teacher-CE gain increasing with
  evidence length (`r=0.0128`, `p=.779`).

Interpretation: the no-evidence selector is biased toward examples requiring
less external knowledge. This motivates the reset, but does not itself prove
that evidence explains every prior gain.

Implementation completed:

- `Text2SQLExample` introduced with backward-compatible `SpiderExample` alias;
- explicit `spider`, `bird_with_evidence`, `bird_no_evidence`, and `legacy`
  profiles added;
- evidence is rendered consistently in client SFT, server SFT/KD, teacher
  targets, teacher-logit caches, and evaluation;
- profiles/evidence modes enter fingerprints and incompatible data fail before
  model loading;
- federated split construction now accepts arbitrary processed train/test CSVs;
- server artifact retirement is dry-run/quarantine based and never deletes;
- versioned explicit BIRD JSON/database ingestion now supports filtered-train
  and cleaned/original dev without relying on archive layout;
- full nested test suite: 345 passed.

P2.0a then froze deterministic audits at nested commit `4ae6e35`. Spider has
8,659 train and 1,034 test rows. Original BIRD has 9,428/1,534 rows with
8,783/1,386 populated evidence values. Both train/test pairs have zero DB
overlap; the BIRD prompt probe contains `### Evidence:` and the Spider probe
does not.

## 2026-09-04 — overnight baseline preparation

Nested commits `346342c` and `11ab685` close the remaining training-input mechanics:
immutable protocol-v2 CSV materialization, semantic schema grouping for a
BIRD K5 split, immutable shard hashes, and deterministic `client_train` result
paths. Full test suite: 347 passed.

The official filtered/cleaned release and evaluator remain open. Nevertheless,
the audited original 9,428/1,534 BIRD release is a valid explicitly labeled
with-evidence compatibility track. Centralized E1/E2 and pure-FL T1–T3 may be
trained now because evaluation implementation cannot change their checkpoints.
No EX result from this track becomes canonical until every checkpoint is scored
through the same official BIRD evaluator.

## 2026-09-04 — baseline runner and evaluator closure

Nested commit `9d777db` fixes a final protocol gap: although dataset profiles
previously recorded `evaluator=bird`, the shared loop still executed Spider EX.
Evaluation now dispatches the official BIRD SQLite set-of-row-tuples comparison,
records scorer identity `bird_official_set_v1` in resume fingerprints, and has
fixtures showing the intended differences from Spider column/order semantics.
This historical identity was superseded by the 30-second pair contract in
`2178d5a`; only its saved SQL, not its embedded EX, remains reusable.

The same commit adds `scripts/run_protocol_v2_baselines.ps1`. Separate phases
validate code, quarantine 31 exact invalid v1 roots, materialize and publish
inputs, run training/evaluation, then publish only manifest-resolved compact
outputs. The P2.1 suite yields base, centralized E1/E2, and pure-FL T1/T2/T3
under BIRD-original with evidence. Full nested suite: 350 passed.
Nested commit `40255f4` briefly added two-GPU parallel orchestration. Commit
`e1f3127` supersedes it at operator request: all four compute stages now run
sequentially on physical GPU 0, with scientific flags, output roots, and exact
resume behavior unchanged. Full nested suite remains 350 passed.
Commit `8a17542` fixes server validation only: the runner resolves the locked
`dev` extra for `pytest` and accepts descendants of the required refactor base
without a misleading warning. No scientific or checkpoint contract changed.
Commit `767301d` additionally forces UTF-8 for Python and inherited subprocesses
after a Windows CP1252 console rejected a Unicode diagnostic arrow during the
split test. This is an environment-compatibility fix only.
Commit `d1df12d` normalizes absolute Windows result paths from the federated
manifest before applying the publication allowlist. P2.1 artifacts and metrics
were unaffected; only compact result publication had failed.

## 2026-09-06 — P2.1 audit result and context repair

P2.1q audited all 9,428 train prompts and independently rescored all saved dev
SQL. It found 974 truncated prompts; 754 lost all provided evidence. The old
Spider-tuned `max_len=2560` checkpoints are therefore rejected as canonical.
Scoring itself is stable: only centralized E1 changed by one correct row
(31.55→31.62 EX), five arms were unchanged, no disk-full error recurred, and
1,532/1,534 dev gold queries completed within 60 seconds.

Official BIRD's current fine-tuning example uses a long 18k context and gradient
checkpointing. Nested `d21f777` introduces a measured 7,168-token contract for
our frozen Qwen/full-schema setup, fail-closed overflow handling, fingerprinted
gradient checkpointing, longest-eight-row VRAM smoke, and new immutable roots.
P2.1R must finish before the reference FedLS ladder. The 6,601-row filtered
release remains a separate, explicitly labeled final-release/data-quality gate.

## 2026-09-06 — active-result cleanup

`VALID_RESULTS_AND_ADAPTERS.md` now lists the only retained accuracy rows,
server adapters, and missing baseline/ablation cells. Active result scanners
retain Spider-only Base/Centralized/FL/FedProx, Gemma Base/FL, Secure Sum, and
the independent teacher resource reference. BIRD-dependent v1 results,
truncated-context P2.1 trained arms, mixed/superseded probes, generated teacher
targets, and final-adapter resource comparisons were moved to recoverable Git
archives. No historical evidence was deleted. Nested commit `7b487bd` records
the archive moves, adds the second server-quarantine manifest, and makes active
FedLS examples explicit about BIRD evidence, 4,096-token context, and v2 output
roots. Full nested suite: 356 passed.

## 2026-09-10 — independent direction runners

P2.1R baseline computation completed on the experiment server; its saved BIRD
SQL still requires the official 30-second rescore before publication. The
BIRD-public Qwen-7B target generator has a valid partial row checkpoint. Its
new progress bar counts only pending rows, so `0/2300` denotes a resume after
roughly 7,128 completed rows rather than regeneration of all 9,428 rows.

Nested commit `8caa610` replaces the hard-coded GPU-0/GPU-1 closure scheduler
with two output-disjoint entry points. `run_protocol_v2_spider_private.ps1`
prepares BIRD-public targets for Spider-private/evaluation;
`run_protocol_v2_bird_private.ps1` prepares Spider-public targets for
BIRD-private/evaluation. The calling PowerShell process selects exactly one GPU
through `CUDA_VISIBLE_DEVICES`. The same commit freezes metadata-complete
Spider v2 train/dev files and the existing semantic K5 partition under a new
immutable root. Full nested test suite: 364 passed.

## 2026-09-10 — direction-runner technical review

The two directions were audited end to end. `spider_private` uses Spider K5
private clients/evaluation and BIRD-original public supervision with evidence;
`bird_private` reverses those roles and retains evidence in every BIRD client
and evaluation prompt. Teacher target generation uses full schema, zero demos,
256 output tokens and the declared public profile. Selection first rejects
non-executable SQL, then applies the dataset-specific EX evaluator; the gold-CE
control uses the exact same selected source indices and differs only in target
SQL. Both public teacher dev evaluations together provide the Qwen-7B anchor on
both Spider and BIRD without duplicate inference.

Nested `c13fc9f` adds read-only SQLite execution, atomic recovery of only a
partial final teacher-target checkpoint line, generic source-gold provenance,
and stronger frozen dataset/split guards. Evaluator identities are unchanged,
so accepted historical results are not invalidated. Nested `8c72764` pins the
reviewed runner base. Full nested suite: 369 passed.

The runners deliberately stop after teacher/pool prerequisites. They do not
yet produce FedLS adapters. The next scientific gate is the matched T1 ladder:
pure FL, matched public-gold CE, execution-matched teacher-target CE, and the
  same target CE plus Hinton forward KL from one shared T1 client/FedAvg initialization.

On 2026-09-11, the BIRD teacher dev evaluation completed at EX `47.1%`, EM
`6.5%`, but the wrapper failed afterward because its resume directory contained
three manifests rather than exactly one. No inference result was lost.
Nested `633743c` now validates evaluator, arm set and artifact existence across
all manifests, selects the newest compatible completion, and skips model
inference when such a result already exists. Nested `3b98b54` pins this fix for
server runs. Full nested suite: 370 passed.

## 2026-09-11 — soft-KD baseline reset

Hinton forward KL replaces reverse KL as the active soft-logit baseline. The
server loss is target CE plus `T^2 KL(p_teacher^T || p_student^T)`, with `T=2`
and equal loss weights by default. Nested commits `3e85e77` and `951960b`
remove the RKL/KID implementation and CLI, fingerprint temperature, and require
new caches marked `kd_objective=hinton_forward_kl`; 362 tests pass. Existing
RKL artifacts remain historical only and cannot resume into the new lineage.
No further KD objective is opened until the corrected two-direction T1 ladder
has been evaluated.

## 2026-09-11 — protocol-v2 prerequisite closure and first matched T1

Nested result commit `e2ca26e` publishes both dataset-correct teacher pools,
teacher dev predictions, corrected BIRD baselines, and the first matched T1
ladder. BIRD public→Spider private retains 5,319/9,428 targets (56.42%);
Spider public→BIRD private retains 7,251/8,659 (83.74%). Teacher zero-shot EX
is 47.07 on BIRD dev and 76.69 on Spider.

The official BIRD 30-second pair rescore gives Base 15.97, Centralized E1/E2
31.42/34.94, and Pure FL T1/T2/T3 22.75/28.36/31.10 EX. In the first matched
transfer direction, Pure FL is 56.96, matched-gold CE 56.09, and SeqKD 57.64
EX on Spider. Paired rows show SeqKD corrects 140 Pure-FL errors but regresses
133 Pure-FL successes, a net gain of seven. This does not open T2/T3. Next are
the reverse matched T1 ladder and Hinton-forward-KL T1; method selection remains
open.

## 2026-09-12 — separate SeqKD from canonical Hinton KD

The planned 5,319-row `teacher-target CE + Hinton FKL` hybrid is removed from
the active matrix. Its partially generated full-logit cache uses selected
teacher-SQL prefixes and cannot support canonical Hinton KD. The operator
approved permanent deletion of its exact active/quarantine roots to reclaim
disk; it must not be resumed or regenerated.

The two KD baselines are now intentionally separate: SeqKD trains on the 5,319
execution-verified teacher sequences, while canonical Hinton KD compares full
public-gold CE against full public-gold CE plus `T^2 KL(teacher || student)` on
all 9,428 BIRD public rows under gold-prefix teacher forcing. This requires a
new cache and lineage. GKD/on-policy KD, MiniLLM, and a newly implemented RKL
lineage remain conditional follow-ups after these baselines and the reverse T1
ladder are complete.

The canonical BIRD-public cache is activated at
`artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0`.
It renders all 9,428 original BIRD training rows with evidence and gold SQL,
stores full-vocabulary fp16 teacher logits (temperature is applied later by
training, with canonical `T=2`), and is output-disjoint from
the concurrently running reverse T1 ladder. It remains an uncommitted
intermediate; the downstream training result will publish its fingerprints.

The cache completed in 67,379.4 seconds (7.15 seconds/example): 9,428 examples
map to 9,425 unique content-addressed shards because three rendered token
sequences are duplicates. The downstream T1 comparison is now active on GPU 1:
full-public-gold CE versus balanced Hinton FKL (`lambda_ft=lambda_kd=0.5`,
`T=2`), sharing the accepted Spider-private FedAvg initialization. SeqKD stays
a separate sequence-level reference arm.

Execution priority is now the headline direction: Spider-private client CE ->
FedAvg -> BIRD-public Hinton FKL -> T1. GPU 1 runs Hinton before full-gold CE,
then evaluates Centralized-E3, Pure-FL-T1, SeqKD-T1 and Hinton-T1 on Spider,
Realistic, SYN, DK and BIRD. Existing teacher anchors (Spider 76.69 EX; BIRD
47.07 EX) are reused, with new teacher evaluation only for the three Spider
variants. GPU 0 continues the independent reverse matched T1 ladder unchanged.

## 2026-09-13 — prioritize a terminal-FedAvg endpoint test

An implementation audit corrected the assumed round endpoint. The current
reference runs client LoRA training -> FedAvg -> public server KD and returns
the post-KD `m_g`; repeated rounds also end after KD. It has not historically
deployed a final FedAvg adapter after KD.

The first method-improvement gate after the active T1 jobs is therefore a
private re-anchoring endpoint: `A -> K -> A`, where `A` is client training plus
FedAvg and `K` is public KD. The causal comparison must include `A`, current
`A -> K`, matched-compute no-KD `A -> A`, and candidate `A -> K -> A`. One local
epoch is tested first. Terminal FedAvg is promoted only if it beats both
`A -> K` and `A -> A` on primary Spider/variant EX while retaining useful BIRD
transfer; extra communication is reported. This scheduling test now precedes
new KD objectives and recurrent T2/T3 expansion.

## 2026-09-14 — Hinton T1 exposes public adaptation versus private retention

The P2.2d headline suite completed. On a single shared batch-size-16 evaluation,
Centralized-E3/Pure-FL-T1/SeqKD-T1/Hinton-T1 EX is
67.31/57.35/57.93/58.32 on Spider, 55.91/54.92/46.65/42.72 on Realistic,
54.06/49.32/48.26/44.58 on SYN, 53.27/45.23/45.61/45.42 on DK, and
17.73/14.80/34.68/36.70 on BIRD. Teacher EX on the three newly measured Spider
variants is 71.06 Realistic, 63.83 SYN, and 62.43 DK.

Hinton improves over Pure FL by 0.97 points on Spider and 21.90 on BIRD, but
regresses 12.20 on Realistic and 4.74 on SYN; DK changes by only +0.19. Its
mean over Spider plus the three variants is 47.76 versus 51.71 for Pure FL.
The result therefore supports a domain-retention diagnosis: the terminal BIRD
public update learns BIRD but overwrites part of the Spider-private robustness.
It does not isolate the value of teacher logits because the full-BIRD gold-CE
control is not yet available.

Next, run full-public-gold CE from the identical T1 FedAvg checkpoint and
implement the one-epoch `A -> K -> A` terminal-FedAvg candidate with matched
`A -> A`. Do not open seeds, recurrent T2/T3, or alternative KD losses yet.
The completed manifests and paths were operator-verified, but compact result
publication is still pending. Headline batch size 16 also explains why its
shared-arm numbers must be reconciled rather than silently replacing the
earlier batch-size-8 matched ladder.

## 2026-09-15 — full-gold CE isolates useful logits but not retention

P2.2f evaluates the full-BIRD-public gold-CE adapter at the same batch size 16
as the headline suite. EX is 55.0 Spider, 47.0 Realistic, 43.9 SYN, 40.9 DK,
and 32.1 BIRD. Relative Hinton FKL deltas are +3.32, -4.28, +0.68, +4.52, and
+4.60 points respectively. Forward-KL teacher logits therefore provide signal
beyond ordinary public gold CE on four of five datasets, most clearly on BIRD,
DK, and Spider. They do not solve the Realistic regression.

Against Pure FL, full-gold CE loses 2.35/7.92/5.42/4.33 points on
Spider/Realistic/SYN/DK while gaining 17.30 on BIRD. Together with Hinton, this
confirms that the main observed failure is the terminal public stage shifting
the model away from private Spider robustness. P2.3a terminal private
re-anchoring (`A -> K -> A`) with matched `A -> A` is now the next experiment.
The BIRD NLTK/hardness warnings affect only EM and hardness diagnostics, not EX.
Compact training/evaluation publication remains pending.
