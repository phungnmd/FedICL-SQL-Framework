# FedLS-SQL: what the paper claims

Approved by the owner on 2026-11-26, with the decisions of section 7.
Every brief is built from this file: a section may say less than a
claim's ceiling, in its own words, and never more. Values are those of
`generated/numbers.md` (one training seed); a claim whose rows are not
committed is marked "waits" and gets its values when the rows are in.

## 1. Thesis

In federated Text-to-SQL a client holds two things, questions with gold
SQL and the databases to run SQL on; FedAvg SFT learns from the first
alone, and FedLS-SQL also learns from the second, by running the model's
own queries at the client and training on which of them return the gold
result.

## 2. Contributions

1. A source of supervision. The paper points out that a client's
   databases are supervision that federated fine-tuning leaves unused:
   execution turns the one gold SQL of a question into many right and
   wrong queries of the model's own, and this can be done only at the
   client. To our knowledge it is the first federated Text-to-SQL
   training method that uses it.
2. The method. FedLS-SQL: warm-up rounds of FedAvg SFT, then preference
   rounds in which each client samples queries from the current global
   model, labels them by execution, pairs right with wrong ones and
   trains with a DPO term plus an NLL term. A federated round is one
   re-sampling step, and the round's global model is the reference of
   the DPO term. Only the adapter and the count that weights it (the
   number of pairs) leave a client, as the adapter and the number of
   questions do in FedAvg SFT.
