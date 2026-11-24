# FedLS-SQL: lab log

Every run, result and decision since the clean reset of 2026-11-17, newest
on top. A result reported only in chat is logged as "not committed". The
log of the earlier setup is at the tag `archive/pre-reset-2026-11-17`.

## 2026-11-24: FedAvg SFT round 5 falls on test and dev: the baseline peaks at round 4 (results `d2f08bc3`, `1e6c9737`, `26af69db`; test-suite on the Mac `sft_r5_spider_dev`)

| Row (1.5B) | Spider test EX | Spider dev EX | Spider dev TS |
|---|---|---|---|
| FedAvg SFT round 4 | 74.71 | 75.15 | 67.99 |
| FedAvg SFT round 5 | 73.92 (-0.79, 34 / 51, p 0.082) | 74.18 (-0.97, 25 / 35, p 0.25) | 67.21 (-0.77) |
| Method, k = 2, 4 rounds | **78.20** (+4.29 over round 5, p 2.3e-09) | **77.66** (+3.48, 77 / 41, p 0.0012) | **70.41** (+3.19) |

- The rise on dev from round 3 to 4 (+1.94) does not go on: round 5
  is below round 4 on test, dev EX and dev TS. Execution errors on
  test 173 to 188. FedAvg SFT's best round is 4 on dev and 3 to 4 on
  test (74.71 at both); more rounds do not reach the method.
- Round 6 dropped (owner, 2026-11-24; queue `c6d9720b`): the cards go to the method rows.

## 2026-11-24: the FedAvg weights of a DPO round do not matter: pair counts kept (results `9f4d00bf`, `4f230532`, `7196832a`)

`reagg/*`: the client adapters of `dpo_k2/round_1` (Spider) and
`bird_k2/round_1` (BIRD) averaged again; the pair weights give the
rounds' own global adapters again (checked by hash). Read against them
(exact McNemar, session read of the committed predictions).

| Weights | Spider test | Spider dev | BIRD dev |
|---|---|---|---|
| Pairs (the rounds) | 77.46 | 75.05 | 46.22 |
| Questions | 77.78 (+0.33, 18 / 11, p 0.26) | 74.76 (-0.29, p 0.61) | 46.22 (10 / 10, p 1) |
| Equal | 76.94 (-0.51, 12 / 23, p 0.09) | 75.44 (+0.39, p 0.54) | 46.02 (-0.20, p 0.79) |

- Normalised weights, Spider: pairs 0.11 / 0.20 / 0.28 / 0.29 / 0.11,
  questions 0.10 / 0.18 / 0.23 / 0.40 / 0.08; BIRD: pairs 0.23 / 0.16 /
  0.23 / 0.07 / 0.30, questions 0.21 / 0.17 / 0.22 / 0.07 / 0.32.
- No weighting is separated from the pair counts on any set (all within
  0.51). The method keeps pair-count weights; the paper can state the
  weights and that question and equal weights give the same level.
- `pooled_k2/round_1` trained (8,024 pairs; `57d47c3d`); its evaluation
  waits behind the rows in file order.

## 2026-11-24: FedAvg SFT rounds 5 and 6 of the 1.5B queued (owner; queue `d6aa4ad7`)

On Spider dev FedAvg SFT round 4 gained 1.94 over round 3 (33 / 13,
p 0.0045) while Spider test stayed at 74.71. Rounds 5 and 6 say whether
the baseline reaches the method (77.66 dev, 78.20 test) with more
rounds. Commands: the step of the curve `fedavg_base_ddlrows_alpha01_s0/sft`
with k = 5, 6 (resolved and compared; only `--round`, `--stage` and
`--init-adapter` change); evaluated on Spider test and dev. After
`reagg/*`, before `bird_k2/round_2`.

Also read from the dev rows (same results as the entry below): the
second DPO + NLL round of k = 2 adds 2.61 on dev (42 / 15, p 0.0005;
test +0.74); at 3 rounds k = 2 is 1.84 above FedAvg SFT on dev (68 /
49, p 0.096). At 4 rounds the method is above FedAvg SFT by 5.2 on hard
and 10.3 on extra (easy and medium level); execution errors 52 against
80, wrong results 179 against 177.

## 2026-11-24: k on Spider dev at 4 rounds is 2 under EX and test-suite accuracy; DPO from the base student gains on dev through lucky SQL (results `68c38e28`, test-suite on the Mac `k_by_round_spider_dev`)

The rows by round on Spider dev (1,034), published by the server at
the end of `spider_dev/*`; test-suite accuracy scored on the Mac
(`audits/protocol_v2/test_suite/k_by_round_spider_dev`).

| Total rounds | FedAvg SFT EX / TS | k = 0 EX / TS | k = 2 EX / TS | k = 3 EX / TS |
|---|---|---|---|---|
| 1 | 71.18 / 63.73 | 77.85 / 65.96 | | |
| 2 | 72.73 / 65.76 | 77.76 / 66.83 | | |
| 3 | 73.21 / 66.15 | **80.08** / 69.25 | 75.05 / 68.47 | |
| 4 | 75.15 / 67.99 | 77.27 / 67.21 | **77.66** / **70.41** | 76.50 / 69.92 |

- At 4 rounds, the length of every line in the tables, k = 2 is the
  highest on both metrics: EX +0.39 over k = 0 (69 / 65, p 0.80) and
  +1.16 over k = 3 (47 / 35, p 0.22); TS +3.19 over k = 0 (95 / 62,
  p 0.010) and +0.48 over k = 3 (42 / 37, p 0.65). Against FedAvg SFT
  round 4: TS +2.42 (72 / 47, p 0.027). So "k is chosen on Spider dev
  from {0, 2, 3} at 4 rounds" is true and gives k = 2, the value
  already in use; the paper can say so.
- k = 0 leads on dev EX at 1 to 3 rounds (80.08 at 3 rounds, 5.03 above
  k = 2 at 3 rounds, p < 1e-4) but much less on TS (+0.77, p 0.58).
  Its EX-only rows (correct on the dev database, rejected by the suite)
  are 104 to 123 against 68 to 77 for FedAvg SFT, k = 2 and k = 3: DPO
  from the base student learns SQL that passes one database. With the
  SFT warm start the count stays at the FedAvg SFT level. A finding for
  the paper on why the warm start is part of the method.
- The dev EX of k = 0 moves by 2.8 between rounds 3 and 4 (80.08 to
  77.27); Spider test moves by 0.33 (77.69 to 78.02).

## 2026-11-24: strict labels on the databases with rows only are level with the reference (results `b5793e8e`, `6382f8d8`); the direction is closed

`strict_r/round_1` (owner started it after the read of `strict_d`):
one DPO + NLL round from FedAvg SFT round 2 on the stored round 1
samples, strict labels on 10 variants, no pair on a database without
rows. Read against `dpo_k2/round_1` from the committed predictions
(exact McNemar, session read).

| Row (1.5B, 3 rounds in all) | Spider test EX | Spider dev EX | Execution errors (test) | Wrong results (test) |
|---|---|---|---|---|
| `dpo_k2/round_1` (labels on the original database) | **77.46** | **75.05** | **99** | 385 |
| `strict_r/round_1` (strict labels, databases with rows only) | 77.27 | 74.95 | 136 | **352** |
| Difference | -0.19 (46 fixed, 50 broken, p 0.76) | -0.10 (35, 36, p 1) | | |

- Spider test by hardness, reference then the row: easy 91.49 /
  90.43, medium 80.63 / 79.93, hard 71.06 / 72.57, extra 59.66 /
  59.66. Spider dev: 89.11 / 89.52, 78.25 / 79.15, 64.37 / 64.94,
  56.63 / 52.41.
- Pairs 8,040 as counted beforehand (906 / 1,740 / 2,248 / 2,282 /
  864; client 4 at 28.4%).
- Reading: cleaner chosen sides alone move EX by nothing measurable;
  they trade execution errors for wrong results (+37, -33 on test).
  With `strict_d` (-1.40, p 0.0046), the loss there came from the pairs
  on the databases without rows or the weight they gave client 4. By
  the rule set before the run (level or below closes the direction),
  strict labels are not a part of the method.
- Test-suite accuracy on Spider dev (Mac, `test_suite/strict10_spider_dev`):
  68.96 against 68.47 (+0.48, 40 against 35 questions, not separated);
  EX-only rows 68 to 62. `strict_d`: 69.05 (+0.58).
- Why EX does not move: (1) the change is small: 9.24% of the correct
  samples on databases with rows turn wrong, about 16% of the chosen
  sides, and 69% of the pairs equal the reference's; (2) a lucky SQL
  is also scored correct by EX on the one test database, so cleaner
  chosen sides can show only on the suite, where the gain is +0.5 and
  6 fewer EX-only rows; (3) the pair mix shifts: rejected sides with an
  execution error 4,087 to 3,303 (50.9% to 41.1%), wrong results 3,939
  to 4,737, and the test errors follow (99 to 136, wrong results 385
  to 352). The preference term's gain sits in execution errors (RFT,
  2026-11-18), so the pairs lost there cost about what the cleaner
  side brings.

## 2026-11-24: the trial row of the extension is 1.40 below its reference on Spider test (p 0.0046), level on dev (results `86c23233`, `0ee1ff52`, `ba607804`)

`strict_d/round_1` ran from about 01:57 to 05:16 (the owner stopped
`strict/round_1` and started it), evaluations published 05:27. One DPO
+ NLL round from FedAvg SFT round 2 on the stored round 1 samples,
strict labels on 10 variants, rule `differs` on the databases without
rows, against `dpo_k2/round_1` on the same samples.

| Row (1.5B, 3 rounds in all) | Spider test EX | Spider dev EX | Spider dev test-suite accuracy |
|---|---|---|---|
| `dpo_k2/round_1` (labels on the original database) | **77.46** | **75.05** | 68.47 |
| `strict_d/round_1` (strict labels, databases without rows paired) | 76.06 | 74.85 | **69.05** |
| Difference | -1.40 (38 fixed, 68 broken, p 0.0046) | -0.20 (33, 35, p 0.90) | +0.58 (41, 35, p 0.57) |

- Spider test by hardness, reference then the row: easy 91.49 / 89.79,
  medium 80.63 / 79.11, hard 71.06 / 70.19, extra 59.66 / 58.26.
  Execution errors 99 to 128 (`no such column` 54 to 76), wrong
  results 385 to 386. The broken answers read (8 of them): a join
  left out, or a column taken from the wrong table.
- Spider dev: rows correct on the dev database and wrong on the suite
  68 to 60. Test-suite accuracy scored on the Mac
  (`audits/protocol_v2/test_suite/strict10ed_spider_dev`).
- Pairs 9,464 as counted beforehand (906 / 1,740 / 2,362 / 3,592 /
  864; 1,424 on databases without rows: 114 at client 3, 1,310 at
  client 4). Client 4: weight 29.4% to 38.0%, update norm 2.09 to
  2.56, lowest cosine between two client updates 0.244 to 0.202.
- Time and memory: 3 h 19 min over the five clients, peak reserved
  18.92 GiB (client 3).
- Reading: the row changes three things at once (cleaner chosen sides,
  the new pairs, the weight of client 4), so it does not say which one
  costs the 1.40. By the rule of the method (a part is kept on a
  measured gain) the extension as run is not kept: no gain on test or
  dev EX, and the gain on the suite is not separated.
- Queued and not run (`strict_r`, queue `ba607804`): strict labels on
  the databases with rows only, about 8,040 pairs on the questions of
  the reference, client 4 at 28.4%; about 2.8 h (estimate). It says
  whether cleaner chosen sides alone help. Resolved round command:
  that of `dpo_k2/round_1` with `--out` and `--strict-variants 10
  --strict-variant-seed 0`; the prompts are those of the reference
  (no new question), so none was rendered again. Owner's decision.

## 2026-11-24: the trial row moves to the rule `differs` (phase `strict_d`, queue `240f7bba`)

Owner (about 01:55): `strict/round_1` is only a short way into
training, so stop it and run the more exact labels. Queued as its own
phase and root (`fedpref_sftr2_strict10ed_ddlrows_alpha01_s0`); the
root of the rule `rows` is not touched and continues from its
checkpoint if `--phase strict` is run again. One card and a few hours
hold one row: the rule `differs` is the one the method would keep
(9.96% of accepted labels wrong on the databases without rows against
17.2%).

- Resolved commands: `strict_d/round_1` differs from `strict/round_1`
  in `--out` and `--strict-empty-rule differs` only, and from
  `dpo_k2/round_1` in `--out` and the four strict flags; the relabel
  differs in `--dst`, the rule and the candidates file (the one of
  `e0ab0170`); the evaluations in arm name and adapter. The prompt
  path is that of `strict/round_1`, read then from token ids; the rule
  changes labels only, so no prompt was rendered again.
- Pairs, counted from the committed labels (2 per mixed question):
  906 / 1,740 / 2,362 / 3,592 / 864 by client, 9,464 in all (8,040 on
  databases with rows, 1,424 on the others); client 4 at 38.0% of the
  average (29.4% in `dpo_k2/round_1`).
- Not verified on the Mac: `strict_d/relabel` on the server's samples
  (they exist only there); the tests cover the relabel from a
  candidates file under the rule.

## 2026-11-24: rule `differs` against the suite, committed: 9.96% of accepted labels wrong (rule `rows` 17.2%); what the trial row trains on (results `e0ab0170`, `74df3af8`)

The label-noise run under `--empty-rule differs` ran on the server
beside `strict/round_1` (started 01:43:48, CPU only: variants reused
in 0.9 s, gold pass 15 s, verdicts 68 s; its own folder
`..._r1_b8ef182062ef43dd_differs`). It wrote nothing the round reads:
the round's labels were fixed by `strict/relabel` before training, the
variants were reused, and the rule `rows` keeps its identity under the
pulled code `37a90342`. The training time of the round is not read yet.

Against the official suite on the Mac
(`audits/protocol_v2/db_fuzz_probe/empty_vs_suite_r1_differs`; suite
databases counted by the same rule, 4,736 distinct candidates judged
by both):

| Labels on the databases without rows | Accepted | The suite rejects | Share | By samples | Agreement |
|---|---|---|---|---|---|
| Correct on the original (no rows), the 4,736 of the rule `differs` | 3,539 | 2,411 | 68.1% | 58.7% | |
| 10 variants, rule `rows` (`empty_vs_suite_r1`, 6,095 judged) | 1,880 | 323 | 17.2% | 15.9% | 90.4% |
| 10 variants, rule `differs` | 1,205 | 120 | **9.96%** | 12.4% | **96.3%** |

By database under `differs`: academic 5.5%, geo 11.2%, imdb 14.6%,
restaurants 7.7%, scholar 9.7%, yelp 13.2%; 55 candidates the variants
reject and the suite accepts (51 on `geo`). Questions with a variant
that counts: 1,239 (client 3: 102 of 111, client 4: 1,137 of 1,648);
with the label rule of training 712 of them are mixed (rule `rows`:
780 of 1,308).

What the trial row (rule `rows`) trains on against `dpo_k2/round_1`,
counted from the committed `candidates.csv` with the label rule of
training and 2 pairs per mixed question; the row's own
`client_*_pairs_stats.json` is not published yet:

| Client | Pairs, `dpo_k2/round_1` | Pairs, trial row | Of them on databases without rows | FedAvg weight |
|---|---|---|---|---|
| 1 | 914 | 906 | 0 | 11.4% to 9.4% |
| 2 | 1,642 | 1,740 | 0 | 20.5% to 18.1% |
| 3 | 2,248 | 2,372 | 124 | 28.0% to 24.7% |
| 4 | 2,356 | 3,718 | 1,436 | 29.4% to 38.7% |
| 5 | 866 | 864 | 0 | 10.8% to 9.0% |
| All | 8,026 | 9,600 (+19.6%) | 1,560 | |

- Databases with rows: 3,744 questions stay mixed, 2,772 of them with
  no label changed (the pair draw is seeded per question, so their
  5,544 pairs are those of the reference: 69% of its pairs, 58% of the
  row's) and 972 with a correct sample turned wrong (1,944 pairs drawn
  again); 276 questions come in from all correct (552 pairs), 269 go
  out to all wrong (538 pairs); 4,441 samples turn wrong.
- Databases without rows: 780 questions paired (1,560 pairs: 495 mixed
  on the original, 285 all correct there); 5,224 samples correct on
  the original turn wrong; 451 questions without a variant that counts
  and 528 all correct or all wrong stay without a pair.
- The row therefore differs from its reference in three ways at once:
  cleaner chosen sides, 1,560 new pairs, and client 4 at 38.7% of the
  average instead of 29.4%. The row with the databases with rows only
  separates the first from the two others.

## 2026-11-24: 15.9% of the chosen sides are lucky; on the databases without rows the variants cut wrong accepted labels from 59.5% to 17.2%, and a gold that counts leaves a hole (results `0a4a3102`, `7f951bde`, `60f40279`; code `37a90342`)

`strict/label_noise` ran on the server in 1 min 54 s (not the hour
estimated) and `strict/round_1` trains (owner, in chat, about 01:35).

Label noise of the round 1 samples of the k = 2 root, 10 variants
(`audits/protocol_v2/db_fuzz_probe/fedpref_sftr2_ddlrows_alpha01_s0_r1_b8ef182062ef43dd`):

| Databases with rows | 1 variant | 2 | 5 | 10 |
|---|---|---|---|---|
| Correct samples the variants reject (48,082) | 5.35% | 6.43% | 8.25% | 9.24% |
| The same in the mixed questions, mean over questions | 8.93% | 11.00% | 14.33% | **15.91%** |
| Mixed questions (4,013 on the original) | 4,041 | 4,058 | 4,026 | 4,020 |

- The mean over the mixed questions is the expected share of lucky
  chosen sides under random pairing: 15.91% at 10 variants, by client
  16.2 / 11.0 / 12.9 / 23.2 / 13.0%. The stop line of the direction was
  5%. The number of mixed questions hardly moves (276 gained from all
  correct, 269 lost to all wrong), so the pairs change in content, not
  in count.
- Databases without rows, 10 variants: 1,308 of 1,759 questions have a
  variant that counts; under the script's read (variants alone) 785
  are mixed, 178 all correct, 345 all wrong. Of the samples correct on
  the original 5,224 of 10,586 turn wrong.

The labels on the databases without rows against the official suite
databases of the same six schemas, same scorer and rule, on the Mac
(`scripts/db_fuzz_empty_vs_suite.py`,
`audits/protocol_v2/db_fuzz_probe/empty_vs_suite_r1`; 6,095 distinct
candidates judged by both):

| Label | Accepted | The suite rejects | Share |
|---|---|---|---|
| Correct on the original (no rows) | 4,470 | 2,660 | 59.5% |
| Accepted by the 10 variants | 1,880 | 323 | **17.2%** (15.9% by samples) |

Agreement 90.4%; 260 candidates the variants reject and the suite
accepts. A read of a sample of both kinds (scratch, not committed):
the suite accepts where the gold is a COUNT that returns 0 on every
suite database (a literal in another letter case then matches), and
the variants accept for the same reason where the gold counts 0 on
every variant. So "the gold returns rows" does not hold a gold that
counts: it returns one row on the database without rows too.

Rule `differs` (code `37a90342`; `--strict-empty-rule differs`,
`--empty-rule differs` of the two scripts; its own identity key, the
row in training keeps the rule `rows`): on a database without rows a
variant counts only where the gold result also differs from its result
on the original. Gold pass on the Mac
(`spider_train_alpha01_k5_gold_differs`): 1,239 of 1,759 questions
keep a variant that counts at 10 variants (1,308 under `rows`). The
committed comparison with the suite under this rule is in the entry
above (9.96% of accepted candidates the suite rejects); the scratch
read made here before it gave the same (10.0%, agreement 96.3%).

The row in training stands as the first read: its new pairs carry
about 18% of wrong chosen sides by the filtered suite, against 54 to
68% for labels on the original alone, and its pairs on the databases
with rows are cleaned from 15.9%.

## 2026-11-24: one trial row of the extension queued (phase `strict`, queue `e47906b1`)

Owner: one card is free for a few hours; which run gives a signal. One
row carries the whole extension, so one result says whether it moves
anything: DPO + NLL round 1 from FedAvg SFT round 2 on the stored
round 1 samples of the k = 2 root, relabelled with strict labels on 10
variants, databases without rows included
(`fedpref_sftr2_strict10e_ddlrows_alpha01_s0`), against
`dpo_k2/round_1` (77.46 on Spider test) on Spider test and dev; dev
also for test-suite accuracy on the Mac. The row with the databases
with rows only is not queued; it splits the two effects afterwards.

- Before queuing: the resolved round command differs from
  `dpo_k2/round_1` in `--out` and the three strict flags only; the
  resolved setup differs in `strict_labels` only and the reference
  resolves to its committed `setup.json`. One training example of a
  question on `restaurants` was decoded from its token ids and read:
  the prompt of the SFT stage, with the header of the example rows and
  no row under it.
- Memory: the added pairs are short (client 4, databases without rows:
  846 tokens at the median, 1,141 at most, against 2,948 for its
  databases with rows), so the 18.93 GiB peak of `dpo_k2/round_1` is
  expected to hold (`A5000_RUN_CONFIG.md`).
- Chosen on: nothing yet. The row is read on Spider test and on
  test-suite accuracy of Spider dev.

## 2026-11-24: strict labels reach the databases without rows (option of the rounds); the official suite as their reference (code `a1592b3b`..`de3193ca`)

Owner, 2026-11-24: go ahead with the second half of the extension. One
mechanism, two effects: a client's generated variants reject the
samples that match by accident, and give labels on its databases
without rows, which DPO skips today (1,759 questions, 1,648 of them at
client 4).

- Generator: unchanged, the fuzzer after Zhong, Yu and Klein (EMNLP
  2020, section 4). On a database without rows it has the schema and
  the literals of the client's gold SQL. That paper notes a sampled
  database "might be useful when occasional errors are tolerable (e.g.
  denotation based training)" and does not try it. No published work
  was found that fills such databases with a fixed program at the data
  owner (`LITERATURE.md`, section 1.21: Arctic-Text2SQL-R1 drops the
  Spider questions with an empty gold result and has an LLM write rows
  elsewhere; CoRE-DB has an LLM write a program per database).
- Rule (`--strict-empty-databases`, with `--strict-variants N`; off by
  default and absent from the identity when off): the rule of the
  databases with rows, with one difference: on a database without rows
  a variant counts only where the gold returns rows. A sample correct
  on the original stays correct only if every counted variant accepts
  it; a sample wrong on the original stays wrong. The pair step pairs
  a question that a variant labelled and skips the others as before
  (no counted variant: 451 of 1,759 at 10 variants; or no sample
  correct on the original). Full test suite: 596 passed, 2 skipped.
- Reference for those labels: the official test-suite release holds
  databases for six of the seven schemas (the classical datasets;
  `geography` for `geo`, none for `music_2`).
  `scripts/db_fuzz_empty_vs_suite.py` judges the same candidates on
  them with the same scorer and rule. Its gold pass ran on the Mac
  (`audits/protocol_v2/db_fuzz_probe/empty_vs_suite_gold`): the
  Spider gold returns rows on at least one suite database that counts
  for 1,122 of the 1,659 questions.

| Database | Questions | Suite databases | A suite database counts | A generated variant counts (10) |
|---|---|---|---|---|
| academic | 181 | 412 | 98.9% | 89.5% |
| geo | 564 | 109 | 69.1% | 97.2% |
| imdb | 109 | 201 | 95.4% | 44.0% |
| restaurants | 125 | 91 | 96.8% | 9.6% |
| scholar | 569 | 208 | 38.7% | 58.3% |
| yelp | 111 | 283 | 97.3% | 97.3% |
| music_2 | 100 | none | | 98.0% |

The suite stays a reference and does not enter the method: the client
generates its own content. Open, waiting for the server: the label
noise of the stored round 1 samples (step 5 of `PIPELINE_NEXT.md`,
which already writes the candidates of these databases), then the
comparison with the suite on the Mac (step 6), then the two trial rows.

## 2026-11-23: labels from the variants alone are cleaner than labels from the original database; the questions DPO skips sit on one client (results `40bf693d`)

Read from committed files on the Mac, no new SQL run.

Labels with the original database left out
(`scripts/db_fuzz_variant_only.py`,
`audits/protocol_v2/db_fuzz_probe/variant_only`): a prediction is
accepted when every usable one of the first N variants accepts it
(usable: the gold returns rows there and the order rule keeps it).
16,544 predictions on Spider dev (16 prediction files), three seeds.

| Variants | No usable variant | Wrong among accepted, variants only | Wrong among accepted, original only (same rows) | Agreement with the official suite |
|---|---|---|---|---|
| 1 | 15.9 to 19.8% | 7.6 to 9.1% | 10.4 to 10.8% | 94.1 to 95.0% |
| 2 | 8.3 to 11.1% | 5.1 to 5.5% | 10.7 to 11.4% | 96.4 to 96.8% |
| 5 | 3.5 to 4.0% | 2.2 to 3.1% | 11.2 to 11.4% | 98.1 to 98.6% |
| 10 | 2.0 to 2.7% | **1.8 to 2.1%** | 11.1 to 11.3% | **98.6 to 98.9%** |

Suite-correct predictions rejected: 16 or 17 at 10 variants. The dev
databases hold rows and the fuzzer draws its values from them; on a
database without rows it has only the literals of the gold SQL, so the
table is an upper bound for that case (on the training databases without
rows the gold returns rows on a variant for 53.26% of the cells and 451
of 1,759 questions have no usable variant, entry of the gold pass).

Where the skipped questions are (committed `pairs_stats` of
`fedpref_sftr2_ddlrows_alpha01_s0`, DPO round 1): the pair rule skips
every question on a database without rows, 1,759 of 8,659. Client 4
holds 1,648 of them out of its 3,479 questions (1,098 with mixed
samples), client 3 holds 111, the other three none. The round built
8,026 pairs from 4,013 questions.

CoRE-DB was read in its repository (`LITERATURE.md`, section 1.20a):
central build with the gold SQL of all databases and an external LLM;
the paper itself was not found.

## 2026-11-23: what the lucky SQL is: DPO on one-database labels raises joins written as a scalar subquery; strict labels are an option of the rounds (code `0157fda6`..`fc50995a`, results `c9c42696`)

Both done on the Mac by delegated agents while the server is off
(owner: the Mac work, without the draft); the counts below were
recounted here from `lucky_rows.csv`, the full test suite run here
(593 passed, 2 skipped).

Lucky predictions (EX-correct, rejected by the official suite) by the
kind of difference from the gold SQL, from a structural comparison
(`scripts/lucky_sql.py`, `audits/protocol_v2/test_suite/lucky_sql`):
2,049 over the six 1.5B rows on dev, Syn, Realistic and the ten 0.5B
rows on dev, 1,253 distinct (question, SQL) pairs. Of the distinct
pairs 55% differ in tables or joins, 15% in the GROUP BY key, 9% in a
filter, 8% in a set operation against boolean logic.

| Kind (1.5B, Spider dev, lucky rows) | No training | FedAvg SFT round 4 | k = 0 round 4 | k = 2 round 2 |
|---|---|---|---|---|
| Tables or joins, all | 72 | 28 | 60 | 35 |
| of them: a literal in place of a join | 31 | 10 | 8 | 6 |
| of them: a join written as a subquery | 15 | 7 | 43 | 16 |
| GROUP BY key | 18 | 17 | 14 | 12 |
| Set operation | 11 | 10 | 9 | 12 |
| Filter | 3 | 9 | 8 | 7 |
| All | 110 | 74 | 104 | 75 |

- DPO from the base student raises the join written as a subquery:
  15 to 43 on dev, 5 to 27 on Syn, 4 to 23 on Realistic; FedAvg SFT
  does not (7, 3, 7). On dev 24 of the 43 are `= (SELECT ...)`, which
  keeps one row where several match, and 18 are `IN (SELECT ...)`.
  k = 2 carries 16 on dev against 7 for FedAvg SFT, 13 of them
  `= (SELECT ...)`; the 0.5B goes from 6 at FedAvg SFT round 4 to 16
  at k = 2 round 2.
- DPO removes the literal in place of a join as well as SFT does (31
  to 8 against 31 to 10). Neither training lowers the set-operation
  kind; both raise the filter kind (3 to 8 or 9).
- Of the base student's 110 lucky questions on dev, FedAvg SFT turns 51
  test-suite correct and adds 27 new lucky ones; DPO from the base
  student turns 33 and adds 39. Same direction on Syn (44 and 33
  against 30 and 50) and Realistic (29 and 12 against 15 and 25).
- The lucky share of the EX-correct predictions rises with hardness:
  no training on dev 2.7% (easy) to 31.3% (extra), k = 2 0.9% to 17.3%.
- Limits: the kinds are differences in the SQL text, no prediction was
  run to show that the difference is what the suite rejects; primary
  kind read by hand on 80 predictions by the agent alone (79 the same).

Strict labels in the rounds (step 3 of the direction, code only):
`--strict-variants N` (`--strict-variant-seed`, default 0; 0 = off) on
the commands of `experiments/federated_pref/run.py`. A sample correct
on the original database stays correct only if it matches gold on the
first N variants of that client's database that count for the question
(the rule and the variant cache of `scripts/db_fuzz_label_noise.py`);
one a variant rejects becomes a wrong-result sample, so it can be the
rejected side of a pair and never the chosen one. Databases with rows
only: the seven without rows keep today's handling, so a gain reads as
label precision and not as new pairs. The setting is in `setup.json`
and in the sample identity only when on; a test checks that the
resolved setup of `fedpref_sftr2_ddlrows_alpha01_s0` is byte-identical
to its committed `setup.json`. `scripts/relabel_samples.py
--strict-variants N [--candidates <csv>]` makes stored samples strict
without sampling again (from the verdicts of the label-noise read, or
by running the variants); a test checks that the two ways and the
label step of a round give identical records. The pair counts of a
round record what the variants changed.
- Not exercised: sampling through vLLM followed by strict labels, DPO
  training and aggregation of a strict line, Windows, run time with 10
  variants on the five clients.
- Trial line (not queued; after the label-noise read, step 5 of
  `Run now`): `fedpref_sftr2_strict10_ddlrows_alpha01_s0`, round 1 from
  FedAvg SFT round 2 on the stored round 1 samples of
  `fedpref_sftr2_ddlrows_alpha01_s0` made strict, against
  `dpo_k2/round_1` (77.46 on Spider test), read on test-suite accuracy
  of Spider dev and on the join-as-subquery count.

## 2026-11-23: the generator on Spider dev with seeds 1 and 2: 86.6% to 89.2% of the lucky SQL caught at 10 variants; server off, sampling on the Mac not usable (results `7f9c72f2`)

The dev probe of the entry of step 1 below, run again on the Mac with
two more seeds (`audits/protocol_v2/db_fuzz_probe/spider_dev_s1`,
`_s2`). Lucky rows caught under the order rule, and rows accepted by
the official suite that the variants reject:

| Variants | Seed 0 | Seed 1 | Seed 2 | Rejected though accepted by the suite (seeds 0 / 1 / 2) |
|---|---|---|---|---|
| 1 | 41.39% | 53.06% | 45.78% | 15 / 11 / 15 |
| 2 | 57.37% | 67.47% | 66.23% | 16 / 11 / 16 |
| 5 | 84.52% | 83.77% | 83.69% | 16 / 16 / 16 |
| 10 | 87.83% | 86.59% | 89.16% | 16 / 16 / 17 |

- From 5 variants on the seed no longer matters (83.7% to 84.5% at 5,
  86.6% to 89.2% at 10); with 1 or 2 variants it does (41% to 53%).
- The rejections of seeds 1 and 2 under the rule were not read by hand
  (those of seed 0 were all SQL that differs from gold).

The owner switched the server off (2026-11-23, evening; for how long
is not known here). The label-noise read of the round 1 samples (step
5 of `Run now`), `pooled_k2`, the DeepSeek rounds and the queued
evaluations wait for it. A sampling read of the base 1.5B on the Mac
(`read --from-base --engine hf`, MPS, 8 questions per client) did not
finish its first batch of 2 prompts with 10 samples in 9.5 minutes and
was stopped; nothing of it is kept besides two near-empty folders
`artifacts/protocol_v2/macprobe_*` on the Mac. Only the 1.5B weights
are on the Mac.

## 2026-11-23: variants of the clients' training databases: the gold SQL runs on all of them; 451 of the 1,759 questions on databases without rows get no usable variant (code `a33f8cdd`, `4d156b0a`; results `c9f856dc`)

Step 2 of the direction below, the part that needs no samples (Mac,
CPU, by a delegated agent; full test suite run here, 580 passed).
`scripts/db_fuzz_label_noise.py` generates 10 variants per (client,
database), seeded with that client's own gold SQL only, and runs each
gold on them (`--gold-only`); with the stored samples of a round it
also judges every candidate labelled correct on the original database
on each variant. Output of the gold pass:
`audits/protocol_v2/db_fuzz_probe/spider_train_alpha01_k5_gold`.

| Databases | Questions | Gold result not empty on a variant (10 variants) | Cells left out by the order rule | Questions with no usable variant, 1 / 10 variants |
|---|---|---|---|---|
| With rows, 5 clients | 6,900 | 87.47% (clients: 90.6, 91.0, 83.9, 86.9, 86.8) | 9.07% | 611 / 173 (2.51%) |
| Without rows (yelp on client 3, six on client 4) | 1,759 | 53.26% | 1.93% | 955 / 451 (25.64%) |

- No gold SQL fails or times out on a variant (4,731 distinct gold SQL
  on 11 databases each). Generation 11 s for the 146 databases, the
  gold pass 5 s.
- Databases without rows: the questions left without a usable variant
  are restaurants 113 of 125, scholar 237 of 569, imdb 61 of 109,
  academic 19 of 181, geo 16 of 564, yelp 3 of 111, music_2 2 of 100.
  With no source rows the generated content seldom satisfies the joins
  and filters of those gold SQL. 1,308 of the 1,759 questions can be
  labelled on variants.
- On a database with rows a question with no usable variant keeps its
  label of the original database (173 questions at 10 variants).
- Not run: the verdicts on the samples (the label noise itself). The
  samples are on the server; the command is step 5 of `Run now` in
  `PIPELINE_NEXT.md`, on round 1 of the k = 2 line
  (`fedpref_sftr2_ddlrows_alpha01_s0`, samples `r1_b8ef182062ef43dd`,
  the key read from its `round.json`). Decision number: the mean over
  mixed questions of the share of correct samples that turn wrong
  (the expected share of noisy chosen sides under random pairs); stop
  under about 5%. The script was not run on Windows.

## 2026-11-23: stricter labels through database variants generated by the client: the generator catches 88% to 91% of the lucky SQL on Spider dev (owner: try; code `dcba7c13`..`f2f68f2a`, results `1cd6f5ff`)

Direction (owner, 2026-11-23): a sample that matches gold on the one
database by accident is labelled correct and DPO reinforces it. Each
client generates content variants of its own databases and a sample is
correct only if it matches gold on the original and on every variant.
The generator follows the fuzzer of Zhong, Yu and Klein (EMNLP 2020,
section 4 and the `fuzz/` folder of `ruiqi-zhong/TestSuiteEval`),
written anew (that repository states no licence), without their
distillation step. It is item 11 of `RESEARCH_STATE.md`, section 4, in
the form "label noise" instead of "more pairs".

What the committed predictions say about the noise (share of EX-correct
greedy predictions that the official suite rejects, 1.5B, Spider dev /
Syn / Realistic): no training 15.4% / 18.6% / 21.5%; FedAvg SFT round 4
9.5% / 12.3% / 13.1%; k = 0 round 4 13.0% / 17.3% / 19.9%; k = 2 round 2
9.3% / 11.8% / 11.7%. SFT on gold SQL removes lucky SQL, the DPO + NLL
rounds do not: k = 0 stays near the base student, k = 2 at the level of
its FedAvg SFT start (75 rows against 74 on dev). On the 0.5B the rounds
add some (68 rows at FedAvg SFT round 4, 85 at k = 2 round 2). After the
method 75 lucky rows are left on dev (7.3 points of test-suite
accuracy), 77 on Syn, 42 on Realistic: the room, not an expected gain.

Step 1, the generator measured on Spider dev (Mac, CPU, by a delegated
agent; headline numbers recomputed here from `per_row.csv`). Ten
variants for each of the 20 dev databases, seeded with the literals of
the dev gold SQL of that database, seed 0; the 16 committed dev
prediction files (six 1.5B rows, ten 0.5B rows) scored on the original
plus the first N variants. Lucky row: EX-correct and rejected by the
official suite (1,208 over the 16 files); 9,682 rows are accepted by
it. Output: `audits/protocol_v2/db_fuzz_probe/spider_dev`.

| Variants | Lucky rows caught, all variants | Lucky rows caught, order rule | Rows accepted by the suite and rejected by us, all / order rule | Gold result not empty on a variant |
|---|---|---|---|---|
| 1 | 43.71% | 41.39% | 15 / 15 | 88.0% |
| 2 | 60.84% | 57.37% | 23 / 16 | 88.2% |
| 5 | 87.09% | 84.52% | 35 / 16 | 90.2% |
| 10 | 90.89% | 87.83% | 50 / 16 | 89.5% |

