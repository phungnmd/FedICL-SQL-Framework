# FedLS-SQL Research Project Convention

The governing rule is simple: every reported number must be traceable to a
dataset, configuration, checkpoint, prediction file, and Git commit.

## 1. Repository ownership

FedLS-SQL intentionally uses two Git repositories:

- outer repository: private paper material, references, plans, advisor inputs,
  and current research documentation;
- `fedicl-sql/`: releasable code, processed data, committed metrics/configs,
  predictions, tests, and analysis utilities.

Do not mix commits between the two repositories. Reference PDFs and private
notes must not be moved into the releasable code repository.

## 2. Canonical outer layout

```text
paper/
├── drafts/       current manuscript outline/drafts
├── notes/        active architecture, lab log, queue, matrices, registries
├── references/   private source library
├── templates/    venue/manuscript templates
└── archive/      superseded material, retained for history
```

Only active material belongs in `paper/notes/`. Completed runbooks, old email,
superseded figures, obsolete reports, and abandoned proposals belong in an
archive directory with a README explaining their replacement.

## 3. Canonical sources of truth

| Question | Source |
|---|---|
| What is the method? | `paper/notes/system_architecture.md` |
| What evidence is currently valid? | `paper/notes/LAB_LOG.md` |
| What runs next? | `paper/notes/PIPELINE_NEXT.md` |
| Which metric appears in the paper? | `paper/results/MAIN_RESULTS.md` |
| Which checkpoint/result label is canonical? | `paper/notes/RESULT_REGISTRY.md` |
| Which RQ still lacks evidence? | `paper/notes/EXPERIMENT_MATRIX.md` |
| What happened historically? | `paper/archive/` and Git history |

Do not duplicate commands, result tables, or current decisions across multiple
active files without a clear owner.

## 4. Naming and compatibility

- Public method name: FedLS-SQL.
- Paper comparison labels: Centralized, FL, FedLS-SQL/FL-KD.
- Internal package and repository directory may remain `fedicl_sql` and
  `fedicl-sql`.
- Existing arms, run IDs, artifact paths, cache IDs, and setup fingerprints are
  immutable provenance identifiers.
- Renaming a presentation label never authorizes renaming an old checkpoint.

## 5. Data and privacy

- Experiments read processed CSV/JSON metadata, not benchmark raw files directly.
- Raw benchmark inputs remain unchanged after acquisition.
- Every derived split records seed, method, source, and counts.
- Test data never becomes a training, retrieval, or teacher-target pool.
- Client-private data never moves to the server in the canonical protocol.
- Privacy claims must distinguish structural isolation from DP, secure
  aggregation, and resistance to parameter-inference attacks.
- A KD pool selected by teacher/gold execution match belongs to that teacher:
  changing teacher requires regeneration from the complete public source and
  teacher-specific filtering. Never reuse another teacher's selected indices
  or treat its retained count as a fixed method budget.
- The canonical teacher-target selector is two-stage: an 8-second quick
  execution filter, followed by official EX-to-gold scoring on survivors.
  Teacher-family replications must keep both stages and their timeouts fixed;
  changing either creates a new result lineage.

## 6. Experiment lifecycle

### 6.1 Executable command contract

`paper/notes/PIPELINE_NEXT.md` is the only active owner of paper experiment
commands. Commands in archived runbooks are provenance, not the current queue.

Every active experiment command must:

- target PowerShell and occupy one physical line in one `powershell` code
  block;
- run from the `fedicl-sql/` repository root and define every variable it uses,
  so it does not depend on shell state from an earlier block;
- use a deterministic output root containing the method/setup and seed;
- use the same output root and exact scientific flags when resuming;
- fail after a non-zero Python exit and verify the expected terminal artifacts;
- use a dataset/seed/config-specific `--resume-dir` plus `--skip-completed` for
  evaluation;
- use `${name}` when a PowerShell variable is immediately followed by `:` or
  another character that can be parsed as part of the variable name;
- avoid deletion, wildcard cleanup, checkpoint copying, and silent overwrite.

For every new centralized/client `experiments/client_train/run.py` command with
`--epochs > 1`:

- include `--save-epoch-checkpoints`;
- verify adapter-only snapshots at `<out>/epochs/epoch_1` through
  `<out>/epochs/epoch_N` and the single full-state checkpoint at
  `<out>/resume_latest`;
