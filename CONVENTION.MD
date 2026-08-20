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

## 6. Experiment lifecycle

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
5. update `LAB_LOG.md` with the result and its claim limit;
6. move superseded eval runs out of the active scanner into a dated archive.

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
