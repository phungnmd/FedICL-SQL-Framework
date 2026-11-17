# FedLS-SQL: lab log

Every run, result and decision since the clean reset of 2026-11-17, newest
on top. A result reported only in chat is logged as "not committed". The
log of the earlier setup is at the tag `archive/pre-reset-2026-11-17`.

## 2026-11-17: the prompt, two schema styles (code `3d05fa33`)

Owner: implement candidates A and B, with the SQLite sentence, no
repetition penalty and a length limit that fits.

In the code:

- One layout, taken from the Qwen2.5-Coder evaluation code: schema text,
  `-- Using valid SQLite, answer the following questions for the tables
  provided above.`, `Question: ...`, "Please output only the final SQL
  query, starts with keyword `SELECT`." One user message through the chat
  template.
- `--schema-style ddl_rows` (A, default): `CREATE TABLE` text and 3 example
  rows per table. `ddl_values` (B): `CREATE TABLE` text rebuilt per column
  with 2 example values as a comment (OmniSQL's schema text; no column
  descriptions, no question-matched values). `ddl`: no rows.
- Decoding greedy, penalty 1.0, 256 new tokens. `--max-len 7168`, policy
  `error`.
- One `extract_sql` for evaluation and DPO labels; target = gold SQL
  without a final `;` plus the end token; the prompt identity hashes a
  rendered prompt and is in the evaluation, sample and stage fingerprints;
  the sampling seed is derived per round and client.

Token lengths with the student's tokenizer (Mac, whole sets):

| Style | Spider train, sequence p50 / p99 / max | Spider test, prompt max |
|---|---|---:|
| `ddl_rows` | 821 / 3,863 / 6,927 | 2,547 |
| `ddl_values` | 620 / 3,129 / 6,440 | 1,939 |
| `ddl` | 480 / 1,653 / 2,334 | 1,086 |

No row exceeds 7,168. The longest database is `baseball_1`. BIRD is not
measured (its databases are not on the Mac).

Smoke on the Mac, not a result: the base model, HF, 40 random Spider test
rows, greedy. `ddl_rows` 25/40, `ddl_values` 27/40; every output ended at
the end token and was plain SQL with no code fence. 421 tests pass.

Queued: the base model on all of Spider test with A and B (`prompt/*`,
vLLM `inproc`).

Not done: the SFT shuffle seed per client and round, LoRA dropout and
weight decay set on purpose, a key check when an adapter is loaded.

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
section 4), then the settings of stage 3. (Prompt: see the entry above.)
