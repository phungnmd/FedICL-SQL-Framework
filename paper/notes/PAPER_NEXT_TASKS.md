# FedLS-SQL — current operator dashboard

| Order | Task | Compute | Ready? |
|---:|---|---|---|
| 1 | P2.1R longest-eight-row BIRD context/VRAM smoke | GPU 0 | ready (`d21f777`) |
| 2 | Corrected centralized E1/E2 + pure-FL T1/T2/T3 and BIRD EX | GPU 0 | after smoke |
| 3 | Audit/reuse Spider-only baselines under explicit profile | CPU/GPU | after 2 |
| 4 | Main flow: Spider private FL → BIRD public gold/SeqKD/SeqKD+RKL → Spider eval | GPU | after baseline acceptance |
| 5 | Reverse flow using corrected BIRD private baselines | GPU | after main flow |
| 6 | Select targeted KD/federated improvement | adaptive | after reference ladder |

Source/profile audit and EX dispatch are implemented. Old P2.1 results at
`f99febd` are diagnostic only: 754 train rows lost all evidence. P2.1R uses
7,168 tokens, fail-closed overflow handling, gradient checkpointing and fresh
roots. Evidence is required input, not an active effect ablation.

Do not spend GPU on seeds, Gemma, or new KD/Federated mechanisms before the
dataset-correct baseline and reference ladder exist.
