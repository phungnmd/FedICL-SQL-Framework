# Editor's notes: Section 3, Method

Wording notes on one draft (`WRITING_PLAN.md`, section 7.0); they die
with it. What stays true whatever the draft says is in `03_checks.md`.
The messages as sent are in the log of the writer's session
(`build/writer_03/`, outside Git); this file keeps what each note asked
and what the writer did.

## Draft 1 (2026-11-28)

Checks on the draft: build passes; lint has the one stop of the
abstract and no note that concerns the section (abbreviations are
expanded in Section 1; "FedDPO" is read as a lab word by the tool);
no run of five words shared with the closest papers or the example
papers; 30% of the words stand in runs of five or more words of the
brief (the definitions of its Materials); register close to the method
sections of the reference papers except for few "we" sentences and few
adverbs. Mechanical, fixed by the editor: the figure float `[!t]`, the
space after `\method`, the appendix references by label.

### Round 1, five notes

| # | Place | The note | Source |
|---|---|---|---|
| 1 | 3.1 last paragraph, 3.5 first sentence | "No query is executed on it" and "never queries the client databases" are false on Spider, where the rows of the prompt are read from the database. True: neither the gold SQL query nor a query of the model is executed, and no execution result enters the loss | claim audit |
| 2 | 3.5 | The time limit reads as incorrect in one paragraph and unlabeled in the next; the rule on BIRD given as facts. "Three cases receive no label" against the further exclusion of 3.6. The last sentence is wrong as a probability | cold read (F5, F10), claim audit |
| 3 | 3.6 first paragraph | The pair count is stated for a set that the next sentence reduces (false on Spider); "independently, without replacement"; identical samples; what a question without pairs receives in the round; the role of M | claim audit, cold read (F2, F6) |
| 4 | 3.7 fourth paragraph | The reason for pair-count weights; the rule before the exception; Algorithm 1 against the text on a client without pairs; name the integer | cold read (F4, F8) |
| 5 | 3.2, 3.4 | Which setup the three counts belong to; the denominator; "remain without a correct sample" states a larger set than 2,698 measures | cold read (F7), claim audit |

Not sent, with the reason:

- Execution match as a label can accept an incorrect query (cold read
  F1): a limitation, stated once in Section 6.
