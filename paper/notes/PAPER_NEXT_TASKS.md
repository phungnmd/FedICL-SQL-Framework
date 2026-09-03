# FedLS-SQL — current operator dashboard

| Order | Task | Compute | Ready? |
|---:|---|---|---|
| 1 | Run P2.0a source/prompt audit | CPU | yes; command in `PIPELINE_NEXT.md` |
| 2 | Review P2.0b server retirement dry-run | CPU | after P2.0a |
| 3 | Import/freeze filtered BIRD train and selected dev release | CPU | code task |
| 4 | Add official BIRD evaluator adapter + fixture | CPU | code task |
| 5 | Run BIRD base/centralized/FL smoke and full baselines | GPU | after 3–4 |
| 6 | Rerun old method as a reference in both directions | GPU | after 5 |
| 7 | Select a method improvement from observed failures | adaptive | after 6 |

Do not spend GPU on seeds, Gemma, or new KD/Federated mechanisms before the
dataset-correct baseline and reference ladder exist.
