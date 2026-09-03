# FedLS-SQL — active lab log

## Current state

- Active protocol: `v2`, dataset profiles explicit.
- Primary metric: execution accuracy (EX).
- Method status: open; previous FedAvg + verified-target CE + optional RKL is a
  reference implementation, not a frozen final contribution.
- GPU work: paused until the BIRD release/data audit and protocol-v2 smoke pass.
- Historical record: `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`.

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

## Next decision

Publish the BIRD-original v2 materialization and semantic K5 split, then use the
available overnight window for centralized E1/E2 and pure-FL T1–T3 training.
In parallel only after those processes finish, close the official evaluator and
release gates. Evaluate all baseline checkpoints before opening the reference
FedLS ladder. The resulting EX/error transitions determine whether to improve
KD, aggregation/local optimization, target selection, or cross-dataset transfer.
