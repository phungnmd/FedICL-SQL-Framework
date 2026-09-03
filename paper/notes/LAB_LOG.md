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
- full nested test suite: 344 passed.

## Next decision

Freeze one official BIRD release pair, rebuild processed data with release and
source-row provenance, then run zero-GPU prompt/split/evaluator smoke tests.
Only after those pass should centralized, FL, and the reference FedLS ladder be
rerun. The resulting error analysis determines whether to improve KD,
aggregation/local optimization, target selection, or cross-dataset transfer.
