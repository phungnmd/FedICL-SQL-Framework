# FedLS-SQL agent instructions

Before generating or changing experiment commands, read `CONVENTION.MD` §6.1
and the active queue in `paper/notes/PIPELINE_NEXT.md`.

For every new centralized/client `experiments/client_train/run.py` command with
`--epochs` greater than 1:

- include `--save-epoch-checkpoints`;
- expect adapter-only snapshots at `<out>/epochs/epoch_N`;
- expect the only persistent optimizer/scheduler checkpoint at
  `<out>/resume_latest`;
- resume an interrupted invocation by rerunning the exact command and output
  root (`_ckpt` handles crash recovery);
- extend completed training only from `resume_latest`, into a new immutable
  output root, with the new total `--epochs` and `--allow-epoch-extension`;
- never describe an extended cosine horizon as identical to a longer horizon
  planned from step zero.

Do not store full trainer state in every old epoch directory. Old epoch
snapshots exist for evaluation; only the farthest completed epoch is resumable.