- The pair count as a message says something about the client (cold
  read F3; the writer's notes): Section 6; `REVIEW_NOTES.md`, C41.
- The three departures from FedDPO are standard in centralized
  iterative preference optimization (cold read F9): Section 2.2 carries
  that comparison, once for the paper.
- "Receives no signal about which of its own queries are incorrect" is
  too strong for the reader who counts the mass that NLL moves away
  from all other sequences (cold read F10): the sentence is the thesis
  of the paper as approved; kept for the owner (`REVIEW_NOTES.md`).
- Fig. 2 against the text ("2 FedAvg rounds", "N = 10", "Global model",
  the loss as L_DPO + lambda L_NLL, the server weights): the figure is
  fixed as committed; the caption is the place, round 2.
- Repetition (FedAvg SFT does not use the databases, five times; data
  stay at the client, four times; the round told in 3.3, the caption
  and Algorithm 1): round 2 if it still stands.

What the writer did with round 1: all five carried out. 3.1 and 3.5
state that neither the gold SQL query nor a query of the model is
executed and that no execution result enters the loss; the time limit
is given per benchmark and the cases without a label hang on one
criterion (the sample is never compared with the gold result); the
probability sentence is gone; 3.6 gives the condition for pairs first,
the two draws apart, identical samples not merged, the pair count after
the exclusion, what a question without pairs receives and the role of
M; the aggregation paragraph reads rule, reason, exception; Algorithm 1
has a conditional for a client without pairs; 3.2 names the setup and
the denominator and both counts of 3.4 refer to one set. Left out by
the writer, with its reason: that no client was without pairs (an
observation of the experiments), and the single-sample case (it
follows from "with replacement otherwise").

### Round 2, five notes (from the second cold read)

| # | Place | The note | What the writer did |
|---|---|---|---|
| 1 | lead; 3.3 first sentence | "Retains an NLL term" and "in addition to the gold SQL queries" read as a term on the gold SQL query in a preference round; its role in each kind of round | lead: "adds to the loss an NLL term on the correct sample"; 3.3 states the role of the gold SQL query in each kind of round |
| 2 | Fig. 2, caption | The figure shows the default configuration, writes "Global model" and L_DPO + lambda L_NLL, and weights by pairs; the caption retold the round | the caption now says what the figure depicts and maps its labels to the terms of the section |
| 3 | lead; 3.4; 3.7 second paragraph | Three sentences both readers read twice | all three rewritten |
| 4 | 3.5, 3.6 | The gold SQL query is executed once per question and its time counts against the limit of each sample on BIRD; "do not discriminate between queries" on databases without rows | both stated at that precision |
| 5 | 3.6 second paragraph | "One resampling step" had no referent | replaced by the relation: one iteration of preference optimization coincides with one communication round |

After round 2 (no further cold read, owner): build passes, lint has the
one stop of the abstract, no overlap with the closest or the example
papers, 24% of the words in runs of five or more words of the brief,
1,654 words with the caption (limit 1,700 without it).

Left for the owner to edit: 3.6, "queries of different meaning return
the same result" over a database without rows is stated without "can"
(a count and a column of names still differ there).

## After the drafts: Fig. 2 redrawn (2026-11-28)

The figure now draws the framework whole; the caption describes the
earlier figure and has to be written again. What the figure shows:

| Part | In the figure | In the section |
|---|---|---|
| Server | FedAvg of the adapters into the global model, weighted by the number of questions in a warm-up round and of pairs in a preference round | 3.7, Eq. (aggregation) |
| Clients | a row Client 1, ..., Client k, ..., Client K, each with its own databases; client k opens into the panel below | 3.1 |
| Between server and each client | the global model down, the adapter and one count up; labelled once, at client k | 3.1 |
| Panel of client k | questions, gold SQL and databases never leave it | 3.1 |
| Warm-up rounds, t = 1 to T_w | prompt, model, NLL on the gold SQL query, "as in FedAvg SFT: gold SQL is the training target" | 3.4 |
| Preference rounds, t = T_w + 1 to T | steps 1 and 2 (labeling), 3 (pairs), 4 (training on L_DPO + lambda L_NLL, reference the global model of t - 1); "gold SQL is the reference for the labels, not a target" | 3.5, 3.6, 3.7 |

No longer in the figure: the top row (order of a run, deploy), the
number of warm-up rounds, and the sentences between server and client
("only the adapter and one count leave a client"; "preference rounds
sample again from each new global model", now carried by "from
θ^{t-1}" in step 1); N = 10 stays in step 1. The sentence of the
caption on the weighting of a warm-up round is now in the figure.

## Caption of Fig. 2 written again (2026-11-28)

A new writer conversation of Section 3 (the Antigravity agent; the
first writer's session is closed) wrote the caption for the redrawn
figure from the table above, editing nothing else. Checked against the
figure and the section: subsections, equations, the count as n_k or
|P_k^t| and the reference model are right; build, lint and overlap
clean. One note round, two notes: "(labeled at client k)" read as if
the clients were labeled at client k; the parenthesis on theta^{t-1}
read twice. Both carried out: the arrows are "labeled once at client
k", and the arrow labels, theta^{t-1} as the model and reference, and
N and the two terms stand in three short sentences.

## Draft against the results of 2026-11-28 (no note)

FedDPO on BIRD dev at 3 and 4 rounds and RFT at 4 rounds read against
the section: it reports no result, and its statements on FedDPO (design
as published) and on the NLL term (a property of its definition, with a
pointer to Table 4) stay true. The evidence cell of the checks file
follows B3 and B4.
