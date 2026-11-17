# FedLS-SQL: lab log

Every run, result and decision since the clean reset of 2026-11-17, newest
on top. A result reported only in chat is logged as "not committed". The
log of the earlier setup is at the tag `archive/pre-reset-2026-11-17`.

## 2026-11-17: clean reset (owner)

Decision: the project is set up again from clean. The prompt of every
earlier adapter carried a sentence from the ICL project ("The examples
below show SQL patterns for reference..." with no example shown), most rows
were decoded with an unset repetition penalty of 1.1, and the code still
held the ICL fields and many dropped lines. Every earlier number is
reference only.

Owner's rulings of the day:

- The client stage follows CodeLutra's recipe (DPO with an SFT term on
  execution-labelled samples of the current model). Work starts with the
  client stages; the server stage and the teacher come after.
- No repetition penalty.
- Rounds and settings may be chosen on Spider test; the number is reported
  as chosen on Spider test.
- The prompt and the training recipe follow what widely used papers do.
  The `codes` prompt code leaves with the other dropped lines.
- The package is renamed `fedls_sql`.

Done:

- Worker stopped by the owner during `synvc_s0/sft_plain`; the last
  published result is `a428e174`.
- Tag `archive/pre-reset-2026-11-17` pushed in both repositories (code
  `aa17258c`, workspace `9ef705b`); both trees copied to
  `archive/reset_2026-11-17/` with an overview note and the code review.
- Code repository `7d9aab8d`: committed results, audits and the old queue
  removed from `main`; the queue holds the worker selftest only.
- A read-only review of the code found, besides the three known defects:
  the chat template adds Qwen's default system message (training and
  evaluation agree; no note had it), the prompt identity hashed a
  placeholder and not the rendered schema, the sampling seed of a question
  did not change between rounds, the default model of four entry points was
  the non-Coder Qwen2.5-1.5B, the SFT runner defaulted to a 2,560-token
  limit that cuts the start of the prompt, evaluation and DPO labels
  extracted SQL with two different functions, and the training target
  ended with a newline after the end token.

CodeLutra, read again in the paper (arXiv 2411.05199v3): it starts from
the base model with no SFT stage; its SFT model is a separate baseline
(1 epoch, lr 5e-5). Iteration 1 equals that baseline on Spider (67.8
against 67.9) and the gain comes in iterations 2 and 3 (72.4, 76.6). Its
prompt is zero-shot with the `CREATE TABLE` text of the SQLite file; the
template is not printed and no code is published. It names no repetition
penalty and evaluates one sample at T 0.2.

Prompt and training practice of ten works: `LITERATURE.md`, section 1.19.
Most add a few database values to `CREATE TABLE` text; the student's own
report uses `CREATE TABLE` plus 3 example rows per table after Chang and
Fosler-Lussier (2023).

Open, for the owner: the prompt (three candidates in `RESEARCH_STATE.md`,
section 4), then the settings of stage 3.
