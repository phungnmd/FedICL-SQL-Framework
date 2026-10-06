# Superseded branch update instructions

The owner confirmed the server was stopped and requested integration into main.
Use the active PIPELINE_NEXT.md command instead.

## 0. Existing server: remove counters and preserve prepared work

Code fix: nested `e15cc77`, compatibility helper `4b5eb8f`, published on
`origin/fix/p218-remove-counter`. Nested `origin/main` is deliberately untouched
while the current server cohort may still publish. The
[counter-based queue](../archive/superseded_runbooks/PIPELINE_0P5B_COUNTER_GUARD_2026-10-06.md)
is superseded.

Wait for GPU 1 to finish its baseline and reach the publication wait, or stop its
terminal with Ctrl+C to update immediately. GPU 0 has already exited on the
counter failure. Before updating, both training/evaluation processes must be
stopped; stop any waiting wrappers too, then restart the two lane commands in
step 3 afterward. Do not publish baselines before this update. Leave adapters,
`_ckpt`, `resume_latest`, manifests, and all untracked results in place.

Run once from the server repository on `main`, only when both lanes are idle:

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; uv run --no-sync python -c "from scripts.run_p218_student_schedule import idle_lanes; locks=idle_lanes(); locks.close()"; if ($LASTEXITCODE -ne 0) { throw 'A lane is still running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/fix/p218-remove-counter; if ($LASTEXITCODE -ne 0) { throw 'Update failed' }; uv run --no-sync python -m scripts.migrate_p218_counter_removal --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Prepared identity migration failed' }
```

The helper accepts only the exact counter-removal files, unchanged training
code/data/commands and successful existing probe reports. It preserves original
identities and measurements, then updates their compatibility identity. It does
not rerun probes, rebuild the teacher cache, or modify adapters/checkpoints.
A mismatch stops the migration without bypassing provenance checks. New clean
runs skip this one-time migration and use steps 1-2 normally.

Restart each terminal with its existing step-3 command. Finished clients and
rounds are reused; interrupted training resumes from its saved checkpoint.
Unsaved microsteps are recomputed. The server's later baseline publication push
will also integrate the counter-removal commits into `origin/main`.

