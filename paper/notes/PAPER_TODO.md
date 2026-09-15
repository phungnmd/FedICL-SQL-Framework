# FedLS-SQL — adaptive protocol-v2 TODO

Executable commands belong only in `PIPELINE_NEXT.md`. Reorder later tasks when
an earlier result changes the method hypothesis.

## P2.0 — Freeze the corrected experimental protocol

- [x] Archive the protocol-v1 architecture, lab log, queue, registry, and main tables.
- [x] Add explicit Spider/BIRD profiles and evidence-aware prompt plumbing.
- [x] Fingerprint train, KD cache, teacher target, federated, and eval policies.
- [x] Make federated split construction dataset-neutral.
- [x] Support explicit, versioned filtered-train/cleaned-dev BIRD ingestion.
- [x] Add dry-run/quarantine server cleanup utility.
- [x] Freeze exact BIRD-original train/dev identities and checksums.
- [x] Add official BIRD SQLite EX dispatch, a versioned scorer fingerprint, and
  known-answer fixtures distinguishing BIRD set semantics from Spider (`9d777db`).
- [x] Audit current Spider/original-BIRD processed data: hashes frozen, evidence
  probes correct, and zero train/test `db_id` overlap (`4ae6e35`).
- [ ] Build/audit the selected filtered/cleaned BIRD v2 release.
- [ ] Run prompt parity smoke across teacher, centralized, client, server, and eval
  after the corrected full-context baseline.
- [x] Add reproducible protocol-v2 materialization, semantic DB grouping, and
  deterministic centralized result IDs (`346342c`).
- [x] Make v2 split reruns content-hash verified and immutable (`11ab685`).
- [x] Add one phase-separated Windows runner for cleanup, input publication,
  sequential GPU-0 training/evaluation, and allowlisted result publication
  (`9d777db`, `e1f3127`).
- [x] Freeze/publish the original-BIRD compatibility split before launching GPUs.

## P2.1 — Establish dataset-correct baselines

- [x] Publish legacy-width BIRD-original diagnostics (`f99febd`).
- [x] P2.1q audit (`e9bde43`): scorer accepted; checkpoints rejected because
  974 prompts were truncated and 754 lost all evidence.
- [x] Implement 7,168-token fail-closed training, gradient checkpointing,
  longest-row smoke and fresh immutable roots (`d21f777`).
- [x] Pass P2.1R longest-eight-row context/VRAM smoke.

- [x] Rescore the saved BIRD base prediction and all corrected baselines at the
  official 30-second pair timeout.
- [x] P2.1R BIRD-original centralized SFT with evidence, continuous E1/E2,
  `max_len=7168`, no truncation.
- [x] P2.1R BIRD-original pure FL with evidence, semantic K5 split, T1–T3,
  `max_len=7168`, no truncation.
- [x] Rescore corrected centralized E1/E2 and FL T1/T2/T3 through
  `bird_official_set_pair_timeout30_v2`; no model regeneration is required.
- [ ] Audit/re-evaluate Spider base, centralized, and pure FL under explicit
  profile; metadata-complete Spider v2 train/dev and K5 split are frozen in
  `8caa610`.
- [ ] Report EX and execution-error transitions; keep EM secondary.

## P2.2 — Rerun the current reference method in both directions

- [x] Split the two transfer directions into output-disjoint, caller-GPU
  runners and technically audit profile/evidence/evaluator/resume contracts.
- [x] Complete both public-teacher prerequisite lanes and freeze teacher EX,
  selection coverage, and exact matched-pool identities.
- [x] Spider-private clients -> FedAvg -> full-BIRD-public
  Hinton T1; compare Centralized-E3, Pure-FL-T1, SeqKD-T1, Hinton-T1 and the
  teacher across Spider, Realistic, SYN, DK and BIRD. Published `ec5b5e1`;
  earlier/current shared-arm differences documented by paired predictions.
- [x] BIRD public → Spider private/evaluation: matched public gold and
  teacher-target CE, canonical full-public-gold CE, and gold-prefix
  Hinton-forward-KL T1 are complete and published (`5e4f005`, `ec5b5e1`).
- [x] Spider public → BIRD private/evaluation: matched gold/SeqKD ladder
  published (`1b2c46a`): 22.88/20.73/24.45 EX. Reverse Hinton is deferred.
