# FedLS-SQL — active result registry

Only protocol-v2 results may enter new method/accuracy tables. The complete v1
registry is preserved at
`paper/archive/protocol_v1_no_bird_evidence/RESULT_REGISTRY_v1.md`.
The compact source of truth for retained numeric rows, valid server adapters,
and missing controls is `VALID_RESULTS_AND_ADAPTERS.md`.

## Canonical protocol-v2 results

| Stable ID | Status | Required lineage |
|---|---|---|
| `v2.bird.base` | accepted inference baseline: 15.97 EX | original BIRD dev, full prompt with evidence; `f99febd`, rescore `e9bde43` |
| `v2.bird.central` | pending P2.1R rerun | old 31.62/35.07 EX are diagnostic only; train context truncated |
| `v2.bird.fl` | pending P2.1R rerun | old 22.56/27.31/29.99 EX are diagnostic only; train context truncated |
| `v2.spider.fl` | pending/reuse audit | Spider-only lineage independent of BIRD |
| `v2.bird_to_spider.reference` | pending | corrected BIRD-public evidence policy |
| `v2.spider_to_bird.reference` | pending | corrected BIRD-private/eval evidence policy |

## Protocol-v2 audits

P2.1q closed the scorer audit but rejected the trained checkpoints: 974/9,428
prompts were truncated and 754 lost all evidence. Five rescored arms were
unchanged; centralized E1 gained one row; no disk-full error recurred. BIRD
`test.csv` here is the 1,534-row **development** set.

| Stable ID | Artifact | Status |
|---|---|---|
| `audit.v2.spider.original` | `fedicl-sql/audits/protocol_v2/spider_original.json` | passed; nested `4ae6e35` |
| `audit.v2.bird.original` | `fedicl-sql/audits/protocol_v2/bird_original.json` | passed with evidence; compatibility release only; nested `4ae6e35` |
| `audit.v2.bird.p21` | `fedicl-sql/audits/protocol_v2/p21_bird_qwen15b_integrity_t60_s0/` | complete; scorer accepted, trained arms superseded; nested `e9bde43` |

All new BIRD result entries must record execution scorer
`bird_official_set_v1`; manifests with the historical Spider scorer are
protocol-v1 context even when their prompts otherwise contain evidence.

## Evidence retained independently of BIRD prompt v1

- Spider-only centralized and pure-FL baselines;
- Spider-only FedProx negative baseline;
- deterministic LoRA parameter/communication accounting;
- Secure Sum numerical compatibility audit;
- teacher-only Qwen 7B controlled Spider inference measurement.

These remain usable only after verifying that their source lineage does not
consume a BIRD-derived checkpoint or pool.

The old student-versus-teacher resource comparison used a protocol-v1 FedLS
student adapter. Its student side is archived; benchmark the eventual v2 final
adapter again before making a deployment comparison. Communication accounting
for the Spider-only FL adapter is valid, while the final FedLS communication
row remains pending the v2 method.

## Protocol-v1 status

All Qwen/Gemma FedLS, SeqKD, public-gold controls, RKL value tests, stronger-skew
FedLS endpoints, and BIRD evaluations that consumed no-evidence BIRD prompts are
`protocol-v1 contextual`, not canonical v2 results. Their predictions,
provenance, evidence audits, and negative branches remain archived; do not
silently delete or relabel them.
