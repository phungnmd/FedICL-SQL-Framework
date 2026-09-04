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
- [ ] Acquire and freeze exact BIRD train/dev release identifiers and checksums.
- [x] Add official BIRD SQLite EX dispatch, a versioned scorer fingerprint, and
  known-answer fixtures distinguishing BIRD set semantics from Spider (`9d777db`).
- [x] Audit current Spider/original-BIRD processed data: hashes frozen, evidence
  probes correct, and zero train/test `db_id` overlap (`4ae6e35`).
- [ ] Build/audit the selected filtered/cleaned BIRD v2 release.
- [ ] Run prompt parity smoke across teacher, centralized, client, server, and eval.
- [x] Add reproducible protocol-v2 materialization, semantic DB grouping, and
  deterministic centralized result IDs (`346342c`).
- [x] Make v2 split reruns content-hash verified and immutable (`11ab685`).
- [x] Add one phase-separated Windows runner for cleanup, input publication,
  sequential GPU-0 training/evaluation, and allowlisted result publication
  (`9d777db`, `e1f3127`).
- [ ] Freeze/publish the original-BIRD compatibility split before launching GPUs.

## P2.1 — Establish dataset-correct baselines

- [ ] BIRD base model with evidence.
- [ ] BIRD-original centralized SFT with evidence, continuous E1/E2 checkpoints
  (may train before evaluator completion; no EX claim yet).
- [ ] BIRD-original pure FL with evidence, semantic K5 split, T1–T3 checkpoints
  (may train before evaluator completion; no EX claim yet).
- [ ] Evaluate base, centralized E1/E2, and FL T1/T2/T3 through one official
  BIRD evaluator after P2.0d.
- [ ] Audit/re-evaluate Spider base, centralized, and pure FL under explicit profile.
- [ ] Report EX and execution-error transitions; keep EM secondary.

## P2.2 — Rerun the current reference method in both directions

- [ ] BIRD public → Spider private/evaluation: matched public gold, teacher-target
  CE, and CE+RKL controls.
- [ ] Spider public → BIRD private/evaluation: same ladder with BIRD evidence on
  private/eval rows and explicit source identities.
- [ ] Start with smoke, then T1; open T3 only for interpretable EX gain.
- [ ] Test at least one second training seed only after the architecture gate.

## P2.3 — Select or improve the method

Do not choose a mechanism in advance. Diagnose the v2 results, then rank only
the relevant candidates:

- target construction/selection if teacher targets fail despite good teacher EX;
- CE versus soft KD if hard targets dominate or RKL remains null;
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
