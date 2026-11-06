# FedLS-SQL project convention

Every reported number must be traceable to a dataset, configuration,
checkpoint, prediction file and Git commit. The rest of this file is how the
two repositories are organized; the binding rules are the "Hard rules" in
`AGENTS.md`.

## 1. Repositories

- Outer repository: private paper material, references, notes, advisor files.
- `fedicl-sql/`: releasable code, processed data, committed metrics, configs,
  predictions, tests. Reference PDFs and private notes never go there.

## 2. Outer layout

```text
paper/
├── drafts/       manuscript drafts
├── notes/        RESEARCH_STATE, LAB_LOG, PIPELINE_NEXT (more only when needed)
├── references/   private source library
├── templates/    venue templates
```

Superseded material from both repositories lives in `archive/` at the
workspace root, local only and ignored by Git (`archive/README.md`).

## 3. Naming

- Paper name: FedLS-SQL. The code keeps `fedicl-sql` / `fedicl_sql`.
- Existing arm names, run IDs, artifact paths, cache IDs and fingerprints are
  immutable; presentation names may change.

## 4. Data

- Experiments read processed CSVs, never raw benchmark files; raw files are
  never modified.
- Every run declares its dataset profile (`spider`, `bird_with_evidence`,
  `bird_no_evidence`); a dataset is never inferred from a path. Protocol-v2
  outputs live under `artifacts/protocol_v2/`.
- Every derived split records seed, method, source and counts.
- A teacher-selected pool belongs to that teacher; a new teacher regenerates
  its own.

## 5. Commands

Server commands live in `paper/notes/PIPELINE_NEXT.md`: PowerShell, one
physical line per command (the owner copy-pastes over a remote session), run
from the `fedicl-sql/` root, define every variable they use, throw after any
non-zero exit, and resume by rerunning the same command. Results are committed afterwards by staging only compact files. When
a guard (fingerprint, lineage, cache identity) rejects a command, use the
original flags or a new output root; if the guard itself is wrong, fix it in
code with a test.

For a resource table in the paper, measure on fresh, non-resumed runs with no
other job on that GPU, repeat at least three times, and report the median;
keep one-time teacher or cache cost separate from recurring client and
inference cost.

## 6. Results

Keep a result where it is while a manifest refers to it; move results that
nothing uses any more to the local `archive/` folder with an index entry
(Git history keeps the committed copy). Never delete
silently.

## 7. Statistics

State the seed count. Use paired tests on identical evaluation rows; pooled
seeds use the question-clustered test. A single-seed paired test is not an
across-seed claim. State whether a comparison matches private data passes or
total compute.

## 8. Git

Separate commits for archive, docs, code and results where practical; never
commit unrelated user changes; never rewrite published run IDs or result
history; run `git diff --check` and the relevant tests before committing.