- treat `_ckpt` only as crash recovery for an unfinished invocation and resume
  it by rerunning the exact command against the same output root;
- extend a completed run only from `resume_latest`, into a new immutable output
  root, with `--epochs` set to the new total and
  `--allow-epoch-extension` supplied explicitly;
- never copy trainer state into every old epoch directory, and never imply that
  a cosine-horizon extension is identical to declaring the longer horizon at
  step zero.

Epoch adapters from one `N`-epoch run are valid checkpoints of that continuous
trajectory and should be reused for convergence evaluation. They are not
separate runs whose cosine schedules were independently planned for 1, 2, ...,
`N` epochs.

Federated `setup.json`, `manifest.json`, stage fingerprints, and
`adapter_config.json` are the completion/lineage contract. A partial `_ckpt`
directory is resumable by rerunning the exact command. A setup, lineage, cache,
or evaluation fingerprint mismatch is a scientific configuration error: use
the original flags or a new output/resume root; never bypass the guard.

Keep long-running blocks independently resumable. Prefer one command per
scientific checkpoint (training seed, matched evaluation, transfer suite) over
one all-or-nothing command spanning the entire experiment queue.

Before running:

1. identify the RQ and missing comparison in `EXPERIMENT_MATRIX.md`;
2. define a unique output directory and seed;
3. freeze all dataset/model/retrieval/training flags;
4. confirm the comparison changes only the intended factor.

During and after running:

1. write resumable artifacts outside Git;
2. commit metrics, config, predictions, and manifests where defined;
3. record the producing Git SHA;
4. update `RESULT_REGISTRY.md` only after validation;
5. update the affected canonical table in `paper/results/MAIN_RESULTS.md`;
6. update `LAB_LOG.md` with the result and its claim limit;
7. move superseded eval runs out of the active scanner into a dated archive.

### 6.2 Paper resource-measurement contract

Accuracy and resource eligibility are separate. A run on a shared server may
provide valid checkpoints and predictions while providing non-comparable wall
time, throughput, or memory pressure.

For a number to enter a paper resource table:

- use a fresh, non-resumed measurement on an otherwise idle selected GPU;
- record the exact GPU, runtime versions, precision, batch size, sequence
  length, warm-up, measured scope, and repetition count;
- synchronize the accelerator at timing boundaries;
- repeat the fixed recipe at least three times and report median plus
  dispersion;
- report process peak RSS separately from system RAM;
- label PyTorch allocated and reserved VRAM separately and never present either
  as total device VRAM;
- exclude resumed eval timing and round wall time assembled from reused stages;
- keep offline one-time teacher/cache cost separate from recurring client,
  server-round, and deployment inference cost.

`paper_timing_eligible=true` in a result means the code observed a fresh,
non-reused measurement path. It is necessary but not sufficient: the run log
must also confirm exclusive hardware. Communication bytes are artifact-derived
and do not require an exclusive machine.

## 7. Result retention

Keep a result active when it directly supports a current table, claim,
baseline, robustness result, replication, or open decision.

Archive a result when it is:

- tied to a retired method such as ICL, FLoRA-NA, or SC;
- an early PoC replaced by a stricter/full run;
- a duplicate, invalid, mismatched, or superseded control;
- no longer consumed by current analysis or documentation.

Archive means Git move plus an index, never silent deletion. Training and
federated result records referenced by artifact manifests remain in place even
when their method branch is closed; breaking manifest provenance is worse than
directory clutter.

## 8. Statistical reporting

- Report seed count explicitly.
- Use paired tests on identical evaluation rows.
- Do not convert a single-seed paired-question significance test into an
  across-seed method claim.
- Report negative and null results when they determine architecture choices.
- Use EX and execution-error rate for pre/post-KD comparisons; EM may change
  because of SQL surface convention.
- Distinguish private-data-pass matching from total-compute matching.

## 9. Git discipline

- Use focused commits: archive, documentation, code, results, and generated
  artifacts should be separable.
- Never commit unrelated user changes opportunistically.
- Do not rewrite published run IDs or result history.
- Run `git diff --check` and relevant tests before committing.
- Keep both repository worktrees clean at handoff.
