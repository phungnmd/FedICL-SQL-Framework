# FedLS-SQL — active experiment queue

> Pure FL Block K completed on 2026-08-20. Its command is preserved at
> `paper/archive/pre_fedls_2026-08/legacy_runbooks/PIPELINE_BLOCK_K_completed_2026-08-20.md`.

## Status

| Priority | Task | Status |
|---|---|---|
| P0 | Centralized vs FL vs FedLS-SQL, seed 0 | complete |
| P0 | Consolidate communication/resource metrics | next |
| P1 | Multi-round seeds 1 and 2 | pending |
| P2 | FedProx, size/rank/skew sensitivity | scope with advisor first |

## Completed baseline evidence

The independent pure-FL lineage uses `arm=fedavg`, five non-IID clients,
`alpha=0.5`, one local epoch per round, `train_k=0`, and seed 0. It has one
immutable setup ID across T1-T3:

```text
229fe736042acd80df29a19e577963e4f69a5e6bb62d41ac5964fbeee9f629d2
```

Canonical final checkpoints:

```text
Centralized = artifacts/probe_p/central_3ep/adapter
FL          = artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter
FedLS-SQL   = artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g
```

## Next block — efficiency evidence

Extract and report, without rerunning accuracy evaluations:

1. trainable LoRA parameter count and adapter size;
2. upload/download bytes per client, per round, and total through T3;
3. client and server wall time;
4. client and server peak VRAM;
5. deployed SLM inference latency and model footprint.

Keep client, server, and end-to-end costs separate. FedLS-SQL adds public
server work over pure FL, so do not describe the T3 comparison as compute
matched.

## After efficiency consolidation

1. Replicate pure FL and FedLS-SQL T1-T3 for seeds 1 and 2.
2. Report seed-level trajectories rather than treating question-level paired
   significance as multi-seed method significance.
3. Do not run new ICL, FLoRA-NA, self-consistency, or T4/T5 experiments.
4. Do not start P2 sweeps until their necessity is agreed with the advisor.
