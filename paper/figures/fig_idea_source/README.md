# Source of the example in Fig. 1 (`fig_idea`)

The question, gold SQL and samples drawn in `fig_idea.svg` come from one
local run, 2026-11-28, code repository at `4a962ced`:

    cd fedicl-sql
    uv run python ../paper/figures/fig_idea_source/fig1_samples.py out.jsonl

- Model: pretrained Qwen2.5-Coder-1.5B-Instruct (no adapter), MPS on the Mac.
- Question: Spider train `train:2053`, client 1 of `alpha_0.1/k5`,
  database `party_people`; prompt `ddl_rows`, as in the Spider rounds.
- Sampling as in the preference rounds: 10 samples, temperature 1.0,
  top_p 1.0, 256 new tokens, no repetition penalty; seed 8 (the index of
  the question in the script's list).
- Labels from `label_question` with the Spider evaluator: 7 correct,
  1 wrong result, 2 execution errors. The figure shows one of each, SQL
  verbatim (line breaks added).
- Results drawn: gold and SQL 1 return `Ebenezer Ako-Adjei (MP)`, SQL 2
  returns `Dr. Kwame Nkrumah (MP)`, SQL 3 fails with
  `no such column: T2.Partition_ID`.

`fig1_samples.jsonl` holds the labelled samples of all 16 questions the
script drew.
