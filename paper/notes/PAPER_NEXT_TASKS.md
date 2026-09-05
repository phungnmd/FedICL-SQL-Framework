# FedLS-SQL — current operator dashboard

| Order | Task | Compute | Ready? |
|---:|---|---|---|
| 1 | P2.1q actual token retention, independent dev gold, saved-SQL rescore | CPU | implemented; run on server |
| 2 | Review P2.1q; accept checkpoints or fix measured input loss | CPU/code | after 1 |
| 3 | Audit/reuse Spider-only baselines under explicit profile | CPU/GPU | after 2 |
| 4 | Main flow: Spider private FL → BIRD public gold/SeqKD/SeqKD+RKL → Spider eval | GPU | after baseline acceptance |
| 5 | Reverse flow using BIRD private baselines | GPU | after main flow |
| 6 | Select targeted KD/federated improvement | adaptive | after reference ladder |

Source/profile audit and EX comparison dispatch are implemented. Original BIRD
P2.1 results were published at `f99febd`; acceptance awaits task 1. Filtered BIRD
release is a separate later data-quality comparison. Evidence is required input,
not an active effect ablation.

Do not spend GPU on seeds, Gemma, or new KD/Federated mechanisms before the
dataset-correct baseline and reference ladder exist.
