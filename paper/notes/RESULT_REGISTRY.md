# FedLS-SQL — active result registry

Only protocol-v2 results may enter new method/accuracy tables. The complete v1
registry is preserved at
`paper/archive/protocol_v1_no_bird_evidence/RESULT_REGISTRY_v1.md`.

## Canonical protocol-v2 results

| Stable ID | Status | Required lineage |
|---|---|---|
| `v2.bird.base` | pending | explicit BIRD release + `bird_with_evidence` eval |
| `v2.bird.central` | pending | standard with-evidence centralized SFT |
| `v2.bird.fl` | pending | database-disjoint BIRD clients, with evidence |
| `v2.spider.fl` | pending/reuse audit | Spider-only lineage independent of BIRD |
| `v2.bird_to_spider.reference` | pending | corrected BIRD-public evidence policy |
| `v2.spider_to_bird.reference` | pending | corrected BIRD-private/eval evidence policy |

## Protocol-v2 audits

| Stable ID | Artifact | Status |
|---|---|---|
| `audit.v2.spider.original` | `fedicl-sql/audits/protocol_v2/spider_original.json` | passed; nested `4ae6e35` |
| `audit.v2.bird.original` | `fedicl-sql/audits/protocol_v2/bird_original.json` | passed with evidence; compatibility release only; nested `4ae6e35` |

## Evidence retained independently of BIRD prompt v1

- Spider-only centralized and pure-FL baselines;
- Spider-only FedProx negative baseline;
- deterministic LoRA parameter/communication accounting;
- Secure Sum numerical compatibility audit;
- Qwen 1.5B versus 7B controlled Spider inference benchmark.

These remain usable only after verifying that their source lineage does not
consume a BIRD-derived checkpoint or pool.

## Protocol-v1 status

All Qwen/Gemma FedLS, SeqKD, public-gold controls, RKL value tests, stronger-skew
FedLS endpoints, and BIRD evaluations that consumed no-evidence BIRD prompts are
`protocol-v1 contextual`, not canonical v2 results. Their predictions,
provenance, evidence audits, and negative branches remain archived; do not
silently delete or relabel them.
