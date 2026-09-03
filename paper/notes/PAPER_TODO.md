# FedLS-SQL — adaptive protocol-v2 TODO

Executable commands belong only in `PIPELINE_NEXT.md`. Reorder later tasks when
an earlier result changes the method hypothesis.

## P2.0 — Freeze the corrected experimental protocol

- [x] Archive the protocol-v1 architecture, lab log, queue, registry, and main tables.
- [x] Add explicit Spider/BIRD profiles and evidence-aware prompt plumbing.
- [x] Fingerprint train, KD cache, teacher target, federated, and eval policies.
- [x] Make federated split construction dataset-neutral.
- [x] Add dry-run/quarantine server cleanup utility.
- [ ] Freeze exact BIRD train/dev release identifiers and checksums.
- [ ] Add official BIRD evaluator adapter and a known-answer test fixture.
- [ ] Build/audit v2 processed data; require zero train/test `db_id` overlap.
- [ ] Run prompt parity smoke across teacher, centralized, client, server, and eval.

## P2.1 — Establish dataset-correct baselines

- [ ] BIRD base model with evidence.
- [ ] BIRD centralized SFT with evidence using a database-disjoint validation policy.
- [ ] BIRD pure FL with evidence.
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