- [ ] Start with smoke, then T1; open T3 only for interpretable EX gain.
- [ ] Test at least one second training seed only after the architecture gate.

P2.2d–f diagnose strong public-domain adaptation but poor retention: Hinton is
36.70 EX on BIRD (+21.90 over Spider-private Pure FL) and 58.32 on Spider
(+0.97), but loses 12.20/4.74 points on Realistic/SYN and is essentially flat
on DK. Full-public-gold CE reaches 55.03/47.05/43.91/40.93/32.14 on
Spider/Realistic/SYN/DK/BIRD. Hinton beats it on four sets, supporting the
combined Hinton recipe, while both public updates reduce private robustness.
The cause is not isolated. Terminal FedAvg is now the active method candidate,
before seeds or recurrent rounds.

## P2.3 — Select or improve the method

Do not choose a mechanism in advance. Diagnose the v2 results, then rank only
the relevant candidates:

- [x] **Highest-priority architecture gate (promoted by P2.2d):** implement a terminal
  private consolidation stage so the candidate deploys after FedAvg
  (`A -> K -> A`) rather than after public KD (`A -> K`). Implemented as
  composable `run.py stage private|public` chains from committed parent rows
  (nested `810d8c4`, review hardening through `014b118`: parent hashes/Git
  guards, historical objective validation, and publication recovery).
- [ ] Sync `014b118` or a descendant once, smoke `stage private` from the
  Hinton T1 row, and publish compact smoke evidence before full training.
- [ ] Run the one-local-epoch matched endpoint ladder from the same T1 lineage:
  `A`, `A -> K`, no-KD `A -> A`, and KD/re-anchored `A -> K -> A`.
  GPU 0: `A>A`; GPU 1: `A>K[fkl]>A`. Both are student-only, disjoint-root
  jobs. Keep Git unchanged until both exit; then five-set eval and publication.
- [ ] Promote terminal FedAvg only if `A -> K -> A` improves Spider/variant EX
  over both `A -> K` and matched-compute `A -> A`, while retaining useful BIRD
  transfer. Account for its extra client round and adapter communication.
- [ ] Test three private re-anchoring epochs only after the one-epoch gate;
  stop if they overwrite the KD gain or increase client drift.
- [ ] If consolidation helps, add `A→gold CE→A` to isolate the teacher's
  contribution at the final endpoint; then freeze the recipe before confirmation.
- [ ] Defer recurrent `(A -> K)^T`, GKD, MiniLLM, and fresh RKL until the
  endpoint gate identifies whether the primary weakness is KD or scheduling.
- target construction/selection if teacher targets fail despite good teacher EX;
- SeqKD (sequence level) versus canonical full-data Hinton forward KL (token
  level); do not confound this comparison with a combined SeqKD+Hinton arm;
- GKD/on-policy KD, MiniLLM, or a fresh RKL implementation only if the two
  standard KD baselines leave a measured failure worth targeting;
- FedAvg/local optimizer if client drift is the limiting factor;
- evidence-aware or privileged-information transfer if the two directions
  expose an information-asymmetry gap;
- round schedule/public budget if gain appears only at one stage.

Each candidate needs one matched control, frozen budget, EX promotion gate, and
stop rule. Negative v1 FedDF, preference KD, and FedProx branches stay closed
unless v2 reveals the exact failure they were designed to solve.

## P2.4 — Paper closure

- [ ] Select final method from evidence rather than legacy naming.
- [ ] Run minimal robustness: two seeds, one stronger non-IID split, two model families if feasible.
- [ ] Restore only lineage-valid resource/privacy/communication evidence.
- [ ] Rebuild tables, figures, manuscript claims, and reproducibility manifest.

Minimum outline-aligned closure evidence before writing the headline claim:

- matched T1 causal ladder in both transfer directions;
- T1–T3 convergence for the promoted method and pure FL;
- a second seed and one stronger non-IID setting for the promoted method;
- final student-versus-teacher latency/memory plus adapter communication size;
- paired EX/error analysis. EM remains descriptive only.

Teacher/student size sweeps, a second model family, FedProx on BIRD, and
federated 7B training are conditional extensions rather than blockers for the
first defensible paper result. They become priorities only if the primary
Qwen evidence is weak or reviewers require a broader generality claim.