- Stop line (under 50% at 10 variants): not met; the direction goes on.
- Order rule: a variant is left out for a question when the gold's
  ORDER BY has tied keys there (or its LIMIT cuts through a tie). The
  34 rejections it removes are all a gold `ORDER BY x DESC LIMIT 1`
  against a prediction `WHERE x = (SELECT max(x) ...)` on a variant
  with a tied maximum: correct SQL that would be labelled wrong. Cost:
  37 lucky rows no longer caught, 8% of the (question, variant) cells
  left out. The rule checks a top-level ORDER BY on a plain SELECT
  (229 of the 237 dev golds with ORDER BY).
- The 16 rejections left under the rule (5 questions) were read by the
  agent: SQL that differs from gold and that the official suite misses
  (`=` for a case-insensitive `LIKE`, a scalar subquery for a join on a
  name shared by several rows, a filter on the wrong column).
- Rows of the 1.5B on "original + 10 variants, order rule" against the
  official suite: no training 59.38 (58.32), centralized SFT 67.21
  (66.44), FedAvg SFT round 4 68.67 (67.99), k = 0 68.47 (67.21),
  fixed pairs 69.92 (69.44), k = 2 71.37 (70.41). Same order of the six
  rows.
- Two changes were made after the first scores, both recorded in
  `summary.json` with the numbers before them: double-quoted strings of
  the gold SQL are read as literals (sqlglot reads `"Aberdeen"` as a
  column; recall at 10 variants from 77.90% to 90.89%), and the order
  rule also flags a LIMIT that cuts through a tie.
- Cost: 6 s to generate the 200 variants, 499 s to score 4,959 distinct
  predictions on 11 databases each.
- Limits: one seed; variants are smaller than the official suite's
  databases (median 135 rows against 790); 36 of the 1,208 lucky rows
  are rejected by the official suite only where the gold's own ORDER BY
  is tied.

Next, each with a stop line: (2) variants for the training databases of
each client and the stored round 1 samples labelled again on them
(server, CPU): the share of "correct" samples that turn wrong; stop
under about 5% of the chosen sides. (3) one DPO + NLL round on the
strict labels against `dpo_k2/round_1`, read on test-suite accuracy of
dev; stop under 1 point. The stored samples are on the server only.

## 2026-11-23: test-suite accuracy of the six 1.5B rows on Spider dev, Syn, Realistic: the SFT warm-up shows here, k = 2 is 3.2 to 5.1 above k = 0 (results `c99b7bf4`)

Scored on the Mac from the committed predictions, committed under
`audits/protocol_v2/test_suite/qwen15b_spider_dev`, `_syn`,
`_realistic`. Each cell is EX / test-suite accuracy.

| Row (1.5B, 4 total rounds) | Spider dev (1,034) | Spider-Syn (1,034) | Spider-Realistic (508) |
|---|---|---|---|
| No training | 68.96 / 58.32 | 56.77 / 46.23 | 65.16 / 51.18 |
| FedAvg SFT round 4 | 75.15 / 67.99 | 59.09 / 51.84 | 67.72 / 58.86 |
| Centralized SFT epoch 2 | 73.02 / 66.44 | 60.83 / 53.09 | 67.13 / 58.86 |
| DPO + NLL from the base student (k = 0), round 4 | 77.27 / 67.21 | 62.09 / 51.35 | 71.26 / 57.09 |
| DPO + NLL from round 2 (k = 2), round 2 | 77.66 / 70.41 | 62.96 / 55.51 | 70.47 / 62.20 |
| Fixed pairs from round 2, round 2 | 76.21 / 69.44 | 60.74 / 54.06 | 70.67 / 61.22 |

- k = 2 against FedAvg SFT on the suite: +2.42 on dev (72 questions
  against 47, p 0.027), +3.68 on Syn (75 against 37, p 0.0004), +3.35
  on Realistic (38 against 21, p 0.036).
- k = 0 against FedAvg SFT on the suite: -0.77 (p 0.58), -0.48
  (p 0.76), -1.77 (p 0.40). Its gain on EX (+2.13, +3.00, +3.54) does
  not hold on the suite: 104, 111 and 72 of its rows are right on the
  one database only, against 75, 77 and 42 for k = 2.
- k = 2 against k = 0 on the suite: +3.19 on dev (95 against 62,
  p 0.010), +4.16 on Syn (109 against 66, p 0.0014), +5.12 on Realistic
  (56 against 30, p 0.0067). On EX the two are level (+0.39, +0.87,
  -0.79). This is the measured effect of the FedAvg SFT stage before
  the rounds on the 1.5B.
- k = 2 against fixed pairs on the suite: +0.97 (p 0.25), +1.45
  (p 0.082), +0.98 (p 0.47); same sign on the three sets, not
  separated on any.
- k = 2 against centralized SFT on the suite: +3.97 on dev (p 0.0011),
  +2.42 on Syn (p 0.057), +3.35 on Realistic (p 0.068).
- Spider-DK is not scored on the suite: 127 of its 535 rows use
  databases outside the 20 dev databases of the suite (the first is
  `new_concert_singer`), and `score_test_suite` stops on them. DK stays
  an EX column.
- These numbers equal the reading of 2026-11-21 that was not committed
  then.

## 2026-11-23: test-suite accuracy of the 0.5B rows on Spider dev: the method keeps 3.5 to 3.9 over FedAvg SFT (results `0ebd7daf`)

Scored on the Mac from the committed Spider dev predictions
(`scripts/score_test_suite.py`; correct on the original database and on
every suite database of the db_id), committed under
`audits/protocol_v2/test_suite/qwen05b_spider_dev`.

| Row (0.5B, Spider dev) | Total rounds | EX | Test-suite accuracy |
|---|---|---|---|
| No training | 0 | 55.22 | 47.78 |
| FedAvg SFT round 3 | 3 | 58.99 | 52.61 |
| FedAvg SFT round 4 | 4 | 59.77 | 53.19 |
| FedAvg SFT round 5 | 5 | 59.48 | 52.90 |
| FedAvg SFT round 6 | 6 | 59.28 | 53.09 |
| FedAvg SFT round 7 | 7 | 58.03 | 52.03 |
| DPO + NLL from round 2, round 1 | 3 | 63.35 | 56.09 |
| DPO + NLL from round 2, round 2 | 4 | 65.09 | 56.87 |
| DPO + NLL from round 4, round 1 | 5 | 63.15 | 56.09 |
| DPO + NLL from round 6, round 1 | 7 | 62.57 | 55.90 |

- Test-suite accuracy, the method against FedAvg SFT at equal rounds:
  +3.48 at 3 rounds (75 questions against 39, p 0.00096), +3.68 at 4
  (76 against 38, p 0.00048), +3.19 at 5 (from round 4, p 0.0061),
  +3.87 at 7 (from round 6, p 0.00017). Against FedAvg SFT round 6 the
  row at 4 rounds is 3.77 above (p 0.0010).
- The gain on EX (4.35 to 5.32) is larger than on the suite: part of
  it is SQL that returns the gold result on the one dev database only.
- The start does not matter on the suite either: after one DPO + NLL
  round 56.09, 56.09, 55.90 from rounds 2, 4, 6. The second round from
  round 2 adds 0.77 (34 against 26, p 0.37), not separated; on EX it
  added 1.74 (p 0.047).
- FedAvg SFT against no training: +5.42 on the suite (p 6.5e-05).

## 2026-11-23: the rows of the tables on Spider dev and on Syn, Realistic and DK queued (queue `e425fa42`)

Owner (chat): evaluate the rounds that are needed in full, on dev and
on the other Spider measures.

- Queued, evaluations only, after `pooled_k2` and before the DeepSeek
  rounds (about 2 h, estimate): the two ablation rounds of the 1.5B on
  Spider dev (no NLL term; NLL on the correct samples alone); the 1.5B
  rows by round on Syn, Realistic and DK (FedAvg SFT rounds 1 to 3,
  k = 0 rounds 1 to 3, k = 2 round 1, k = 3 round 1); the ten 0.5B rows
  on Syn, Realistic and DK; the pooled rounds on Spider dev.
- Queued after the DeepSeek rounds (about 1 h, estimate): the seven
  DeepSeek rows (no training, FedAvg SFT rounds 1 to 4, DPO + NLL
  rounds 1 and 2) on Spider dev and on the three other sets.
- Checked: 33 of the new commands are the row's Spider test evaluation
  with the set changed (`--sets spider`, or `--sets syn realistic dk`);
  the three FedAvg SFT rows of the 1.5B have no queued test command
  (the curve ran them) and follow `spider_variants/fedavg_r4`. Queue
  tests: 45 passed, 2 skipped.
- Test-suite accuracy needs no GPU: it is scored on the Mac from the
  committed dev, Syn and Realistic predictions
  (`scripts/score_test_suite.py`) and committed under
  `audits/protocol_v2/test_suite/`.
- Not queued: the dropped parts (nearest pairs, gold as the chosen
  side) on the other sets.

## 2026-11-23: the start of the DPO + NLL rounds on the dev sets; the 1.5B rows by round on Spider dev queued (queue `185d41cd`)

Owner (chat): read k on dev. What the committed rows hold, EX:

| Set | FedAvg SFT | k = 0 | k = 1 | k = 2 | Later start |
|---|---|---|---|---|---|
| Spider dev, 1.5B, 4 rounds | 75.15 | 77.27 | | 77.66 | k = 3 not evaluated on dev |
| Spider dev, 0.5B | 59.77 (round 4, its best) | not run | | 63.35 at 3 rounds, 65.09 at 4 | k = 4: 63.15 at 5 rounds; k = 6: 62.57 at 7 |
| BIRD dev, 1.5B | 43.68 (round 3, its best) | 43.02 at 2 rounds | 44.26 at 2 rounds | 46.22 at 3 rounds | |

- 1.5B on Spider dev: k = 2 is 2.51 above FedAvg SFT (72 questions
  against 46, p 0.021), k = 0 2.13 above (p 0.082), k = 2 against
  k = 0 +0.39 (p 0.80).
- On each dev set k = 2 is the highest row or level with it, and no
  later start is above it. The sets do not separate k = 0 from k = 2
  on the 1.5B Spider rows.
- Queued, evaluations only (about 25 min, estimate): FedAvg SFT rounds
  1 to 3, DPO + NLL rounds 1 to 3 from the base student, round 1 from
  FedAvg SFT round 2 and round 1 from round 3 (k = 3), all 1.5B on
  Spider dev. Each command is the row's Spider test evaluation with
  the set changed. Not run on any set: k = 0 on the 0.5B.
- Note for reading the result files: Spider dev and Spider-Syn both
  have 1,034 rows; a row's set is `test_csv` in its `config.json`.

## 2026-11-23: the 0.5B on Spider dev and from round 4: an early start is at least as good; the pair read from a BIRD-trained start (results `a4c114ec`, `d4ccba13`, `8a8974d2`, `12f109f0`, `5dffc203`)

Qwen2.5-Coder-0.5B, EX. Spider dev is the set on which no round or
setting was chosen; exact McNemar computed here from the committed
prediction files.

| Row | Total rounds | Spider test | Spider dev |
|---|---|---|---|
| No training | 0 | 54.40 | 55.22 |
| FedAvg SFT round 3 | 3 | 62.69 | 58.99 |
| FedAvg SFT round 4 | 4 | 64.09 | 59.77 |
| FedAvg SFT round 5 | 5 | 64.18 | 59.48 |
| FedAvg SFT round 6 | 6 | 64.56 | 59.28 |
| FedAvg SFT round 7 | 7 | 64.32 | 58.03 |
| DPO + NLL from round 2, round 1 | 3 | 65.86 | 63.35 |
| DPO + NLL from round 2, round 2 | 4 | 66.19 | 65.09 |
| DPO + NLL from round 4, round 1 | 5 | 65.49 | 63.15 |
| DPO + NLL from round 6, round 1 | 7 | 65.44 | 62.57 |

- `qwen05b_k4/round_1` on Spider test: 65.49, 1.40 above its start
  (132 questions against 102, p 0.058), 1.30 above FedAvg SFT at 5
  rounds (p 0.075), 0.37 below the round from round 2 (p 0.62).
- Spider dev, the method against FedAvg SFT at equal rounds: +4.35 at
  3 rounds (p 3.3e-05), +5.32 at 4 (91 against 36, p 1.1e-06), +3.68
  at 5 (from round 4, p 0.0015), +4.55 at 7 (from round 6, p 2.0e-05).
  Against the best FedAvg SFT round on dev (round 4, 59.77) the row
  from round 2 at 4 rounds is 5.32 above; against round 6, 5.80 (p
  6.1e-07).
- One DPO + NLL round over its start on dev: +3.38 from round 4 (p
  0.0028), +3.29 from round 6 (p 0.00099). On Spider test these were
  +1.40 and +0.88, so the small gain of a late start is a reading of
  Spider test, not of both sets.
- The level after one DPO + NLL round does not depend on the start:
  dev 63.35, 63.15, 62.57 and test 65.86, 65.49, 65.44 from rounds 2,
  4, 6 (no pair differs: p 0.92, 0.58 on dev). The second DPO + NLL
  round from round 2 adds 1.74 on dev (46 against 28, p 0.047) and 0.33
  on test (p 0.62); on dev it is 2.51 above the round from round 6 (p
  0.020).
- FedAvg SFT on dev does not rise after round 4 and round 7 is 1.74
  below it (p 0.085).
- Read: the start does not have to wait for FedAvg SFT to level off,
  and more SFT rounds before the DPO + NLL rounds buy nothing on either
  set. The threshold set in chat for a later start (67.2 on Spider
  test from round 4) is not met: k = 2 stands for the 0.5B.

`public_start/read` (1.5B, 10 samples at T 1.0 on the Spider clients,
`ddl_rows`), the start being FedAvg SFT round 3 on the BIRD clients:

| Start | Mixed questions | All correct | All wrong | Samples correct |
|---|---|---|---|---|
| Base student | 5,951 | 1,631 | 1,074 | 56.1% |
| FedAvg SFT round 3 on BIRD | 5,864 | 1,819 | 973 | 60.6% |
| FedAvg SFT round 2 on Spider | 5,192 | 2,891 | 573 | 71.4% |

- A start trained on BIRD samples on the Spider clients like the base
  student: about as many mixed questions and 101 fewer all-wrong ones.
  The SFT rounds on Spider halve the all-wrong questions. As a stand-in
  for a public stage in place of the SFT stage it gives no more pairs
  than no stage; a stage on top of the SFT rounds is not what it
  measures.

## 2026-11-23: gold-prefix probe on the 0.5B: a correct sample for 57% to 88% of the all-wrong questions, mostly the gold SQL (results `9fb6bb66`)

`prefix/probe`: the 1,168 all-wrong questions of `qwen05b_k2/round_2`
sampled again from the round 1 global adapter, 10 samples at T 1.0,
the input ending with the first part of the gold SQL tokens.

| Gold prefix | With a correct sample | Mixed | All correct | All wrong | Correct samples equal to the gold SQL | Sample accuracy |
|---|---|---|---|---|---|---|
| 0 (control, second draw) | 175 (15.0%) | 175 | 0 | 993 | 22.4% | 2.4% |
| 25% (12 tokens on average) | 666 (57.0%) | 375 | 291 | 502 | 61.2% | 40.9% |
| 50% | 895 (76.6%) | 332 | 563 | 273 | 66.6% | 65.0% |
| 75% | 1,027 (87.9%) | 274 | 753 | 141 | 76.2% | 80.0% |

- Against the control, question by question: at 25%, 530 questions get
  a correct sample only with the prefix and 39 only without it; at 50%
  737 and 17; at 75% 859 and 7.
- What it says: pairs can be made for these questions (the round's 10
  wrong samples as rejected, a prefix sample as chosen): 666 questions
  at 25%, next to 3,353 mixed questions in that round. What it does
  not say: whether training on them helps. The chosen side is the gold
  SQL in 61% to 76% of the correct samples (similarity to gold 0.96 to
  0.99), and gold as the chosen side was 2.61 below on BIRD (p 0.007),
  gold NLL rows for the all-wrong questions 0.65 below (p 0.43).
- The hint probe on BIRD (2026-11-21) gave fewer questions a correct
  sample (31.7% against 10.4% without the hint) but only 8.9% of its
  correct samples were the gold SQL.
