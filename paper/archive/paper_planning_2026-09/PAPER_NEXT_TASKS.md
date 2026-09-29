# FedLS-SQL — current operator dashboard

See `VALID_RESULTS_AND_ADAPTERS.md` for the only retained accuracy rows and
adapter paths. Anything absent there must not initialize a new run.

| Order | Task | Compute | Ready? |
|---:|---|---|---|
| 1 | Resume BIRD-public targets for Spider-private direction | caller-selected GPU | active; partial checkpoint |
| 2 | Build Spider-public targets for BIRD-private direction | caller-selected GPU | ready; may run independently |
| 3 | Review teacher EX, pool retention, and official P2.1R rescore | CPU | after direction runners |
| 4 | Matched T1: FL vs gold CE vs SeqKD vs SeqKD+Hinton-FKL, both directions | GPU | after step 3 |
| 5 | Open T2/T3 only for an interpretable T1 EX gain | GPU | gated |
| 6 | Select targeted KD/federated improvement | adaptive | after reference T1 |

Source/profile audit and EX dispatch are implemented. P2.1R computation is
complete on the server and awaits its official 30-second rescore/publication.
Nested `8caa610` supplies two independent runners; the caller selects a single
GPU for each, so they may run sequentially or concurrently without shared
output roots.

Do not spend GPU on seeds, Gemma, or additional KD/Federated mechanisms before the
dataset-correct baseline and reference ladder exist.
