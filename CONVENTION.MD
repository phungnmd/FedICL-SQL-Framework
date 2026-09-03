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
| What paper work remains and in what order? | `paper/notes/PAPER_TODO.md` |
| Which metric appears in the paper? | `paper/results/MAIN_RESULTS.md` |
| Which checkpoint/result label is canonical? | `paper/notes/RESULT_REGISTRY.md` |
| Which RQ still lacks evidence? | `paper/notes/EXPERIMENT_MATRIX.md` |
| What novelty/claim boundary is defensible? | `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md` |
| How is the manuscript mapped to evidence? | `paper/notes/MANUSCRIPT_SKELETON.md` |
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
- Every new run declares an explicit dataset profile. `spider` has no evidence;
  `bird_with_evidence` renders provided evidence; `bird_no_evidence` is an
  ablation; `legacy` is protocol-v1 compatibility and is prohibited for new
  paper runs.
- Private/client, public/server, and evaluation dataset roles are configured
  independently. Dataset names must never be inferred from a path.
- Dataset release, role, evidence mode, prompt/schema policy, evaluator, and
  source hashes belong in every protocol-v2 setup fingerprint.
- Protocol-v2 outputs use `artifacts/protocol_v2/`. Cleanup never authorizes
  reusing a protocol-v1 root.
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

Every newly activated task must also include a separate **publication command**
immediately after its run command. The publication command is operator-invoked
only after the run's completion checks pass and must:

- target PowerShell and occupy one physical line in its own `powershell` block;
- verify that no files are already staged, then add only an explicit allowlist
  of compact result/config/metrics/prediction/manifest/provenance files;
- never add `artifacts/`, adapters, model weights, resume caches, trainer state,
  telemetry scratch data, or an entire result parent directory by wildcard;
- resolve timestamped output directories through the task's config,
  fingerprint, or exact printed path, never by an unchecked “newest folder”;
- verify the staged path set before committing, use a task-specific commit
  message, fail after a non-zero commit, and run `git push` only after the
  commit succeeds;
- remain separate from the long-running command so resuming computation never
  implicitly commits or pushes partial output.

If a producer cannot expose a deterministic result path, improve the producer
or provide a fingerprint-checked resolver before activating the task. A
publication command may push only the releasable `fedicl-sql/` result commit;
paper-document updates remain a separate outer-repository commit after local
validation.

On a shared experiment server, unrelated tracked processed-data edits may
coexist with a valid run. A run preflight may therefore require a clean
**scientific scope** instead of a globally clean worktree, but it must enumerate
that scope explicitly: imported code/package directories, dependency locks,
the exact split/audit files, and every training/evaluation input. Untracked
datasets and caches outside that scope are preserved and ignored. A dirty file
inside the declared scope remains a hard failure. Evaluation commands must
include their centralized train/test inputs in the scoped check even when the
preceding training command did not use them.

Once a long-running experiment starts, do not pull, checkout, commit, or edit
its code worktree until the process exits. Some artifacts resolve `git_sha` at
finalization rather than process launch, so a mid-run worktree change can make
the recorded SHA newer than the code already loaded in memory. Use a separate
worktree for concurrent development.

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

Every new federated command must state its aggregation protocol explicitly.
Matched accuracy, ablation, seed, FedProx, and non-IID runs use
`--aggregation-protocol plaintext`. Use `--aggregation-protocol secure_sum`
only for a separately labeled Secure Sum compatibility/overhead audit; do not
mix it into an accuracy lineage or imply that historical plaintext results were
cryptographically produced.

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

- use fresh, non-resumed repetitions on one selected GPU; the operator chooses
  a window with no intentionally concurrent GPU workload;
- treat repetitions as independent measurements and retain raw device
  utilization, memory, clock, and pstate telemetry without PID enumeration;
- record the exact GPU, runtime versions, precision, batch size, sequence
  length, warm-up, measured scope, and repetition count;
- synchronize the accelerator at timing boundaries;
- run at least five fixed repetitions, require at least three fresh successful
  repetitions for the primary latency summary, and report median plus
  dispersion;
- report process peak RSS separately from system RAM;
- label PyTorch allocated and reserved VRAM separately and never present either
  as total device VRAM;
- exclude resumed eval timing and round wall time assembled from reused stages;
- keep offline one-time teacher/cache cost separate from recurring client,
  server-round, and deployment inference cost.

`paper_timing_eligible=true` in a result means the code observed enough fresh,
successful, non-resumed repetitions. It does not prove scheduler-level
hardware exclusivity: quiet-window selection is an operator-controlled part of
the protocol, and GPU telemetry is descriptive rather than an automatic
exclusion rule. If fewer than three eligible repetitions are available,
latency is observational only. Communication bytes are artifact-derived and
do not depend on timing conditions.

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

Server-only retirement is dry-run first and quarantine-only on apply. Manifests
must contain exact repository-relative roots; wildcard or default deletion is
forbidden.

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