3. The evidence. On BIRD dev and Spider test, at the same number of
   rounds, the model is 6.19 and 3.49 EX points above FedAvg SFT, and
   further FedAvg SFT rounds do not close the gap. The paper shows where
   the gain comes from (execution errors fall by half; more answers are
   right with other tables or columns than the gold SQL's), what each
   part adds, and what a client pays in compute.
4. The release: code, client splits, and the predictions of every row.

## 3. Claims

Macro arguments are `{set}{line}{round}`; lines: `fedavg` FedAvg SFT,
`k2` the method, `fixed` pairs and reference of the first preference
round, `rft` without the preference term, `feddpo` without the NLL term,
`k0` and `k3` no and three warm-up rounds. p is the exact McNemar p.

### A. Against FedAvg SFT (RQ1; Table 3, Fig. 2)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| A1 | At 4 rounds the method is above FedAvg SFT | BIRD dev `\ex{bird}{k2}{4}` 48.76 against `\ex{bird}{fedavg}{4}` 42.57: `\gain{bird}{fedavg}{4}{k2}{4}` +6.19, `\nfix` 153 questions against `\nbrk` 58, `\pval` 4.6e-11. Spider test 78.20 against 74.71: `\gain{spider}{fedavg}{4}{k2}{4}` +3.49, p 6.4e-7 | BIRD dev, Spider test | "above FedAvg SFT at the same number of rounds on both datasets", significant after correction. The headline number is the BIRD gain |
| A2 | More FedAvg SFT rounds do not reach it | BIRD: FedAvg SFT is highest at round 3 (43.68); the method is `\gain{bird}{fedavg}{3}{k2}{4}` +5.08 above that (p 4.9e-8). Spider: FedAvg SFT is 74.71 at rounds 3 and 4 and 73.92 at round 5; the method is `\gain{spider}{fedavg}{5}{k2}{4}` +4.28 above round 5 | BIRD dev (4 rounds), Spider test (5 rounds) | "FedAvg SFT stops improving after round 3 on both datasets." Its falls (BIRD round 4 -1.11, p 0.068; Spider round 5 -0.79, p 0.082) are not significant: not "degrades", not "has converged" |
| A3 | The gain is on every difficulty level | BIRD simple / moderate / challenging `\lvl{bird}{k2}{4}{...}` 56.00 / 39.66 / 31.72 against 51.35 / 29.96 / 26.90. Spider easy / medium / hard / extra 91.91 / 81.91 / 71.06 / 60.50 against 90.64 / 78.18 / 66.74 / 55.74 | BIRD dev, Spider test | "higher on every level; largest on the moderate questions of BIRD and the extra-hard of Spider." No test per level |
| A4 | One preference round adds more than a further SFT round from the same model | From FedAvg SFT round 2: BIRD `\gain{bird}{fedavg}{2}{k2}{3}` +3.52 (p 2.9e-4) against `\gain{bird}{fedavg}{2}{fedavg}{3}` +0.98 (p 0.11); Spider +3.36 (p 1.4e-6) against +0.61 (p 0.25) | BIRD dev, Spider test | as stated |
| A5 | Against centralized SFT | Spider: centralized SFT 75.03, level with FedAvg SFT (`\gain{spider}{fedavg}{4}{central}{3}` +0.32, p 0.69); the method is 3.17 above it | Spider test; BIRD waits | "above SFT on the pooled data" for Spider. The test of the method against centralized SFT is not yet in the generator |
| A6 | Against local SFT, FedProx SFT and federated DPO as published | waits (Table 3: both sets) | | no sentence until the rows are in |

### B. The parts (Table 8)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| B1 | Pairs sampled again each round, with the round's global model as reference, are better than the pairs and reference of the first preference round | BIRD at 4 rounds: `\ex{bird}{fixed}{4}` 46.15, `\gain{bird}{k2}{4}{fixed}{4}` -2.61, p 5.7e-4. Spider test: 78.02 against 78.20, p 0.78 | BIRD dev | Stated for BIRD. Never "on both datasets", never "essential". On Spider test the two are level |
| B2 | The second preference round still adds | BIRD `\gain{bird}{k2}{3}{k2}{4}` +2.54 (p 2.1e-4); Spider +0.74 (p 0.093) | BIRD dev | "On BIRD"; on Spider "a smaller, non-significant step" |
| B3 | The NLL term is needed | Spider at 3 rounds: without it `\ex{spider}{feddpo}{3}` 73.59, `\gain{spider}{k2}{3}{feddpo}{3}` -3.87 (p 7.6e-9), and below the model it started from (74.10) | Spider test, one preference round; BIRD waits | "Without the NLL term the preference round lowers accuracy" on Spider |
| B4 | The preference term removes execution errors that training on the model's correct samples alone leaves | At 3 rounds, without it: BIRD `\nerr{bird}{rft}{3}` 248 execution errors against `\nerr{bird}{k2}{3}` 102, EX `\gain{bird}{k2}{3}{rft}{3}` -1.83 (p 0.057); Spider 153 against 99, EX -1.59 (p 0.015) | BIRD dev, Spider test, one preference round; the 4-round rows wait | The error counts carry the claim. For EX: "lower on both datasets", not significant after correction |
| B5 | Warm-up rounds make the gain hold under test-suite accuracy | Spider test EX is level for 0, 2 and 3 warm-up rounds (78.02, 78.20, 77.97). Test-suite accuracy at 4 rounds (Table 6), no warm-up `\ts{...}{k0}{4}` / two warm-up rounds `\ts{...}{k2}{4}` / FedAvg SFT: Spider dev 67.21 / 70.41 / 67.99; Spider-Syn 51.35 / 55.51 / 51.84; Spider-Realistic 57.09 / 62.20 / 58.86. The method against itself without warm-up, `\tsgain{...}{k0}{4}{k2}{4}`: +3.20 (p 0.010), +4.16 (p 0.0014), +5.11 (p 0.0067) | Spider dev, Syn, Realistic; BIRD at equal rounds waits | No claim that warm-up raises EX: on these sets EX is level with and without it, and on Spider-DK, which has no test suite, EX is higher without it (67.10 against 63.55, p 0.032, printed in Table 6). "Without warm-up the method's EX gain does not carry over to test-suite accuracy; with two warm-up rounds it does." After correction the difference is significant on Spider-Syn |
| B6 | The weights of the server average do not matter | Weights by pairs, by questions, equal: BIRD within 0.20 (`\gain{bird}{k2}{3}{reagge}{3}`, `...{reaggq}{3}`), Spider within 0.52, none significant | BIRD dev, Spider test, at 3 rounds | one sentence |
| B7 | Clients pooled in the preference rounds | waits (Spider) | | |

### C. What changes in the answers (RQ4; Fig. 3)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| C1 | The preference rounds halve the execution errors | At 4 rounds, FedAvg SFT against the method: BIRD `\nerr{bird}{fedavg}{4}` 268 against `\nerr{bird}{k2}{4}` 128; Spider 173 against 84 | BIRD dev, Spider test | as stated |
| C2 | Queries that run and return a wrong result do not become fewer | BIRD `\nwr{bird}{fedavg}{4}` 613 against `\nwr{bird}{k2}{4}` 658; Spider 370 against 384 | BIRD dev, Spider test | The paper says this plainly. Never "fewer wrong results than FedAvg SFT". Inside the method the second preference round lowers them on BIRD (723 to 658) |
| C3 | The method finds right answers that are not written like the gold SQL, and FedAvg SFT does not | Right answers that read other tables or columns than the gold SQL: BIRD, FedAvg SFT 136, 135, 136 at rounds 2, 3, 4, the method 174 at round 3 and 191 at round 4; Spider test at 4 rounds 83 against 103 (83 without training). Right answers on the gold SQL's tables and columns at 4 rounds: BIRD 517 against 557, Spider 1,521 against 1,576 | BIRD dev, Spider test | Macros `\fact{form.<set>.<line>.<round>.other_right}` and `.gold_right` (with `.other`, `.gold` for the group sizes), from the committed predictions. On BIRD 55 of the 95 questions of net gain, on Spider 20 of 75: "a large part of the gain on BIRD", never "the gain sits there". A prediction that does not parse counts with the others |

### D. Breadth (RQ2, RQ3; Tables 4, 5, 6)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| D1 | A smaller model | Qwen2.5-Coder-0.5B: `\ex[qwen05]{spider}{k2}{4}` 66.19 against 64.09, `\gain[qwen05]{spider}{fedavg}{4}{k2}{4}` +2.10, p 0.0056 | Spider test | "also above FedAvg SFT, by a smaller margin", significant |
| D2 | A model of another family (DeepSeek-Coder-1.3B) | waits (Spider rounds, all of BIRD) | | |
| D3 | Other federated setups (IID, alpha 0.5 with 5 and with 10 clients) | waits | | until then the paper has two setups, both at alpha 0.1 with 5 clients |
| D4 | The gain holds on perturbed questions and under test-suite accuracy | EX gain at 4 rounds: Spider dev `\gain{spiderdev}{fedavg}{4}{k2}{4}` +2.51 (p 0.021), Syn +3.87 (p 6.3e-4), Realistic +2.75 (p 0.10), DK +3.92 (p 0.017). Test-suite accuracy: dev `\tsgain{spiderdev}{fedavg}{4}{k2}{4}` +2.42 (p 0.027), Syn +3.67 (p 4.2e-4), Realistic +3.34 (p 0.036) | Spider dev, Syn, Realistic, DK | "Above FedAvg SFT on all four sets and under both metrics"; significant after correction on Spider-Syn only. Not "robust": both models lose about 15 points from Spider dev to Spider-Syn |

### E. Cost (Table 7)

| # | Claim | Values and macros | Ceiling |
|---|---|---|---|
| E1 | No added communication | The same adapter in every round of either kind: `\fact{cost.bird.adapter_mb}` 73.9 MB per client per round. Samples, labels and pairs stay at the client | as stated |
| E2 | The cost is client compute | Minutes for the five clients of a round on one RTX A5000. BIRD: a FedAvg SFT round `\fact{cost.bird.sft.train_min}` 173; the preference rounds 28 + 159 + 283 = 470 and 28 + 168 + 195 = 391 (sampling, labels, training). Spider: 124; 18 + 3 + 182 = 203 and 19 + 3 + 88 = 109. Pairs fall from the first preference round to the second (BIRD 11,754 to 7,066; Spider 8,026 to 3,354) | "A preference round costs a client about 2.3 to 2.7 times an SFT round on BIRD and 0.9 to 1.6 times on Spider." The times are the five clients one after another on one card, not the wall-clock time of a federation. A2 is the answer to "FedAvg SFT with the same compute" |

## 4. Wording that has to survive revision

1. The label needs the gold SQL: a sampled query is correct when its
   result equals the result of the gold SQL on the client's database.
   Never "without gold SQL", "unlabelled", "self-supervised", or
   "execution shows whether an answer is right".
2. One training seed. Significance is the exact McNemar test on paired
   predictions with Holm correction inside each table. (When the second seed of the two
   main BIRD rows is in, its two rows are added to Table 3.)
3. BIRD numbers are on BIRD dev; its test set is not public. No number
   is called held-out, on either dataset.
4. B1 and B2 are stated for BIRD.
5. No EX gain is claimed for the warm-up rounds, and none for the
   weights of the average.
6. C2: wrong results do not fall against FedAvg SFT.
7. "To our knowledge" on the first contribution, and its scope is
   federated training for Text-to-SQL. FL4SP is the earlier federated
   Text-to-SQL work (SFT). Verifier-driven federated training exists
   for math and code, federated DPO for human preferences (OpenFedLLM),
   and the same sample, label and DPO + NLL loop centrally (CodeLutra):
   the paper says so, and says that its sampling and loss settings
   follow CodeLutra.
8. Privacy is that data stay at the client. No claim about differential
   privacy or about what an adapter reveals.
9. No "state of the art". Every comparison is inside one setup: the
   same model, prompt, decoding and rounds.
10. "Federated Text-to-SQL" means federated training of the model, said
    once in the introduction.
11. The cost figures are sums over five clients run on one card.

## 5. Limitations the paper states (Discussion)

1. A client needs gold SQL for its questions and databases it can
   query; the method does not use unlabelled questions.
2. Five clients (ten in one setup) that all take part in every round.
   Partial participation and many clients are not studied.
3. Data isolation, not differential privacy.
4. More client compute per round (E2).
5. A label is the match of results on one database: a wrong query can
   match by chance, and a question on a database without rows gives no
   pair. Test-suite accuracy on Spider is the check the paper has.
6. One training seed for most rows.
7. Models of 0.5 to 1.5 billion parameters with LoRA, on SQLite
   benchmarks in English.
8. The number of warm-up rounds is a setting; where FedAvg SFT is still
   improving fast (the 0.5B model) the gain is smaller.

## 6. Term sheet and notation

The terms and the notation of the paper are in `TERMS.md`. The owner
revised them on 2026-11-26 to the terms of the field: the labels are
"correct" and "incorrect", the two kinds of incorrect query are
"execution error" and "incorrect result", the model generates a query,
a client samples and executes. Sections 1 to 5 above keep the words
they were approved in; a brief states them in the terms of `TERMS.md`.

Lab words, which the paper never uses, and what stands for each:

| Lab word | Paper |
|---|---|
| student | the model |
| base student | the pretrained model |
| k2, FedPref | `\method` |
| fedavg, bird_sft | FedAvg SFT |
| SFT stage, k | warm-up rounds |
| DPO + NLL round | preference round |
| err, wr | execution error, incorrect result |
| I1 | on-policy pairs |
| feddpo | FedDPO |
| RFT | the method without the preference term |
| arm, line | a row of a table (no term) |
| bird, spider, syn, ... | the evaluation sets by name |

## 7. Decided (owner, 2026-11-26)

1. The Holm correction runs inside each table: the tests of a table
   answer one question and form one family. A test is counted once, in
   the first table that prints it, and the comparisons quoted only in
   the text form a family of their own. The Setup section states it.
2. Table 8 keeps a BIRD block and a Spider block until the BIRD rows of
   B3, B4 and B5 are read. B1 is worded for BIRD either way.
3. Table 6 has a row for the method without warm-up rounds and its test
   against the method, on every set of the table.
4. C3 is a result of the paper, written by `paper_numbers.py` from the
   committed predictions; the Results brief carries it in RQ4.
5. The names of section 6 stand: "warm-up round", "preference round",
   "FedDPO" for the published baseline. The labels and the verbs
   were revised the same day (`TERMS.md`).
6. The first contribution is worded as in section 2.
7. The second contribution names what leaves a client exactly: the
   adapter and the count that weights it.
8. The method constructs two pairs per question where CodeLutra
   constructs ten, and the paper gives the reason: the number of pairs
   sets the length of local training. No claim on accuracy at other
   numbers of pairs; none was run.
9. The numbers of questions that yield pairs and of pairs per round are
   columns of Table 7 (E2) and are read in Section 5.4, not in the
   Method section.