- No decision. A training round with these pairs is not in code.
- The second card started at about 17:07 (the probe's timing file).

## 2026-11-23: the 0.5B rows on Spider dev queued (queue `2c62fbb2`)

Owner (chat): whether to read Spider dev. Queued here on that question,
not on a yes; the rows are evaluations only and can be taken out.

- `qwen05b_dev`: ten adapters of the 0.5B on Spider dev (1,034 rows):
  no training, FedAvg SFT rounds 3 to 7, DPO + NLL rounds 1 and 2 from
  round 2, round 1 from round 6, round 1 from round 4 (when its round
  is done). About 30 min (estimate). Before `pooled_k2` in the file.
- Why: rounds and settings were read on Spider test, and its numbers
  do not separate the starts of the DPO + NLL rounds (65.44, 65.86,
  66.19). Spider dev is a set on which nothing was chosen, and the set
  most papers at this size report.
- Checked: each command is the row's Spider test evaluation with the
  set changed (`--sets spider` for `--sets spider_test --allow-test`),
  as the `spider_dev` rows of the 1.5B. Queue tests: 45 passed, 2
  skipped.

## 2026-11-23: FedAvg SFT round 7 of the 0.5B is 64.32; a second card (results `b21754a0`, `94a7f115`)

- FedAvg SFT round 7 of Qwen2.5-Coder-0.5B on Spider test: 64.32, 0.23
  below round 6 (49 questions against 54, p 0.69). Rounds 4 to 7:
  64.09, 64.18, 64.56, 64.32.
- At 7 rounds the DPO + NLL round from round 6 (65.44) is 1.12 above
  it (108 against 84, p 0.097). The method from round 2 at 4 rounds
  (66.19) is 1.86 above round 7 (151 against 111, p 0.016).
- GPU 1 is free again (owner, chat, about 17:00): a second worker
  without `--phase` takes the probes and `pooled_k2` while the first
  card runs `qwen05b_k4/round_1`.

## 2026-11-23: reads that can change the method first; DPO + NLL with the clients pooled queued (queue `c92b0dd3`)

Owner (chat, about 16:25): yes to the order below.

- Order after `qwen05b_k4/round_1`: `prefix/probe`, `public_start/read`
  (1 h together, no training), the new `pooled_k2` rounds 1 and 2, then
  the pending DeepSeek rows. A row that depends on the method is run
  after these reads; rows that do not (FedAvg SFT of DeepSeek, FedProx,
  local-only) may fill the card at any time.
- `pooled_k2`: the two DPO + NLL rounds of `dpo_k2` (1.5B, from FedAvg
  SFT round 2, 74.10) with `--pooled --n-clients 1` on the centralized
  `train.csv`, so no aggregation. Read against 77.46 and 78.20. It
  separates two readings of the small second round (+0.74): the
  federation thins the client updates (pairwise cosine 0.013 to 0.055
  in DPO round 2), or the signal is used up after one round.
- The start is FedAvg SFT round 2, not centralized SFT: the runner
  takes a federated or a stage row as parent, and a row of
  `client_train` is refused (`stage_chain.resolve_parent`). The row
  from centralized SFT epoch 2, the reference of the paper's table,
  needs that change in code and is not queued.
- Checked before the push: resolved commands against `dpo_k2` differ in
  the split directory, `--pooled --n-clients 1` and the output root;
  the evaluations in the arm name and the adapter. The pooled setup
  reads 8,659 questions, as the five clients together, and the prompt
  of a row is the text of the same row in its client; one training
  sequence read from its token ids (1.5B tokenizer, 278 prompt tokens,
  target `SELECT count(*) FROM list<|im_end|>`). The samples are a new
  draw (the sampling seed is per round and client). Queue tests: 45
  passed, 2 skipped. Not checked: a run of the pooled round on the
  server; memory is expected as `dpo_k2` (peak reserved 18.93 GiB).

## 2026-11-23: on the 0.5B a DPO + NLL round from the levelled-off FedAvg SFT adds 0.88 (results `fc09dc79`, `ca57b242`)

- `qwen05b_k6/round_1`, one DPO + NLL round from FedAvg SFT round 6, on
  Spider test: 65.44 against its start 64.56, +0.88 (97 questions
  against 78, p 0.17). By hardness 84.47 / 70.25 / 50.32 / 48.46
  against 83.40 / 69.43 / 50.11 / 46.78. Predictions with an execution
  error 332 against 366, executable with a wrong result 410 against
  395 (counted here from the prediction files).
- Against the rows from FedAvg SFT round 2: 0.42 below DPO + NLL round
  1 (65.86, 3 rounds; p 0.61) and 0.75 below round 2 (66.19, 4 rounds;
  p 0.35). The later start reaches no higher level with 3 more rounds.
- The round's gain over its start by start round: +5.26 from round 2
  (p 1.9e-12), +0.88 from round 6. FedAvg SFT round 7, the row at equal
  rounds, is not read.
- The pairs are not what is short: 7,340 pairs from 4,734 mixed
  questions (round 1 from round 2: 8,328 from 5,532); 659 all-wrong
  questions (1,233); 70.6% of the samples correct (56.1%).
- The 1.5B differs: from FedAvg SFT round 3, the first round after
  which FedAvg SFT stops gaining, one DPO + NLL round gave 77.97
  against 74.71 (+3.26). Round 6 of the 0.5B is two rounds past that
  point (round 4), so `qwen05b_k4/round_1` is the matching row; queued
  after FedAvg SFT round 7, expected about 18:40 (estimate).
- Read so far: a start from the levelled-off FedAvg SFT is not a better
  definition of the method on the 0.5B. No decision.

## 2026-11-23: FedAvg SFT of the 0.5B levels off at about 64.1 to 64.6 on Spider test (results `417bfd96`, `49346171`)

- FedAvg SFT rounds 4, 5, 6 of Qwen2.5-Coder-0.5B on Spider test:
  64.09, 64.18, 64.56. Round 5 against round 4: +0.09 (49 questions
  against 47, p 0.92); round 6 against round 5: +0.37 (53 against 45,
  p 0.48); round 6 against round 4: +0.47 (71 against 61, p 0.43). No
  round adds more than 0.5 over round 4, so the gain rule (more than
  0.5 over the best round, patience 2) stops the line with round 4 as
  its best round.
- The method's rows from FedAvg SFT round 2 against round 6: DPO + NLL
  round 2 (66.19, 4 rounds) is 1.63 above (142 against 107, p 0.031),
  round 1 (65.86, 3 rounds) 1.30 above (142 against 114, p 0.091).
  Against round 5: +2.00 (p 0.0063) and +1.68 (p 0.024). So on the 0.5B
  the method at 4 rounds is above what FedAvg SFT reaches in 6, not
  only ahead of it at equal rounds.
- The level off is below the estimate of the reading entry of this
  morning (64 to 68, likely 65 to 67).
- Exact McNemar computed here from the committed prediction files.
  Next: `qwen05b_k6/round_1` (DPO + NLL from round 6), expected about
  15:45 (estimate).

## 2026-11-23: pair read from a start trained on BIRD queued, a stand-in for a public stage (code `392b5e6f`, queue `c0e4802d`)

Owner (chat): if the SFT stage helps the DPO + NLL rounds, would a
stage on public data help them more. The task was written by a
delegated agent and read here before the push.

- `public_start/read` and `public_start/publish_read`, at the end of
  the queue: the pair read of the base student
  (`pairread/base_ddl_rows`) with the start changed to the global
  adapter of `bird_sft/round_3`. The Spider clients sample their 8,659
  questions from it (10 at T 1.0, `ddl_rows`) and label them. No
  training. About 25 min (estimate; the base read took 1,358 s).
- What it stands in for, and where it differs: a federated adapter on
  the BIRD clients for a server stage on BIRD; it was trained on the
  `ddl` text with evidence and is sampled here with the Spider
  `ddl_rows` prompt.
- The two starts it is compared with, from the committed pair counts
  (`fedpref_base_p2_ddlrows_alpha01_s0` and
  `fedpref_sftr2_ddlrows_alpha01_s0`, `dpo/round_1`), of 8,659
  questions:

  | Start | Mixed | All correct | All wrong | Mixed on databases with rows |
  |---|---|---|---|---|
  | Base student | 5,951 | 1,631 | 1,074 | 4,454 |
  | FedAvg SFT round 2 on Spider (k = 2) | 5,192 | 2,891 | 573 | 4,013 |

  Two FedAvg SFT rounds on the clients' own questions take 501
  questions out of all wrong and put 1,260 more into all correct: the
  start of the k = 2 line has 441 fewer questions with pairs than the
  base student.
- Read as: mixed on databases with rows at or under 4,013, the stage
  gives the DPO rounds no more than the SFT stage does and the
  direction is dropped; above it with all wrong under 1,074, the next
  step is one line from a start trained on public data (not queued).
- Checked before the push: the resolved command differs from the base
  read in `--from-base` against `--parent-stage
  fedavg_bird_ddl_a01_r3_s0` and in `--out`
  (`fedpref_birdsftr3_ddlrows_alpha01_s0`); one prompt decoded from its
  token ids read (client 1, `train:361`, 690 tokens); the parent row is
  committed (`federated__fedavg__s0__7ecd649662f3__5e43d16b__r3`), 1.5B
  and LoRA r 16 as the read; alpha 32 is the code default of that run,
  the adapter's own config is on the server and was not read.
- No guard compares the dataset or split of a parent row with the
  line's: a Spider line can start from a BIRD row. Used here on
  purpose, not changed.
- Code: the pair read now also writes the questions on databases
  without rows, per client and by kind; only the read uses those keys.
  Tests on the files touched: 57 passed, 2 skipped (run here); the
  agent reports 557 passed, 2 skipped on the whole suite.
- Not run: the read itself (GPU, server only).

## 2026-11-23: one card; the 0.5B rows in the order they answer (queue `2a79a22e`)

Owner (chat, about 09:35): one card only, which row first. The entry
below was written for two cards.

- Order in the queue file now: `qwen05b_sft/round_5`, `round_6`,
  `qwen05b_k6/round_1`, `qwen05b_sft/round_7`, `qwen05b_k4/round_1`,
  then the DeepSeek rows and the prefix probe. No command changed.
- Why: the question is whether the method ends above the level FedAvg
  SFT reaches. Rounds 5 and 6 (about 3 h 50 min) say whether FedAvg
  SFT alone passes the method's 65.86 and 66.19; the DPO + NLL round
  from round 6 says whether a round still adds from there. The start
  from round 4 is a point between two measured starts and waits.
- Expected (estimates, from about 09:45): FedAvg SFT round 6 about
  13:35, DPO + NLL from round 6 about 16:05, FedAvg SFT round 7 about
  18:00.

## 2026-11-23: the 0.5B first; DPO + NLL from FedAvg SFT round 6 and FedAvg SFT round 7 queued (queue `447f8423`)

Owner (chat, about 09:30): know the 0.5B early, DeepSeek waits.

- The 0.5B rows (`qwen05b_k4/round_1`, `qwen05b_sft/round_5` and
  `round_6`) now stand before the pending DeepSeek rows in the queue
  file. A worker takes the first ready task in file order, so both
  cards go to the 0.5B without `--phase`, and a DeepSeek row runs only
  when no 0.5B task is ready. No command of an existing task changed.
- New, row 26: `qwen05b_k6/round_1` (one DPO + NLL round from FedAvg
  SFT round 6) and `qwen05b_sft/round_7`, each with its evaluation.
  With `qwen05b_k2` and `qwen05b_k4` that is the gain of one DPO + NLL
  round at three starts (rounds 2, 4, 6) next to the FedAvg SFT curve
  to round 7.
- The two questions run side by side, not one after the other: the
  FedAvg SFT rounds on one card, the DPO + NLL rounds on the other.
  Waiting for FedAvg SFT to level off before any DPO + NLL round puts
  that round, about 2.5 h, after the last FedAvg SFT round (estimate).
- Checked before the push: resolved commands of `qwen05b_k6/round_1`
  against `qwen05b_k4/round_1` differ in the parent stage and the
  output directory only; `qwen05b_sft/round_7` against `round_6` in the
  round, the stage name and the start adapter; the two evaluations in
  the arm name and the adapter. Prompt: the one rendered for
  `qwen05b_k4` this morning, no code change since. Queue tests: 44
  passed, 2 skipped.
- Expected (estimates, two cards from about 09:45): the read at 5
  rounds about 12:15, the read at 7 rounds about 16:00.

## 2026-11-23: published Spider numbers for the 0.5B and DeepSeek-Coder-1.3B (reading)

Owner (chat): what the two small students reach on Spider elsewhere, to
judge a start of DPO + NLL from a converged FedAvg SFT. A delegated
agent read the sources; its report is
`archive/scan_2026-11-23/R2_small_models_spider.md` (outside Git). The
rows below are as the report gives them, not opened again here.

- No paper has a greedy row for either model after SFT on Spider train
  alone, so no published number is the baseline of our setup.
- Qwen2.5-Coder-0.5B: SLM-SQL (arXiv 2507.22478, Table 3), Spider test
  with a vote of 16: 42.23 without training, 67.26 after SFT on 916K
  rows, 70.42 after GRPO on BIRD on top. FINER-SQL (arXiv 2605.03465):
  Spider dev 70.2 with a schema ranker and a vote of 30. A community
  repository (not citable), Spider test, greedy, LoRA r 16, lr 2e-4,
  2 centralized epochs: 48.3 to 63.5 (its 1.5B: 66.4 to 75.4).
- DeepSeek-Coder-1.3B: SQL-Factory 50.2 without training, 70.7 after
  SFT on Spider train (3 epochs; split and base or instruct not named).
  SLM-SQL, Spider test with a vote of 16: 49.09, 75.13 after SFT, 77.05
  after GRPO.
- RL after a converged SFT in SLM-SQL (Spider test, vote of 16): +3.16
  at 0.5B, +1.92 at DeepSeek 1.3B, +1.07 at 1.5B.
- The agent's estimate of where FedAvg SFT levels off in our setup:
  0.5B 64 to 68, DeepSeek 71.5 to 74.5 (estimates, from the gap to the
  1.5B in the papers that train both). Our rows: 0.5B 64.09 at round 4
  and still rising, method 65.86 and 66.19; DeepSeek 69.82 at round 2,
  method 75.08.
- Not kept from the report: that one FedAvg round moves the model as
  far as a fifth of a centralized epoch. On the 1.5B, FedAvg SFT
  against centralized SFT at the same count is -2.65, -1.63, -0.32 at
  1, 2, 3, so a round is close to an epoch here.
- Read that settles it for the 0.5B: `qwen05b_k4/round_1` against
  `qwen05b_sft/round_5`, then `round_6` (queued, row 25).

## 2026-11-23: gold-prefix probe queued (code `49f7adff`, queue `d2e9e3df`)

Owner (chat): the probe of form 3 of the entry below, written by a
delegated agent and read here before the push.

- `scripts/prefix_probe.py`: the all-wrong questions of one round are
  sampled again from the model that round sampled; the model input is
  the round's prompt token ids followed by the first round(f * n) token
  ids of the training target of the gold SQL, so it is the start of
  that question's training sequence. The SQL of a sample is the prefix
  and the continuation decoded together from their token ids, labelled
  as the round labels. f = 0 is the control, a second draw without a
  prefix. Counts per fraction: questions mixed, all correct, all wrong,
  correct samples equal to the gold SQL, and each question against the
  control.
- Queued as `prefix/probe` and `prefix/publish_probe` at the end of the
  queue: `qwen05b_k2` round 2 (1,168 all-wrong questions, the round 1
  global adapter), f = 0, 0.25, 0.5, 0.75, 10 samples at T 1.0 as the
  round. About 35 min (estimate).
- Checked: the prompt part equals the ids the round's sampling sends to
  the engine, and prompt plus prefix is a prefix of the training
  sequence (0.5B tokenizer, question `train:345`, 4 of 7 gold tokens:
  the input ends `<|im_start|>assistant\nSELECT name , `). Tests: 72
  passed, 2 skipped on the files touched; the agent reports 555 passed,
  2 skipped on the whole suite. Not run: the vLLM path of the script on
  the server.
- Read as: under about a third of the questions mixed at f = 0.5 above
  the control, form 3 is dropped.

## 2026-11-23: DeepSeek-Coder-1.3B on Spider test: one DPO + NLL round from FedAvg SFT round 2 gives 75.08 against 69.82

Run `eval_arms__s0__20261123T013433__615e83f81ab3__2865d8ab97b247bf9a92b88b62949ec0`
(arm `fedpref_deepseek13b_sftr2_p2_dpo_ddl_rows_a01_r1_vllm_inproc`,
`bb0c505b`, 08:34; round `6802090e`, 08:29). Read on the Mac at 08:50
with `scripts.compare_predictions`.

- The DPO + NLL round adds 5.26 over its start (192 questions fixed, 79
  broken, exact McNemar p 5.0e-12); by hardness 86.60 / 80.98 / 67.39 /
  55.74. The same step added 5.26 on the 0.5B and 3.36 on the 1.5B.
- Execution errors 218 to 110; wrong results 430 to 425 (2 outputs end
  at the length limit). Of the 192 fixes, 100 were execution errors and
  92 wrong results; of the 79 breaks, 29 and 50.
- Not read yet: FedAvg SFT round 3 of this model
  (`deepseek13b_sft/round_3`, next in the queue). The method is judged
  at equal rounds; FedAvg SFT would need 5.26 in its third round, and
  its second added 5.82.

## 2026-11-23: the 0.5B from a later start queued: one DPO + NLL round from FedAvg SFT round 4, and FedAvg SFT round 5 (owner; queue `7bb8b06d`)

Owner's question: why the DPO + NLL rounds start at round 2 and not at
the best FedAvg SFT round. On the 1.5B the start does not matter at 4
rounds on Spider test (k = 0, 2, 3: 78.02, 78.20, 77.97; round 3 is the
best FedAvg SFT round there). It is not measured where FedAvg SFT still
rises: the 0.5B adds 1.40 at round 4.

- Queued after the DeepSeek line and the prefix probe:
  `qwen05b_k4/round_1` (root `fedpref_qwen05b_sftr4_p2_ddlrows_alpha01_s0`,
  arm `fedpref_qwen05b_sftr4_p2_dpo_ddl_rows_a01_r1_vllm_inproc`) and
  `qwen05b_sft/round_5` (arm `fedavg_qwen05b_ddl_rows_a01_r5_vllm_inproc`),
  each evaluated on Spider test and published.
- Read: the two rows against each other at 5 rounds, from the same
  start (64.09), exact McNemar; and against the k = 2 line (65.86 at 3
  rounds, 66.19 at 4).
- Checked before queuing: the resolved commands differ from
  `qwen05b_k2/round_1` only in the parent stage and the root, and from
  `qwen05b_sft/round_4` only in the round, the stage label and the start
  adapter; one training sequence of the 0.5B read from its token ids
  (508 prompt tokens, target `SELECT * FROM people<|im_end|>`).
- About 2.5 h and 1 h 55 min (estimates).
- 09:10 (owner): a second card is free and runs the 0.5B phases alone
  (`run --gpu 1 --phase qwen05b_k4 qwen05b_sft`); `qwen05b_sft/round_6`
  added behind round 5 (queue `9b2ecca2`), to read the level FedAvg SFT
  reaches on this model.

## 2026-11-23: a scout report on the server part and its review (no run, nothing decided)

Owner's request: one research agent on the server part, reviewed by the
session. The report is `archive/scan_2026-11-23/R1_server_part.md` (the
owner's Mac, outside Git). Six of its tables were read again through a
page-fetch agent.

The report's ranking, with its own odds of at least +1 EX on Spider test
after the client round over the method without the part:

1. A server round after FedAvg SFT round 2 with the clients' loss on
   BIRD, plus a reverse-KL term to the frozen teacher on the student's
   own samples of the questions with no correct sample: 35% (the
   teacher's own part over the same round without it: 20%).
2. The proposal of the entry below (the teacher's SQL as the chosen side
   when it returns the gold result): 25%. Its SQL is kept only when it
   matches the gold result, so it carries no more of the answer than
   gold; what is left is that it may be closer to the student's own
   SQL, which no paper measures for SQL.
3. A frozen model that scores the student's wrong SQL next to the gold
   SQL and pushes down only the tokens it disfavours: 15%.

Checked on the pages and confirmed: KID Table 3 (average of 5 sets
against SFT 43.85; forward KL -0.86 / -0.08 / -0.42, reverse KL on the
student's samples +3.09 / +4.62 / +4.35, at 10.9 to 13.9 times the SFT
time; teachers fine-tuned on the same training set); Step-DPO Table 4
(54.8, 55.1 with GPT-4 chosen steps, 55.8 with self-generated ones);
DistiLLM-2 (Appendix C.2: the student row 30.73 is after SFT on gold);
OmniSQL Table 4, greedy (Qwen2.5-Coder 7B: Spider test 82.2, BIRD dev
50.9; 14B: 86.6, 61.5); Reasoning-SQL Table 5 (7B on Spider: 77.85
without training, 68.08 after SFT on BIRD train, 78.72 after GRPO on
it; Gemini schema linking first, split not named).

Where the report is wrong or goes past its source:

- CodeLutra's 76.6 on Spider is iteration 3; iteration 4 is 76.3.
- OmniSQL's sentence on training sets names "some open-source LLMs
  (e.g., Qwen2.5-Coder-32B-Instruct ...)" and says "likely"; it does
  not name the 7B.
- The page does not say what prompt OmniSQL's baseline rows get, so
  82.2 and 86.6 are not numbers for our prompt.
- KID's page does not say that its row on student samples carries the
  term on gold.

The session's review of design 1:

- Its teacher term has no execution check and acts on the questions
  where the teacher is weakest. If it is run, only on the questions
  where the teacher's own SQL returns the gold result; the count of
  those decides designs 1 and 2 alike.
- Its evidence is from teachers fine-tuned on the task and tested in
  the same domain; no SQL result has a frozen teacher on other data.
- Its stop rule (1.0 above the gold stage before the client round)
  would have dropped the teacher in the earlier setup, where it was
  +0.23 before the DPO rounds and +0.98 after. A read at the stage
  level does not settle it; the full arms do (about 36 h, the report's
  estimate).
- A stage after FedAvg SFT round 2 moves the model toward BIRD just
  before the client round. The earlier measurement is for a stage
  before the rounds.
- With BIRD clients and Spider as the public set the student has no
  correct sample for 12% of the public questions, so a teacher term has
  little to act on there; the part may show on one dataset only.

Proposed order (not decided, nothing queued): the three reads of the
entry below, with the 14B teacher next to the 7B; then the stage
without a teacher, from adapters that exist: the Spider line (two FedAvg
SFT rounds, one DPO + NLL round) started from `bird_k2/round_1` and from
`bird_sft/round_3`, against the k = 2 line (77.46 at 3 rounds), about
8 h a line (estimate; whether a line can start from an adapter of
another split is not checked in the code); a teacher term only if the
stage adds 1 EX after the client round. Session's odds: 40% for the
stage, 20 to 25% for a teacher's own part.

Notes corrected from the checked pages: `DPO_RESEARCH.md` 2.7 (the
CodeLutra row), `LITERATURE.md` 1.5 and 1.7 (DistiLLM-2, Step-DPO).

## 2026-11-23: reading on a server part for the method (owner: the method is too simple; no run, nothing decided)

Owner's question: which direction makes the method more than "FedAvg SFT
rounds, then a DPO + NLL round", for example a distillation round at the
server. Read: the notes, the earlier setup (reference only) and two
papers through a page-fetch agent, not by eye.

What the earlier setup measured for a server stage (old prompt,
repetition penalty, two seeds pooled; reference only, never a result):

- Teacher soft targets on BIRD before FedAvg: +2.12 on Spider test
  before the DPO rounds and +1.40 after them (p 0.01); after DPO +3.53
  on Spider dev, +4.11 on DK, +2.03 on Syn.
- The teacher's own part against gold SQL on the same BIRD rows: +0.98
  after DPO (p 0.04), +0.23 before.
- The 7B teacher without training (77.22) was right on 129 of the
  method's 442 wrong results; the soft-target stage did not pass those
  rows on.

Nothing of this is measured since the reset: no server stage, no
teacher row. The server preference round with the teacher's SQL as the
chosen side (`srvx_s0`, `srvt_s0`) was queued on 2026-11-17 and never
read.

Papers:

- FedCoLLM (arXiv 2411.11707 v3): after every aggregation the server
  trains the small model and its own LLM on labelled auxiliary data
  with cross-entropy plus mutual KL. Table 2, client model, FedAvg to
  FedCoLLM: CQA 58.6 to 60.8 and OBQA 27.2 to 29.2 (OPT-1.3B), ARC-E
  59.97 to 60.01. The FedAvg baseline has no auxiliary data and no row
  removes the KL term, so the gain mixes the teacher with the extra
  labelled data. The server LLM is trained, not frozen.
- PubSwap (arXiv 2604.12160 v1): federated GRPO where the clients take
  steps on shared public prompts and a client with few correct
  responses gets correct ones of the other clients. Qwen3-1.7B on
  DeepMath, 10 / 40 / 90 / 120 local steps: +2.2 / +0.3 / +2.9 / +5.1
  over FedAvg-GRPO; on MATH -0.9 / +1.1 / +1.4 / +0.7. No teacher, no
  SQL or code task, and no baseline that also trains on the public set.

Proposal (not decided): a server part with the same loss as the
clients. On the public data the student samples, execution labels the
samples, and where no sample is correct the teacher's SQL is the chosen
side when it returns the gold result. Controls: the stage with gold SQL
only, and gold as the chosen side for the same questions (on the BIRD
clients gold as chosen was 2.61 below, p 0.007).

Reads before any training, none queued:

1. The adapters trained on the BIRD clients (`bird_sft/round_3`,
   `bird_k0/round_1`, `bird_k2/round_1`) evaluated on Spider test, and
   the Spider adapters on BIRD dev: what training on the public set
   gives the other set with this prompt, with gold and with the
   execution loss (evaluation only; a federated adapter stands in for a
   server stage).
2. The 7B teacher without training on Spider test and BIRD dev with the
   present prompt, and the share of the method's wrong results it gets
   right.
3. CPU only: of the base student's 4,035 all-wrong BIRD train
   questions, the share where the stored teacher SQL returns the gold
   result.

## 2026-11-23: reading on one loss for gold SQL and execution preference (literature and committed audits, no run, nothing decided)

Owner's question: the method flattens after its first DPO + NLL round
while FedAvg SFT still rises on the 0.5B; is there a form with one
story instead of "SFT, then DPO + NLL". Papers read through a page-fetch
agent, not by eye; parts the agent had only as a summary are marked.

Papers:

- SRFT (arXiv 2506.19767, listed at ICLR 2026). One stage: NLL on
  demonstrations, policy gradient on the model's own rollouts, both
  weighted by the policy entropy. Qwen2.5-Math-7B, five maths
  benchmarks: SFT 47.3, RL 49.4, SFT then RL 52.5 (54.5 in its Table
  2), SRFT 59.5; with either weight fixed to 1, 55.1 and 56.2.
  Demonstrations are DeepSeek-R1 traces, not gold. No number for the
  plain sum of the two losses.
- Fernando et al. (arXiv 2410.15483 v4). SFT and DPO on two different
  datasets; sequential training forgets the first one. The plain
  weighted sum ("Mix") is as good as their alternating schemes and costs
  over 50% more run time; Llama3-8b numbers from the agent's summary of
  the appendix.
- ReLIFT (arXiv 2506.07527 v3), Table 1, Qwen2.5-Math-7B: SFT 49.0, RL
  46.9, RL with an SFT loss on all questions 48.6, SFT then RL 50.7 and
  50.8, ReLIFT 52.6. A fine-tuning step after every RL step on the same
  batch collapses (23.8, "conflicting optimization objectives"). SFT
  targets are DeepSeek-R1 solutions.
- UFT (arXiv 2505.16984 v2, NeurIPS 2025). The rollout starts from a
  prefix of the gold solution; the prefix length is annealed to zero and
  an NLL term trains the prefix. Table 8, average of nine sets, SFT /
  RFT / SFT then RFT / UFT: Qwen2.5-0.5B 4.46 / 3.25 / 7.28 / 9.45;
  1.5B 9.36 / 16.08 / 11.70 / 22.23; 3B 15.25 / 32.15 / 17.34 / 30.93.
  Maths, Countdown and logic with GRPO.
- Federated DPO: Distributed DPO (arXiv 2605.20696, listed at ICML
  2026) and FedPDPO (arXiv 2603.19741) both train on fixed pairs
  labelled by people, with a frozen reference and no likelihood term,
  on DistilGPT-2 (FedPDPO also TinyLlama-1.1B); no pairs sampled from
  the current model, no task with an executable check. FedPDPO's
  federated DPO baseline is FedDPO (Ye et al. 2024).

None of them is Text-to-SQL, federated with on-policy pairs, or DPO on
SQL-only output; all the SFT + RL papers train reasoning chains with
GRPO.

From the committed audits (`delta_stats` of each round): cosine between
client updates, lowest to highest pair.

| Line | FedAvg SFT round 1 | round 2 | round 3 | round 4 | first DPO + NLL round from round 2 | second |
|---|---|---|---|---|---|---|
| 1.5B, Spider | 0.13 to 0.33 | 0.01 to 0.05 | -0.01 to 0.02 | -0.02 to 0.01 | 0.24 to 0.32 | 0.01 to 0.05 |
| 0.5B, Spider | 0.21 to 0.46 | 0.01 to 0.06 | -0.01 to 0.02 | -0.03 to 0.01 | 0.27 to 0.34 | 0.02 to 0.09 |
| 1.5B, BIRD | 0.19 to 0.25 | 0.03 to 0.04 | 0.00 to 0.02 | -0.02 to 0.01 | 0.27 to 0.34 | not run |
| DeepSeek 1.3B, Spider | 0.45 to 0.69 | 0.05 to 0.10 | | | | |

From round 2 the FedAvg SFT updates of the clients are orthogonal; the
first DPO + NLL round from the same start gives updates the clients
share, and its second round does not. The 0.5B still gains 2.09 and
1.40 in SFT rounds with cosine near 0, so the cosine does not say when
FedAvg SFT stops gaining and is no rule for k.

Three forms, by what supports them:

1. FedAvg SFT rounds, then one DPO + NLL round as the last round. All
   7 starts measured are above the SFT round from the same start. Two
   stages.
2. One loss each round: NLL on the gold SQL of every question next to
   DPO + NLL on the pairs. Proposed on 2026-11-21 and dropped after
   `bird_k0_goldnll/round_2` (entry of that day); not run. Papers: for
   (SRFT, Fernando et al.) and against (ReLIFT's row and collapse), all
   in other settings.
3. Samples that start from a prefix of the gold SQL (UFT's mechanism
   with DPO + NLL and execution labels): the same prompt, the prefix as
   the start of the answer; chosen and rejected share the prefix, so
   the pair differs only in what the model wrote. Prefix as long as the
   gold SQL is SFT, prefix of length 0 is the present round. It gives
   pairs for questions with no correct sample without a second prompt
   (the hint of item 12d needed one). Against it: gold rows for the
   all-wrong questions did not raise EX on BIRD. Not run, no code.

Probes proposed, none queued: adding the updates of
`qwen05b_sft/round_3` and `qwen05b_k2/round_1` to their parent and
evaluating (form 2, evaluation only); sampling the 1,168 all-wrong
questions of the 0.5B from 25%, 50% and 75% of the gold SQL and
counting the questions that become mixed (form 3, sampling and labels
only).

## 2026-11-23: Qwen2.5-Coder-0.5B at 4 rounds on Spider test: the method 66.19, FedAvg SFT 64.09 (+2.10, p 0.0056), the second DPO + NLL round adds 0.33; DeepSeek-Coder-1.3B FedAvg SFT rounds 1 and 2: 64.00, 69.82

Runs `eval_arms__s0__20261122T161428__496e40c7a502__fbade66ddd2e48b1a61b76c86f2e70f0`
(arm `fedpref_qwen05b_sftr2_p2_dpo_ddl_rows_a01_r2_vllm_inproc`,
`ef7ad11a`, 2026-11-22 23:14; round `23014ad3`, 23:10),
`eval_arms__s0__20261122T180749__1425448d52e5__ddf45ad48a96446abff05c0b9fa6a459`
(arm `fedavg_qwen05b_ddl_rows_a01_r4_vllm_inproc`, `7f9a6d77`, 01:08;
round `590caaa2`, 01:04),
`eval_arms__s0__20261122T195618__218de81d1cd2__4f0e69eca87e462d9f903211292cdea9`
(arm `fedavg_deepseek13b_ddl_rows_a01_r1_vllm_inproc`, `036a2735`,
02:56; round `315adef7`, 02:50) and
`eval_arms__s0__20261122T214336__4f772a0ad960__e1ec55cb6dca4f5fb74af4fd7631042a`
(arm `fedavg_deepseek13b_ddl_rows_a01_r2_vllm_inproc`, `311385de`,
04:43; round `6ee53886`, 04:39). Read on the Mac at 05:15; comparisons
with `scripts.compare_predictions`.

| Row | Spider test EX | Easy | Medium | Hard | Extra | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| 0.5B FedAvg SFT round 3 | 62.69 | 82.55 | 66.86 | 51.62 | 40.90 | 392 | 409 |
| 0.5B FedAvg SFT round 4 | 64.09 | 84.47 | 69.08 | 50.11 | 43.42 | 365 | 406 |
| 0.5B k = 2, DPO + NLL round 1 (3 rounds) | 65.86 | 84.04 | 70.71 | 54.43 | 45.10 | 304 | 429 |
| 0.5B k = 2, DPO + NLL round 2 (4 rounds) | 66.19 | 84.04 | 70.95 | 55.08 | 45.66 | 268 | 458 |
| DeepSeek 1.3B without training | 55.85 | 73.40 | 61.84 | 42.76 | 35.29 | 152 | 796 |
| DeepSeek 1.3B FedAvg SFT round 1 | 64.00 | 82.98 | 68.49 | 53.78 | 41.46 | 340 | 433 |
| DeepSeek 1.3B FedAvg SFT round 2 | 69.82 | 87.45 | 73.05 | 57.88 | 54.34 | 218 | 430 |

- 0.5B at 4 rounds: the method is 2.10 above FedAvg SFT (149 questions
  right only with the method, 104 only with FedAvg SFT, exact McNemar p
  0.0056); by hardness -0.43, +1.87, +4.97, +2.24. At 3 rounds the gap
  was 3.17. The 1.5B: 2.75 at 3 rounds, 3.49 at 4.
- FedAvg SFT round 4 adds 1.40 (71 against 41, p 0.0059). Its rounds
  give +3.73, +2.47, +2.09, +1.40: slower each round, not flat.
- The second DPO + NLL round adds 0.33 (77 against 70, p 0.62): level
  with the first. Execution errors fall again (304 to 268) and wrong
  results rise (429 to 458). The 1.5B's second round added 0.74.
- The method at 3 rounds is 1.77 above FedAvg SFT at 4 rounds (142
  against 104, p 0.018).
- Round 2 of the method: 4,810 pairs (538 / 916 / 1,384 / 1,434 / 538;
  round 1: 8,328), 2,300 rejected sides execution errors and 2,510
  wrong results. Of the 8,659 questions 3,353 are mixed, 4,135 all
  correct, 1,168 all wrong (13.5%; before round 1: 14.2%); 71.3% of the
  samples are correct (56.1%). Client updates: cosine 0.02 to 0.09
  (round 1: 0.27 to 0.34), norms 0.63 to 0.99. The 1.5B shows the same
  from round 1 to round 2: 8,026 to 3,354 pairs, cosine 0.24 to 0.32
  down to 0.01 to 0.05. One round removes most of what the pairs carry,
  and it does not reach the all-wrong questions.
- What this means for the 0.5B row of the paper: the gain at equal
  rounds holds at 3 and at 4 rounds, and it narrows, because the method
  is flat after its first DPO + NLL round while FedAvg SFT still adds
  1.4 a round. Where FedAvg SFT ends is not measured; at this pace it
  could be near 66 after two or three more rounds. Two rows would
  settle it, neither queued: FedAvg SFT rounds 5 and 6 (about 1 h 55
  min each with evaluation), and one DPO + NLL round from FedAvg SFT
  round 4 (about 2.5 h), which is compared with round 5 at equal rounds
  and says whether the DPO + NLL gain adds to a later SFT start.
- Time and memory, 0.5B: the DPO + NLL round 1 h 40 min (sampling 34
  min, labels 2 min, reference 14 min, updates 49 min), peak reserved
  14.14 / 17.88 / 19.33 / 17.63 / 17.53 GiB; FedAvg SFT round 4 was
  published 1 h 50 min after the publication before it.
- DeepSeek-Coder-1.3B: FedAvg SFT round 1 adds 8.15 over the model
  without training (393 against 218, p 1.4e-12) and round 2 another
  5.82 (195 against 70, p 8.1e-15). Round 1 moves the model to the form
  of the gold SQL (exact match 15.37 to 51.14; only 1.3% of its SQL
  strings are the same as before): wrong results fall from 796 to 433
  and execution errors rise from 152 to 340, then fall to 218 in round
  2. At 2 rounds it is 9.22 above the 0.5B and 4.28 below the 1.5B. A
  round is published 1 h 42 min after the one before it; peak reserved
  9.80 GiB in both rounds.
- Next in the queue: `deepseek13b_k2/round_1`, then
  `deepseek13b_sft/round_3`. DeepSeek's FedAvg SFT is far from flat at
  the start of the DPO + NLL round (+5.82 in round 2), more so than the
  0.5B (+2.47).

## 2026-11-22: Qwen2.5-Coder-0.5B at 3 rounds on Spider test: the method 65.86, FedAvg SFT 62.69 (+3.17, p 1.3e-05); FedAvg SFT still rises on this model

Run `eval_arms__s0__20261122T142818__250a2b8b0707__65a91f9784904247bad026834d4b75a3`
(arm `fedavg_qwen05b_ddl_rows_a01_r3_vllm_inproc`, `102fcb99`, 21:28;
round `370bd7fa`, 21:23). Read on the Mac at 22:20; comparisons with
`scripts.compare_predictions`.

| Row | Spider test EX | Easy | Medium | Hard | Extra | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| 0.5B FedAvg SFT round 2 (start of the two rows below) | 60.60 | 82.55 | 64.29 | 49.68 | 36.97 | 429 | 417 |
| 0.5B FedAvg SFT round 3 | 62.69 | 82.55 | 66.86 | 51.62 | 40.90 | 392 | 409 |
| 0.5B k = 2, DPO + NLL round 1 (3 rounds) | 65.86 | 84.04 | 70.71 | 54.43 | 45.10 | 304 | 429 |

- At 3 rounds the method is 3.17 above FedAvg SFT (154 questions right
  only with the method, 86 only with FedAvg SFT, exact McNemar p
  1.3e-05), on every hardness level (+1.49, +3.85, +2.81, +4.20). The
  1.5B at 3 rounds: +2.75 (77.46 against 74.71).
- FedAvg SFT round 3 adds 2.09 over round 2 (83 questions against 38, p
  5.3e-05). FedAvg SFT has not flattened on this model: +3.73, +2.47,
  +2.09 a round, where the 1.5B gave +4.38, +1.67, +0.61, 0.
- From the same start the DPO + NLL round adds 5.26 and the SFT round
  2.09. Both take their gain from execution errors (429 to 304, 429 to
  392); wrong results go to 429 and to 409.
- 6 answers of the method's row end at the output length limit (FedAvg
  SFT round 2: 1, round 3: 0).
- The start at round 2 while FedAvg SFT still rises (owner's question).
  The comparison is at equal rounds and the DPO + NLL round carries the
  NLL term, so no round of supervised training is given up. Every start
  measured so far gives the same picture, the DPO + NLL round above the
  SFT round from the same start: 0.5B from round 2 +3.17; 1.5B from the
  base +3.44, from round 2 +2.75, from round 3 +3.26; BIRD from the base
  +3.00, from round 1 +1.56, from round 2 +2.54. On the 1.5B a later
  start changed nothing at 4 rounds (k = 0, 2, 3: 78.02, 78.20, 77.97).
  Not measured: a start at round 3 on the 0.5B.
- Open on this model: 4 rounds do not show where FedAvg SFT flattens.
  On the 1.5B the method (78.20) is above the flat FedAvg SFT (74.71)
  and above centralized SFT (75.73); on the 0.5B that reading needs
  FedAvg SFT run until it stops rising (rounds 5 and 6, about 2 h each
  with evaluation). Not queued; read round 4 first.
- Time: round 3 was published 2 h 01 min after the publication before
  it (19:22 to 21:23), its evaluation 5 min later.

## 2026-11-22: Qwen2.5-Coder-0.5B on Spider test: one DPO + NLL round from FedAvg SFT round 2 gives 65.86 against 60.60 (p 1.9e-12); DeepSeek-Coder-1.3B without training 55.85

Runs `eval_arms__s0__20261122T094629__61c7ecba9979__96f811b706ca45189c0a7498ce6b606a`
(arm `fedavg_qwen05b_ddl_rows_a01_r2_vllm_inproc`, `689a7d93`, 16:46;
round `5d0dc3b9`, 16:33),
`eval_arms__s0__20261122T122229__c902f1d1e2c1__5f81b731568445878dbded12f0f81912`
(arm `fedpref_qwen05b_sftr2_p2_dpo_ddl_rows_a01_r1_vllm_inproc`,
`1085d38e`, 19:22; round `51b4a288`, 19:18) and
`eval_arms__s0__20261122T094130__9e150ac7941f__78cae2fa685d43e8b387380a73ea3dc9`
(arm `zs_deepseek13b_ddl_rows_vllm_inproc`, `12c4ccd3`, 16:41). Read on
the Mac at 20:10.

| Row | Spider test EX | Easy | Medium | Hard | Extra | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| 0.5B FedAvg SFT round 1 | 58.13 | 83.40 | 62.31 | 46.22 | 30.25 | 476 | 423 |
| 0.5B FedAvg SFT round 2 | 60.60 | 82.55 | 64.29 | 49.68 | 36.97 | 429 | 417 |
| 0.5B DPO + NLL round 1 from FedAvg SFT round 2 (3 rounds) | 65.86 | 84.04 | 70.71 | 54.43 | 45.10 | 304 | 429 |
| DeepSeek-Coder-1.3B without training | 55.85 | 73.40 | 61.84 | 42.76 | 35.29 | 152 | 796 |

- FedAvg SFT round 2 adds 2.47 over round 1 (112 questions fixed, 59
  broken, exact McNemar p 6.2e-5).
- The DPO + NLL round adds 5.26 over its start (187 fixed, 74 broken,
  p 1.9e-12), on every hardness level. The same step on the 1.5B added
  3.36 (74.10 to 77.46).
- As on the 1.5B the gain is in execution errors (429 to 304; the 1.5B
  183 to 99) and the wrong results do not fall (417 to 429; the 1.5B 373
  to 385).
- Not read yet: FedAvg SFT at 3 rounds for this model
  (`qwen05b_sft/round_3`, the next row of the queue). The method is
  judged at equal rounds, so the row above is a gain over its start
  only. FedAvg SFT would need 5.26 in its third round to reach 65.86;
  its second added 2.47.
- The round: 8,328 pairs (1,022 / 1,726 / 2,410 / 2,258 / 912; the 1.5B
  8,026), 4,702 rejected sides execution errors and 3,626 wrong results.
  Of the 8,659 questions 5,532 are mixed, 1,891 all correct, 1,233 all
  wrong (14.2%) and 3 have a gold error; 56.1% of the samples are
  correct. Client updates: cosine 0.27 to 0.34 (the 1.5B 0.24 to 0.32),
  norms 0.98 to 1.57.
- Measured: 2 h 29 min (sampling 35 min, labels 2 min, reference 23
  min, updates 1 h 29 min); peak reserved 11.50 / 18.37 / 19.33 / 17.46
  / 17.59 GiB. FedAvg SFT round 2: peak reserved 20.25 GiB, as round 1.
- DeepSeek-Coder-1.3B with the tokenizer of its `tokenizer.json`: 55.85
  without training, 1.45 above the 0.5B and 12.2 below the 1.5B. The
  path that was not checked in the entry below (the engine returning
  token ids, the decode on Windows) works on the server. Its errors are
  wrong results (796) more than execution errors (152), and its exact
  match is 15.37 (the 0.5B 43.27): it writes SQL in another form than
  the gold. Probe on the 4 longest rows (8,158 to 8,238 tokens): peak
  reserved 8.29 GiB with gradient checkpointing, 3.6 s a step
  (`audits/protocol_v2/model_probes/deepseek13b_spider_ddl_rows.json`).

## 2026-11-22: direction scan for a Q2 method (literature only, no run, nothing decided)

Owner's request: a method direction for a Q2 journal searched from the
task and the literature, not bound to what the project has, no niche
conditions; later in the session, directions that are too niche or have
low odds are dropped. Twelve reports: 5 literature maps, 3 sets of
proposals (10 directions; one writer knew only the task), 2 checks
against prior work and cost, 2 assessments of late directions. Result:
`DIRECTION_SCAN_2026-11-22.md`. Raw reports: `archive/scan_2026-11-22/`
(Mac only). The reports worked from the numbers of the morning, before
`bird_k2/round_1` (46.22) was read; their odds on BIRD are set against
44.26.

- No new mechanism beats the core. Every proposed direction died or
  shrank to an extra part with 6% to 12% odds of +1.5 EX on both sets
  over a row that already has the preference rounds.
- Checked gap: no federated Text-to-SQL paper with a language model in
  2024 to 2026 (only Zhang et al., ACL 2023); the 2026 federated
  preference and GRPO papers do not touch SQL or a database.
- BIRD: gold wrong in content for about a quarter of BIRD train (two
  audits), errors in 34% to 53% of sampled dev rows; filtering the train
  set is worth nothing on the released dev in two published tests.
- Q2 bar from 20 journal articles: an adapted mechanism, 1 or 2
  benchmarks, gains of +0.75 to +7, mostly one run, a module ablation.
  The k = 2 line (+3.5 on Spider test, +2.54 on BIRD dev) is inside it.
- Recommendation (not decided): no second mechanism now; the compute goes
  to the second and third model, the published federated baselines, the
  local-only row and the loop run centrally (item 12a becomes a row the
  paper needs).
- Kept as an optional added row: a selector trained on the same execution
  labels (about 50% over voting on BIRD dev, 12% on both sets; not a
  federated part). Low odds, not proposed: the hinted pair for the
  unsolved questions (item 12d; 20% on BIRD dev, 10% on both), questions
  generated by the clients (30% and 6%, new code). The rest is dropped,
  with the reason for each in the note.
- Proposed reads, not queued (owner): vote and best of 8 on existing
  checkpoints (about 1 GPU hour); the stored BIRD train samples joined
  with BIRD-Platinum (CPU).
- A correction: the brief for the reports lacked the row "NLL on the
  model's own correct samples" (75.87 on Spider test, between FedAvg SFT
  74.71 and DPO + NLL 77.46); one report calls that part never isolated,
  which holds for BIRD only.
- Owner, during the scan: delegated work runs on the cheaper model, the
  larger one is for the main session only (cost; `AGENTS.md`, Defaults).

## 2026-11-22: DeepSeek-Coder-1.3B ran with a tokenizer that dropped whitespace; its base row (EX 0.00) is not a result; fixed and queued again

Found at 16:00 when the base row came back at 0 of 2,147 (run
`eval_arms__s0__20261122T055518__3517edc2c415__fbb93282e1894ef394dff2f3235329d3`,
arm `zs_dsc13b_ddl_rows_vllm_inproc`, commit `db26468f`). Every
prediction carried the byte-level markers of its tokens
(`ĊSELECTĠCOUNT(*)ĠFROMĠclub`) and failed as a syntax error.

- Cause: Transformers 5 (5.10.2 in the lock file) builds a tokenizer
  class from that class's own pipeline and takes only the vocabulary from
  `tokenizer.json` (its migration guide: "tokenizer behavior is now fully
  determined by the class definition or `tokenizer.json`"). The config of
  deepseek-coder names `LlamaTokenizerFast` over a byte-level BPE file,
  so `AutoTokenizer` gave a Metaspace tokenizer on that vocabulary: every
  space and newline of a prompt was dropped
  (`CREATETABLE"club"("Club_ID"int);Question:Howmany...`), and the engine
  joined its output tokens without decoding them. The model still wrote
  the right tokens for simple questions from such a prompt.
- What is not a result: the base row above; the lengths of the first
  probe (`audits/protocol_v2/model_probes/dsc13b_spider_ddl_rows.json`,
  longest 6,070); the lengths and the "prompt and target read" row for
  DeepSeek in the entry below. Its memory reading stands as a reading at
  6,070 tokens: 7.55 GiB reserved, 4.52 GiB allocated, 2.35 s a step. No
  training ran on that tokenizer: the line was taken out of the queue
  before its first round (`2c1d5ef2`, 16:05).
- The check before queuing did not see it: the rendered prompt was read
  as text before tokenization, and the template's ids were compared with
  the ids of that text, two paths through the same tokenizer. The rule is
  now to read a prompt decoded from its token ids (both `AGENTS.md`).
- Fix (`58cd89f7`): `fedls_sql.models.tokenizer.load_tokenizer` replaces
  every direct `AutoTokenizer` load. It encodes a probe text with
  `AutoTokenizer` and with the shipped `tokenizer.json`, loads the file
  as shipped when they differ, and refuses a tokenizer that does not
  give the text back. For such a model the vLLM side returns the output
  token ids and the Windows side decodes them. Qwen 1.5B, 0.5B: the
  loader returns the `AutoTokenizer` object as before (same ids on the
  probe, same template text), and the engine's text is used as before.
  A test builds the same mismatch from a small tokenizer; 548 tests pass.
- With the right tokenizer (Mac, 8,659 Spider client rows): longest
  training sequence 8,238 tokens (`train:3698`, `baseball_1`), median
  1,030 (Qwen: 6,927 and 821); 82 rows above 7,168, all on client 3, 2
  above 8,192, none above 8,704. Longest per client: 3,266 / 4,853 /
  8,238 / 3,845 / 4,502. One example read from its ids: one
  begin-of-sentence token, the model's system sentence, `### Instruction:`,
  the prompt with its spaces and newlines, `### Response:`, the SQL, a
  newline and `<|EOT|>`.
- Queued again (`e694b9fe`, 16:12) under the tag `deepseek13b`, since
  the names of the first pass are taken by rows that are not results:
  roots `fedavg_deepseek13b_base_ddlrows_alpha01_s0` and
  `fedpref_deepseek13b_sftr2_p2_ddlrows_alpha01_s0`, arms
  `zs_deepseek13b_...`, `fedavg_deepseek13b_...`,
  `fedpref_deepseek13b_sftr2_p2_dpo_...`. The line of the 1.5B with the
  model and the length limit changed: `--max-len 8704`, under which no
  row is cut or refused, as for the Qwen models under 7,168. Its probe
  and base row stand before the rest of the 0.5B line, so the fix is
  read at the next task boundary; the line itself runs after the 0.5B
  line.
- Not checked: the token-id path on the server (vLLM returning ids, the
  decode on Windows); the base row of `models/base_deepseek13b` shows it.
- Seen on the way, not looked into: at about the same length DeepSeek
  takes 2.35 s and 4.5 GiB allocated a training step where the 0.5B
  takes 5.19 s and 11.5 GiB, so the cost of a long row in the Qwen
  models comes from their attention path, not from their size.

## 2026-11-22: Qwen2.5-Coder-0.5B on Spider test: base 54.40, FedAvg SFT round 1 58.13

Runs `eval_arms__s0__20261122T055046__75cca4be6dce__f2fc8b0a8932410fb2f116593052842d`
(arm `zs_qwen05b_ddl_rows_vllm_inproc`, `db26468f`, 12:55) and
`eval_arms__s0__20261122T074501__f057588d0c63__bc20a8f4bc1c48d89f5b1304c818b40b`
(arm `fedavg_qwen05b_ddl_rows_a01_r1_vllm_inproc`, `4d62bf81`, 14:45);
round `af7182a3` (14:39). Read on the Mac at 16:00.

| Row | Spider test EX | Easy | Medium | Hard | Extra | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| 0.5B without training | 54.40 | 80.43 | 60.09 | 40.60 | 24.37 | 469 | 510 |
| 0.5B FedAvg SFT round 1 | 58.13 | 83.40 | 62.31 | 46.22 | 30.25 | 476 | 423 |
| 1.5B without training | 68.05 | 87.45 | 71.41 | 59.18 | 45.94 | 287 | 399 |
| 1.5B FedAvg SFT round 1 | 72.43 | 89.15 | 75.26 | 63.71 | 54.90 | 215 | 377 |

- Round 1 adds 3.73 (196 questions fixed, 116 broken, exact McNemar p
  7e-6); on the 1.5B it added 4.38 (165 against 71).
- The 0.5B is 13.7 below the 1.5B without training and 14.3 below after
  one round. Its execution errors do not fall in round 1 (469 to 476),
  where the 1.5B's did (287 to 215).
- Memory and time: probe 19.25 GiB reserved, 11.53 GiB allocated, 5.19 s
  a step on the 4 longest rows
  (`audits/protocol_v2/model_probes/qwen05b_spider_ddl_rows.json`,
  `6efc1909`). Round 1: 1.72 h of client training (the 1.5B: 2.04 h),
  12:55 to 14:39 on the clock; peak reserved 20.25 GiB on client 3,
  above the 1.5B's 19.83 (clients 1 to 5: 7.91 / 18.16 / 20.25 / 14.56 /
  18.11). The estimate of the entry below (about 12 GiB allocated, peak
  near the 1.5B's) held for this model; the hour per round did not.

## 2026-11-22: `bird_sft/round_4`, FedAvg SFT on BIRD at 4 rounds: 42.57, 1.11 below round 3

Run `eval_arms__s0__20261122T053951__87bb97ea8b37__64d8e9a9ae374ea6b8f193d343f70729`,
arm `fedavg_bird_ddl_a01_r4_vllm_inproc`; round `5b2a72bf` (12:32),
evaluation `0603f35a` (12:40). Read on the Mac from the committed
predictions at 16:00.

| Row | Rounds | BIRD dev EX | Simple (925) | Moderate (464) | Challenging (145) | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| FedAvg SFT round 2 | 2 | 42.70 | 50.49 | 31.25 | 29.66 | 286 | 593 |
| FedAvg SFT round 3 | 3 | 43.68 | 51.57 | 32.54 | 28.97 | 276 | 588 |
| FedAvg SFT round 4 | 4 | 42.57 | 51.35 | 29.96 | 26.90 | 268 | 613 |
| k = 2 (`bird_k2/round_1`) | 3 | 46.22 | 53.08 | 36.85 | 32.41 | 102 | 723 |

Exact McNemar, FedAvg SFT round 4 against:

| Row | Only round 4 right | Only the other right | Difference | p |
|---|---|---|---|---|
| FedAvg SFT round 3 | 30 | 47 | -1.11 | 0.068 |
| FedAvg SFT round 2 | 60 | 62 | -0.13 | 0.93 |
| k = 2 at 3 rounds | 77 | 133 | -3.65 | 0.0001 |
| k = 1 at 2 rounds | 115 | 141 | -1.69 | 0.12 |

- FedAvg SFT on BIRD has its best round at 3 (43.68) and is back at the
  level of round 2 at round 4; the fall from round 3 is on the moderate
  questions (5 fixed, 17 broken, p 0.017).
- The method at 3 rounds is 3.65 above FedAvg SFT at 4 rounds (p
  0.0001), on the moderate questions 50 against 18 (p 0.0001): the
  baseline does not reach it with one more round. The row of the method
  at 4 rounds (`bird_k2/round_2`) is not queued.
- Time and memory (`metrics.json`): 2.95 h of client training (1,545 /
  1,255 / 1,912 / 740 / 5,177 s), peak reserved 19.84 GiB on client 5.

## 2026-11-22: the Spider line queued on two more student models, Qwen2.5-Coder-0.5B and DeepSeek-Coder-1.3B (owner)

Owner in chat this morning, on the session's proposal; queue commit
`05cf77cc` (10:29). Nothing of it has run.

- Why these two: Qwen2.5-Coder-0.5B-Instruct is the same family one size
  down (hidden 896, 24 layers, 14 heads; apache-2.0) and
  deepseek-coder-1.3b-instruct another family at about the size of the
  1.5B (hidden 2,048, 24 layers, 16 heads); both are open and ship
  `model.safetensors` (configs and file lists read on Hugging Face).
  Qwen2.5-Coder-3B was left out on a memory estimate by parameter count
  (26 to 32 GiB); by the scaling below it would need about 18.5 GiB
  allocated (estimate), so a probe could settle it if a third Qwen size
  is wanted.
- What runs: for each model the line of Qwen2.5-Coder-1.5B with the
  model changed and nothing else. FedAvg SFT rounds 1 to 4 (lr 2e-4,
  batch 1 x 16, length limit 7,168), DPO + NLL rounds 1 and 2 from
  FedAvg SFT round 2 (10 samples at T 1.0, 2 random pairs per mixed
  question, beta 0.1, lr 5e-5), prompt `ddl_rows` through the model's own
  chat template, greedy evaluation of 256 new tokens on Spider test.
  k = 2 is the k of the 1.5B and is not chosen again per model. Plain
  tasks, not curves, so the four FedAvg SFT rounds run whatever their
  gain.
- Names: tags `qwen05b` and `dsc13b`. Roots
  `fedavg_<tag>_base_ddlrows_alpha01_s0` and
  `fedpref_<tag>_sftr2_p2_ddlrows_alpha01_s0`, stage labels
  `fedavg_<tag>_ddl_rows_a01_r{k}_s0`, arms `zs_<tag>_ddl_rows_vllm_inproc`,
  `fedavg_<tag>_ddl_rows_a01_r{k}_vllm_inproc` and
  `fedpref_<tag>_sftr2_p2_dpo_ddl_rows_a01_r{k}_vllm_inproc`.
- Order in the queue, after `bird_sft/round_4`: the probe of each model
  (it downloads the model, which the vLLM tasks then read from the cache
  only, and runs two training steps on each of the 4 longest rows,
  failing above 21.5 GiB reserved), the base model of each on Spider
  test, the 0.5B line, the DeepSeek line. Inside a line: FedAvg SFT
  rounds 1 and 2, DPO + NLL round 1, FedAvg SFT round 3 (the read at 3
  rounds), DPO + NLL round 2, FedAvg SFT round 4 (the read at 4 rounds).

Corrected the same day (entry above): the DeepSeek rows of this entry
(prompt and target, lengths, memory and time estimates) came from a
tokenizer that dropped whitespace and do not hold; the tag `dsc13b` is
not used for results.

Checked on the Mac before queuing:

| Check | Result |
|---|---|
| Resolved commands against the 1.5B line (FedAvg SFT rounds 1 and 3, DPO rounds 1 and 2, their evaluations, the base row) | only the model, the stage label, the roots and the arm names differ; `--model` is on every command, the evaluations included |
| The 54 new commands through their own argument parsers | all parse |
| The 161 tasks and 8 curves already in the file | resolve to the same commands as before (`SFT` is now the model plus `SFT_RECIPE`) |
| Rendered prompt and target, 0.5B | the ChatML template and system line of the 1.5B; the target ends with `<|im_end|>` |
| Rendered prompt and target, DeepSeek | its template: the begin-of-sentence token, its own system sentence ("You are an AI programming assistant, utilizing the Deepseek Coder model, ..."), `### Instruction:`, the prompt, `### Response:`; the target ends with `<|EOT|>` (32021); the prompt ids of the template equal those of the rendered text, which is what sampling sends |
| Training guards of `_assemble` (prompt is a prefix, answer ends with EOS) | pass on all 8,659 Spider client rows with both tokenizers |
| Lengths as training renders them, 8,659 rows | Qwen tokenizer: longest 6,927 (`train:3698`, `baseball_1`), median 821; DeepSeek: longest 6,070, median 909; none above 7,168. Longest per client 1 to 5: 2,658 / 3,900 / 6,927 / 3,082 / 3,638 and 2,974 / 4,339 / 6,070 / 3,405 / 3,967 |
| Test suite of the code repository | 541 passed |

Not checked, and where it shows: memory and time of both models (the
probes, then each round's record); that the server downloads the models
(the probes); that vLLM in WSL loads DeepSeek (its base row) and its
LoRA adapters (`dsc13b_sft/eval_1`). A failed task stops the worker,
the other model's line included.

Memory before the probes (estimate): at batch 1 the 1.5B's need on a
long row is carried by the float32 attention tensors, heads x length
squared (`A5000_RUN_CONFIG.md`: 14.4 GiB allocated at 7,601 tokens, and
the out-of-memory pass of 2 rows x 12 heads x 7,290 squared). One tensor
at the longest row: 1.5B 12 x 6,927 squared, 2.14 GiB; 0.5B 14 heads,
2.50 GiB; DeepSeek 16 x 6,070 squared, 2.20 GiB. With about 4.4 such
tensors and the weights, all three come to about 12 to 12.5 GiB
allocated. The 0.5B is therefore not below the 1.5B (peak reserved
19.83 GiB, which includes the allocator's cache).

Time (estimate, nothing measured): the 0.5B about 1 h per FedAvg SFT
round and 1.5 to 2 h per DPO round, about 8 h for the line; DeepSeek
about 2 h and 3 h, about 15 h. The 1.5B's client training took 2.04,
2.09, 2.11 and 2.19 h in rounds 1 to 4 (`metrics.json` of the rounds).

## 2026-11-22: `bird_k2/round_1`, one DPO + NLL round from FedAvg SFT round 2 on BIRD: 46.22, 2.54 above FedAvg SFT at 3 rounds (p 0.0087)

Run `eval_arms__s0__20261122T023449__df23a1e4c235__f80957af63534196bb45a975405e3a61`,
arm `fedpref_bird_sftr2_p2_dpo_ddl_a01_r1_vllm_inproc`, round record
`audits/protocol_v2/fedpref_bird_sftr2_p2_ddl_alpha01_s0/dpo/round_1/`;
round `bc0837cb` (09:28), evaluation `7e36808c` (09:34). Read on the Mac
from the committed predictions at 09:53. k = 2 was the k of the best
Spider line and was set before this read (queued 2026-11-21); no round
or setting of this row was chosen on BIRD dev.

| Row | Rounds | BIRD dev EX | Simple (925) | Moderate (464) | Challenging (145) | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| FedAvg SFT round 2 (its start) | 2 | 42.70 | 50.49 | 31.25 | 29.66 | 286 | 593 |
| FedAvg SFT round 3 | 3 | 43.68 | 51.57 | 32.54 | 28.97 | 276 | 588 |
| k = 0 round 2 | 2 | 43.02 | 50.70 | 35.13 | 19.31 | 250 | 624 |
| k = 1 | 2 | 44.26 | 50.38 | 37.07 | 28.28 | 127 | 728 |
| k = 2 (`bird_k2/round_1`) | 3 | 46.22 | 53.08 | 36.85 | 32.41 | 102 | 723 |

Exact McNemar, k = 2 against:

| Row | Only k = 2 right | Only the other right | Difference | p | Simple | Moderate | Challenging |
|---|---|---|---|---|---|---|---|
| FedAvg SFT round 3 (equal rounds) | 125 | 86 | +2.54 | 0.0087 | 71 / 57, p 0.25 | 41 / 21, p 0.015 | 13 / 8, p 0.38 |
| FedAvg SFT round 2 (its start) | 135 | 81 | +3.52 | 0.0003 | 75 / 51, p 0.040 | 46 / 20, p 0.0019 | 14 / 10, p 0.54 |
| k = 1 (2 rounds) | 106 | 76 | +1.96 | 0.031 | 62 / 37, p 0.015 | 32 / 33 | 12 / 6, p 0.24 |
| k = 0 round 2 (2 rounds) | 151 | 102 | +3.19 | 0.0025 | 78 / 56, p 0.069 | 51 / 43, p 0.47 | 22 / 3, p 0.0002 |

- The read of the table in `PIPELINE_NEXT.md` ("`bird_k2/round_1` above
  `bird_sft/round_3`"): yes by the rule (0.5 EX or more, p below 0.05).
  The first gain over FedAvg SFT at equal rounds from an SFT start that
  is separated on BIRD; the method stands at k = 2 on both datasets
  (Spider test 78.20 against 74.71 at 4 rounds).
- All three difficulty levels are above FedAvg SFT round 3, the
  moderate one separated. The challenging level, which fell from the
  base start (19.31 at k = 0 round 2), is 32.41.
- From the same start the DPO + NLL round fixes 135 answers and breaks
  81, the SFT round 45 and 30. As before, the round removes execution
  errors (286 to 102) and leaves more wrong results (593 to 723).
- Tables and columns against the gold's (session read, as in the entry
  below): predictions on the gold's tables and columns 718 (FedAvg SFT
  round 3: 715), EX on those 74.5 (74.8); predictions on the gold's
  tables 1,081 (1,020); EX on the rest 21.3 (16.5). The gain over
  FedAvg SFT is again in right answers on other tables or columns.
- The round: 11,754 pairs (2,726 / 1,922 / 2,758 / 782 / 3,566; the
  rejected side an execution error in 6,616 and a wrong result in
  5,138), 737 updates. Of the 9,428 questions 5,877 are mixed, 2,698
  have no correct sample (3,220 after one SFT round, 3,017 after one
  DPO round from the base student), 416 have only correct ones, 437
  have a gold that does not run. 87 golds met the 30 s budget (50 in
  `bird_k1/round_1`, 72 in `bird_k0/round_2`). Sample accuracy 32.7%.
- Measured: 7 h 50 min (sampling 28 min, labels 2 h 39 min in 5 calls,
  reference 1 h 01 min, updates 3 h 41 min); peak reserved 17.39 / 12.74
  / 17.39 / 17.45 / 18.90 GiB; evaluation 6 min. The labels took 2 h 39
  min, not the 1.5 h estimated after code `0910b84f`. Written into
  `fedicl-sql/docs/A5000_RUN_CONFIG.md`.
- Card: `bird_sft/round_4` is next in file order, so since about 09:35;
  not confirmed (about 3 h, estimate).
- Session estimates after this read (judgement): the method above
  FedAvg SFT at 4 rounds on BIRD 90%, separated 65%. For the paper the
  largest open item is now the gain on a second and a third model.
- Not decided (owner): the slot after `bird_sft/round_4`. The session's
  earlier proposal for a separated read sends the card to FedAvg SFT of
  a second model on Spider; the two reviewers' order runs
  `bird_k2/round_2` and its fixed-pair twin first.

## 2026-11-22: `bird_sft/round_3`, FedAvg SFT on BIRD at 3 rounds: 43.68, 0.98 above round 2

Run `eval_arms__s0__20261121T183455__16c32a3b85ca__8893c69d683e424a84065861a15f57d1`,
arm `fedavg_bird_ddl_a01_r3_vllm_inproc`, round record
`federated__fedavg__s0__7ecd649662f3__5e43d16b__r3`; round `94c2966f`
(01:28), evaluation `f5b4eba2` (01:35). Read on the Mac from the
committed predictions at 08:35. Errors are the committed `exec_errors`
field (timeouts included).

| Row | Rounds | BIRD dev EX | Simple (925) | Moderate (464) | Challenging (145) | Execution errors | Wrong results |
|---|---|---|---|---|---|---|---|
| FedAvg SFT round 1 | 1 | 38.85 | 46.16 | 28.66 | 24.83 | 372 | 566 |
| FedAvg SFT round 2 | 2 | 42.70 | 50.49 | 31.25 | 29.66 | 286 | 593 |
| FedAvg SFT round 3 | 3 | 43.68 | 51.57 | 32.54 | 28.97 | 276 | 588 |
| k = 0 round 2 | 2 | 43.02 | 50.70 | 35.13 | 19.31 | 250 | 624 |
| k = 1 | 2 | 44.26 | 50.38 | 37.07 | 28.28 | 127 | 728 |

Exact McNemar, FedAvg SFT round 3 against:

| Row | Only round 3 right | Only the other right | Difference | p |
|---|---|---|---|---|
| FedAvg SFT round 2 (its start) | 45 | 30 | +0.98 | 0.11 |
| FedAvg SFT round 1 | 126 | 52 | +4.82 | below 0.0001 |
| k = 1 (2 rounds) | 117 | 126 | -0.59 | 0.61 |
| k = 0 round 2 | 141 | 131 | +0.65 | 0.59 |

- FedAvg SFT slows on BIRD: +9.38, +3.85, +0.98 over rounds 1 to 3. On
  Spider test it added +1.67, +0.61 and 0 after round 1. By difficulty
  the third round moves the simple questions by 27 against 17, the
  moderate by 15 against 9, the challenging by 3 against 4.
- k = 1 at 2 rounds is level with FedAvg SFT at 3 rounds, on the
  method's side (0.59, p 0.61); on the moderate questions it is above
  (50 against 29, p 0.024), level on the simple (65 against 76) and the
  challenging (11 against 12). Against k = 0 round 2, FedAvg SFT round 3
  is above on the challenging questions (18 against 4, p 0.0043).
- The bar of `bird_k2/round_1` (one DPO + NLL round from FedAvg SFT
  round 2, 3 rounds in all) is 43.68; a separated gain is about 45.8.
  The round has to add about 3.1 to its start (42.70). One DPO + NLL
  round added 5.41 from FedAvg SFT round 1 on BIRD and 3.36 from round
  2 on Spider.
- Measured: rounds 1 and 2 took 2 h 54 min and 2 h 48 min (round wall
  time); round 3 was stopped for the gold-row round and continued, its
  last call ran 2 h 40 min with client 1 from row 1,040 (the record
  marks the time as not that of the round). Peak reserved 19.84 GiB in
  rounds 1 and 2 and 19.86 GiB in round 3, on client 5. Evaluation 6
  min. Written into `fedicl-sql/docs/A5000_RUN_CONFIG.md`.
- Card: `bird_k2/round_1` is next in file order, so since about 01:36;
  not confirmed, and nothing of it was on the remote at 08:35 (6.5 to 8
  h, estimate: read between 08:15 and 09:45).
- Session estimate after this read (judgement): `bird_k2/round_1` above
  `bird_sft/round_3` 90%, separated 50 to 55% (85% and 50% before it:
  the baseline moved less than a point).

## 2026-11-22: a third reviewer's independent proposal, a plan line before the SQL (not decided); the read behind it checked (no new run)

Owner's request (00:10): a third reviewer agent with an independent
view, not bound to the directions or results so far, for a method with
high EX on BIRD and Spider. It wrote its own list from the task and a
literature search first, then checked it against the notes; read-only.
Its texts were in the session's temporary folder and are not kept.

Proposal (reviewer C). Keep the loop (FedAvg SFT stage, then on-policy
DPO + NLL rounds) and change what the student writes: two comment lines
that name the tables and columns it will use, then the SQL. The plan of
a training row is parsed from the gold SQL (`gold_tables_columns`), no
model writes it. SFT rounds train on plan + gold SQL, the DPO rounds
sample plan + SQL; one prompt, one greedy call at test. Optional second
part: an all-wrong question is sampled again with its gold plan forced
as the start of the output, which is the hint without a second prompt.
Story: execution tells a client that a SQL is wrong, not where; a
stated plan puts the choice of tables and columns under the preference
term.

- C's first experiment: FedAvg SFT round 1 on BIRD in the new format (2
  h 50 min), stop under 36.8 against 38.85 for SQL-only; then one DPO +
  NLL round from it (about 8 h), continue at 44.8 or more on BIRD dev
  (2.1 over FedAvg SFT round 2), stop at 44.26 or less.
- C's estimates: +2 to +4 over FedAvg SFT on BIRD dev; 0.45 for a
  separated gain over FedAvg SFT, 0.30 over FedAvg SFT in the same
  output format; about 60 GPU hours for the rows in the new format, 115
  with the rest the paper needs.
- It needs a target builder, a new answer line in the prompt (the
  present one asks for the SQL only) and 320 new tokens. Every row would
  run again in the new format; the present rows become the ablation
  without a plan.
- C's other candidates, each of which lifts every row: example values
  and column descriptions in the BIRD prompt; execution at inference
  (fallback or a vote).
- C would stop new variants inside the SQL-only round and hold
  `bird_k2/round_2`, its fixed-pair twin and the other models until the
  first experiment is read; `bird_sft/round_3` and `bird_k2/round_1`
  stay as the SQL-only reference.
- Papers C names, none checked again by the session: Liu et al., arXiv
  2502.11656 (C: read in the paper; on BIRD dev DPO moves ten models by
  -1.3 to +0.8 with SQL-only output and +0.8 to +4.5 with reasoning; it
  is in `DPO_RESEARCH.md`); CodeS 2402.16347, CSC-SQL 2505.13271,
  SLM-SQL 2507.22478, GradeSQL 2509.01308 (C: read in the paper); ExCoT
  2503.19988 (abstract).

Checked by the session on the committed predictions (BIRD dev; the
tables and `table.column` names of a SQL read with `gold_tables_columns`
and the database's schema, both sets equal to the gold's; C compared
unqualified names, so C's counts are higher):

| Row | EX | Predictions on the gold's tables and columns | EX on those | EX on the rest |
|---|---|---|---|---|
| Base student | 29.47 | 459 | 72.5 | 11.1 |
| FedAvg SFT round 1 | 38.85 | 621 | 75.4 | 14.0 |
| FedAvg SFT round 2 | 42.70 | 690 | 75.2 | 16.1 |
| k = 0 round 1 | 41.85 | 627 | 74.2 | 19.5 |
| k = 0 round 2 | 43.02 | 628 | 74.7 | 21.1 |
| k = 1 | 44.26 | 699 | 73.4 | 19.9 |
| k = 0 round 2 with gold rows | 42.37 | 616 | 74.0 | 21.1 |

- Holds: a prediction on the gold's tables and columns is right in 72
  to 75% of cases in every row, a prediction on others in 11 to 21%. At
  FedAvg SFT round 2, 844 of the 1,534 predictions are in the second
  group.
- Does not hold as C words it ("SFT rounds raise that count, DPO rounds
  do not"): from the same parent a first DPO round raises it as much as
  an SFT round (459 to 627 against 621; 621 to 699 against 690). The
  second DPO round from the base student leaves it where it was (627 to
  628).
- At equal rounds the gain of the DPO lines over FedAvg SFT sits in the
  second group (EX 19.5 to 21.1 against 14.0 to 16.1): answers on other
  tables or columns that return the gold result. In line with the
  test-suite read of 2026-11-21.
- Not checked: C's counts of `no such column` errors and of string
  literals; whether a plan line costs this student accuracy (before the
  reset a long plan was 9 points under SQL-only on Spider test,
  reference only).

Session view, not decided (owner): the first proposal that changes what
the student writes and not what a round trains on, with a short first
step (one FedAvg SFT round after the code). It goes against the setup
row "SQL-only output: fixed" and changes the prompt. Open: whether the
plan lifts the method more than it lifts FedAvg SFT in the same format
(C: 0.30).

The three reviewers on the proposal (01:00 to 01:25; owner's question:
are the odds and the basis too low). A and B critiqued it, C answered
the check above; read-only, their texts are not kept.

| Probability, BIRD dev | A | B | C before | C after | Session |
|---|---|---|---|---|---|
| Plan-first FedAvg SFT round 1 at 36.8 or more | 0.65 | 0.75 | none | 0.70 | none |
| Plan-first method separated from SQL-only FedAvg SFT | 0.30 | 0.35 | 0.45 | 0.30 | 0.30 |
| Plan-first method separated from plan-first FedAvg SFT | 0.40 | 0.30 | 0.30 | 0.10 (0.15 with the forced gold plan) | 0.15 to 0.20 |
| The plan adds a separated gain to the method as it stands | 0.15 | "none" | none | none | none |

- C accepts the check and withdraws "the plan makes the method gain
  more over FedAvg SFT": no number supports it. All three: the plan is
  an ordering of names the SQL already shows, not new supervision; not
  the main improvement; at most one gated experiment.
- A and B find the session's 0.15 to 0.20 too low: that row is the
  method's own question in another format (their 0.40 to 0.45 at 3
  rounds), less a risk from the format. C went lower for another
  reason, the 439 against 439 below.
- Counts they give, checked by the session on the committed
  predictions (BIRD dev, from FedAvg SFT round 1):

| | Fixes | of them with other tables or columns than the parent's answer | landing on the gold's | Breaks | with other tables or columns | from the gold's set | into an execution error |
|---|---|---|---|---|---|---|---|
| DPO + NLL round (k = 1) | 173 | 150 | 119 | 90 | 68 | 60 | 11 |
| SFT round (FedAvg SFT round 2) | 98 | 85 | 72 | 39 | 27 | 27 | 15 |

- Wrong answers by where they differ from the gold: k = 1 (855): other
  tables 402, the gold's tables with other columns 257, the gold's
  tables and columns 186, not parsed 10. FedAvg SFT round 2 (879): 479,
  227, 171, 2. Predictions on the gold's tables: base 840, FedAvg SFT
  944 and 996 at rounds 1 and 2, k = 0 1,035 and 1,050, k = 1 1,062: a
  DPO round moves the tables more than an SFT round, the columns as
  much.
- Where the method's gain over FedAvg SFT at two rounds sits: right
  answers on the gold's tables and columns 513 against 519; right
  answers on other tables or columns 166 against 136. On the 561
  questions where both rows use the gold's set each solves 439.
- C's closing point: the room is in what a DPO round breaks (90 against
  39 for an SFT round from the same parent; 79 of the 90 end in a wrong
  result, 56 of the 90 are simple questions). With the SFT round's 39 breaks
  the k = 1 row would stand 3.3 points higher; that is a ceiling, not an
  estimate. The merge probe already in the reviewers' order is the
  short read of it.
- Papers: Liu et al., arXiv 2502.11656, read in the paper by A, B and C
  (Table 1: DPO over SFT in one format, -1.3 to +0.8 SQL-only and +0.8
  to +4.5 with reasoning, on 6.7B to 15B models with about 400 tokens
  of reasoning from GPT-4o-mini; reasoning SFT is below SQL-only SFT
  for both Qwen2.5 7B models; Table 3, 7B: table errors fixed 13.0%
  with SQL-only DPO and 15.9% with reasoning, columns 10.3% and 16.1%).
  Its SQL-only DPO gains nothing where ours gains (k = 0 round 1 is
  3.00 over FedAvg SFT round 1, k = 1 is 1.56 over round 2). DTS-SQL,
  arXiv 2402.01117 (C: read in the paper; a separate 7B model for the
  tables, Spider dev 71.9 to 78.6). C's one search found no paper with
  the plan in the output of a fine-tuned model under 3B. ExCoT:
  abstract only; CodeS and RESDSQL: from memory (B). None read again by
  the session.
- Not checked by the session: A's 86.6% of 3,810 right and wrong
  answers of one question that differ in tables or columns (the
  session's count over three rows: 517 of 630, 82.1%); C's token
  position of the first difference; B's 13.2% and 1.65% of samples.
- Proposed, not decided (owner): an oracle read before any plan-first
  training (B, C): the FedAvg SFT round 2 and k = 1 adapters on BIRD
  dev with the gold SQL's tables and columns as a hint line, 7 to 15
  minutes of evaluation after a small change to the evaluation script,
  notes only (the dev gold is in the prompt). B: under +8 EX, drop the
  plan. C expects its own bar to fail. Order on the card: A puts C's
  first step after `bird_k2/round_1`, B only after the oracle read
  passes; neither holds `bird_k2/round_2` or its fixed-pair twin.

## 2026-11-21: `bird_k0_goldnll/round_2`, NLL on the gold SQL of the all-wrong questions next to the pairs: 42.37, not above the round without it

Run `eval_arms__s0__20261121T154802__f90b5cf8d781__dd596c44cd1a4904be3aa733fdbaf809`,
result commits `d69684ea` (round, 22:40) and `1a75d23e` (evaluation,
22:48), arm `fedpref_bird_base_p2_goldnll_dpo_ddl_a01_r2_vllm_inproc`.
Round 2 from `bird_k0/round_1` on the 8,840 pairs of `bird_k0/round_2`
plus one row with the gold SQL and the NLL term alone for each of its
3,017 all-wrong questions (pairs + gold rows per client: 1,992 + 625,
1,516 + 595, 2,150 + 641, 552 + 284, 2,630 + 872; FedAvg weights by
rows).

BIRD dev (1,534 rows), by official difficulty:

| Row | EX | Simple (925) | Moderate (464) | Challenging (145) |
|---|---|---|---|---|
| FedAvg SFT round 2 | 42.70 | 50.49 | 31.25 | 29.66 |
| `bird_k0/round_1`, the parent | 41.85 | 50.16 | 31.25 | 22.76 |
| `bird_k0/round_2`, the same pairs without gold rows | 43.02 | 50.70 | 35.13 | 19.31 |
| `bird_k0_goldnll/round_2` | 42.37 | 49.73 | 33.41 | 24.14 |
| `bird_k1/round_1` (1 SFT round, then DPO + NLL) | 44.26 | 50.38 | 37.07 | 28.28 |

Exact McNemar (questions only the gold-row round has / only the other):

| Against | All | Simple | Moderate | Challenging |
|---|---|---|---|---|
| `bird_k0/round_2` | 59 / 69, -0.65, p 0.43 | 32 / 41, 0.35 | 19 / 27, 0.30 | 8 / 1, 0.039 |
| FedAvg SFT round 2 | 118 / 123, -0.33, p 0.80 | 66 / 73, 0.61 | 43 / 33, 0.30 | 9 / 17, 0.17 |
| `bird_k1/round_1` | 83 / 112, -1.89, p 0.045 | 54 / 60, 0.64 | 22 / 39, 0.040 | 7 / 13, 0.26 |
| its parent | 89 / 81, +0.52, p 0.59 | 47 / 51, 0.76 | 32 / 22, 0.22 | 10 / 8, 0.81 |

- From the shared parent (642 correct answers) the round without gold
  rows fixes 85 and breaks 67, 28 of them into execution errors; with the
  gold rows 89 and 81, 41 into execution errors. Execution errors
  (`exec_errors` of the results, timeouts included): 219 at the parent,
  250 without the gold rows, 298 with them.
- The gold rows do what they were added for on the challenging level (8
  questions against 1), half way to FedAvg SFT, and lose more on the two
  other levels. Against the rule of the queue table (above 43.02, the
  challenging level near 29.66, the simple one not below 50.70): no on
  each. The one-loss form is not kept.
- At the same total rounds the line with an SFT stage (k = 1) is 1.89
  above it. Gold SQL helps as a stage before the DPO rounds; inside a DPO
  round it has not helped in either form tried on BIRD (chosen side of a
  pair -2.61, NLL rows -0.65).
- Spider: no round with gold rows was run and none is queued.
- Measured (`round.json`, `client_*_train.json`): training 4 h 52 min
  for 743 updates (reference pass 1 h 07 min, updates 3 h 44 min; the
  estimate was 4.5 h), 6 calls, started 16:08 and published 22:40; peak
  reserved 17.72 / 17.14 / 17.79 / 17.43 / 18.96 GiB for clients 1 to 5,
  budget never lowered; evaluation 7 min.
- Cards (owner, chat, about 22:20): one card only. Nothing of
  `bird_sft/round_3` is published at 23:30, and a round takes 2 h 50
  min: it did not run through on GPU 0 from 18:06, as the status of
  18:25 assumed. The worker takes `bird_sft/round_3`, `bird_k2/round_1`
  and `bird_sft/round_4` in file order; not confirmed after 22:48.

Proposed in chat, not decided (owner):

1. Gold rows for every question (part 2 of what the reviewers signed,
   entry below) are not written. Their reason was fewer broken answers,
   and here the gold rows raised them (81 against 67).
2. After `bird_k2/round_1`: above `bird_sft/round_3` without a
   separation, `bird_k2/round_2` runs before any new part (the method at
   4 rounds; its fixed-pair twin later); separated, the card goes to a
   second model on Spider; below, stop and read.
3. The hinted round stays open. For it: the queue table names it as the
   remaining form. Against it: the gold rows covered all 3,017 all-wrong
   questions and moved the challenging level by 7 questions net, the hint
   reaches about a third of them, and with an SFT stage that level is
   already at 28.28 against 29.66.

Estimates given in chat of a gain separated on BIRD dev (about 2.1 EX, p
below 0.05), judgement and not measurement: the method as it stands at 3
rounds 50%, at 4 rounds 55%, either of the two 60 to 65%; on-policy
rounds over fixed pairs from an SFT start 55%; the hinted round 10 to
15%; gold rows for every question 10 to 15%; verified positives 15%.
Before this result the gold rows for the all-wrong questions were given
30%, the same for every question 30% and the hint 25%.

The two reviewers asked again (23:50, the owner's question; two new
agents, each given that reviewer's last text, the joint text of the
entry below and the two results of the evening; read-only, each answered
alone). Chance of a gain separated on BIRD dev / of a gain at all:

| Direction | Reviewer A | Reviewer B | Verdict of both |
|---|---|---|---|
| The method with the SFT stage at 3 rounds (`bird_k2/round_1` against `bird_sft/round_3`) | 0.40 / 0.85 | 0.45 / 0.85 | goes on (both had 0.55) |
| The same at 4 rounds (`bird_k2/round_2`) | 0.50 / 0.85 | 0.45 / 0.80 | goes on, with its fixed-pair twin (A: 0.35 / 0.75 for the twin) |
| A round with hinted pairs | 0.12 / 0.45 | 0.12 / 0.50 | last; a table row, if the owner allows the second prompt |
| The probe that adds the two updates | 0.08 at 46.0 | 0.15 at 45.3 | kept: about 0.3 h of evaluation (needs a script); it only decides whether the row below gets a run |
| Gold rows for every question | 0.10 / 0.35 | 0.10 / 0.30 | dropped unless the probe passes |
| Verified positives | 0.05 / 0.25 | 0.05 / 0.30 | dropped |

- Both close part 2 of their text (gold SQL as an NLL target inside the
  rounds) as the main improvement: its reason was fewer broken answers,
  and the gold rows raised them (81 against 67).
- Both add a second model on Spider, as what CMC asks for.
- A: with one DPO round the on-policy line and the fixed-pair line train
  on the same pairs, so only the second DPO round from an SFT start can
  show the method above federated DPO as published.
- The same order on one card from both, 37 to 41 h (estimate):
  `bird_sft/round_3`; `bird_k2/round_1` (below `bird_sft/round_3`: stop
  and read); the probe; `bird_sft/round_4`; `bird_k2/round_2`; its
  fixed-pair twin; a second model on Spider; the hinted round.
- Main improvement in both texts: on-policy DPO + NLL rounds with
  execution labels after a FedAvg SFT stage, gold SQL and execution in
  separate rounds. Still needed: a separated gain over FedAvg SFT on
  BIRD at equal rounds (k = 1: +1.56, p 0.13).
- Not agreed: the bar of the probe (46.0 or 45.3).

## 2026-11-21: test-suite accuracy of the Spider rows: the line from the base student keeps no gain, the line with an SFT stage does; what a DPO round breaks (no new run)

Read on the Mac from the committed predictions; none of it is a committed
result yet. The counts come from a discussion of two reviewer agents the
owner asked for (federated learning; Text-to-SQL); each one below was run
again by the session that logs it.

Test-suite accuracy (Zhong et al. 2020; the project's judge,
`fedls_sql/eval/test_suite.py`: correct on the original database and on
every suite database of the db_id). The suite holds the 20 Spider dev
databases, so it covers dev, Syn, Realistic and 408 of the 535 DK rows.

| Set | Base student | FedAvg SFT round 4 | Centralized SFT epoch 2 | k = 0 round 4 | k = 2 | k = 2 on fixed pairs |
|---|---|---|---|---|---|---|
| Spider dev (1,034) | 58.32 | 67.99 | 66.44 | 67.21 | 70.41 | 69.44 |
| Syn (1,034) | 46.23 | 51.84 | 53.09 | 51.35 | 55.51 | 54.06 |
| Realistic (508) | 51.18 | 58.86 | 58.86 | 57.09 | 62.20 | 61.22 |
| DK (408 rows) | 50.74 | 53.19 | 50.98 | 55.39 | 55.15 | 56.37 |

Exact McNemar on the suite verdicts (questions only the first line has /
only the second, p):

| Comparison | Spider dev | Syn | Realistic | DK |
|---|---|---|---|---|
| k = 0 against FedAvg SFT | 74 / 82, 0.58 | 85 / 90, 0.76 | 40 / 49, 0.40 | 36 / 27, 0.31 |
| k = 2 against FedAvg SFT | 72 / 47, 0.027 | 75 / 37, 0.0004 | 38 / 21, 0.036 | 25 / 17, 0.28 |
| k = 2 against k = 0 | 95 / 62, 0.010 | 109 / 66, 0.0014 | 56 / 30, 0.0067 | 26 / 27, 1.0 |
| k = 2 against fixed pairs | 35 / 25, 0.25 | 40 / 25, 0.082 | 18 / 13, 0.47 | 7 / 12, 0.36 |
| k = 2 against centralized SFT | 96 / 55, 0.0011 | 92 / 67, 0.057 | 47 / 30, 0.068 | 36 / 19, 0.030 |
| FedAvg SFT against the base student | 148 / 48, <0.0001 | 128 / 70, <0.0001 | 68 / 29, 0.0001 | 37 / 27, 0.26 |

- The line from the base student (k = 0) has no gain over FedAvg SFT on
  the suite; the line with the SFT stage (k = 2) keeps 2.42, 3.67 and 3.34
  on dev, Syn and Realistic. On EX the two lines are level (dev: 69 / 65,
  p 0.80). "The FedAvg SFT stage gives no gain on Spider" holds for test
  EX alone.
- The entry on the variant rows says FedAvg SFT is not separated from the
  base student on Syn and Realistic: that is EX. On the suite it is above.
- Limits: Syn and Realistic reuse the databases and gold SQL of dev;
  Spider test and BIRD have no suite; on DK nothing is separated.
- To commit it: `scripts/score_test_suite.py` on the six prediction files
  of each set (CPU, about a minute a set on the Mac); the owner's yes.

What a round breaks. BIRD dev, both rounds from FedAvg SFT round 1: the
DPO + NLL round (`bird_k1/round_1`) fixes 173 questions (98 of them
execution errors) and breaks 90 (79 into wrong results); the SFT round
fixes 98 and breaks 39. From the base student the two break the same (64
and 65) and the DPO round fixes more (254, 198 of them execution errors,
against 209 and 155).

Spider test, one round from FedAvg SFT round 2 (1,591 correct answers),
the same samples and pairs:

| Round | Correct answers written differently | Broken | Fixed |
|---|---|---|---|
| NLL on the model's own correct samples | 6.0% | 21 | 59 |
| Preference term alone | 36.5% | 168 | 157 |
| DPO + NLL | 19.4% | 74 | 146 |
| FedAvg SFT round 3 | 14.4% | 48 | 61 |

The preference term makes the fixes and the breaks; the NLL term holds
the rewriting down.

Decision (owner, 2026-11-21): questions without gold SQL are not a
setting of this paper (a client without gold SQL would have no questions
either). Item 12c of `RESEARCH_STATE.md` is skipped.

What the two reviewers signed (a proposal, not approved):

1. The method keeps the FedAvg SFT stage; k is printed with its ablation
   and k = 0 is an ablation row; the Spider tables carry a test-suite
   column for dev, Syn and Realistic, DK without a claim.
2. Candidate main part: the gold SQL as an NLL target for every question
   inside each DPO round, outside the preference term, in one local loss
   next to the NLL on the model's own sample. `bird_k0_goldnll` does it
   for the all-wrong questions only, and a null there does not close it:
   the breaks sit on questions the model already answers. First run: one
   round from `bird_sft/round_1` on the stored samples of
   `bird_k1/round_1` (about 6.5 h, estimate; needs a gold row for every
   question), kept at 45.3 or more on BIRD dev with at most 60 broken
   answers, and read against `bird_sft/round_4` for equal compute.
3. Controls and rows: a chosen side that also carries the tables and
   join keys of the gold SQL, after a CPU probe on the stored samples;
   centralized DPO + NLL from the SFT start and local-only; the hint as a
   table row at best (it samples under a prompt that training and testing
   never use).
4. Dropped: other aggregation weights, k decided by client counts,
   pairs anchored on the greedy output.

Not agreed: an evaluation-only probe that adds the updates of
`bird_sft/round_2` and `bird_k1/round_1` to their parent (go at 45.3 or
at 46.0); the weight of the gold rows (1 or 4). Their estimates of a
separated gain on BIRD: 0.20 to 0.35 for part 2, 0.55 for
`bird_k2/round_1` against `bird_sft/round_3`.

Papers the agents read by page fetch; title and abstract checked here,
the numbers inside them not: arXiv 2410.15483 (Fernando et al.:
sequential SFT then preference learning forgets the first stage, joint
training instead), 2505.12380 (Graph-Reward-SQL), 2603.20004 (verified
BIRD training data), 2609.04697 (SQL-Zero), 2610.11502 (Fed-GRPO).

## 2026-11-21: control of the hint probe: the hint adds 21.4 points of all-wrong questions with a correct sample

`.../hint_probe/r2_740967ede559a725_nohint.json`, result commit `10c65a49`
(18:05) on code `7e8a9a2e`. The all-wrong questions of `bird_k0/round_2`
on clients 1, 3 and 4 (1,550 of the 3,017), sampled again as in the probe
without the hint line.

| Client | Questions | With the hint | Without | Difference | Sample accuracy with / without |
|---|---|---|---|---|---|
| 1 | 625 | 31.7% | 11.0% | 20.6 | 12.8% / 1.8% |
| 3 | 641 | 30.4% | 9.4% | 21.1 | 11.9% / 1.6% |
| 4 | 284 | 34.9% | 11.3% | 23.6 | 15.9% / 1.5% |
| All three | 1,550 | 31.7% | 10.4% | 21.4 | 13.0% / 1.6% |

- Per question: a correct sample in both draws 114, with the hint only
  378, without it only 47, in neither 1,011. Exact McNemar p 2.5e-65;
  difference 21.4 points, 95% interval 19.0 to 23.7.
- A second draw alone gives 10.4% of these questions a correct sample at
  a sample accuracy of 1.6% (the Beta estimate of the entry below: 11 to
  16% and 2%). The hint's own part is 21.4 points: under the 25 points
  proposed as the bar for a training round with hinted pairs, above 0
  beyond doubt. At that rate on the 3,017 questions: about 640 questions
  from the hint, about 310 from the second draw.
- 65% of the questions have no correct sample in either draw.
- Time: 43 min (generation step 10 min, labels 24, 6 and 2 min). The
  generation step has two start lines (17:22:03, 17:23:45): the task was
  started twice.
- Not decided (owner): the hinted round. Proposed in chat: no code for it
  until `bird_k0_goldnll/round_2` is read; the gold rows cover all 3,017
  questions without a second sampling, and the hint is worth a round only
  if that row leaves the challenging level low.

## 2026-11-21: hint probe: 32.6% of the all-wrong questions hold a correct sample with the hint (control pending)

`audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_ev3_s0/hint_probe/r2_740967ede559a725.json`,
result commit `fcbd86b7` (17:21) on code `7e8a9a2e`. The 3,017 all-wrong
questions of `bird_k0/round_2`, sampled again from its round 1 global
adapter, 10 samples at T 1.0, with the tables and columns of the gold SQL
in one line after the question (2.1 tables and 5.0 columns on average).

| Client | All wrong before | With a correct sample | Share | Sample accuracy |
|---|---|---|---|---|
| 1 | 625 | 198 | 31.7% | 12.8% |
| 2 | 595 | 198 | 33.3% | 12.8% |
| 3 | 641 | 195 | 30.4% | 11.9% |
| 4 | 284 | 99 | 34.9% | 15.9% |
| 5 | 872 | 294 | 33.7% | 13.9% |
| All | 3,017 | 984 | 32.6% | 13.2% |

- Of the 984, 918 are mixed (they would give pairs: 1,836 at 2 a
  question, next to the round's 8,840) and 66 all correct. 2,026 stay all
  wrong and 7 lost their gold to the 30 s budget in this run.
- Samples: 3,983 correct of 30,170; 18,904 wrong results, 6,645 execution
  errors, 545 cut at 256 tokens. 355 of the correct samples (8.9%) equal
  the gold SQL after normalisation; mean similarity to the gold 0.75. The
  hint does not make the model copy the gold.
- Not read from this number: how much of the 32.6% the hint adds. The
  draw uses other seeds than the round, so some questions get a correct
  sample without a hint; the control on clients 1, 3 and 4 (queued, entry
  below) measures that share.
- Time: 1 h 36 min (generation step 17 min, labels 1 h 19 min; 24, 25, 5,
  4 and 21 min for clients 1 to 5), with the gold-row round training on
  the other card. The estimate of 30 min was wrong.
- Estimate of the share a second draw gives without a hint, until the
  control is read (script run in chat on the Mac, not committed): a Beta
  distribution of the per-question chance of a correct sample, fitted to
  the round's committed counts (9,006 questions with a gold result: 33.5%
  with 0 of 10 correct, 17.4% with 10 of 10, mean 43.6%), with or without
  a share of questions at chance 0. It gives 11 to 16% of the all-wrong
  questions a correct sample in ten more draws, at a sample accuracy near
  2%. Against that the probe has 32.6% and 13.2%: about 17 to 21 points
  of questions from the hint (500 to 650 questions), under the 25 points
  proposed as the bar. A model, not a measurement.

## 2026-11-21: the hint probe runs; a control without the hint is queued (code `7e8a9a2e`)

- Probe on GPU 0 (worker log in chat, not committed): 3,017 questions
  sampled in 12 min 07 s (1.8% of the samples cut at 256 tokens). Labels
  of client 1 at 605 of 625 questions (16:10): 31.1% of them hold a
  correct sample, sample accuracy 12.5%; 24 questions with a SQL short of
  CPU were run again in 2 min 42 s. The estimate of 30 min for the probe
  counted the sampling only; with the labels of clients 2 to 5 it ends
  about 16:55 (estimate).
- The probe as built does not separate the hint from a second draw: a
  question with no correct sample in ten can get one in ten more whatever
  the prompt. Control (owner: yes, about 16:14): `hint_probe --no-hint`,
  the same questions with the probe's seeds and the prompt without the
  hint line, on clients 1, 3 and 4 (1,550 of the 3,017 questions; the
  clients whose labels are fast). The read is the hinted share minus the
  control's, and the count per question of which draw has a correct
  sample. The 25% of the earlier entry is read on that difference.
- GPU 1: the owner stopped `bird_sft/round_3` (about 16:08) to run
  `bird_k0_goldnll/round_2` first: 8,840 pairs and 3,017 gold rows, per
  client 1,992 + 625, 1,516 + 595, 2,150 + 641, 552 + 284, 2,630 + 872
  (worker log in chat). `bird_sft/round_3` goes on from its checkpoints
  on GPU 0 after the probe and the control.

## 2026-11-21: one loss for mixed and all-wrong questions, and the k = 2 round on BIRD, queued (code `38610a58`)

Owner's yes in chat (about 15:55), after the reading by difficulty below:
`bird_k0/round_2` is 10 points under FedAvg SFT on the challenging level
(19.31 against 29.66) and never trains its 3,017 all-wrong questions.

- New pair-rule setting `--gold-nll`: an all-wrong question gives one row
  with its gold SQL as the chosen side and no rejected side. The trainer
  puts the NLL term alone on it (no preference term, no reference
  log-probability), in the same updates and schedule as the pairs. The
  pairs themselves do not change. FedAvg weights are the rows a client
  trained on (pairs plus gold rows). One row per question, weight 1: not
  tuned. This is not gold as the chosen side of a pair, which lost 2.61
  on BIRD at 1 round.
- `bird_k0_goldnll/round_2`: round 2 from `bird_k0/round_1`
  (`--continue-from`), samples of `bird_k0/round_2` copied, so 8,840 pairs
  and 3,017 gold rows expected, training only. Read against
  `bird_k0/round_2` 43.02 (same pairs, no gold rows), `bird_k1/round_1`
  44.26, `bird_sft/round_2` 42.70, overall and by difficulty. It is also
  the control of a round with hinted pairs: both use the gold SQL of the
  same questions.
- `bird_k2/round_1`: DPO + NLL from FedAvg SFT round 2, the command of
  `bird_k1/round_1` with the parent round changed; the method at 3 rounds
  against `bird_sft/round_3`. Placed before `bird_sft/round_4`. It runs in
  the loss as it stood (no gold rows): its samples can train a round with
  gold rows later without sampling again.
- Checked on the Mac: 541 tests pass; resolved commands compared in the
  queue tests (the gold-row round differs from `bird_k0/round_2` in the
  root, `--gold-nll` and the two continue flags; the k = 2 round from
  `bird_k1/round_1` in the parent stage and the root); one gold row
  rendered with the real tokenizer on a BIRD dev database (the training
  prompt of the line, target the gold SQL and the end token). Packed and
  one-row-per-pass training give the same weights after one update on a
  tiny model. Not run on a GPU: memory and time are estimates
  (`docs/A5000_RUN_CONFIG.md`).
- State at 16:02: pushed, not pulled on the server yet. The cards run
  `hint/probe` and `bird_sft/round_3` (owner, about 15:48).

## 2026-11-21: BIRD dev by official difficulty: k = 0 loses the challenging questions, the DPO lines gain on the moderate ones (no new run)

Read from the committed predictions of the eight BIRD dev arms and of the
Spider arms; `difficulty` from `data/raw/bird/dev_20240627/dev.json` (925
simple, 464 moderate, 145 challenging; same row order as the evaluation
file, checked on the question text). Scripts run in chat on the Mac, not
committed.

| BIRD dev | Rounds | EX | Simple | Moderate | Challenging |
|---|---|---|---|---|---|
| Base student | 0 | 29.47 | 35.89 | 20.47 | 17.24 |
| FedAvg SFT | 1 | 38.85 | 46.16 | 28.66 | 24.83 |
| k = 0 | 1 | 41.85 | 50.16 | 31.25 | 22.76 |
| k = 0 with gold as chosen | 1 | 39.24 | 46.38 | 29.74 | 24.14 |
| FedAvg SFT | 2 | 42.70 | 50.49 | 31.25 | 29.66 |
| k = 0 | 2 | 43.02 | 50.70 | 35.13 | 19.31 |
| k = 0, round 2 on fixed pairs | 2 | 40.81 | 48.22 | 31.03 | 24.83 |
| k = 1 | 2 | 44.26 | 50.38 | 37.07 | 28.28 |

- Exact McNemar inside a level (questions only the first line solves /
  only the second). k = 0 against FedAvg SFT at 2 rounds: simple 76 / 74,
  moderate 54 / 36 (p 0.07), challenging 3 / 18 (p 0.0015). k = 1 against
  FedAvg SFT: simple 64 / 65, moderate 51 / 24 (p 0.0024), challenging
  12 / 14. k = 1 against k = 0: challenging 17 / 4 (p 0.007). k = 0
  against FedAvg SFT at 1 round: simple 98 / 61 (p 0.004). These are 18
  tests chosen after the results were seen; with a Bonferroni correction
  the bar is 0.0028, which the two main ones pass.
- Reading: the equal EX of k = 0 and FedAvg SFT at 2 rounds is a gain on
  the moderate questions cancelled by a loss on the challenging ones. With
  one SFT round first (k = 1) the loss is gone and the gain on moderate
  stays. On the simple questions the three lines are at one level (50.4
  to 50.7); DPO reaches it a round earlier.
- Gold as chosen loses on the simple level (46.38 against 50.16), not on
  the challenging one (24.14 against 22.76).
- Spider, k = 0 round 4 against FedAvg SFT round 4, the same count: test
  easy 11 / 19, medium 65 / 40 (p 0.019), hard 49 / 22 (p 0.0018), extra
  53 / 26 (p 0.0032); dev hard 26 / 10 (p 0.011), extra 21 / 9 (p 0.043).
  On Spider the gain sits in the hardest levels, on BIRD k = 0 loses
  there. The base student has no correct sample for 12% of the Spider
  train questions and for 42.8% of the BIRD ones.
- SQL form on BIRD dev, share of the predictions with a subquery: gold
  SQL 8.2%, FedAvg SFT round 2 6.8%, k = 0 round 1 27.1%, round 2 25.3%,
  k = 1 20.3%, fixed pairs 30.2%, gold as chosen 21.4% (cut outputs 1, 8,
  3, 8, 21, 29). Where the gold SQL has joins and no subquery, a
  prediction that uses a subquery is not right less often (k = 0 round 2:
  44.6% of 242 against 40.1% of 831). Spider test: gold SQL 16.1%, FedAvg
  SFT round 4 17.0%, k = 0 round 4 28.4%, k = 2 20.3%.
- Wrong results by kind, each run again on the Mac's BIRD dev databases
  (25 s per SQL): the same profile in the base student, FedAvg SFT round
  2, k = 0 round 2 and k = 1. For k = 1 (728): one wrong number 26.6%, an
  empty result 24.5%, one wrong value of another type 13.2%, another
  row count 9.2%, another column count 7.1%, right rows with missing or
  extra columns 4.7%. Of the empty results 39 to 47% filter on a string
  literal that the gold SQL does not have (6 to 9% of the correct
  predictions do). The BIRD prompt (`ddl`) shows no values.
- Right in FedAvg SFT round 2, k = 0 round 2 or k = 1: 827 questions
  (53.9%); in any of the eight arms 884 (57.6%); in none 650.
- In Git and not in the notes until now: 8 of the 18 `spider_variants`
  evaluations came with commit `d246d243`.

| Set | Base student | FedAvg SFT round 4 | Centralized SFT epoch 2 |
|---|---|---|---|
| Spider-Syn (1,034) | 56.77 | 59.09 | 60.83 |
| Spider-Realistic (508) | 65.16 | 67.72 | 67.13 |
| Spider-DK (535) | 60.19 | 59.63 | not in |

Papers on the questions without a correct sample, looked up today. Read
through a page-fetch tool (about the first 40% of each page as text, the
rest as the tool's summary), not by eye:

- ReLIFT (arXiv 2506.07527, listed as an ICLR 2026 poster): "RL excels
  at improving performance on questions within the model's original
  capabilities, while SFT is more effective at enabling progress on
  questions beyond the current scope". It runs SFT only on the questions
  with no correct rollout (acc(q) = 0), on solutions of a stronger model
  kept when the answer is right, between the RL steps. Qwen2.5-Math-7B,
  average of six benchmarks: SFT 49.0, RL 46.9, SFT then RL 50.7 and
  50.8, RL with an SFT loss on all questions 48.6, ReLIFT 52.6; at 1.5B
  32.6 / 34.2 / 36.5 (SFT / RL / ReLIFT). Math with reasoning, GRPO.
- SuperRL (arXiv 2506.01096, preprint): per question, policy gradient
  if any rollout has a reward, SFT on the demonstration if none has. In
  its Table 1 it is above RL in 24 of 35 cells; on HiTab (table
  questions) it is below RL and below SFT then RL (18.47 against 30.03
  and 38.64).
- BREAD (arXiv 2506.17211, listed at NeurIPS 2025): when the rollouts of
  a question fail, a prefix of the expert solution is put in the prompt
  and the model completes it; Qwen2.5 1.5B and 3B. It reports SFT on
  hard expert traces lowering a 1.5B model (GPQA 0.258 to 0.177).
- UFT (arXiv 2505.16984, listed at NeurIPS 2025): rollouts start from a
  partial solution (a hint) whose length falls over training, with a
  log-likelihood term on the hint; Qwen2.5 0.5B to 3B.
- Two more searches for federated Text-to-SQL found nothing besides
  Zhang et al. 2023. A search snippet gives CodeLutra as published in
  TMLR (06/2025) and reports its non-executable SQL falling from 40% to
  11%; the page was not opened.

None of these is on SQL-only output, with DPO, or federated. Our gold as
chosen is not their form: they put no preference term on the
demonstration.

What this adds to the order proposed today (`PIPELINE_NEXT.md`: the hint
probe, then a round with the hint or DPO from `bird_sft` round 2); not
approved, nothing queued. BREAD and UFT are the published form of a hint
for the questions no rollout solves, and they keep the hint in the
prompt while training; training the hinted sample under the prompt
without the hint is context distillation (Snell et al., arXiv
2209.15189, seen in a search summary only). A round with the hint needs
a control on the same samples: the pairs of `bird_k0/round_2` unchanged
plus NLL on the gold SQL of its 3,017 all-wrong questions, no preference
term on them (the form of ReLIFT and SuperRL). The reads are by level:
challenging at the FedAvg SFT level, no loss on simple.

## 2026-11-21: the six Spider rows on Spider-Syn, Spider-Realistic and Spider-DK; the hint probe is queued

Results `ca8c3a18` (and `5a8b7c8f` for the rows that finished with Spider
dev). EX, greedy, the adapters of the Spider table; nothing was chosen on
these sets. Exact McNemar tests: second table (read from the committed
predictions, 2026-11-21 15:50).

| Row | Spider test | Spider dev | Syn (1,034) | Realistic (508) | DK (535) |
|---|---|---|---|---|---|
| Base student | 68.05 | 68.96 | 56.77 | 65.16 | 60.19 |
| FedAvg SFT round 4 | 74.71 | 75.15 | 59.09 | 67.72 | 59.63 |
| Centralized SFT epoch 2 | 75.73 | 73.02 | 60.83 | 67.13 | 60.56 |
| DPO + NLL from the base student, round 4 (k = 0) | 78.02 | 77.27 | 62.09 | 71.26 | 67.10 |
| 2 SFT rounds then 2 DPO + NLL rounds (k = 2) | 78.20 | 77.66 | 62.96 | 70.47 | 63.55 |
| the same on fixed pairs, fixed reference | 78.02 | 76.21 | 60.74 | 70.67 | 62.62 |

- Over FedAvg SFT: k = 0 is +3.00, +3.54 and +7.47 on Syn, Realistic and
  DK; k = 2 is +3.87, +2.75 and +3.92. The method is above FedAvg SFT and
  centralized SFT on all five Spider sets.
- On-policy against fixed pairs (k = 2): +2.22 on Syn, -0.20 on
  Realistic, +0.93 on DK.
- FedAvg SFT is below the base student on DK (59.63 against 60.19).

Exact McNemar tests, two-sided: questions only the first line solves /
only the second, then p.

| Comparison | Spider test | Spider dev | Syn | Realistic | DK |
|---|---|---|---|---|---|
| k = 0 against FedAvg SFT round 4 | 178 / 107, 3.1e-5 | 84 / 62, 0.082 | 104 / 73, 0.024 | 51 / 33, 0.063 | 64 / 24, 2.4e-5 |
| k = 2 against FedAvg SFT round 4 | 150 / 75, 6.4e-7 | 72 / 46, 0.021 | 86 / 46, 0.0006 | 39 / 25, 0.10 | 46 / 25, 0.017 |
| k = 0 against centralized SFT epoch 2 | 187 / 138, 0.0077 | 98 / 54, 0.0004 | 107 / 94, 0.40 | 53 / 32, 0.029 | 66 / 31, 0.0005 |
| k = 2 against centralized SFT epoch 2 | 159 / 106, 0.0014 | 98 / 50, 0.0001 | 91 / 69, 0.097 | 47 / 30, 0.068 | 50 / 34, 0.10 |
| k = 2 on-policy against fixed pairs | 58 / 54, 0.78 | 38 / 23, 0.072 | 48 / 25, 0.0095 | 15 / 16, 1 | 16 / 11, 0.44 |
| FedAvg SFT round 4 against the base student | 235 / 92, 1.4e-15 | 114 / 50, 6.3e-7 | 106 / 82, 0.093 | 49 / 36, 0.19 | 44 / 47, 0.83 |

- Against FedAvg SFT, 7 of the 10 tests of the two lines are under 0.05;
  at a Bonferroni bar of 0.005 over the 10, four hold (Spider test for
  both lines, Syn for k = 2, DK for k = 0). Realistic and DK have 64 to
  88 discordant questions each.
- FedAvg SFT round 4 is not separated from the base student on Syn,
  Realistic and DK; both method lines are above FedAvg SFT there.
- On-policy rounds against fixed pairs separate on Syn alone.

Hint probe (owner: yes, 2026-11-21; code `40ae6bce`, 534 tests pass):
`scripts/hint_probe.py` takes the all-wrong questions of one round, puts
one line after the question with the tables and columns of the client's
gold SQL (sqlglot, per query scope; every one of the 9,428 BIRD and 8,659
Spider training golds gives a hint), samples them again from the model
the round sampled (10 at T 1.0, another seed) and labels them as the
round does. Queued as `hint/probe` for `bird_k0/round_2` (3,017
questions), before `bird_sft/round_3`. Not trained on; the prompt without
a hint is byte for byte as before (prompt tests). Read: the share of the
3,017 with a correct sample; 25% or more goes on to one training round.

## 2026-11-21: BIRD at 2 rounds: `bird_k0/round_2` 43.02, level with FedAvg SFT; fixed pairs 40.81; the six Spider rows on Spider dev

Results `77079f67`, `b16a365a` (`bird_fixed/round_2`), `40dc6a3c`,
`d246d243` (`bird_k0/round_2`), `5a8b7c8f` (Spider dev), `20b43a92`
(record of the centralized SFT curve: 3 epochs, best epoch 2).

| BIRD dev, 2 total rounds | EX | Execution errors | Wrong results | Cut outputs |
|---|---|---|---|---|
| FedAvg SFT | 42.70 | 285 | 593 | 1 |
| DPO + NLL from the base student (k = 0) | 43.02 | 247 | 624 | 3 |
| the same, round 2 on the round 1 pairs, fixed reference | 40.81 | 162 | 725 | 21 |
| FedAvg SFT round 1, then one DPO + NLL round (k = 1) | 44.26 | 120 | 727 | 8 |

- k = 0 against FedAvg SFT: +0.32, exact McNemar p 0.80 (133 questions
  fixed, 128 broken). The +3.00 of round 1 (p 0.005) is not there at
  round 2: the second DPO round adds 1.17 (41.85 to 43.02, p 0.17), the
  second SFT round 3.85.
- k = 0 against k = 1: -1.24, p 0.19 (84 fixed, 103 broken). By the read
  in `PIPELINE_NEXT.md` (k = 0 at least equal to k = 1): no; the method
  on BIRD keeps an SFT stage, with k as a value. Neither line is
  separated from FedAvg SFT at 2 rounds (k = 1: +1.56, p 0.13).
- On-policy rounds against fixed pairs: +2.21, p 0.008 (94 fixed, 60
  broken): kept by the rule, the first set where it separates (Spider
  test: 78.20 against 78.02). The fixed line falls from its round 1
  (41.85 to 40.81, p 0.17) and is 1.89 below FedAvg SFT (p 0.09).
- Round 2 of k = 0 removes wrong results (673 to 624) and gives back
  execution errors (211 to 247). Its pairs reject a wrong result in 61%
  (5,352 of 8,840; round 1: 24%); its samples: 41.6% correct, 17.0%
  execution errors, 35.3% wrong results (round 1: 19.8%, 50.0%, 17.0%).
- Committed question kinds of round 2 as in the entry below. Golds on
  the 30 s budget: 72 (1 / 14 / 22 / 0 / 35 per client) against 50 in
  `bird_k1/round_1` and 30 for the base samples labelled on CPU; samples
  on the budget 439 against 165 and 164.
- Times of `bird_k0/round_2`: training 3 h 51 min (reference 51 min,
  updates 3 h 00 min; client 5 alone 2 h 30 min for 2,630 pairs). The
  sampling ran in three calls (03:04, 05:24, 10:33; two were stopped), so
  its total is not complete: the label calls that finished add up to 2 h
  13 min. Client 1 was labelled before code `0910b84f` (committed 04:55)
  in 62 min, clients 3 and 4 after it in 7.6 and 3.0 min (4.5 and 1.9
  min in `bird_k1/round_1`, with 43% of the samples failing against 17%
  here). The effect of the held-back second runs is not measured by
  this round; the `SQL budget` lines of the log were not seen.
- `bird_fixed/round_2`: training 3 h 32 min on the 9,714 pairs of round 1.

| Spider, same six adapters | Spider dev (1,034) | Spider test (2,147) |
|---|---|---|
| Base student | 68.96 | 68.05 |
| FedAvg SFT round 4 | 75.15 | 74.71 |
| Centralized SFT epoch 2 | 73.02 | 75.73 |
| DPO + NLL from the base student, round 4 (k = 0) | 77.27 | 78.02 |
| 2 SFT rounds then 2 DPO + NLL rounds (k = 2) | 77.66 | 78.20 |
| the same on fixed pairs, fixed reference | 76.21 | 78.02 |

- On Spider dev, where no round or setting was chosen, the gain over
  FedAvg SFT is +2.12 for k = 0 (p 0.08; 84 fixed, 62 broken) and +2.51
  for k = 2 (p 0.02; 72 fixed, 46 broken); on Spider test +3.31 and
  +3.49. The fixed-pair line is +1.06 (p 0.38).
- On-policy against fixed pairs on Spider dev: +1.45, p 0.07 (38 fixed,
  23 broken). k = 0 against centralized SFT: +4.25, p 0.0004; FedAvg SFT
  is 2.13 above centralized SFT there (p 0.06).
- Spider-Syn, Spider-Realistic and Spider-DK: not published at 15:07.
- Queued (code `de56e3cd`): `bird_sft` rounds 3 and 4, needed by every
  outcome (the baseline to 4 rounds and the starts of the lines with an
  SFT stage); about 2 h 50 min a round.

## 2026-11-21: `bird_k0/round_2`, the questions after one DPO + NLL round on BIRD: 3,017 without a correct sample (owner's console, 12:25, not committed)

The status output and the five `pairs from` lines of the task log, pasted
in chat. At 12:25 the round was in the DPO updates of client 4 (update 11
of 35); nothing of it is published.

| BIRD train, 9,428 questions, 10 samples each | All correct | Mixed | All wrong | No label | Pairs | Sample accuracy |
|---|---|---|---|---|---|---|
| Base student (`bird_k0/round_1`, committed) | 156 | 4,857 | 4,035 | 380 | 9,714 | 0.198 |
| After 1 FedAvg SFT round (`bird_k1/round_1`, committed) | 196 | 5,612 | 3,220 | 400 | 11,224 | 0.259 |
| After 1 DPO + NLL round (`bird_k0/round_2`, console) | 1,569 | 4,420 | 3,017 | 422 | 8,840 | 0.416 |

"No label" is the gold that fails or meets the budget; the log line does
not print it, so the last row has 9,428 minus the three kinds. All wrong
per client: base 822 / 741 / 929 / 324 / 1,219; after the SFT round 642 /
629 / 716 / 309 / 924; after the DPO round 625 / 595 / 641 / 284 / 872.

- One DPO + NLL round takes 1,018 questions (net, 25%) out of all wrong,
  one FedAvg SFT round 815 (20%), and the DPO round is lower on every
  client. Round 1 trained on no pair of those questions; FedAvg SFT
  trained on their gold SQL. 32% of the questions still give no pair.
- The pairs hold on BIRD: 8,840 in round 2 against 9,714 in round 1
  (91%). Spider, k = 0: 4,566 against 8,908 (51%), and the all-wrong
  questions there went 1,074, 902, 886, 860 over the four rounds.
- No label: 422 against 400 (`bird_k1/round_1`, labels before `0910b84f`)
  and 380 (the base samples labelled again on CPU). The rise is on client
  2 (20; 10 and 8 before) and client 5 (375; 361 and 360), the clients
  with most second runs. To read from the published
  `client_*_pairs_stats.json` (`questions_gold_timeout`) and the
  `SQL budget` lines: do more golds end on the 30 s budget when the
  second runs go 4 at a time?
- Label time on code `0910b84f`: not in this output. The pairs came 34
  min after the task started on GPU 0 (10:33), less than the sampling
  and the labels of a BIRD round without any second run (27 and 64 min in
  `bird_k1/round_1`), so an earlier call did part of the step;
  `timing.json` counts every call.
- Queue at 12:25: one worker, on GPU 0. `bird_fixed/round_2` trained
  there in 3 h 35 min (06:58 to 10:33); its publication and its
  evaluation are ready and wait, as do the Spider dev rows: no worker on
  GPU 1. `bird_k0/round_2`: EX about 14:45 (estimate; client 5 is left
  with 2,630 pairs, and it took 2.65 s per pair in round 1).

## 2026-11-21: `bird_k0_gold/round_1`, gold as chosen for the all-wrong questions on BIRD: 39.24, below the line without gold

Results `0c5258a9` (round, published 06:50), `ff917437` (BIRD dev). Same
samples and labels as `bird_k0/round_1`; the gold rule adds 2 pairs for
each of the 4,035 questions without a correct sample (gold as chosen, a
wrong sample as rejected): 17,784 pairs against 9,714, 8,070 of them
with gold.

| BIRD dev, 1 round | EX | Execution errors | Wrong results | Cut outputs |
|---|---|---|---|---|
| FedAvg SFT | 38.85 | 371 | 566 | 1 |
| DPO + NLL from the base student | 41.85 | 211 | 673 | 8 |
| the same with gold as chosen | 39.24 | 76 | 827 | 29 |

- Against the line without gold: -2.61, 86 questions fixed and 126
  broken, exact McNemar p 0.007. Against FedAvg SFT round 1: +0.39, p
  0.76 (141 fixed, 135 broken). By the rule of the read: gold as chosen
  is not kept, and its round 2 is not queued. On Spider the same rule
  was above at round 1 (76.67 against 75.87) and fell at round 2.
- The gold pairs remove execution errors (211 to 76) and add more wrong
  results than that (673 to 827): 114 of the 126 broken questions now
  run and return another result. Lower at every hardness level (easy
  50.00 against 51.55, medium 46.08 against 48.83, hard 30.36 against
  33.00, extra 25.16 against 28.06).
- Time: training 8 h 09 min (reference 1 h 46 min, updates 6 h 23 min)
  against 3 h 30 min; 1.65 s per pair against 1.30 s.
- The server took code `0910b84f` before this publication (the result
  commit sits on it), so `bird_k0/round_2`, a new process started after
  it, labels with the second runs held back.
- Next for the all-wrong questions, if the BIRD reads still ask for it:
  the one-loss form (NLL on the gold SQL for them, no preference term;
  `RESEARCH_STATE.md`, section 4), not queued.

## 2026-11-21: the 3 h of BIRD labels are reruns alone, 2 h 03 min of them (log lines of `bird_k1/round_1`, sent in chat, not committed)

Owner: why does a BIRD round take twice a Spider round? Same steps on
both, from the committed times (`run_times/decide/k3/round_1.json`,
`timing.json` of `bird_k1/round_1`):

| Step | Spider, 8,659 questions, 7,220 pairs | BIRD, 9,428 questions, 11,224 pairs |
|---|---|---|
| Sampling | 17 min | 27 min |
| Labels | 2.5 min | 3 h 06 min |
| Training | 2 h 50 min | 4 h 17 min |
| Round | 3 h 12 min | 7 h 50 min |

- Training is not slower per pair: 1.30 to 1.37 s on BIRD, 1.25 to 1.41
  s on Spider. `bird_k0/round_1`, which samples nothing, takes 3 h 30
  min for 9,714 pairs (Spider k = 0 round 1: 3 h 05 min for 8,908).
- The labels are 3 h 03 min of the 4 h 38 min between the two rounds.
  The `SQL budget, this call` lines of the label step, 16 worker
  processes:

| Client | Label step | SQL time (gold) | Workers busy | Met the budget | Jobs run again alone | Seconds alone | Timed out |
|---|---|---|---|---|---|---|---|
| 1 | 1,886 s | 7,216 s (1,106) | 24% | 90 | 52 | 1,114 | 18 |
| 2 | 4,654 s | 14,367 s (4,668) | 19% | 193 | 129 | 3,222 | 76 |
| 3 | 271 s | 3,532 s (837) | 82% | 60 | 0 | 0 | 60 |
| 4 | 116 s | 1,271 s (203) | 68% | 5 | 0 | 0 | 5 |
| 5 | 4,215 s | 11,472 s (4,462) | 17% | 191 | 145 | 3,023 | 67 |

- On clients 1, 2 and 5 a SQL that meets the 30 s on less than 0.8 of
  its time as CPU runs again with every other worker stopped: 326 jobs,
  22.6 s each on average, 7,359 s of the 11,142 s label step (59%, 69%
  and 72% of the three clients' steps). Without those seconds the three
  steps take 13, 24 and 20 min.
- The reruns are needed as labels: of the 474 SQL that met the budget
  on these clients 161 stay timeouts, so about 313 finish inside 30 s
  once they run alone. Under 16 processes the load still pushes SQL
  over the budget on the large databases (`donor`, `movie_platform`,
  `retails`, `language_corpus`, `talkingdata`); the 60 of client 3 used
  the CPU themselves and are not run again.
- Not measured: why these runs wait (disk or memory; the server's disk
  and RAM are not known here), and the label step under fewer worker
  processes on BIRD train. BIRD dev evaluations with 4 processes: 0 jobs
  short of CPU.
- Changed (owner: yes; code `0910b84f`): a label step holds the second
  runs back until its other questions are labelled, then runs them 4 at
  a time; one that is short of CPU once more still runs alone. Budgets
  and the label rule are unchanged; evaluations run a job alone at once
  as before. Arctic-Text2SQL-R1 (arXiv 2505.20315, section 4.1, read
  today) drops the questions whose SQL runs over 5 s instead; not taken,
  the owner keeps every question that can be labelled. 527 tests pass.
  Estimate, not measured: labels about 1.5 h in place of 3 h. The first
  label step on the new code says it in its `SQL budget` lines (jobs
  run again after the others, jobs alone, seconds of each).

## 2026-11-20: `bird_k0/round_1`, DPO + NLL from the base student on BIRD: 41.85

Results `079a5ab8` (round, published 22:29), `2dceb56f` (BIRD dev).

| BIRD dev | Rounds | EX | Execution errors | Wrong results |
|---|---|---|---|---|
| Base student | 0 | 29.47 | 645 | 436 |
| FedAvg SFT | 1 | 38.85 | 371 | 566 |
| DPO + NLL from the base student | 1 | 41.85 | 211 | 673 |
| FedAvg SFT | 2 | 42.70 | 285 | 593 |

- +3.00 over FedAvg SFT at 1 round, 152 questions fixed and 106 broken,
  exact McNemar p 0.005: kept by the rule. Spider at 1 round: +3.44
  (75.87 against 72.43).
- Against FedAvg SFT round 2: -0.85, p 0.46 (127 fixed, 140 broken): one
  DPO round stands where two SFT rounds do.
- By hardness against FedAvg SFT round 1: easy 51.55 / 50.52, medium
  48.83 / 45.94, hard 33.00 / 30.69, extra 28.06 / 22.90.
- Trained on 9,714 pairs from 4,857 of the 9,428 questions (2,298 /
  1,640 / 2,240 / 678 / 2,858); 76% of the pairs reject an execution
  error. Training 3 h 30 min, client 5 alone 2 h 06 min; peak reserved
  17.47 to 18.98 GiB, budget never lowered.

## 2026-11-20: `bird_k1/round_1`, DPO + NLL from FedAvg SFT round 1 on BIRD: 44.26

Results `7e0d032f` (round), `2913db0c` (BIRD dev, 1,534 rows), `144a8a78`
(pair read of the base student with the labels of worker processes).

| BIRD dev, 2 total rounds | EX | Execution errors | Wrong results |
|---|---|---|---|
| FedAvg SFT round 2 | 42.70 | 285 | 593 |
| FedAvg SFT round 1, then one DPO + NLL round | 44.26 | 120 | 727 |

- +1.56 over FedAvg SFT at the same count, 127 questions fixed and 103
  broken, exact McNemar p 0.13: not separated by the keep rule (0.5 EX
  with p below 0.05). Over its own start (38.85): +5.41, where the second
  SFT round adds +3.85.
- The round removes execution errors (285 to 120) and leaves more wrong
  results (593 to 727): of the 103 broken questions 89 end in a wrong
  result. 8 outputs are cut at 256 tokens (FedAvg SFT round 2: 1).
- Questions by kind after the SFT round (9,428): mixed 5,612, all wrong
  3,220, all correct 196, gold fails or meets the budget 400.
  Pairs 11,224 (2,612 / 1,848 / 2,606 / 716 / 3,442). Of the pairs, 63%
  reject an execution error. For the base student, relabelled: mixed
  4,857, all wrong 4,035, pairs 9,714. One SFT round moves 815 questions
  out of all wrong; a third of the questions still give no pair.
- Time: 7 h 50 min for the round (sampling 27 min, labels 3 h 06 min,
  training 4 h 17 min), against 3.1 to 3.6 h for a Spider round 1. The
  labels of clients 2 and 5 take 78 and 70 min with 16 worker processes,
  client 3 with more questions 4.5 min; the timeouts (16 to 66 samples a
  client) do not explain it, the `SQL budget, this call` lines of the
  log would. Client 5 trains for 2 h 43 min of the 4 h 17 min: 10.3M of
  the 22.6M sequence tokens, at twice the time per token. Peak reserved
  14.81 to 18.90 GiB. In `A5000_RUN_CONFIG.md` (code `166b2ce0`).
- Read against the decision table: the first row is a no at 2 rounds by
  the rule, with the difference on the method's side. `bird_k0/round_1`,
  `bird_k0_gold/round_1` and `bird_k0/round_2` decide as queued; the line
  is not dropped on this read.

## 2026-11-20: SPFT-SQL is not used as a reference (owner)

Owner: its numbers look too high to rely on. What the saved text shows:
the untrained Qwen2.5-Coder-1.5B is at 40.6 on BIRD dev there, against
27.5, 28.40 and 28.6 in three other papers and 29.47 here, and at 72.3 on
Spider test against 68.05 here; no prompt and no decoding are printed.
Its SFT adds only 3.7 on BIRD (SQL-Factory 10.6, our two FedAvg rounds
13.2), which fits a baseline prompt that already carries more than the
schema. So its SFT and method rows cannot be set next to ours.

- Taken out of the reference table (`RESEARCH_STATE.md`, 5.1); the
  numbers stay in `LITERATURE.md` 1.4, marked.
- What changes: the "published SFT of this student at 77 to 78" that our
  75 to 76 was measured against was SPFT-SQL's 78.0 (test) and SLM-SQL's
  77.35 (916K rows, vote of 16). The plain row left is SQL-Factory's
  73.2, below our centralized 75.73, so the check run of centralized SFT
  on a 3-epoch schedule has no published number to answer to.
- Not changed: the SFT recipe names SPFT-SQL for lr 2e-4 and 3 epochs
  (`RESEARCH_STATE.md`, section 2); a setting, not a number.

## 2026-11-20: published numbers for this student recorded (`LITERATURE.md` 1.4, `RESEARCH_STATE.md` 5.1)

A search agent read the papers with BIRD dev rows at 0.5B to 3B and
searched for federated Text-to-SQL (owner's request). Read again here in
the saved text: the rows of SQL-Factory, SPFT-SQL, SLM-SQL and Zhang et
al.; the rest is as the agent reported it.

- BIRD dev, Qwen2.5-Coder-1.5B without training: 27.5, 28.40, 28.6 in
  three papers, ours 29.47. SPFT-SQL prints 40.6 and no prompt.
- Plain SFT on BIRD train at this size: 39.2 (SQL-Factory) and 44.3
  (SPFT-SQL, LoRA, 3 epochs). FedAvg SFT is at 42.70 after 2 rounds.
  Every 1.5B number above about 45 adds inputs or voting.
- Spider, same student: SFT 73.2 (SQL-Factory) and 76.8 dev / 78.0 test
  (SPFT-SQL); our centralized SFT ends at 75.73 on Spider test. SPFT-SQL
  also prints Syn, Realistic and DK for its SFT row (59.0, 64.8, 60.9),
  the sets queued today.
- Federated: nothing on BIRD, and no federated Text-to-SQL paper besides
  Zhang et al. The papers citing it were not read (requests refused).

## 2026-11-20: six Spider rows queued on Spider dev, Syn, Realistic and DK (code `930db2d0`)

Owner, 11:15: evaluate the Spider rows on the other Spider sets. Not
required by the journal bar (`JOURNAL_BAR.md`: Spider test and BIRD dev
are at the level of both journals); Spider dev is the set most papers at
this size report (GradeSQL at JIIS prints dev and test), and no round or
setting was chosen on it.

- Rows: base student, FedAvg SFT round 4, centralized SFT epoch 2,
  DPO + NLL from the base student round 4 (k = 0), DPO + NLL round 2 from
  FedAvg SFT round 2 (k = 2), its fixed-pair, fixed-reference line. The
  k = 2 row is there because the method's k is not settled and it is the
  line the fixed-pair row is compared with.
- Tasks `spider_dev/*` (Spider dev, 1,034 rows) and `spider_variants/*`
  (Syn 1,034, Realistic 508, DK 535), after the BIRD rounds; evaluation
  only. Each command is the row's Spider test evaluation with the set
  changed (checked by a queue test and on the resolved commands: only
  `--test-csv` and the resume directory differ). Longest prompt 2,052
  tokens on all four (Spider test 2,547); one DK prompt printed and read.
- Checked on the Mac: every database of the four CSVs exists (20, 20,
  19, 10). Not checked: that the server holds `data/raw/spider_dk/` and
  the five adapters (`PIPELINE_NEXT.md`, step 5).
- The Syn, Realistic and DK CSVs are the processed files of July 2026,
  without the `dataset` and `source_row_id` columns; the loader and the
  `spider` profile accept them.
- `overview_results.py` mapped an evaluation to its dataset by evaluator,
  so a second set of one arm would have stopped it ("two evaluations
  for"). It now maps by the evaluated set and leaves the other sets out;
  its output on the committed results is unchanged.
- Which of these numbers the paper prints is decided when they are in.

## 2026-11-20: FedAvg SFT round 2 on BIRD dev 42.70, still rising; relabel finished; `bird_k1` stays first (results `9ccb7837`, `53c7bee1`)

BIRD dev (1,534 rows), `scripts.error_breakdown`:

| Row | EX | exec errors | wrong results | easy | medium | hard | extra |
|---|---|---|---|---|---|---|---|
| base student | 29.47 | 645 | 436 | 44.33 | 34.53 | 21.78 | 15.81 |
| FedAvg SFT round 1 | 38.85 | 371 | 566 | 50.52 | 45.94 | 30.69 | 22.90 |
| FedAvg SFT round 2 | 42.70 | 285 | 593 | 53.61 | 50.34 | 33.33 | 27.10 |

- Round 2 against round 1: +3.85, 98 fixed, 39 broken, exact McNemar
  p 4.9e-07. FedAvg SFT has not flattened on BIRD (Spider: +1.67 at round
  2, then +0.61 and 0). Execution errors fall (371 to 285) and wrong
  results rise (566 to 593), as on Spider.
- Training: 2 h 49 min for the five clients (22, 19, 31, 12, 85 min);
  peak reserved 20,313 MB at client 5, the highest of any round so far
  (limit about 21.5 GiB); product error of the factor average 0.061.
- What `bird_k1/round_1` is read against: one DPO + NLL round from
  round 1 (38.85) has to end above 42.70, a gain of more than 3.85 in
  one round. On Spider a DPO round from FedAvg round 2 gained 3.36 over
  its start, against 0.61 for the next FedAvg round.

Owner, 11:00: the relabel of `bird/read` has finished (its per-client
lines are not in yet; `bird/read_relabelled` publishes the counts).
Owner asked whether `bird_k0` should now go before `bird_k1`. Kept as
queued (my recommendation): GPU 0 took `bird_k1/round_1` at about 10:58
(inferred from the publication of 10:57); with one card both reads are
in by about 19:00 in either order, and the read of `bird_k1` against
42.70 is the one that settles more, since one round from the base
student on half of the questions (4,783 of 9,428) is unlikely to pass
38.85 and would wait for its round 2. A free second card takes
`bird_k0/round_1` at once (`PIPELINE_NEXT.md`, step 2).

## 2026-11-20: centralized SFT ends at 3 epochs; GPU 0 back on the BIRD rounds (owner; queue `c41c48c2`)

Owner: drop epoch 4; the curve rule is not right here. At 10:49 GPU 0
was in epoch 4 of centralized SFT (762 of 8,659 examples, 1 h 57 min
left): under the order it had loaded the curve stood before the
publication and evaluation of `bird_sft/round_2`, and under the rule
(0.5 over the best, patience 2) a fourth epoch runs after the first
epoch without a gain. The owner stopped the worker and started it
again; it published `bird_sft/round_2` at 10:52 (`9ccb7837`).

The curve `central_base_ddlrows_s0/sft` now has `max_steps = 3`: the
reference row is epochs 1 to 3 (75.08, 75.73, 75.03 on Spider test;
best epoch 2). With that maximum the rule stops at step 3 with best
step 2 (checked on the three values), so `refs/central_sft` trains
nothing more and only writes the curve's record when a worker reaches
it. The checkpoint of epoch 4 stays on the server and is not used.
The other curves that carry the same rule (local SFT per client, the
DPO curve from the base student) are not queued; their rule is
unchanged. 523 tests pass.

## 2026-11-20: centralized SFT epoch 3 falls to 75.03; the federated method is above the centralized SFT reference at every epoch (results `171ee546`, `16f82c69`)

Spider test (2,147 rows), `scripts.error_breakdown`:

| Epochs or rounds | Centralized SFT | FedAvg SFT | DPO from the base student (k = 0) | k = 0 against centralized SFT |
|---|---|---|---|---|
| 1 | 75.08 | 72.43 | 75.87 | +0.79 |
| 2 | 75.73 | 74.10 | 77.18 | +1.45 (p 0.091) |
| 3 | 75.03 | 74.71 | 77.69 | +2.66 (184 against 127 rows, p 0.0015) |

- Epoch 3: EX 75.03 (easy 91.06, medium 78.30, hard 67.17, extra
  56.30), EM 65.07, execution errors 158, wrong results 377, 2 rows on
  the 60 s budget. Against epoch 2: 85 fixed, 100 broken, p 0.30;
  against epoch 1: p 1. The three epochs are one level, 75.0 to 75.7;
  the best is epoch 2. By the rule (0.5 over the best, patience 2)
  epoch 4 runs and is the last unless it reaches 76.23.
- Training: continued from example 5,616 of 8,659 (the stop of GPU 1 at
  07:30), 47 min in this call, 2 calls, 7,763 s in all; peak reserved
  20,359 MB; mean loss of the call 0.046.
- FedAvg SFT against centralized SFT at the same count: -2.65, -1.63
  (p 0.030), -0.32 (p 0.69). FedAvg SFT is slower, not lower: at 3
  rounds it is at the centralized level. This corrects the reading
  under item 12 (a) of `RESEARCH_STATE.md`, section 4: the gap of SFT
  under this split is one of rounds, so the direction rests on the
  method against its own centralized form, not on SFT losing level.
- DPO round 1 from FedAvg round 2 (3 rounds, 77.46) against centralized
  epoch 3: 157 against 105 rows, p 0.0016.
- Open: the SFT reference here is about 75 to 76 with one-epoch steps,
  each with a fresh optimizer and schedule as a FedAvg round has;
  `RESEARCH_STATE.md` (section 4, item 10) puts the SFT of this student
  in the papers at 77 to 78. One centralized run on the usual schedule
  (3 epochs, one schedule; about 6.5 h, estimate) would say whether the
  reference is low because of the steps. Not queued.

Server: the publication merged the queue of 09:55. The continuation
started at about 09:44 (10:31 less 47 min); which card ran it is not
known. No publication of `bird_sft/round_2` yet.

## 2026-11-20: extensions toward Q2 recorded, to try after the method is settled (owner; no run)

Owner: write the directions down; they are tried after the method is
settled on BIRD. In order: (a) centralized DPO + NLL and the gap between
federated and centralized for SFT and for DPO, with the drift of the
client updates; (b) one local loss with NLL on the gold SQL for the
all-wrong questions and DPO + NLL on the mixed ones, only if the BIRD
reads ask for it; (c) questions without gold SQL labelled by the vote
over execution results. Owner on (c): hiding gold is an assumption the
datasets do not make; it is a secondary experiment at most, not a part
of the method, and it needs an SFT baseline with pseudo-labels to be a
fair comparison. Its first step is a CPU probe of the vote labels on
the Spider round 1 samples (script not written). Table with evidence
and costs: `RESEARCH_STATE.md`, section 4, item 12. Nothing is queued.

## 2026-11-20: queue turned to the earliest read of the method on BIRD; SFT stage line `bird_k1` queued; centralized SFT after the BIRD rounds (owner; queue `51d09d80`)

Owner: order the pipeline so that the direction of the method is known
soonest. No new run in this entry.

What is open is one point: what the method does with the questions
that have no correct sample (Spider 12%, BIRD 41.9% for the base
student). Three forms: nothing (k = 0), an SFT stage before the DPO
rounds, gold inside the round. On Spider the first two end equal and
the gold rule fell at round 2; that run changed three things at once
(gold for all-wrong questions, 2,032 pairs; gold on databases without
rows, 3,110 pairs; client 4's weight 0.28 to 0.43), so it is not a
clean reading of gold next to DPO. BIRD train has no database without
rows.

Queue:

- New `bird_k1/round_1`: one DPO + NLL round from `bird_sft` round 1
  (k = 1), the command of `bird_k0/round_1` with `--parent-stage
  fedavg_bird_ddl_a01_r1_s0` in place of `--from-base` and a root of its
  own (`fedpref_bird_sftr1_p2_ddl_alpha01_s0`), evaluation on BIRD dev
  and both publications. Read at 2 total rounds against `bird_sft`
  round 2 and `bird_k0` round 2. It stands before the relabel: it needs
  no label of the base student's samples, so it is the first BIRD read
  of the method a free card can produce. k = 1 and not 2 or the best
  round: its comparison rows at the same total rounds are already
  queued. Checked before queuing (new test): against `bird_k0/round_1`
  only the start and the root differ and the setup (prompt, length,
  LoRA, sampling, pair rule) is equal; against the Spider k = 2 round
  only the parent round, split, profile, schema text and root. The
  parent row resolves from its stage label; one BIRD prompt rendered
  and read. 523 tests pass, 2 skipped. Not measured: its run time, its
  pair count, memory, and free RAM with its 16 label processes next to
  the relabel by hand.
- `refs/central_sft` moves after the BIRD rounds. It stood before them
  since this morning (owner), and under that order GPU 0 would take it
  after `bird_sft/round_2`, before that round's evaluation, for up to 6
  more epochs of 2 h 10 min. It is a reference row and keeps its
  checkpoint in epoch 3.
- Kept in place: `bird_k0/round_1`, `bird_k0_gold/round_1`,
  `bird_k0/round_2`, `bird_fixed/round_2`.

The server gets the order only after a pull; if GPU 0 reaches
centralized SFT first, the worker is stopped and started again
(`PIPELINE_NEXT.md`, step 1).

Owner's expectation: DPO from the best SFT round, 1 to 2 rounds, gives
the highest level. On Spider one DPO round carries most of the gain
(+3.36 from FedAvg round 2, +3.26 from round 3; a second round +0.74,
p 0.093), and the level is the same from k = 0, 2 and 3 (78.02, 78.20,
77.97), so the start does not raise it there; on BIRD it is read from
`bird_k1` first. Not queued, decided on those reads: the BIRD lines to
4 rounds, DPO from the best `bird_sft` round, one local loss with NLL
on the gold SQL for the all-wrong questions only (needs a preference
weight per row), centralized DPO + NLL on Spider.

Journal quartiles, looked up today through search results (the pages
were not opened): Scimago 2025 lists CMC as Q2 (SJR 0.513, Computer
Science Applications) and JIIS as Q2 (SJR 0.775, Information Systems).
JCR: CMC Q3 on Peeref (JCR 2024); JIIS Q3 on Peeref (JCR 2023) and Q2
on LetPub. Which list the owner's requirement counts is open.

## 2026-11-20: FedAvg SFT round 1 on BIRD dev 38.85; 16 worker processes for the BIRD label steps (results `ec5d3ec6`, `91e5fcdd`; queue `4f9e3299`, `f0b35ba9`)

BIRD dev (1,534 rows): FedAvg SFT round 1 on the BIRD clients 38.85
(execution errors 372, 2 rows on the 30 s budget, scorer v3) against the
base student 29.47 (646, 3, scorer v2): +9.38. `bird_k0/round_1` is read
against it.

Owner: the server has 2 x 32 logical processors. The BIRD label steps
not yet run (`bird/relabel`, `bird_k0`, `bird_k0_gold`, `bird_fixed`)
take `--score-workers 16` (4 before, chosen for SQL in threads); the
worker count is not part of a sample file's identity. RAM with 16
processes on BIRD train is not measured. `bird/read_relabelled` keeps
the command of the first read (it labels nothing).

## 2026-11-20: label step runs the gold once per question; only a run short of CPU runs again alone (owner; code `a14f140a`)

Owner: the relabel of `bird/read` takes too long for one round; is the
way it is done the BIRD standard? The evaluation follows the official
evaluator (one 30 s budget per prediction/gold pair, a process per pair,
rows as sets). BIRD defines no rule for labelling training samples: the
30 s per sample is ours. Two costs came from the code of this morning,
not from any rule: the gold ran three times per question and once more
per distinct SQL, and every run that met the budget ran a second time
with the other workers waiting, also a SQL that had used the 30 s itself
(a runaway join).

Changed, the rule and the scorer name unchanged (BIRD v3):

- One job per question: the gold runs once and its measured seconds
  count in every pair (a gold that does not fit twice in 30 s is
  `gold_error`; a SQL that runs and leaves the gold less than its
  seconds gets no label; a SQL that meets 30 s is a timeout). Spider:
  60 s for the gold and for each SQL.
- A run that met the budget is repeated alone only when it had less
  than 0.8 of its wall-clock time as CPU time.
- The pool logs the SQL seconds (all, gold, runs alone).

Checked on the Mac, old against new, with each gold, two other golds of
its database and one failing SQL as the SQL to score: the same result
for all 26,804 SQL of the 8,659 Spider train questions and all 6,136
SQL of the 1,534 BIRD dev questions (6 timeouts either way); BIRD dev
179.5 s against 106.9 s with 4 workers. Not measured on the server or
on BIRD train (its databases are not on the Mac). The relabel running
by hand keeps the code it loaded; the first label step on the new code
is `bird_k0/round_2`. Its `SQL budget` line then says where the time
goes. Open for the owner: a shorter budget for label steps only (a
sample over it gets no label), and more than 4 score workers on BIRD.

## 2026-11-20: gold line round 2 falls on Spider; centralized SFT epochs 1 and 2; queue order (results `73850020`..`0643b48c`; queue `b438dec4`, `42046d18`)

Spider test (2,147 rows), read with `scripts.error_breakdown`:

| Arm | EX | exec errors | wrong results |
|---|---|---|---|
| k = 0 line with gold, round 2 (`k0_gold/round_2`) | 75.73 | 76 | 442 |
| k = 0 line, round 2 | 77.18 | 92 | 398 |
| k = 0 line with gold, round 1 | 76.67 | 53 | 444 |
| centralized SFT, epoch 1 | 75.08 | 164 | 370 |
| centralized SFT, epoch 2 | 75.73 | 149 | 370 |
| FedAvg SFT, round 2 | 74.10 | 183 | 373 |

- Gold line: round 2 is 1.45 below the k = 0 line at 2 rounds (84 rows
  fixed, 115 broken, McNemar p 0.033) and 0.94 below its own round 1.
  It does not rise, so rounds 3 and 4 are not queued. On Spider, gold as
  chosen where the samples give no correct side is not kept.
- Centralized SFT: epoch 1 continued from example 624 of 8,659 (the
  stop of 2026-11-18), epoch 2 ran in one call (2 h 10 min, peak
  reserved 20,321 MB). Epoch 2 gains 0.65 over epoch 1 (p 0.34), so the
  rule goes on to epoch 3. Against centralized epoch 2: FedAvg round 2
  is 1.63 below (p 0.030); the k = 0 DPO line at 2 rounds is 1.45 above
  (173 against 142 rows, p 0.091).
- These evaluations ran with SQL in worker processes on the server
  (`exec_timeouts` 1 in each): the first runs of the pool on Windows.

Queue (owner): centralized SFT stands before the BIRD rounds; GPU 1
started with `--until 07:30`. The relabel of `bird/read` runs by hand
since about 01:00 and stands after `bird_sft/round_1` in the queue, so
a free card trains meanwhile. Its pace on client 1: 575 of 2,011
questions after 26 min, against 26 min for the whole client in the
first read (`run_times/bird/read.json`: generate 36 min, label 2 h 42
min); result not in yet. Measured on the Mac: the golds of the 8,659
Spider train questions (17,318 jobs) take 25.8 s in threads with the
earlier check and 4.5 s in 16 worker processes.

## 2026-11-20: BIRD train golds lost to the 30 s budget came from SQL run in threads; SQL now runs in worker processes (owner; code `0063d2a3`, `addba08d`..`4b4df521`)

Owner: the BIRD read gave 534 `gold_error` questions against about 400
counted on the Mac; check the 30 s budget, then avoid the fault as far
as possible on Spider and BIRD.

Measured:

- `bird/read` labels (`timeouts_r1_base.json`, `799543a1`): 534
  `gold_error` = 350 SQL errors (the Mac count; 330 in `retail_world`)
  + 184 golds on the budget (`donor` 71, `retails` 34,
  `world_development_indicators` 20, `language_corpus` 16; client 2 85,
  client 5 73). 196 samples of 94,280 labelled `exec_error` by a
  timeout, 10 without a label (budget ended on the gold).
- The 184 golds and the 8 golds of the unlabelled samples run once
  alone on the server, stop at 60 s (`gold_retime_r1_base.json`,
  `b2aeef14`): 159 under 15 s, 13 in 15 to 30 s, 6 in 30 to 60 s, 14
  over 60 s. Of the 184: 151, 13, 6, 14.
- Cause, measured on the Mac with the repository's timeout code: the
  budget check is a Python call from SQLite every 1,000 steps, and in
  threads it waits for the interpreter lock. One 0.3 s query: 0.4 s
  alone; 0.4 s in 4 threads; about 260 s in 4 threads next to one busy
  Python thread; about 5 s the same at 100,000 steps; 0.4 s in 4
  processes. Not measured on the server itself.
- Committed evaluations: every row that timed out is slow on its own.
  Run alone on the Mac, the predictions of BIRD dev rows 106 and 369
  take 98 s and 141 s, the gold of row 701 over 180 s, the predictions
  of Spider test rows 1044 and 1040 (`aan_1`) 112 s to over 180 s. No
  published EX lost a row to load.
- Spider train labels: `gold_error` is 3 of 8,659 in all 16 label steps
  (the 3 golds known not to run). Samples labelled `exec_error` by a
  timeout on Spider: not counted (sample files are on the server).

Changed (owner: yes to SQL in processes, a sparser check, a second run
alone, timeouts written in the results):

- Every prediction and gold of an evaluation or a label step runs in a
  worker process (`fedls_sql/eval/sql_pool.py`), as the official BIRD
  evaluator runs each pair in a process of an `mp.Pool` with one 30 s
  budget (`DAMO-ConvAI/bird/llm/src/evaluation.py`, read 2026-11-20).
  The check comes every 100,000 steps. A job that meets its budget next
  to other jobs runs once more with no other job of the pool running,
  and that result counts. A worker that fails stops the run.
  Evaluations write `exec_timeouts`; pair counts carry
  `questions_gold_timeout` and `samples_exec_timeout` when not zero.
  Budgets unchanged (30 s BIRD pair, 60 s Spider query).
- Checked on the Mac: the committed predictions scored again through
  the pool give the committed EX, 1,675 of 2,147 on Spider test (k = 0
  round 4, 78.02) and 452 of 1,534 on BIRD dev (base student, 29.47;
  its 3 timeouts time out alone too). 520 tests pass.
- BIRD scorer is v3. The Spider scorer keeps its name (my choice: under
  the threads no Spider gold met the budget and no evaluation row was
  lost; a new name would stop the running Spider lines at their
  identity checks).
- `scripts/relabel_samples.py` labels the samples of `bird/read` again
  into `fedpref_bird_base_p2_ddl_alpha01_ev3_s0`; the BIRD DPO lines
  (`bird_k0`, `bird_fixed`, `bird_k0_gold`) run in `_ev3` roots and wait
  for it (`bird/relabel`, `bird/read_relabelled`). The first read stays
  as it is.

Not done: the relabel has not run (how many of the 184 come back is not
known; 151 fit by their time alone); the pool has not run on Windows.
Open for the owner: the label step runs a gold twice in one budget, so
the 13 golds of 15 to 30 s stay `gold_error`; running the gold once per
question would take them in (0.14% of the questions).

## 2026-11-20: a stopped and continued run keeps its results and its totals (owner; code `a1679b75`)

Owner: later runs must give the right numbers whatever is restarted,
stopped or continued. Read through every step for what a stop does.

Found wrong and fixed:

- SFT with dropout (FedAvg SFT, centralized SFT; LoRA dropout 0.05). A
  call that continued a checkpoint seeded itself again, so its dropout
  masks were not those of the uninterrupted training: a valid training,
  but another one. The checkpoint now holds the state of torch's
  generators; the test stops a training with dropout at a checkpoint,
  continues it and gets the same weights, and fails without the fix. No
  committed result is touched: all 20 FedAvg SFT client trainings ran in
  one call. `refs/central_sft` was stopped in epoch 1 under the earlier
  code: its continuation of that epoch is not the uninterrupted one
  (logged here so the row is read with it); from its next checkpoint on
  it is.
- Times of a continued DPO training covered the last call only. Now each
  update keeps its seconds in the checkpoint and the reference pass keeps
  its own, so `update_seconds` and `reference_seconds` count the whole
  training once whatever the number of calls (`calls`); peak memory is
  over all calls.
- Times of a continued SFT training: `calls`,
  `elapsed_seconds_all_calls` and the peak over all calls, next to the
  last call's numbers.
- Sampling and labels: a call killed inside the step left no trace and
  the next call's entry looked like the whole step. Each step now writes
  a `started` entry before and a `done` entry after, with the questions
  it found left; `round.json` sums them and `complete` is false when a
  call was stopped inside a step (its times are then in the task log).

Checked and already right: a continued DPO training equals the
uninterrupted one (seeded pair order, no dropout, test on the weights);
samples and labels are kept per question, evaluations per row; pairs
are rebuilt from the samples and compared; aggregation and publication
are written whole or not at all.

Where a part is unknown (a checkpoint of earlier code) the total is
`null`, never a part given as the whole. The rule is in
`fedicl-sql/AGENTS.md` (Hard rules) and
`docs/PROTOCOL_V2.md`, "Runs that are stopped and continued". 510 tests
pass on the committed tree. Not run on the server: the first round that
starts after the next pull writes the new fields.

## 2026-11-20: wall times of the finished tasks are in Git: 46 tasks since the reset (result `5aa73a62`, code `a2230da9`)

`scripts/log_times.py` ran on the server's logs: one file per finished
task under `audits/protocol_v2/run_times/`. The steps it reads cover 98%
or more of each round's time, so the parser matches the real logs. Its
cut was the day 2026-11-17, which let in 13 tasks of the earlier setup
from that morning (`gate_s0`, `sqlcv2_s0`, `synvc_s0`, `vote_s0`); the
cut is now 2026-11-17 11:20 and those 13 files are removed.

Spider, wall time per round on one A5000 (h:mm; FedAvg SFT from its own
records):

| Round | FedAvg SFT, training | DPO from the base student (k = 0): sampling + labels + training | Pairs |
|---|---|---|---|
| 1 | 2:02 | 0:20 + 3:05 | 8,908 |
| 2 | 2:05 | 0:19 + 1:45 | 4,566 |
| 3 | 2:06 | 0:19 + 1:15 | 3,222 |
| 4 | 2:11 | 0:18 + 1:06 | 2,740 |
| All | 8:24 | 8:27 | |

- Four rounds cost the same wall time for both lines (8:24 against
  8:27) and end at 74.71 against 78.02. A DPO round gets cheaper each
  round because fewer questions stay mixed.
- Within a DPO round's training about one fifth is the reference pass
  (round 1: 0:36 of 3:05).
- Round 1 with the gold rule: 14,050 pairs, 4:15 of training.
- `bird/read`: sampling 0:35, labels 2:42 with 4 workers (Spider: 0:02
  with 16). Labels are 82% of a BIRD sampling step.

What the earlier rounds now hold for the paper: EX and EM per question
with the prediction and the error; question kinds, samples by outcome
and pairs per client; loss, margin and accuracy per update; peak
memory; update norms and cosines; wall time per step. Not held and not
recoverable without running again: the preference and NLL parts of the
loss per update. Not held but countable on the server without a GPU:
tokens trained on (from the pairs). Bytes sent follow from the adapter
size (73,911,080 bytes) and the clients that trained.

Stops, checked against the files (owner: do stops change the numbers):

- Results. Every evaluation ran in one start. FedAvg SFT: the task was
  stopped twice, both times between rounds; all 20 client trainings are
  recorded as `fresh`. DPO: a stop inside a client's training continues
  from a checkpoint (adapter, optimizer, schedule; every 25 updates),
  the order of the pairs is a seeded shuffle and the LoRA dropout is 0,
  so the continued training is the uninterrupted one (the test compares
  the weights, equal to 1e-6). Two clients were continued this way:
  client 3 of `decide/k0_gold/round_1` (from update 25 of 206) and
  client 4 of `decide/wrfirst/round_1` (from 75 of 148). The stop of
  `dpo_k2/round_1` fell after client 1. No round was stopped while
  sampling.
- Times. The table above uses only rounds run in one start. A continued
  round's task total also holds the updates done again after the last
  checkpoint, and its interrupted client has no full step. Times are
  wall time on a machine whose other card may run a task: five
  trainings on the same 8,026 pairs took 3:02 to 3:08, so that effect
  is about 3%. The FedAvg column is the trainer's own clock; by the
  task log the four rounds with their four evaluations took 8:45.

## 2026-11-20: loss parts, setup time and environment recorded; times of finished tasks read from the logs (owner; code `03f0eb9a`, `15032280`)

Owner: later runs must hold every result and setting the paper needs,
and the earlier runs are filled in from the logs on the server.

- Later runs (every task that starts after the server pulls the code):
  each update's loss is recorded with its preference part and its NLL
  part; `timing` gains the seconds before the first update; `round.json`
  carries the runtime environment. With the
  entry below this closes what was missing in the preference rounds. A
  call that continues a checkpoint written by the earlier code works;
  its earlier updates keep the total loss only.
- Earlier runs: `scripts/log_times.py` reads `.queue_state/logs/` on the
  server and writes `audits/protocol_v2/run_times/<task id>.json` for
  every task that finished since 2026-11-17: per start of the task the
  GPU, command, start, end, seconds and exit code, and the steps its
  lines show (generation, labels per client, training per client with
  the reference pass and the updates, aggregation). A file is written
  once and never changed, because the publication step refuses a
  checkout with changed tracked files; a rerun adds the tasks finished
  since. Tested on logs built from the code's own format strings, not
  yet on the server's logs: the first run there is the check
  (`PIPELINE_NEXT.md`, Run now).
- What the logs cannot give back for the rounds already run: the
  preference and NLL parts of the loss. Token counts can still be
  counted from the pairs, which are on the server only.

`docs/PROTOCOL_V2.md`, section "What each run records", lists the files
per kind of run. 502 tests pass.

## 2026-11-19: base student on the BIRD clients: a correct SQL among 10 samples for 52.4% of the questions (results `55b883c9`, `799543a1`)

`bird/read`: 10 samples at T 1.0 for each of the 9,428 BIRD train
questions at 5 clients, labelled by execution under the 30 s budget
with 4 workers; 20:23 to 23:42. Spider, same read: 87.6% with a correct
sample, 12% all wrong.

| Client | Questions | All correct | Mixed | All wrong | Gold fails | of them: budget / SQL error | Pairs (2 per mixed question) | Sample accuracy |
|---|---|---|---|---|---|---|---|---|
| 1 | 2,011 | 34 | 1,142 | 817 | 18 | 14 / 4 | 2,284 | 23.6% |
| 2 | 1,595 | 26 | 783 | 695 | 91 | 85 / 6 | 1,566 | 17.5% |
| 3 | 2,080 | 25 | 1,119 | 925 | 11 | 11 / 0 | 2,238 | 18.8% |
| 4 | 683 | 20 | 337 | 325 | 1 | 1 / 0 | 674 | 21.3% |
| 5 | 3,059 | 51 | 1,402 | 1,193 | 413 | 73 / 340 | 2,804 | 18.2% |
| All | 9,428 | 156 (1.7%) | 4,783 (50.7%) | 3,955 (41.9%) | 534 (5.7%) | 184 / 350 | 9,566 | 19.6% |

- DPO from the base student without gold trains on half of the BIRD
  questions (4,783 of 9,428); 3,955 questions have no correct sample
  and give no pair. On Spider that share was 12%. The gold rule
  (`bird_k0_gold/round_1`, queued) adds those 3,955 questions; this is
  where it is read with the most at stake.
- Gold fails, 534: 350 SQL errors as counted before (`retail_world`
  330, `works_cycles` 10, `app_store` 6, `shooting` 4; 208 `no such
  column`, 142 `no such table`) and 184 golds that met the 30 s budget
  (`donor` 71, `retails` 34, `world_development_indicators` 20,
  `language_corpus` 16, `movie_platform` 11, `talkingdata` 11,
  `bike_share_1` 8, others 13). About 50 were expected
  (`fedicl-sql/AGENTS.md`); whether the other 130 are slow golds or the
  effect of 4 labels running at once is read by timing each gold alone (`label_timeouts --retime`,
  `PIPELINE_NEXT.md`). Until then the workers stay at 4.
- Samples that met the budget: 196 of 94,280 (0.2%), in 154 questions;
  10 samples in 8 questions were left without a label because the
  budget ended on the gold.
- 8,947 samples (9.5%) were cut at 256 new tokens at T 1.0 (greedy on
  BIRD dev: 1 of 1,534). They count as wrong samples.
- 271 questions have a gold that returns no rows (186 of them mixed):
  a sample that returns no rows is labelled correct there.

The split of the gold fails was counted by `scripts/label_timeouts.py`
(code `0063d2a3`).

## 2026-11-19: what the result files record, checked; wall time added to the preference rounds (owner; code `5f34c048`)

Owner: is everything recorded that the paper may need, so that nothing
has to run again. Checked on the committed files. Evaluations: one row
per question with the prompt, the prediction, EX, EM, the execution
error, token counts and the finish reason, so every accuracy breakdown
(per database, BIRD difficulty, error kinds, tests) is computed later
without a GPU. FedAvg SFT rounds: seconds, examples, updates, loss, peak
memory per client and bytes sent. Preference rounds: pairs and question
kinds per client, loss, margin and accuracy per update, peak memory,
update norms and cosines; they had no wall time, token count or bytes
sent in the files (times were only in the console and in the logs on
the server). Added from this commit on, for every run that starts after
the server pulls it: per client `timing` (seconds of the call and of the
updates, updates measured in this call, the update it resumed from) and
`sequence_tokens` in `client_N_train.json` and `round.json`;
`timing.json` in the round's folder with the seconds of the generation
and of each client's labels (for a pair read: `pair_read/timing_rN.json`);
`communication_bytes` in `round.json`. None of it enters a signature or
an identity (496 tests pass). For the rounds already run, the times are
in the logs on the server (`.queue_state/logs/`, a timestamp per line)
and in no committed file; bytes sent follow from the adapter size
(73,911,080 bytes, as in the FedAvg record). Not recorded and not added:
the preference and NLL parts of the loss per update (the total, the
margin and the accuracy are). Adapters, samples and logs exist on the
server's drive D only.

## 2026-11-19: what CMC and JIIS require and publish, read (owner; `JOURNAL_BAR.md`)

Owner: have the two target journals researched for what to learn before
writing. 7 CMC papers read in full, 4 JIIS papers in full and 5 by
abstract; the closest two (LESFT at CMC, GradeSQL at JIIS) read a second
time from the source. One seed with McNemar tests is the protocol of
GradeSQL (JIIS, "a fixed seed of 42", Bonferroni correction) and more
than any CMC paper read reports. The gap against both samples is one
model: every CMC language-model paper has 3 or more (LESFT: Qwen2.5-0.5B,
1.5B, 3B), GradeSQL has 7. Also seen in the federated papers and not in
our plan yet: a cost or communication table, one federated factor
varied, 4 or more baselines. JIIS fits the topic better and costs
nothing (25 pages, LaTeX); CMC is faster (USD 1,600 for 15 pages). Both
require the use of AI tools to be disclosed. Not verified: the SJR and
JCR quartiles. Nothing is queued from this; which gaps to close is the
owner's decision.

## 2026-11-19: the gold line is carried on: round 2 on Spider, round 1 on BIRD (owner; queue `1ac2c545`)

Owner: the k = 0 line with gold was higher at round 1 (76.67 against
75.87) and that is enough to follow it; its level after more rounds was
never read. The rule `--gold-chosen --gold-on-empty-databases` uses the
gold SQL only where the samples give no correct side (all-wrong
questions; databases without rows), so DPO stays the main part and the
all-correct questions are left alone. Its pairs do not run out the way
the k = 0 line's do (8,908, 4,566, 3,222, 2,740). Queued:
`k0_gold/round_2` (Spider, on-policy, in the root of `decide/k0_gold`;
the round 1 command with another round number), first among the tasks
not started so that GPU 1 takes it at once; read against k = 0 round 2
(77.18; 92 / 398), rounds 3 and 4 follow if it still rises.
`bird_k0_gold/round_1` (BIRD, same rule, samples of `bird/read` copied
into a root of its own), after `bird_k0/round_1`; read against
`bird_k0` and `bird_sft` at 1 round. BIRD train has no database without
rows, so there the rule is gold as chosen for all-wrong questions. Each
with evaluation and publications (test; 495 tests pass, 2 skipped).
Reading note: round 1 of the gold line trains on 14,050 pairs, about
the pairs of k = 0 rounds 1 and 2 together (13,474; 77.18), so at equal
rounds it has trained more. Proposed in chat and dropped, not run: NLL
on the gold SQL for every question without a pair in the same local
loss as DPO; by round 3 only 19% of the questions give a pair, so most
of such a round would be SFT (owner).

## 2026-11-19: the wrong-result count hides a turnover; the three lines solve different questions (no new run)

Question by question on Spider test from the committed predictions (C
correct, E execution error, W wrong result; script run in chat, not
committed). From the untrained student (C 1,461, E 287, W 399):

| To | E to C | E to W | E to E | W to C | W to E | W to W | C to W | C to E |
|---|---|---|---|---|---|---|---|---|
| FedAvg SFT round 4 | 107 | 77 | 103 | 128 | 38 | 233 | 60 | 32 |
| k = 0 round 4 | 147 | 94 | 46 | 130 | 13 | 256 | 53 | 10 |
| k = 2 DPO round 2 | 144 | 93 | 50 | 157 | 19 | 223 | 68 | 15 |
| k = 3 DPO round 1 | 139 | 87 | 61 | 167 | 24 | 208 | 67 | 26 |

The wrong results near 400 in every run are a net figure: each line
fixes 130 to 167 of the 399, takes in 87 to 94 questions that used to
fail to execute, and breaks 53 to 68 that were right. This corrects the
wording of the entry "the wrong results are where the untrained student
left them" below: the count stays, the questions do not. Across the
three lines at 4 rounds (k = 0, 2, 3; 1,675, 1,679, 1,674 right): right
in all three 1,508, right in at least one 1,830 (85.2%), wrong in all
three 317; wrong in every run of the table and the untrained student
256. Reading: the lines reach the same EX on partly different questions
(322 are solved by some and not all), and each loses 63 to 93 questions
the untrained student had right. No run so far tests a round that
trains on the gold SQL and on the pairs in one local loss.

## 2026-11-19: on-policy rounds read on BIRD: round 2 on the round 1 pairs queued (owner; queue `6b18a407`)

Owner: carry out the read of on-policy rounds on BIRD. On Spider at
k = 2, round 2 on the round 1 pairs with a fixed reference gives 78.02
against 78.20 on-policy (p 0.78) with 8,026 pairs against 3,354, so
re-sampling shows no gain there; BIRD is where the base student is weak
and the samples may change more between rounds. Queued after
`bird_k0` round 2: `bird_fixed/round_2`, the command of
`bird_k0/round_2` in a root of its own
(`fedpref_bird_base_p2_fixed_ddl_alpha01_s0`) with `--continue-from` the
`bird_k0` root at round 1, `--samples-from-round 1` and
`--fixed-reference`; then its evaluation on BIRD dev and both
publications. It trains one round and samples nothing. Checked before
queuing (new test): a line that continues a line from the base student
with both flags trains from that line's round 1 global adapter, on that
line's round 1 pairs, with that line's fresh LoRA initialisation (the
base student) as the reference, and writes nothing in that line's root.
494 tests pass, 2 skipped. Not run: nothing on BIRD has trained yet;
time (3 h) and memory are estimates. The matching round on Spider from
k = 0 is not queued.

## 2026-11-19: base student on BIRD dev: 29.47, 42% of the outputs fail to execute (result `bfa497a8`)

`bird/zs`: base student, BIRD dev (1,534 rows), evidence, `ddl` prompt,
greedy, 256 new tokens: EX 29.47 (452 right; easy 44.33, medium 34.53,
hard 21.78, extra 15.81 by structural hardness), EM 4.69. Execution
errors 646 (42.1%), wrong results 436 (28.4%). Of the errors, 570 are
`no such column`: in 529 the column is in the prompt's schema and is
taken from the wrong table or alias, in 11 it is spelled another way, in
30 it is not in the schema (counted with a pattern over the schema text
of the prompt). The rest: 29 syntax, 26 `no such function`, 10 misuse of
an aggregate, 7 `no such table`, 3 timeouts of the 30 s pair budget
(rows 106 and 369 on the prediction, row 701 on the gold SQL).
One output is cut at 256 tokens. By database EX runs from 11.2
(`california_schools`, 63% errors) to 42.6 (`european_football_2`). The
run took 272 s. Reading: the 256-token limit is not a factor on BIRD dev
(1 row), and the budget costs 3 rows. On Spider the same student starts
at 68.05 with 13% execution errors, and training removed mostly those;
on BIRD the errors are three times that share, so there is more of what
the method has removed so far. The level printed in the Qwen2.5-Coder
report for this size is in a figure only (Figure 12, no table), so it is
not compared here.

## 2026-11-19: k = 3 gives 77.97 at 4 rounds: no gain from the SFT stage on Spider at k = 0, 2 or 3 (results `bc901890`, `b3075597`)

`decide/k3`: DPO + NLL round 1 from FedAvg SFT round 3, 2 random pairs
per question (7,220 pairs from 4,629 mixed questions; all wrong 483, all
correct 3,544; 452 updates; peak reserved 17.01 to 18.94 GiB). Spider
test: 77.97 (easy 91.28, medium 80.86, hard 72.35, extra 60.78), EM
65.11, execution errors 111, wrong results 362, one cut output.

| At 4 total rounds | EX | exec errors | wrong results | k = 3 fixed | k = 3 broke | p |
|---|---|---|---|---|---|---|
| k = 3 (3 SFT + 1 DPO) | 77.97 | 111 | 362 | | | |
| k = 2 (2 SFT + 2 DPO) | 78.20 | 84 | 384 | 68 | 73 | 0.74 |
| k = 0 (4 DPO) | 78.02 | 69 | 403 | 133 | 134 | 1.00 |
| FedAvg SFT round 4 | 74.71 | 173 | 370 | 146 | 76 | 3e-06 |

Against its start (FedAvg round 3, 74.71): fixed 149, broke 79,
p 4e-06. Reading: at 4 total rounds the three lines are the same within
a rerun (77.97, 78.20, 78.02), each 3.3 to 3.5 above FedAvg SFT. More
SFT rounds before DPO leave more execution errors and fewer wrong
results (69 / 403, 84 / 384, 111 / 362), the same trade seen with gold
inside the round, and the sum does not move. On Spider the SFT stage is
not a part that shows an effect; BIRD is read next.

## 2026-11-19: queue turned to what settles the method: SFT and DPO from the base student on BIRD; the long Spider DPO line dropped (owner; queue `186aaf58`, `80b6f287`)

Owner: drop the long DPO line from FedAvg round 3 (`dpo/after_fedavg`)
and queue what is needed to settle the method. Settled on Spider: DPO +
NLL with execution labels on the model's own samples (NLL term and
preference term each show a gain). Open: the FedAvg SFT stage (no gain
on Spider at 3 and 4 rounds; the owner's concern is a harder dataset)
and, after it, a gold path for the questions without a correct sample.
Queued after `bird/read`, in this order, each round evaluated on BIRD
dev and published: `bird_sft/round_1` (FedAvg SFT on the BIRD clients),
`bird_k0/round_1` (DPO + NLL from the base student on the samples of
`bird/read`), `bird_sft/round_2`, `bird_k0/round_2`. The FedAvg commands
are those of the Spider line with the BIRD split, profile, schema text,
stage label and root; the DPO rounds those of the Spider k = 0 line with
the BIRD split, profile, schema text, root and 4 score workers, and one
setup with `bird/read` (test; 492 tests pass, 2 skipped with the removed
curve). Read at the same number of rounds. The line with an SFT stage on
BIRD (DPO from a `bird_sft` round) and the gold path are queued after
round 1 of both lines and the read are in. The curve
`fedpref_sft_ddlrows_alpha01_s0/dpo` and its task are removed from the
queue; `decide/k3` keeps its one round. Centralized SFT on Spider now
follows the BIRD rounds. One commit (`186aaf58`) emptied
`tests/test_active_queue.py` by mistake; restored in `80b6f287`, no run
was affected.

## 2026-11-19: the rejected-side rules flip the error type on the same questions (no new run)

Question by question on Spider test, from the committed predictions
(outcome C correct, E execution error, W wrong result; the script was run
in chat and is not committed):

| Pair | E to W | W to E | E to C | W to C | C to E or W |
|---|---|---|---|---|---|
| random R1 (`be787676`) to wrong-result first R1 (`cd4727a7`) | 6 | 38 | 11 | 27 | 42 |
| random R2 (`5c33e622`) to wrong-result first R2 (`06e81fdf`) | 5 | 16 | 5 | 12 | 28 |
| random R1 to gold chosen (`cf644e95`) | 13 | 27 | 11 | 27 | 39 |
| k = 0 R1 (`96007ff6`) to k = 0 gold rule (`9e7c66b0`) | 43 | 10 | 26 | 64 | 73 |

Reading: most of the drop in wrong results under wrong-result first is
the same questions turning into execution errors (38 of 43), and most of
the drop in execution errors under the gold rule is the same questions
turning into wrong results (43 of 44). About 320-356 wrong results and
74-82 execution errors stay in both runs of each pair. The rules change
how the model fails on questions it does not solve; they do not add
correct answers. A rule that mixes both rejected kinds can at most hold
back these flips (about 40 questions per run), not reach the stable
errors.

## 2026-11-19: BIRD zero-shot and pair read queued after k = 3 (owner; queue `4045d3af`)

Owner: queue the two BIRD runs, labels with 4 workers. `bird/zs` (base
student on BIRD dev, evidence, `ddl`, arm `zs_bird_ddl_vllm_inproc`) and
`bird/read` (10 samples per question at T 1.0 from the base student on
the BIRD `alpha_0.1/k5` clients, labelled with the BIRD evaluator,
`--score-workers 4`, root `fedpref_bird_base_p2_ddl_alpha01_s0`, 2 pairs
per question so that round 1 from the base student reuses the samples),
each with its publication, after `decide/k3` and before centralized SFT.
The read differs from `pairread/base_ddl_rows` in split, profile, schema
style, root, pairs per question and score workers; the zero-shot from
`prompt/zs_ddl_rows` in arm, set and schema style (test; 493 tests pass).
No training in either. Not measured on BIRD: run time and the share of
samples that hit the 30 s budget.

## 2026-11-19: wrong-result rejects in round 2 trade error types again, not kept (results `0f698bfa`, `06e81fdf`)

`decide/wr_round2`: DPO round 2 after dpo_k2 round 1, same samples as
dpo_k2 round 2 (3,354 pairs), rejected side from wrong results first
(2,198 wrong-result rejects against 1,921). Spider test: 77.69 (easy
91.70, medium 80.98, hard 70.84, extra 60.22), execution errors 107,
wrong results 372, no cut output.

| Against | EX | exec errors | wrong results | Fixed | Broke | p |
|---|---|---|---|---|---|---|
| dpo_k2 round 2, random pairs | 78.20 | 84 | 384 | 17 | 28 | 0.14 |
| dpo_k2 round 1 (its start) | 77.46 | 99 | 385 | 43 | 38 | 0.66 |
| k = 0 round 4 | 78.02 | 69 | 403 | 115 | 122 | 0.70 |

As in round 1: 12 fewer wrong results, 23 more execution errors, EX 0.51
lower (p 0.14). The rule moves errors from one type to the other at a
loss and is not kept; the first queued use of `--continue-from` ran
without a stop. Peak reserved 14.39-18.97 GiB, 211 updates.

## 2026-11-19: the 256-token limit and the execution budgets against the published code (no run)

Read today in the code of each source:

| Source | New tokens | Execution budget | A timeout scores |
|---|---|---|---|
| BIRD official (`DAMO-ConvAI/bird/llm/src`: `gpt_request.py`, `evaluation.py`) | 256 | 30 s for prediction and gold together (`--meta_time_out` default 30.0) | 0 |
| Spider test-suite (`taoyds/test-suite-sql-eval`, `exec_eval.py`) | | 60 s per query (`TIMEOUT = 60`) | 0 ("wrong if execution fails") |
| CodeS (`text2sql_zero_shot.py`) | 256, 4 beams | | |
| Qwen2.5-Coder evaluation (`bird-spider/test.sh`) | 1,024 | 30 s | |
| OmniSQL (README; `infer.py` not found) | 2,048, output holds reasoning | | |

Ours: 256 new tokens, 60 s per query on Spider, 30 s per pair on BIRD, a
timeout scores 0: the official evaluators' values. On Spider test the
limit does not bind: over the 20 committed arms the median output is
20-27 tokens, the 99th percentile 84-126, the longest finished output
209; 16 arms have no cut output, the others 2-4 (outputs that run to the
limit, not long SQL). Timeouts on Spider test: 0 or 1 of 2,147 per arm.
On BIRD 6 of the 1,534 dev golds and 1 train gold are longer than 256
tokens; the outputs of the model on BIRD are not measured yet. Kept as
they are; the zero-shot run on BIRD dev gives the number of cut outputs
and of timeouts, and the limit on BIRD is read again on that.

## 2026-11-19: BIRD train as a second set of clients, set up and checked on the Mac; nothing queued (owner; code `ab6bc960`..`3cfd42d3`)

Owner: BIRD clients are prepared before the decision on the SFT stage,
with the prompt as BIRD is prompted (evidence). Done on the Mac, CPU
only.

- Prompt, checked against the Qwen2.5-Coder evaluation code
  (`qwencoder-eval/instruct/bird-spider/sql_suites/preprocess_bird.py`,
  read twice, the second time independently): schema is `CREATE TABLE`
  text without rows (`SCHEMA_EXAMPLE_ROWS = 0`, our `ddl`); the lines
  `-- External Knowledge: {evidence}` and `-- Using valid SQLite and
  understanding External Knowledge, ...` go on every question, the
  evidence as given. Ours left them out when the evidence was empty and
  stripped it: fixed. On all 1,534 BIRD dev rows our text equals the
  source's except `sqlite_sequence`, which our schema leaves out (4 dev
  databases; as on Spider, kept). The Spider prompt hashes are pinned by
  a test and did not change.
- Length (limit 7,168): `ddl` longest BIRD train sequence 6,807 tokens,
  longest dev prompt 2,207, no row over; `ddl_rows` 872 train rows over
  (longest 220,797), `ddl_values` 474. BIRD runs use `ddl`.
- Split `BIRD/original_train9428_dev1534/federated/alpha_0.1/k5`, built
  as the Spider main split (Dirichlet 0.1 over 4 database tiers, seed
  42, a database whole at one client): 16 / 14 / 16 / 5 / 18 databases,
  2,011 / 1,595 / 2,080 / 683 / 3,059 questions. Tiers by share of hard
  and extra golds, the levels from Spider's hardness rules on sqlglot's
  parse (Spider's own parser reads 15% of BIRD golds; the new one agrees
  with it on 8,656 of 8,658 Spider train golds). Checked here: the five
  files are the centralized train rows exactly, no database at two
  clients, none shared with BIRD dev.
- Golds (one thread on the Mac): no BIRD train database is empty; 350
  golds raise an SQL error (340 at client 5, mostly `retail_world`), 9
  run over 60 s, about 40 more spend the 30 s pair budget; 398 questions
  would be labelled `gold_error` and give no pair. Two BIRD dev golds
  spend the pair budget and score 0 for every arm.
- Code: a public pool that holds a client database is rejected; BIRD
  rows take hardness from the sqlglot rules; a pair whose budget ends on
  the gold side is a timeout instead of a crash, and such a sample gets
  no label (it ran, its result was never compared) rather than
  `exec_error`. 492 tests pass.
- Not done: no run on the server. The memory of BIRD training is not
  measured, the labels under several score workers are not timed, the
  FedAvg SFT command was read but not run.

Open for the owner: queue the read of the base student on BIRD
(sampling and labels, no training) and the zero-shot evaluation on BIRD
dev; keep or drop the 350 failing golds for FedAvg SFT; 256 new tokens
(6 BIRD dev golds are longer).

## 2026-11-19: k = 0 round 4 reaches 78.02, equal to the k = 2 line at 4 rounds (results `4fd84bee`, `4215a7e1`)

Spider test: 78.02 (easy 88.94, medium 81.10, hard 72.57, extra 63.31),
EM 54.73, execution errors 69, wrong results 403, no cut output.

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|
| 1 | 72.43 | | 75.87 |
| 2 | 74.10 | | 77.18 |
| 3 | 74.71 | 77.46 | 77.69 |
| 4 | 74.71 | 78.20 | 78.02 |

| k = 0 round 4 against | Fixed | Broke | p |
|---|---|---|---|
| k = 0 round 3 (77.69) | 48 | 41 | 0.53 |
| k = 2 DPO round 2 (78.20; 4 rounds each) | 116 | 120 | 0.85 |
| fixed pairs and reference with NLL, round 2 (78.02) | 121 | 121 | 1.0 |
| FedAvg round 4 (74.71; 4 rounds each) | 178 | 107 | 3.1e-05 |

At 3 and at 4 total rounds the line without the FedAvg SFT stage equals
the line with it (p 0.80, p 0.85): on Spider with this student the SFT
stage shows no gain. The k = 0 line: 75.87, 77.18, 77.69, 78.02; the
steps after round 2 are within what a rerun gives (+0.51 p 0.27, +0.33
p 0.53). Round 4 trained on 2,740 pairs (174 updates; rounds 1-3: 8,908,
4,566, 3,222), peak 18.84 GiB. Training questions with no correct
sample: 1,074, 902, 886, 860 at the start of rounds 1-4. Whether the
stage stays in the method is the owner's decision; the owner's concern
(2026-11-19) is a dataset or model where the base student has no correct
sample for many more questions, so BIRD clients are being set up before
the decision.

## 2026-11-19: reading: training removes execution errors; the wrong results are where the untrained student left them (no new run)

Spider test, from the committed metrics:

| Run | EX | EM | exec errors | wrong results |
|---|---|---|---|---|
| Student without training | 68.05 | 53.33 | 287 | 399 |
| FedAvg SFT round 4 | 74.71 | 64.46 | 173 | 370 |
| k = 2, DPO round 2 | 78.20 | 64.42 | 84 | 384 |
| k = 0, DPO round 3 | 77.69 | 55.29 | 82 | 397 |

Every run so far has 342-444 wrong results against 399 without
training; the EX gains are execution errors removed (287 to 173 with
gold SFT, to 82-84 with DPO). Gold SFT moves EM by 11 points and DPO
from the base student by 2: the SFT stage teaches the form of the gold
SQL, which EX does not count. On the training questions the untrained
student already has a correct SQL among its 10 samples for 7,582 of
8,659 (87.6%). Whether Qwen2.5-Coder saw Spider in pre-training is not
stated in its report (arXiv 2409.12186, read 2026-11-19): section 7.4
evaluates on Spider and BIRD (split and metric not given, results only
in figure 12) and credits "finely crafted synthetic data during both
pre-training and fine-tuning" for the Text-to-SQL level; the data
sections name no Text-to-SQL dataset; the decontamination step (section
5, 10-gram overlap) names HumanEval, MBPP, GSM8K and MATH only.

## 2026-11-19: DPO from the base student matches the SFT-then-DPO line at 3 rounds; gold inside the round not kept (results `3f9ada19`, `9e7c66b0`, `2bdd4c73`, `a3fed6d6`, `548acdab`, `947ca9d8`)

Spider test, by total rounds trained (every row one federated round of
the 5 clients per round):

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) | k = 0 with the gold rule |
|---|---|---|---|---|
| 1 | 72.43 | | 75.87 | 76.67 |
| 2 | 74.10 | | 77.18 | |
| 3 | 74.71 | 77.46 | 77.69 | |
| 4 | 74.71 | 78.20 | running | |

| Run | EX | easy | medium | hard | extra | exec errors | wrong results |
|---|---|---|---|---|---|---|---|
| k = 0 round 1 | 75.87 | 90.43 | 79.00 | 68.90 | 58.26 | 101 | 417 |
| k = 0 round 1, gold rule (`decide/k0_gold`) | 76.67 | 89.79 | 80.28 | 68.47 | 61.34 | 57 | 444 |
| k = 0 round 2 | 77.18 | 90.64 | 80.51 | 70.84 | 59.66 | 92 | 398 |
| k = 0 round 3 | 77.69 | 90.43 | 80.98 | 70.41 | 62.46 | 82 | 397 |
| k = 2, DPO round 1 (3 rounds) | 77.46 | 91.49 | 80.63 | 71.06 | 59.66 | 99 | 385 |
| k = 2, DPO round 2 (4 rounds) | 78.20 | 91.91 | 81.91 | 71.06 | 60.50 | 84 | 384 |

Question by question (fixed, broke, exact McNemar p):

| Compared | Fixed | Broke | p |
|---|---|---|---|
| k = 0 round 2 against round 1 | 69 | 41 | 0.0097 |
| k = 0 round 3 against round 2 | 46 | 35 | 0.27 |
| k = 0 round 2 against FedAvg round 2 (2 rounds each) | 166 | 100 | 6e-05 |
| k = 0 round 3 against FedAvg round 3 (3 rounds each) | 170 | 106 | 0.00014 |
| k = 0 round 3 against k = 2 DPO round 1 (3 rounds each) | 124 | 119 | 0.80 |
| k = 0 round 3 against k = 2 DPO round 2 (3 against 4 rounds) | 109 | 120 | 0.51 |
| k = 0 round 2 against k = 2 DPO round 1 (2 against 3 rounds) | 131 | 137 | 0.76 |
| gold rule against k = 0 round 1 | 90 | 73 | 0.21 |
| gold rule against k = 2 DPO round 1 (1 against 3 rounds) | 106 | 123 | 0.29 |
| k = 0 round 2 against the gold rule (2 against 1 round) | 90 | 79 | 0.44 |

The k = 0 line: at the same total rounds DPO from the base student is
3.08 above FedAvg SFT at 2 rounds and 2.98 at 3, and equal to the k = 2
line at 3 rounds (+0.23, p 0.80). The FedAvg SFT stage shows no gain at
3 rounds; round 4 (running) is read against 78.20. Round 2 is a gain by
the rule (+1.31, p 0.0097); round 3 adds 0.51 (p 0.27). Pairs per round
8,908, 4,566, 3,222 (288 and 204 updates in rounds 2 and 3). On the
training samples the line leaves more questions with no correct sample
than gold SFT does: 1,074 (base), 902 after round 1, 886 after round 2,
against 573 after 2 FedAvg SFT rounds.

The gold rule (`--gold-chosen --gold-on-empty-databases`, round 1 from
the base student, same samples as k = 0 round 1): 14,050 pairs against
8,908, 5,142 with the gold as chosen (3,110 on databases without rows,
2,912 of them at client 4; 2,032 on questions whose samples are all
wrong); rejected sides 9,284 execution errors and 4,765 wrong results
(k = 0 round 1: 5,339 and 3,568). Client 4 gets 6,064 pairs (weight
0.43 in the average, 0.28 before). On test: +0.80 (p 0.21), execution
errors 101 to 57 (the lowest of any row), wrong results 417 to 444, 4
cut outputs. Not kept by the rule; the two settings do not run alone.
The added pairs are mostly "gold against a SQL that does not run", and
that is what moves on test: 44 fewer execution errors, 27 more wrong
results. Peak reserved 17.38-18.99 GiB (client 4 17.63), 880 updates.
k = 0 rounds 2 and 3 peak 18.94 and 18.90 GiB.

Server: the results came one after another in the order a single worker
gives (k = 0 round 2, then `decide/k0_gold`, then the evaluations at
12:09 and 12:13, round 3 at 13:57), so GPU 0 has run alone since 07:00
(inferred from the publication times; the owner has not sent the
worker's lines).

## 2026-11-19: wrong-result rejects queued for round 2; the NLL term stays (owner; queue `d1a3aa9f`)

Owner: the method keeps the NLL term. Wrong results on Spider test by
run: FedAvg rounds 2 and 3 373 and 379; DPO + NLL round 1 385 (random),
382 (nearest), 368 (gold chosen); round 2 384 (on-policy), 375 (fixed);
RFT 365; wrong-result rejects first 342. The gain of every DPO run so far
is in execution errors (183 at the start, 84-117 after); only the
wrong-result rule moves the wrong results, and in round 1 it pays for it
with execution errors (146). In on-policy round 2, 1,433 of the 3,354
rejected sides are still execution errors. Queued before `decide/k3`:
`decide/wr_round2`, a line that takes dpo_k2 round 1 as its own
(`--continue-from`, first queued use) and runs round 2 on the samples of
dpo_k2 round 2 (copied) with `--pair-rule wrong_result_first`; the
command differs from dpo_k2 round 2 in the rule, the root and the two
continue flags (test; 467 tests pass on the Mac). Read against dpo_k2
round 2 (78.20; 84 and 384). Root
`fedpref_sftr2_rand1wr2_ddlrows_alpha01_s0`, arm
`fedpref_sftr2_rand1wr2_dpo_ddl_rows_a01_r2_vllm_inproc`.

## 2026-11-19: without the NLL term DPO gains nothing; wrong-result rejects trade error types (results `aa05e549`, `cd4727a7`, `3a4759b5`, `f8485b4b`)

Both runs are DPO round 1 from FedAvg round 2 on its samples (8,026
pairs each), one setting changed. Spider test:

| Run | EX | easy | medium | hard | extra | exec errors | wrong results |
|---|---|---|---|---|---|---|---|
| FedAvg round 2 (the start) | 74.10 | 89.36 | 78.65 | 65.23 | 54.62 | 183 | 373 |
| RFT (NLL on correct samples only) | 75.87 | 90.43 | 79.35 | 67.60 | 59.10 | 153 | 365 |
| DPO without NLL (`decide/nonll`) | 73.59 | 88.94 | 75.50 | 68.03 | 56.02 | 167 | 400 |
| DPO + NLL, wrong-result rejects first (`decide/wrfirst`) | 77.27 | 91.06 | 79.70 | 71.49 | 60.78 | 146 | 342 |
| DPO + NLL, random pairs (dpo_k2 round 1) | 77.46 | 91.49 | 80.63 | 71.06 | 59.66 | 99 | 385 |

No NLL (NLL weight 0, same pairs, pair hashes not compared): against
DPO + NLL fixed 62, broke 145, McNemar p < 1e-6; against its start
FedAvg round 2 fixed 157, broke 168, p 0.58; against RFT fixed 123,
broke 172, p 0.005. Training reaches a larger margin (1.47-2.81 against
1.01-1.67) with the same accuracy, larger updates (norms 1.53-2.34
against 1.35-2.12), and the median output grows from 23 to 27 tokens.
Reading: the preference term alone does not move the model from its
start (as the papers on SFT then plain DPO report, `DPO_RESEARCH.md`
2.1); the NLL term alone gives +1.77; both give +3.36. The NLL term is
a part of the method by the rule. Round 1 of federated DPO as
`DPO_RESEARCH.md` describes OpenFedLLM (plain DPO, fixed pairs, fixed
reference; the paper was not read again today) is this run, since
round 1 has the same pairs and reference either way: 73.59, 3.87 below
the method. The fixed line of 2026-11-18 (77.64, 78.02) kept the NLL
term, so it is not that baseline.

Wrong-result rejects first: 5,526 of the 8,026 rejected sides are wrong
results (random: 3,939). Against random pairs fixed 38, broke 42,
p 0.74: the same EX. Wrong results fall from 385 to 342 and execution
errors rise from 99 to 146: the rejected side decides which errors DPO
removes, at about one for one. Not kept by the rule (no gain of 0.5).
Peak reserved 12.65-19.03 GiB in both runs.

## 2026-11-19: a worker can stop itself at a given time (owner; code `3958a1af`)

Owner: GPU 1 runs until 07:00 and stops by itself.
`scripts.gpu_worker run --gpu 1 --until 07:00` stops the worker and its
task at that local time the way Ctrl+C does (on Windows the Ctrl+C event
of the console; if the worker still runs 3 min later it ends its own
process tree); the task stays due and another worker continues it. Run
on the Mac with a throwaway queue: the worker stopped at the minute,
exit 0, no child left (466 tests pass). Not run on Windows yet.

## 2026-11-19: gold inside the DPO round from the base student queued; k = 0 runs before k = 3 (owner; code `c1784b46`)

Owner: run the gold rule whole, not by half. From the base student
4,205 of the 8,659 questions give no pair in round 1: 1,631 all right,
1,074 all wrong, 1,497 right and wrong on databases without rows, 3
whose gold does not run; the SFT stage trains on all of them. The run
`decide/k0_gold` is `decide/k0` round 1 on the same samples with two
settings: `--gold-chosen` (gold as chosen for an all-wrong question, in
the code since the k = 2 run, where it gave 77.41 against 77.46) and the
new `--gold-on-empty-databases`: on a database without rows the chosen
side is the gold SQL and the rejected side is drawn from the wrong
samples (an execution error or another result than the gold is wrong
whatever the rows; only "correct" says nothing there). A question there
whose samples all match the gold result still gives no pair: NLL on the
gold alone for those is not written (cut; 192 of the 1,648 such
questions of client 4). Without the setting every rule keeps its
identity and pairs (464 tests pass on the Mac). Root
`fedpref_base_p2_goldrule_ddlrows_alpha01_s0`, arm
`fedpref_base_p2_goldrule_dpo_ddl_rows_a01_r1_vllm_inproc`; about 14,000
pairs against 8,908 (estimate), FedAvg weights by pair count, so client
4 weighs more. Read against 75.87 (kept at +0.5 with p below 0.05) and
77.46. No prompt was rendered again: the command is that of `decide/k0`
round 1 with the two flags and another root (test).

Queue order now: `decide/k0_gold`, `dpo_k0/round_2..4`, then `decide/k3`
(it was before the k = 0 line): the open question is the start of the
method, and k = 3 only tunes k. At 03:28-03:29 the owner's log shows
`decide/wrfirst` on GPU 1 (client 3, peak reserved 18.98 GiB) and
`decide/nonll` on GPU 0 (client 1 done), so both cards are free at about
05:45 (estimate).

## 2026-11-19: direction recorded: content generated by the clients for their databases; to run after the method is settled (owner)

Source: an idea scan by research agents (three on ways to raise EX, one on
the empty databases). Their reports are in chat only. Paper numbers below
were read through page fetches, not by eye, and the agents' counts on the
public Spider files are not committed.

Measured here on committed predictions (Spider test, 2,147 rows):

| Row | Correct | Execution errors | Wrong results |
|---|---|---|---|
| FedAvg round 3 | 1,604 | 164 | 379 |
| FedAvg round 4 | 1,604 | 173 | 370 |
| DPO round 2 (k = 2) | 1,679 | 84 | 384 |

The 75 questions gained over FedAvg round 4 are execution errors removed;
the wrong results do not fall. FedAvg rounds 3 and 4 give the same 74.71
with different predictions (44 questions each way).

Why the wrong results may not move (agent counts, not committed):

- The seven databases without rows hold 1,759 questions (20.3%), 792 of
  the 1,579 training SQL with two or more JOINs and 753 of the 1,446 with
  DISTINCT. They give no pair in the DPO rounds.
- The other databases are small (median 9.3 rows per table). Removing
  DISTINCT from the gold SQL leaves the result unchanged in 168 of 434
  cases.
- Pairs fall from 8,026 to 3,354 between DPO rounds 1 and 2 and the
  all-correct questions rise from 33% to 67% (read by an agent from the
  committed `round.json` files).

Direction (owner: recorded, not started). Each client generates content
for its own databases: rows in foreign-key order, typed values, seeded
with the literals of its own gold SQL, and for a gold SQL that still
returns nothing a chain of rows that satisfies its joins and filters. First
for the seven empty databases, then a few variants of every database, a
sample counting as correct only if it matches gold on every variant. The
samples of the 1,759 questions are already stored (sampling covers every
question; `skip_empty_databases` acts at the pair step), so a trial round
needs relabelling on CPU and training, no new sampling.

| Step | What | Where | Stop if |
|---|---|---|---|
| 1 | The generator; share of gold SQL with a non-empty result on the seven databases | Mac, CPU | under 85% |
| 2 | Relabel the stored round 1 samples; count the new pairs and what the rejected side is | server, CPU, about 1 h (estimate) | new pairs under 10% of the round's pairs, or the rejected side is mostly execution errors |
| 3 | One DPO round from FedAvg round 2 with the new pairs, against 77.46 | server, about 4 h GPU (estimate) | under +0.5 EX and wrong results still at 365 to 385 |

The thresholds of steps 1 and 2 were set here, not by the owner. After
step 3: variants for every database. Things the generator has to handle:
ties under ORDER BY ... LIMIT and MAX/MIN, self-joins, composite keys,
HAVING COUNT thresholds, NOT IN and EXCEPT, foreign keys declared wrongly
in the Spider schemas (take them from `tables.json`), and database size
(execution time for 10 samples per question).

Standing of the direction (owner, 2026-11-19): optional, taken up later
if wanted. The paper does not need it: without it, "a question on a
database without rows gives no pair" stays a line of the setup, and
Arctic-Text2SQL-R1 drops such data too.

- No gain by the reading rule (0.5 EX, p < 0.05): dropped, nothing in the
  paper changes.
- A gain with fewer wrong results: the method corrects errors of meaning
  for the first time, has a part of its own that wins an ablation row,
  and the gain adds to the gap, because FedAvg SFT executes nothing and
  federated DPO as published has no such step.
- A gain made only of execution errors: it is the 20% of questions put
  back to use; it can stay in the method and does not change the story.
  Step 2 tells these two cases apart before any GPU time.
- Order, if it is tried: before the runs over seeds and alphas. Tried
  after them, a win means running that package again with the new part.

Relation to earlier notes: the boundary-value form of counterexample
relabelling was dropped on 2026-11-18 (entry below). This form rests on
the empty databases and on general content variants, which that probe did
not measure. Prior work that trains with enriched or counterexample
databases exists (SQLoom, CoRE-DB, ReViSQL; `LITERATURE.md`, sections 1.20
and 1.21), so the claim would be the adaptation to clients that own their
databases, not the mechanism.

Other ideas of the scan, not planned:

| Idea | Agents' chance of +1.5 EX over 78.20 | Note |
|---|---|---|
| SQL written by the client on its own schema, checked by execution, with a model-written question (about 3k rows) | 35 to 40% | needs the decision of 2026-11-17 against unlabelled questions reopened; SPFT-SQL reports 78.0 to 82.3 on Spider test at this student with a 7B question writer, GAZP reports a loss for synthesis on training databases |
| Negatives sampled on databases the sampling model has not trained on (two folds) | 25% | no Text-to-SQL DPO paper found doing it |
| Distractor tables from the client's other databases in the prompt schema | 20 to 25% | SQLong: +1.4 to +1.7 on Spider test at 7B; FedAvg can use it too |
| The server as a sixth participant on public databases | 35 to 50% in level | adds data; the baselines get the same rows; a control row, not a part of the method |
| Reasoning before the SQL | 25% | breaks SQL-only output; 4 to 6 times the sampling tokens |

Checks the scan named that need no training, not run: FedAvg round 4 with
a retry when the SQL fails to execute (a reviewer's control for a gain
made of execution errors); the existing adapters on Spider-Syn, Realistic
and DK (the data is under `data/raw/`); the server step size swept over
the saved client adapters. The agents also put the level of this student
with a DDL prompt and greedy decoding at about 78 to 80 on Spider test in
the papers, so a gain of several points more on Spider test is not
expected.

## 2026-11-19: DPO round 1 from the base student reaches 75.87; k = 0 line queued to 4 rounds (results `1e999231`, `96007ff6`; queue `787c0197`)

`decide/k0`: DPO + NLL round 1 from the base student (no SFT stage), on
the samples of the pair read, 2 random pairs per question: 8,908 pairs
(1,062 / 1,896 / 2,470 / 2,458 / 1,022 per client), rejected side 5,339
execution errors and 3,568 wrong results. Of the 8,659 questions, 5,951
have right and wrong samples (1,497 of them on databases without rows,
which give no pair), 1,631 are all right, 1,074 all wrong. Spider test
75.87 (easy 90.43, medium 79.00, hard 68.90, extra 58.26); execution
errors 101, wrong results 417; 3 outputs are cut at 256 tokens (nested
subqueries that repeat); the rows compared below have none.

| Against | EX | fixed | broke | McNemar p |
|---|---|---|---|---|
| base student, zero-shot | 68.05 | 225 | 57 | < 1e-6 |
| FedAvg round 1 (same total: 1 round) | 72.43 | 168 | 94 | 6e-06 |
| FedAvg round 2 | 74.10 | 157 | 119 | 0.026 |
| FedAvg round 3 and round 4 | 74.71 | 156 | 131 | 0.16 |
| RFT round 1 from FedAvg round 2 | 75.87 | 122 | 122 | 1 |
| DPO round 1 from FedAvg round 2 | 77.46 | 114 | 148 | 0.041 |

Training: final accuracy 0.84-0.91, final margin 0.48-1.52; client
updates: norms 1.56-2.56, pairwise cosine 0.365-0.462 (DPO round 1 from
FedAvg round 2: 0.244-0.321); peak reserved 16.99-18.98 GiB; 559 updates;
round, evaluation and publications about 3 h 10 min. Client 4 has 2,458
pairs, not the 4,000 expected: 1,648 of its 3,479 questions are on
databases without rows.

Reading: one DPO + NLL round from the base student, with no gold SQL in
the loss, is above every FedAvg SFT round (+3.44 at the same single
round, +1.16 over the best, the latter not significant) and 1.59 below
one DPO round after two FedAvg rounds (three rounds in total). It removes
execution errors as the k = 2 line does (101 against 99) and leaves more
wrong results (417 against 385). Whether the SFT stage is needed is not
settled by one round: the comparison is at the same total rounds. By the
rule written before the run (about 74 or more), the k = 0 line runs to 4
rounds: `dpo_k0/round_2..4`, on-policy as dpo_k2 round 2, the command of
round 1 with another round number (462 tests pass on the Mac), placed
after the decision runs and before centralized SFT. Read: round 2 against
FedAvg round 2 (74.10), round 3 against 77.46, round 4 against 78.20 and
FedAvg round 4 (74.71).

## 2026-11-19: second card free; one publication at a time (owner; code `ee1615e8`)

Owner: GPU 1 is free, run tasks on it in parallel. The queue already
gives each card its own worker (a lock per card and per task); the
second worker takes the first ready task, `decide/wrfirst`, while GPU 0
runs `decide/k0`. `scripts/publish_results.py` now holds a lock file in
the Git directory, so two workers publishing at once wait for each other
instead of one failing on its push and stopping both (461 tests pass on
the Mac; the Windows lock call is the one `exclusive_lock` uses, not run
there yet). Pushed together with `0017c487`.

## 2026-11-19: fixed pairs and reference match on-policy at round 2 (results `6717c7f6`, `aaae06ad`)

Round 2 of `decide/fixed`: the 8,026 pairs of round 1 again (pair hashes
equal), reference FedAvg round 2, start the line's own round 1. Spider
test 78.02 (easy 91.70, medium 81.56, hard 70.41, extra 61.34);
execution errors 97, wrong results 375. Against on-policy round 2
(78.20; 84 and 384): fixed 54, broke 58, McNemar p 0.78. Against its own
round 1 (77.64): fixed 53, broke 45, p 0.48. Against FedAvg round 4:
fixed 159, broke 88, p 7e-06. Training: the first update of each client
has a margin of 0.58-1.57 (the policy starts away from the reference),
final accuracy 0.83-0.96, final margin 1.38-2.23; client updates: norms
1.06-1.62, pairwise cosine 0.031-0.092; peak reserved 12.93-18.92 GiB.
Reading: at round 2 on-policy rounds do not beat fixed pairs with a fixed
reference; the difference (0.18) is the size of a rerun, so by the rule
on-policy rounds are not shown to be a part of the method. On-policy
round 2 reaches the level with 3,354 pairs against 8,026 (about 210
updates against 505). The fixed line does not win, so no run with its
pairs cut follows. Both lines are at about 78 after two rounds.

## 2026-11-18: a line can continue another line's finished rounds (owner; code `0017c487`)

Owner: a finished round is not trained again for another line; the fixed
line should have reused DPO round 1 instead of spending 3 h 15 min on it.
`--continue-from <root> --continue-round N` (with `--continue-arm`) makes
rounds 1..N of a line those of another root with the same setup (the pair
rule may differ): the line trains from round N + 1 under its own
settings, and round 1's start (the fixed reference) and the samples of an
earlier round are read from the root that ran them. Arms without the flag
keep their identity and behaviour (461 tests pass on the Mac). In the main
table, federated DPO as published and the method then share round 1 for
every seed and alpha. Pushed on 2026-11-19 with the publication lock;
the server's publish step merges `origin/main` before each publish, so
the tasks that follow load it. No queued task uses the flag yet.

## 2026-11-18: fixed line round 1 repeats DPO round 1 within 0.18 EX (results `7ace0aa3`, `67c17163`)

Round 1 of `decide/fixed` is the training of dpo_k2 round 1 run again in
its own root: same samples, same 8,026 pairs (pair hashes equal per
client). Spider test 77.64 (easy 91.28, medium 81.21, hard 71.27, extra
59.38); execution errors 99, wrong results 381. Against dpo_k2 round 1
(77.46): fixed 14, broke 10, McNemar p 0.54; 154 of the 2,147 predicted
SQL differ in text. So running one DPO round again moves EX by about 0.2
and flips about 24 questions; a difference of that size between two
settings is noise. On-policy round 2 (78.20) is 0.56 above this rerun
(fixed 44, broke 32, p 0.21) and 0.74 above the first run (p 0.093).
Round 2 of the fixed line runs now. Round 1 was published 3 h 15 min
after the gold-chosen run.

## 2026-11-18: gold as chosen for all-wrong questions gives the same EX (results `674b993d`, `cf644e95`)

DPO round 1 from FedAvg round 2 on the samples of dpo_k2 round 1, with
the gold SQL as the chosen side for the questions whose 10 samples are
all wrong: 9,140 pairs against 8,026, of them 1,114 with gold as chosen
(per client 120 / 204 / 364 / 328 / 98; all-wrong questions on databases
without rows give none). Spider test 77.41 (easy 90.64, medium 80.98,
hard 70.84, extra 59.94); execution errors 117, wrong results 368.
Against DPO round 1 (77.46; 99 and 385): fixed 38, broke 39, McNemar
p 1. Against RFT: fixed 106, broke 73, p 0.017. Against FedAvg round 2:
fixed 141, broke 70, p 1e-06. Reading: no gain, so the setting is not
kept. Wrong results fall by 17 and execution errors rise by 18: the gold
pairs move rows between the two kinds and fix none on net. Its result
was published 3 h 45 min after RFT's (estimate for the run: 2.5 h).

## 2026-11-18: when a train database hides a boundary error (CPU, results `e16c8f75`)

Across the five Spider train clients, 77 distinct (database, SQL text)
entries matched a simple single-table numeric inequality on a populated
database. Toggling whether the boundary is included changed the result on
30 originals. Of the other 47, setting one existing numeric cell to the
boundary in an in-memory copy separated 38. Five still agreed, three had
no numeric row to edit and one database had an invalid foreign-key
declaration. Counts are for constructed mutants, with repeated SQL text
within a database counted once. They measure an instance's ability to
expose one class of error. The prevalence in student samples and the EX
effect of training on the corrected labels are open.

Reproduce from the code repository with `python3 scripts/probe_spider_boundaries.py`.
The deterministic probe and per-client counts are in the same commit.
Owner dropped counterexample relabelling. The owner found zero direct
boundary-operator swaps among the 370 executable wrong answers of FedAvg
R4 and the 384 of DPO R2. The pilot does not explain those errors.

At the FedAvg R2 checkpoint used to start DPO, greedy evaluation on
Spider test (2,147 questions, `0699ac6d`) gives 1,591 correct, 373
executable wrong answers and 183 execution errors. Ten samples from
that checkpoint at T=1.0 give 250 all-wrong questions (`762b74a2`).
At least 556 - 250 = 306 greedy failures therefore have a correct sample;
at least 373 - 250 = 123 are executable wrong answers with a correct
sample. These are set-size bounds from the published aggregates at the
start of DPO. The number of train questions for which forcing the greedy
answer into the rejected slot would change an existing pair is unknown.

## 2026-11-18: line without on-policy rounds queued next (owner; code `5aedf463`)

`--fixed-reference` keeps round 1's start as the DPO reference of every
round; with `--samples-from-round 1` it is federated DPO as published
(fixed pairs, fixed reference). The line `decide/fixed` runs two rounds
from FedAvg round 2 right after the gold-chosen run: round 1 repeats the
training of dpo_k2 round 1 in its own root; round 2 trains on the same
8,026 pairs against FedAvg round 2, to be read against on-policy round 2
(78.20, 3,354 pairs). Why first: on-policy round 2 gained 0.74 over round
1 with p 0.093, so whether on-policy rounds are a part of the method is
open, and it decides the story before the other settings. A pair rule
mixing one execution-error and one wrong-result rejected side per
question waits for the wrong-results-first run. BIRD as a second
benchmark is left to the owner after the fixed line and the no-NLL run.

## 2026-11-18: RFT round 1 below DPO, above FedAvg (results `e1e49ee0`, `424cd93e`)

RFT (chosen side only, NLL, no preference term) on the same samples and
the same 8,026 pairs as DPO round 1 from FedAvg round 2 (pair hashes
equal per client): 75.87 on Spider test (easy 90.43, medium 79.35, hard
67.60, extra 59.10); execution errors 153, wrong results 365. Against
DPO round 1 (77.46): fixed 76, broke 110, McNemar p 0.015. Against
FedAvg round 2 (74.10): fixed 59, broke 21, p 2.5e-05. Client updates:
cosine 0.024-0.058 (DPO 0.24-0.32), norms 0.94-1.41. Reading: training
on own correct samples gives about half of the gain (+1.77 of +3.36);
the preference term adds the rest, almost all from execution errors
(153 to 99). Wrong results go the other way (365 RFT, 385 DPO), so DPO
trades some wrong results for fewer errors. The preference term stays
in the method.

## 2026-11-18: decision runs queued before centralized SFT (owner; code `baf58106`)

Owner stopped centralized SFT in epoch 1 to settle the method first. Six
one-round runs, each read against DPO round 1 from FedAvg round 2
(77.46): RFT (preference weight 0), gold as chosen for all-wrong
questions, DPO from the base student with 2 pairs per question (k = 0),
a new pair rule `wrong_result_first` (rejected side from executable
wrong results when there are any; same pair count as random), DPO
without NLL, and DPO from FedAvg round 3 (k = 3). Rows from FedAvg round
2 reuse the samples of dpo_k2 round 1. Why: nearest and random pairs
reject the same outcomes (51% execution errors) and give the same EX;
the wrong-result count stays at 370-385 in every row; CodeLutra reports
17.2 Spider EX without its NLL term, and RFT tells whether the gain needs
the preference term at all.

## 2026-11-18: FedAvg round 4, line stopped at best round 3 (results `f7adcebe`, `da0871d4`, `7285253d`)

FedAvg SFT round 4 on Spider test: 74.71 (easy 90.64, medium 78.18, hard
66.74, extra 55.74), the same as round 3; execution errors 173, wrong
results 370; against round 3 fixed 44, broke 44, McNemar p 1. Client
updates: pairwise cosine -0.020 to 0.011. The curve stopped at step 4
with best step 3. DPO round 2 of the k = 2 line (78.20) against FedAvg
round 4: fixed 150, broke 75, p 1e-06.

## 2026-11-18: nearest pairs no better; DPO round 2 reaches 78.20 (results `c3effaea`, `9253ef8e`, `8fc37f77`, `5c33e622`)

Nearest-correct pairs, round 1 from FedAvg round 2 on the samples of the
random round: 77.08 on Spider test (random 77.46); against random fixed
34, broke 42, McNemar p 0.42. Its pairs are closer (mean similarity
0.85-0.86 against 0.74-0.76) and fewer (6,869 against 8,026: one pair per
distinct wrong SQL), but they reject the same outcomes (51% execution
errors), and the wrong results stay at 382. Random won by 8 questions
(1,663 against 1,655), so round 2 ran with random pairs.

Round 2 of the random line (samples and reference: round 1's global
model): 78.20 (easy 91.91, medium 81.91, hard 71.06, extra 60.50);
execution errors 84, wrong results 384. Against round 1 fixed 48, broke
32, p 0.093; against FedAvg round 3 fixed 142, broke 67, p 2.3e-07. The
round-1 model samples the training questions far better (sample accuracy
0.82-0.86, round 1: 0.68-0.75): mixed questions fall from 5,192 to 2,244,
all-correct rise from 2,891 to 5,784, all-wrong from 573 to 628; pairs
8,026 to 3,354, execution-error rejects 51% to 43%. Training: final
accuracy 0.75-0.79 and margin 0.26-0.69 (round 1: 0.80-0.96, 0.90-1.67).
Client updates: norms 0.70-1.20, pairwise cosine 0.013-0.055 (round 1:
0.24-0.32). Round 2 took about 1 h 50 min with its evaluation.

Across FedAvg rounds 2-3 and the three DPO rows, 359 test questions are
wrong in all five and 242 are a wrong result in all five (easy 26,
medium 86, hard 65, extra 65); 83.28% are right in at least one.

## 2026-11-18: round 2 of the k = 2 line queued (owner; code `c38e7eb0`)

Owner: a second on-policy round of the k = 2 line runs before FedAvg round
4, with the pair rule that answers more Spider test questions right in
round 1 (random 1,663 / 2,147; nearest pending; a tie keeps random). The
choice is made by the queue (`queue_when arm-gain`, two tasks with
complementary conditions), so the rule is picked on Spider test.

## 2026-11-18: DPO round 1 from FedAvg round 2: 77.46 on Spider test (results `431a17e7`, `be787676`)

`dpo_k2` round 1 (random pairs, 2 per mixed question, 8,026 pairs, one
epoch, beta 0.1, NLL weight 1). On each client the margin rises from
0.06-0.20 in the first quarter of the updates to 1.19-1.55 in the last,
accuracy from 0.67-0.70 to 0.89-0.92; every pair is seen once, so these
are pairs the client had not trained on yet. Client updates against the
round-2 adapter: norms 1.35-2.12 (SFT rounds: 3.9-6.7), pairwise cosine
0.24-0.32 (FedAvg SFT round 2: 0.01-0.05, round 3: about 0), product error
of the factor average 0.005 (SFT: 0.045-0.126). The DPO updates of the
five clients point the same way where the SFT updates had become
orthogonal. Rejected side: 4,087 of 8,026 pairs (51%) reject an execution
error; greedy round 2 has 183 execution errors and 373 wrong results on
Spider test. Peak reserved 12.65-18.93 GiB.

Greedy EX on Spider test (results `be787676`): 77.46 (easy 91.49, medium
80.63, hard 71.06, extra 59.66); FedAvg round 3 74.71, round 2 74.10.
Wrong rows: execution errors 99 (round 3: 164, round 2: 183), wrong
results 385 (379, 373). Against round 3: fixed 134 (63 from execution
errors, 71 from wrong results), broke 75 (21 into execution errors, 54
into wrong results), McNemar p 5.4e-05; against round 2 (its start):
fixed 146, broke 74, p 1e-06. The whole net gain comes from execution
errors; the wrong-result count does not move, as the 51% share of
execution-error rejects predicted.

## 2026-11-18: FedAvg capped at round 4, centralized SFT next (owner; code `cb947362`)

Owner: the FedAvg line stops at round 4 (`max_steps` 8 to 4) and
centralized SFT on the union of the clients runs after it overnight
(`refs/central_sft`, curve `central_base_ddlrows_s0/sft`: same SFT recipe,
LoRA r 16 / alpha 32 / dropout 0.05, prompt and evaluation as FedAvg; one
epoch per step, rule 0.5 / patience 2 / at most 8). Then the DPO line from
the best FedAvg round. pass@k of FedAvg round 3 (results `762b74a2`):
pass@1 68.34, pass@2 77.66, pass@5 84.97, pass@10 88.68 (round 2: 65.78,
76.06, 84.35, 88.36); test questions all correct / mixed / all wrong 788 /
1116 / 243 (round 2: 686 / 1211 / 250). The third SFT round sharpens the
samples (pass@1 +2.56) and leaves pass@10 where it was.

## 2026-11-17: pass@k of FedAvg round 2 on Spider test (owner's console, not committed yet)

`scripts/pass_at_k.py` (code `532256af`), 10 samples at T 1.0, vLLM at 0.30
of the card beside the DPO round: pass@1 65.78, pass@2 76.06, pass@5
84.35, pass@10 88.36; greedy EX of the same adapter 74.10. A correct SQL
is among 10 samples for 88% of the test questions; greedy decoding lies
between pass@1 and pass@2.

## 2026-11-17: pairs at k = 2 (owner's console, not committed yet)

Round 1 of `dpo_k2` sampled from FedAvg round 2 (vLLM, 8,659 questions x
10 at T 1.0 in 15 min 21 s). Per client: sample accuracy 74.5 / 75.2 /
67.9 / 71.0 / 71.5%, pass@10 90.9-94.8%; mixed 457 / 821 / 1205 / 2276 /
433 (51-65%, 60.0% overall), all wrong 60 / 102 / 183 / 179 / 49 (6.6%),
all correct 378 / 619 / 621 / 1021 / 252 (33.4%); pairs 914 / 1642 / 2248
/ 2356 / 866 = 8,026. Base student for comparison (clients 1-3): mixed
59.3 / 61.5 / 66.3%, all wrong 11.8 / 11.7 / 15.4%. Two SFT rounds halved
the all-wrong questions and cut the mixed ones by only 6-8 points, so the
pairs do not run short at k = 2. Client 4 makes 2,356 pairs from 2,276
mixed questions: 1,098 of them are on its six databases without rows and
give none, so its share of the average falls from 0.40 (SFT) to 0.29.

## 2026-11-17: I2 queued on the k = 2 samples (owner; code `922b2660`)

Owner approved. After the random-pair round from FedAvg round 2, the same
round with nearest-correct pairs (`--pair-rule nearest`, 2 per question)
trains on the same samples, copied to root
`fedpref_sftr2_nearest_ddlrows_alpha01_s0` by `scripts/reuse_samples.py`;
same flags otherwise (test in `tests/test_active_queue.py`). Reason: FedAvg
round 3 left the executable wrong results flat at 373-379 since round 1.
Then FedAvg round 4 and on.

## 2026-11-17: FedAvg SFT round 3 (code `845db4bc`, eval `6558ebfe`)

Spider test EX 74.71 (easy 90.21, medium 78.88, hard 67.17, extra
54.06): +0.61 over round 2, a gain under the line's rule (> 0.5), but
not a clear one (fixed 61, broke 48, McNemar p = 0.25). Execution errors
215 / 183 / 164 over rounds 1-3; executable wrong results 377 / 373 / 379,
flat since round 1, and extra hard 54.90 / 54.62 / 54.06. So after round 1
SFT only removes execution errors. Pairwise cosine of the client updates
-0.014 to 0.016 (round 2: 0.01 to 0.05, round 1: 0.13 to 0.33) while the
update norms stay at 3.9 to 6.7: the clients move as far as before, in
unrelated directions, and the average cancels most of it. Mean local
loss 0.070 to 0.103.

## 2026-11-17: method is k SFT rounds, then DPO; k = 2 read queued first (owner; code `46509f1e`)

Owner: the method starts DPO after a fixed SFT stage of k FedAvg rounds,
k a value stated in the paper; "the best round" needs the test set and is
not a method. k is swept over 0, 2 and the best FedAvg round; the paper
can show EX and pairs against k. Reason to read k = 2 early: after SFT on
the clients' own questions, more of them are right in all 10 samples, so
fewer give pairs (base student: 59-66% mixed), and the line from the best
round would only show this after FedAvg ends. Queued before the FedAvg
line: one DPO + NLL round from FedAvg round 2 (root
`fedpref_sftr2_ddlrows_alpha01_s0`, same flags as the line from the best
round), compared with FedAvg round 3. Rule: at least 1 EX above, the k = 2
line continues; about 0, read the pair counts first; below, stop and look.
The worker stopped at 20:43 in FedAvg round 3, client 2; the owner chose
to restart without looking for the cause.

## 2026-11-17: FedAvg SFT round 2 (code `32e3f681`, eval `0699ac6d`)

Spider test EX 74.10 (EM 62.93; easy 89.36, medium 78.65, hard 65.23,
extra 54.62). Against round 1: fixed 85 rows, broke 49 (McNemar
p = 0.0024); execution errors 215 to 183, wrong results 377 to 373.
Mean local loss 0.094 to 0.117. Pairwise cosine of the client updates
(against the round's global start) fell from 0.13-0.33 in round 1 to
0.01-0.05: the shared part of the update was learned in round 1, and the
round-2 updates are almost orthogonal, so averaging shrinks them. Factor
FedAvg relative product error 0.126 to 0.062. Whether this costs accuracy
needs the centralized reference (not run).

## 2026-11-17: FedAvg SFT round 1 (code `29f38add`, eval `d6bfc763`)

FedAvg from the base student, `alpha_0.1/k5`, prompt A (`ddl_rows`), one
local epoch. Spider test EX 72.43 (EM 60.41; easy 89.15, medium 75.26,
hard 63.71, extra 54.90) against 68.05 for the untrained student with
prompt A (results `12456b56`): 165 rows fixed, 71 broken, exact McNemar
p = 8.5e-10. Execution errors 287 to 215, wrong results 399 to 377.
Client sizes 895 / 1542 / 2009 / 3479 / 734 (client 4 weighs 0.40); mean
local loss 0.140 to 0.152 on every client. Pairwise cosine of the client
updates against the round's start adapter 0.13 to 0.33; factor FedAvg
relative product error 0.126. Round 1 trained in 7,339 s with peak
reserved 20,311 MB; the evaluation took 206 s.

## 2026-11-17: aggregation options for the DPO rounds written down (owner)

Owner: the federated options for aggregating the DPO rounds are options to
test, not changes now. Phase 1 keeps factor-wise FedAvg weighted by pair
count. Options and the evidence that would trigger each are in
`RESEARCH_STATE.md` 3.8: equal weights, question weights, FedNova-style
normalisation, exact LoRA aggregation, FedProx (likely redundant), server
optimisers (not planned); plus a re-aggregation probe of DPO round 1
without training, to be scripted once that round exists.

## 2026-11-17: experiment plan; phase 0 and 1 in code (code `62a48999`)

Owner approved the plan of `RESEARCH_STATE.md` section 3.7 (phases 0 to
3) and ruled: drop from the pairs only the questions on databases whose
tables hold no rows, not those whose gold result is empty; 2 pairs per
question.

In the code:

- `PairRule.skip_empty_databases` (on by default; `--keep-empty-databases`
  turns it off) and `fedls_sql.data.spider.empty_databases`. On the
  `alpha_0.1/k5` clients the databases without rows are `yelp` (client 3)
  and `academic`, `geo`, `imdb`, `music_2`, `restaurants`, `scholar`
  (client 4). The pair rule identity changed, so the root of the base
  student's DPO line no longer matches the new code; it is not queued.
- Pair statistics now count the wrong samples by outcome, the mixed
  questions with a wrong-result sample and the questions on empty
  databases. `scripts/pair_composition.py` rebuilds them from a round's
  samples (phase 0a, to run on the server).
- `scripts/error_breakdown.py`: wrong rows split into execution errors,
  wrong results and cut outputs by hardness, with the exact McNemar p
  against the first arm (phase 0b). On the base model: prompt A 287
  execution errors and 399 wrong results; B against A fixed 110 rows and
  broke 122 (p = 0.47).
- `compare_predictions` prints the exact McNemar p.
- Queue: `dpo/after_fedavg`, the curve `fedpref_sft_ddlrows_alpha01_s0/dpo`
  after the FedAvg curve: `--parent-stage` of FedAvg's best round, 10
  samples at T 1.0, 2 pairs per question, rule 0.5 / 2 / at most 6.
  Resolved commands checked against the FedAvg line (prompt, length,
  LoRA, evaluation) by a test; one rendered prompt read.

447 tests pass on the Mac. Nothing of it has run on the server.

## 2026-11-17: direction of the method revised (owner)

Owner: the method is a federated learning method that uses DPO, built to
beat the federated baselines. It is the owner's own design, not CodeLutra
applied to federated learning; CodeLutra was found later to have a
similar loop and is cited as the closest work. A FedAvg SFT stage before
the DPO rounds may itself be one of the parts. Nothing of it runs yet; the server runs the FedAvg SFT
rounds.

Written in `AGENTS.md` (Method) and `RESEARCH_STATE.md` section 3: three
candidate improvements (I1 on-policy rounds with the round's global model
as reference; I2 execution-aware pairs, the main candidate; I3 a FedAvg
SFT stage before the rounds), the rows of the paper with federated DPO as
published (OpenFedLLM: fixed pairs, fixed reference) as a baseline, and
the open settings (2 pairs per question proposed for every DPO line; the
chosen side of a gold-empty question). This replaces "no SFT stage before
the rounds" of the earlier ruling that day.

## 2026-11-17: FedAvg SFT runs alone first (code `407a7ad7`)

Owner: run the FedAvg SFT rounds first; that number is needed whatever
the DPO design becomes. The queue now holds `rounds/fedavg_sft` (the
FedAvg curve under its own rule: gain of more than 0.5 EX point, patience
2, at most 8 rounds). The DPO curve and the reference curves keep their
definitions and are not run; `rounds/sft_vs_dpo` and `refs/central_local`
left the queue. If the DPO line later runs more rounds than FedAvg, a
curve that `extends` the FedAvg one adds them.

Open before the DPO line runs (owner):

- pair rule for questions whose gold result is empty: CodeLutra as is,
  gold as chosen against execution-error samples only, or Arctic's filter;
- pairs per question: 10 (CodeLutra; 59,510 pairs a round, about 13-15 h
  of training, estimate) or 2 (about 11,900, 2-3 h, estimate);
- whether the method is the federated port of CodeLutra or a change to it
  (a pair rule that uses each execution label at the level it informs,
  with the port as a baseline row).

## 2026-11-17: what CodeLutra does with empty or uninformative labels

Read in the paper text (arXiv 2411.05199v3); no code is linked. It does
not name the Spider training split, does not mention empty gold results or
databases without rows, filters no training question (it drops only wrong
samples with repeated strings) and has no step for a question whose
samples are all wrong or all correct. Pairs: 10 samples at T 1.0, 10
random pairs per question. Its section 6 variant without gold (executable
as chosen, error as rejected) lifts BIRD EX 22.3 to 30.9, against 43.1
with gold. On a database without rows our labels reduce to that variant.

## 2026-11-17: pair read of the base student; seven Spider train databases have no rows

Results `1704b03b` (`audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0/pair_read/r1_base.json`),
10 samples per question at T 1.0, prompt A, `alpha_0.1/k5`.

| Client | Questions | Mixed | All correct | All wrong | Gold empty | Pairs (10 per question) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 895 | 531 | 258 | 106 | 30 | 5,310 |
| 2 | 1,542 | 948 | 414 | 180 | 21 | 9,480 |
| 3 | 2,009 | 1,332 | 368 | 309 | 103 | 13,320 |
| 4 | 3,479 | 2,629 | 444 | 403 | 1,433 | 26,290 |
| 5 | 734 | 511 | 147 | 76 | 29 | 5,110 |
| All | 8,659 | 5,951 | 1,631 | 1,074 | 1,616 | 59,510 |

Sample accuracy 56.1%; 3 gold errors; 1,663 samples hit the length limit.
Of the mixed questions, 1,392 have an empty gold result (1,237 at client
4).

Cause: the official Spider release ships seven training databases with
the schema and no rows (`geo`, `scholar`, `academic`, `restaurants`,
`imdb`, `yelp`, `music_2`): 1,759 questions, 1,648 of them at client 4
(47% of its questions). On them every executable SQL returns the empty
gold result and counts as correct. No Spider dev or test question is on
them. Content for `geo` and `restaurants` exists in
`jkkummerfeld/text2sql-data` (checked on copies: 530 of 564 and 56 of 125
gold queries return rows); the others were not checked. FedAvg SFT is not
affected (it trains on gold SQL).

## 2026-11-17: the two lines queued round by round; conditional tasks in the queue (code `66b2c01a`)

Owner: run FedAvg SFT and the DPO rounds one round at a time to see a
signal early, let each go on by the gain rule, and let the queue run a
task on a condition.

In the code:

- `scripts.curve run A B` alternates the curves step by step; with
  `--same-length` a curve whose rule has stopped follows the longer one,
  and its record keeps its own decision (`rule_stop_step`). `plan` prints
  the resolved commands of the first steps.
- A queue task may carry `when`, a check the worker runs without a GPU:
  exit 0 runs the task, exit 3 skips it (and the tasks that need it),
  anything else stops the worker. `scripts.queue_when curve-gain A --over
  B --min X` reads the published curve records.
- 442 tests pass on the Mac. Nothing of it has run on the server.

Queued (`queues/active.toml`), after the read of the pairs:

- `rounds/sft_vs_dpo`: FedAvg SFT and federated DPO from the base student
  on `alpha_0.1/k5`, prompt A, alternating, same length. Rule: gain of
  more than 0.5 EX point, patience 2, at most 8 rounds. The rounds are
  chosen on Spider test.
- `refs/central_local`: centralized SFT and local SFT per client as
  curves of one epoch per step, only if the best DPO round is at least
  2.0 points above the best FedAvg SFT round.

Values set here without a ruling of the owner: the rule (0.5, 2, 8), the
same length, the 2.0 points of the condition, SFT at lr 2e-4 with one
local epoch per round.

The two lines agree in prompt, length limit (7,168), LoRA r 16 / alpha 32,
the seeded LoRA initialisation, one epoch per round, 16 examples or pairs
per update, all 5 clients per round and the evaluation. They differ in:

| Setting | FedAvg SFT | Federated DPO |
|---|---|---|
| Learning rate | 2e-4 | 5e-5 |
| Warmup ratio (cosine) | 0.03 | 0.1 |
| Weight decay | 0.01 (AdamW default) | 1e-4 |
| LoRA dropout | 0.05 | 0 |
| Aggregation weights | client rows | client pairs |

No default of either runner was changed for the queue.

Not measured: peak VRAM of a FedAvg round and of a DPO round with prompt
A (sequences up to 6,927 tokens); the time of a round. Known risk: the
centralized and local runner retrains and overwrites a finished adapter
if its command is run again; the curve's state prevents it unless
`.queue_state/` is lost.

## 2026-11-17: Spider first, with prompt A (owner)

- The method is tried on Spider first (owner). Whether BIRD joins as a
  second set of clients, or becomes the main one, is decided after the
  first read of the DPO rounds against FedAvg SFT on Spider. Behind the
  question: on Spider the SFT of this student is at 77 to 78 in the
  papers and the highest published level is 82.3 (SPFT-SQL), so about 4
  points are left above SFT; on BIRD CodeLutra is 7.5 points above its
  SFT (35.6 to 43.1). Nothing is built for BIRD clients yet (no split, no
  prompt lengths).
- The runs on Spider use prompt A (`ddl_rows`). A and B give the same
  level without training (68.05 and 67.49, p = 0.47); A is the prompt of
  the model's own evaluation code. B is not run again unless a result
  asks for it, so the first comparison is run once, not once per prompt.
- The student stays Qwen2.5-Coder-1.5B-Instruct. Both rows of the
  comparison start from it, so a weaker model lowers both; and the DPO
  rounds need questions the model answers correctly in some samples.

## 2026-11-17: the DPO rounds start from the base student, pairs and defaults after CodeLutra (code `c03bd693`)

The preference rounds were written for DPO after an SFT stage. They now
run the method as set: round 1 from the base student, CodeLutra's pairs.
No GPU run yet.

In the code (`experiments/federated_pref/run.py`):

- `--from-base`: round 1 samples from the base model with no adapter and
  every client trains from one saved LoRA initialisation, the same one the
  FedAvg SFT runner builds from the base model (a test gets bit-identical
  tensors on a tiny model on CPU). The DPO reference of round 1 is the
  base model. A start from a parent adapter still works.
- Pair rule `random` (default), as read in CodeLutra (section 4,
  Algorithm 1 lines 16 to 19, appendix A.1): 10 pairs per question, the
  chosen side drawn at random from the correct samples and the rejected
  side from the wrong ones, with replacement when a set has fewer than 10.
  The draw is over the samples as produced, so a SQL sampled three times
  is three times as likely. All-wrong and all-correct questions give no
  pair. Gold SQL as the chosen side is off (`--gold-chosen` turns it on).
- Pair rule `nearest` is kept as the candidate: each distinct wrong SQL
  with its most similar distinct correct SQL. The similarity is a
  character-level ratio, not the token edit distance of `DPO_RESEARCH.md`,
  section 3.3.
- Defaults: 10 samples at T 1.0, beta 0.1, NLL weight 1, lr 5e-5, 1 epoch
  per round, 16 pairs per update, weight decay 1e-4 (CodeLutra, section
  5.1 and Table 4). LoRA rank stays 16 (the paper has 8).
- `read`: sampling, labels and the counts per client without training,
  into `pair_read/r1_base.json`. Round 1 of the DPO arm on the same root
  reuses its samples.

Where the code is not the paper:

- The NLL term is a per-token mean; the paper writes the log-likelihood of
  the sequence. CodeLutra has no public code to check which it ran.
- Warmup 0.1 with cosine decay: the paper does not state a schedule.
- A response with no SQL counts as wrong (the paper's rule: every sample
  that does not match goes to the rejected set). A sample cut at 256
  tokens is in neither set; the paper filters "answers that contain
  repeated strings", which is not implemented apart from that.
- Aggregation weights are the clients' pair counts; FedAvg SFT weights by
  the number of questions.

Smoke on the Mac, not a result: 2 clients, 4 questions each, HF. The read
ran through (8 questions: 2 all wrong, 4 mixed, 2 all correct, 40 pairs).
The round reused the samples, client 1 trained 2 updates, and the run was
stopped during client 2 (owner: too slow on the Mac). The path from the
base student has not run through aggregation anywhere. 428 tests pass on
the Mac.

Queued: `pairread/*`, the read on `alpha_0.1/k5` with prompt A through
vLLM. Its peak memory on the card is not measured.

## 2026-11-17: the base model on Spider test with both prompts (results `12456b56`)

The student with no training, greedy, vLLM `inproc`, 2,147 rows, code
`083a6a52`. A check of the prompt and the decoding, not a result of the
method.

| Prompt | EX | Easy | Medium | Hard | Extra | Rows that do not execute | EM |
|---|---:|---:|---:|---:|---:|---:|---:|
| A, `ddl_rows` | **68.05** | 87.4 | **71.4** | **59.2** | 45.9 | **287** | **53.3** |
| B, `ddl_values` | 67.49 | **87.7** | 71.2 | 56.4 | **46.5** | 322 | 44.2 |

- A and B do not differ: 1,461 against 1,449 correct rows; 122 rows are
  correct only with A and 110 only with B (exact McNemar p = 0.47).
  1,571 rows are correct with at least one of them.
- The prompt and the decoding are sound. Every output starts with
  `SELECT`, none is empty or in a code fence, and all end at the end token
  except 2 of B that reach 256 tokens. The rows that do not execute are
  the model's errors, not a format defect: `no such column` in 270 of 287
  (A) and 304 of 322 (B), a column taken from the wrong table, most on
  databases with many tables (`bakery_1`, `cre_Doc_and_collections`,
  `cre_Students_Information_Systems`).
- Published numbers of this model on Spider test, each with its own
  prompt: 72.3 (SPFT-SQL, zero-shot), 67.61 (SLM-SQL, a vote over 16
  samples).
- B's lower EM is style (`INNER JOIN`, aliases), not correctness.
- Time: 17 s of generation for the 2,147 rows, about 2.5 min per task
  with the model load. The 10 min of the queue note was an estimate.

The choice between A and B stays open; it is made on the gain of the DPO
rounds over FedAvg SFT (`RESEARCH_STATE.md`, section 4, item 1).

On the server: the pull of the reset went through after the server copies
of 27 tracked files of one earlier result row (`p229_h_plain`) were put in
a stash; what differs in them was not reported. One test failed there
(`test_progress`, it assumed CUDA was not initialized) and was fixed in
`083a6a52`; the test summary on the server after the fix was not reported.

## 2026-11-17: the method is federated DPO; pre-training secondary, the teacher a research direction (owner)

Decision, after the reading in `DPO_RESEARCH.md`. It replaces the three
stages of the reset entry below (server stage with the teacher, FedAvg
SFT, federated DPO).

- Core: federated DPO + NLL. In each round the clients sample from the
  global model, label by execution on their own databases and train; the
  reference is the round's global model. No SFT stage comes before the
  rounds. FedAvg SFT is a baseline.
- Secondary: pre-training at the server with the same loss on public
  data, as the starting point of the rounds.
- The teacher is not part of the method. It stays as a research
  direction.
- Output is SQL only, no chain of thought.

What the papers gave for it (numbers and sources in `DPO_RESEARCH.md`):

- CodeLutra starts from the base model with no SFT stage, and SFT followed
  by plain DPO gives about zero for SQL-only output (Liu et al., ExCoT).
- No Text-to-SQL paper shows a teacher's SQL to beat gold SQL as the
  target. In KID, forward KL to the teacher ends below training on gold
  alone; reverse KL on the student's own samples ends above it.
- Pre-training on public data leaves the clients' questions unseen, so
  they still give pairs. Whether it adds or removes pairs is not known.

Choices inside the rounds (owner, the same day):

- The base form is CodeLutra's: plain loss, random pairs, nothing from a
  question whose samples are all wrong.
- The gold SQL of an all-wrong question in the NLL term (never as the
  chosen side of a pair) is an experiment to run, not a part of the method
  yet. No paper measures it; the one precedent is Iterative RPO on GSM8K.
- Nearest-correct pairing and the rejected side counted on the differing
  tokens join the method if a run shows a clear gain over the base form.
- Unlabelled questions are not in the method; it stays on the clients'
  labelled questions.

Notes changed: `RESEARCH_STATE.md` sections 2 to 4, `DPO_RESEARCH.md`
(sections 2.7 to 2.9 and 3), the run table of `FEDERATED_DATA_SETUP.md`
(13 rows on the main setting instead of 14), both `AGENTS.md`. No run and
no code change; nothing in the queue depends on it.

## 2026-11-17: what the paper prints (owner)

The paper prints what serves it: the setup as values, the results, the
tables. How a seed, a setting, a round or a result was picked is not told
in the paper; this log keeps it. No sentence in the paper is false. This
replaces the wording of the reset entry below, "the number is reported as
chosen on Spider test": the log records the set a choice was made on, the
paper does not have to.

## 2026-11-17: client splits rebuilt by database complexity tier (code `4760352b`)

Owner: rebuild the data processing after `FEDERATED_DATA_SETUP.md`.

In the code:

- Every database still goes whole to one client. The label of the
  Dirichlet is new: each of the 146 train databases gets one of four tiers
  by its share of hard and extra questions (Spider's hardness levels from
  the gold SQL, the function evaluation uses; `db_tiers.json`).
- The partition is NIID-Bench's label-Dirichlet recipe as its code has it
  (`utils.py`, `noniid-labeldir`, read 2026-11-17): per tier the clients'
  shares come from Dir(alpha), the tier's databases are cut by them, a
  client that already holds 146 / K databases takes none of the later
  tiers, and the draw is repeated until every client has 5 databases (3
  with 10 clients). The note's recipe did not have the third rule; without
  it seed 0 gave one client 85 databases and 64% of the questions.
- The IID split puts the databases in random order and cuts them into
  equal parts.
- Removed: the schema-embedding domain groups, their builder and audit,
  and the splits built from them (Spider and BIRD). They are at the tag
  `archive/pre-reset-2026-11-17`.

Hardness of Spider train (8,659 questions): easy 1,983, medium 2,999, hard
1,921, extra 1,755, one unparsed (`train:3153`). 8,658 labels equal the
level of Spider's own parse in the raw files.

| Tier | Databases | Questions | Hard or extra share of a database | Easy | Medium | Hard | Extra |
|---|---:|---:|---|---:|---:|---:|---:|
| 0 | 37 | 1,746 | 0.00 to 0.26 | 30.7% | 49.1% | 12.3% | 8.0% |
| 1 | 36 | 1,506 | 0.26 to 0.33 | 25.8% | 44.8% | 18.6% | 10.8% |
| 2 | 37 | 1,791 | 0.34 to 0.44 | 22.3% | 38.7% | 20.4% | 18.6% |
| 3 | 36 | 3,616 | 0.44 to 0.86 | 18.3% | 21.4% | 29.3% | 31.0% |

Tier 3 holds 42% of the questions: `scholar` (569) and `geo` (564) are in
it.

Split seed: 42 (owner, 2026-11-17), for all four splits. Seed 0 was built
first (code `e5c8134f`): clients of 1,084 / 288 / 1,482 / 1,857 / 3,948
questions, hard or extra 18% to 57%, third draw. The owner then asked for
seed 42 and took it from the split tables, before any training: the
smallest client has 734 questions instead of 288 and the largest 40% of
the questions instead of 46%. The paper gives the seed and the table.

Main split, `federated/alpha_0.1/k5`, seed 42 (first draw):

| Client | Databases | Questions | Easy | Medium | Hard | Extra | Hard or extra | Databases per tier 0 to 3 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 21 | 895 | 27.2% | 42.6% | 20.0% | 10.3% | 30.3% | 0, 20, 0, 1 |
| 2 | 34 | 1,542 | 30.9% | 49.0% | 12.0% | 8.2% | 20.2% | 34, 0, 0, 0 |
| 3 | 42 | 2,009 | 21.1% | 42.2% | 18.6% | 18.1% | 36.7% | 0, 12, 30, 0 |
| 4 | 37 | 3,479 | 18.8% | 21.2% | 28.9% | 31.1% | 60.0% | 0, 3, 0, 34 |
| 5 | 12 | 734 | 25.3% | 38.0% | 24.3% | 12.4% | 36.6% | 3, 1, 7, 1 |

The other splits (seed 42), questions per client and the range of the hard
or extra share:

| Split | Questions per client | Hard or extra share |
|---|---|---|
| `alpha_0.5/k5` | 1,238 / 1,429 / 1,170 / 1,533 / 3,289 | 21.9% to 55.6% |
| `iid/k5` | 1,866 / 1,298 / 2,005 / 1,462 / 2,028 | 33.9% to 52.4% |
| `alpha_0.5/k10` | 442 to 1,903 | 19.4% to 63.1% |
| the earlier domain-cluster split `alpha_0.1/k5` | 1,896 / 1,801 / 2,061 / 1,097 / 1,804 | 36.4% to 57.9% |

What it shows:

- At the level of databases three clients hold one tier almost alone
  (clients 1, 2 and 4); client 3 mixes tiers 1 and 2 and client 5 all
  four. At the level of questions the skew is in the proportions, 20% to
  60% hard or extra. No client lacks a level: client 2, all of tier 0,
  still holds 311 hard or extra questions of 1,542.
- `alpha_0.5/k5` (22% to 56%) is about as skewed as `alpha_0.1/k5` in this
  measure, so the alpha rows may not differ much.
- The IID split is equal in databases, not in questions or hardness
  (extra 14% to 31%), because the databases differ in size.
- Over 200 seeds at alpha 0.1 with 5 clients: the largest client holds 40%
  of the questions on average, the smallest has a median of 522.

Not done: no training on the new splits. Whether the split gives a reason
to federate needs local, FedAvg and centralized rows (`RESEARCH_STATE.md`,
section 4, item 7). 415 tests pass on the Mac.

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
