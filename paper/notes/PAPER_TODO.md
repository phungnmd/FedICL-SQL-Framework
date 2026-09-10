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

- [ ] Rescore the saved BIRD base prediction at the official 30-second pair
  timeout; the prior 15.97 EX is a 60-second diagnostic anchor.
- [x] P2.1R BIRD-original centralized SFT with evidence, continuous E1/E2,
  `max_len=7168`, no truncation.
- [x] P2.1R BIRD-original pure FL with evidence, semantic K5 split, T1–T3,
  `max_len=7168`, no truncation.
- [ ] Rescore corrected centralized E1/E2 and FL T1/T2/T3 through
  `bird_official_set_pair_timeout30_v2`; no model regeneration is required.
- [ ] Audit/re-evaluate Spider base, centralized, and pure FL under explicit
  profile; metadata-complete Spider v2 train/dev and K5 split are frozen in
  `8caa610`.
- [ ] Report EX and execution-error transitions; keep EM secondary.

## P2.2 — Rerun the current reference method in both directions

- [x] Split the two transfer directions into output-disjoint, caller-GPU
  runners and technically audit profile/evidence/evaluator/resume contracts.
- [ ] Complete both public-teacher prerequisite lanes and freeze teacher EX,
  selection coverage, and exact matched-pool identities.
- [ ] BIRD public → Spider private/evaluation: matched public gold, teacher-target
  CE, and CE+Hinton-forward-KL controls.
- [ ] Spider public → BIRD private/evaluation: same ladder with BIRD evidence on
  private/eval rows and explicit source identities.
- [ ] Start with smoke, then T1; open T3 only for interpretable EX gain.
- [ ] Test at least one second training seed only after the architecture gate.

## P2.3 — Select or improve the method

Do not choose a mechanism in advance. Diagnose the v2 results, then rank only
the relevant candidates:

- target construction/selection if teacher targets fail despite good teacher EX;
- SeqKD versus Hinton forward KL if hard targets dominate or soft KD remains null;
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
