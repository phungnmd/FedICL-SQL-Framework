# Notes to the editor: Section 4, Experimental setup (revision 2)

Files revised: `sections/04_setup.tex`, and the lead-in sentence of
`sections/A_prompt.tex` and of `sections/B_settings.tex` (nothing else
in those two files). The paper compiles with them (built into my
scratch folder): no undefined reference or citation, no overfull box,
one `??` (`\setting{fedprox.mu}`). Your macros and the regenerated
Table B1 are kept.

## Length

1,370 words by my count, about 1,335 by yours if the gap of 35 holds:
about 85 over the upper end. The three cuts you accepted are applied.
Notes 1, 2, 4 and 5 add about 180 words of facts; I took about 65 out
elsewhere (listed under "Left out").

| Part | Brief | Revision 1 | Revision 2 |
| --- | --- | --- | --- |
| Opening | 90 | 65 | 65 |
| 4.1 Datasets and metrics | 250 | 432 | 359 |
| 4.2 Federated setups | 190 | 229 | 329 |
| 4.3 Models | 80 | 78 | 69 |
| 4.4 Baselines | 215 | 242 | 248 |
| 4.5 Implementation | 190 | 153 | 189 |
| 4.6 Statistical test | 110 | 93 | 111 |

What I would cut next, in this order (words by my count):

1. "its clients still differ in size, as the databases do" (4.2): 10.
   Table 2 shows it in the "Per client" column.
2. "a smaller $\alpha$ giving a stronger skew" (4.2): 7.
3. "where one table also tests \method{} against its variant without
   warm-up rounds" (4.6): 14, if the caption of Table 6 names its two
   reference rows.
4. "which sets the order of the training examples and the sampling of
   the preference rounds" (4.5): 15, if the seed row of Table B1 says
   it.
5. The redraw rule, "and the partition is drawn again until every
   client holds at least 5 databases (3 with ten clients)" (4.2): 21,
   moved to a row of Table B1.
6. The list of the level names in 4.1 ("simple, moderate or
   challenging ..., easy, medium, hard or extra hard"): 14, keeping
   that results are reported by difficulty level.

Items 1 to 4 bring the section to about 1,290 by your count; all six
to about 1,255.

## What changed for each note

1. Partition (4.2). The paragraph on the partition is rebuilt.
   The reason for the skew now has its three steps: the evaluation
   databases are new to every client, what carries over to them is the
   structure of the SQL queries, so the non-IID setups skew the
   clients by query complexity. The levels: the evaluation script of
   Spider gives them for Spider train; its parser cannot read most
   queries of BIRD train, so the criteria are applied to the query as
   parsed by a general SQL parser, with a pointer to Appendix B, where
   the parser is named. The tiers are "distributed one after another",
   and the rule reads: "A client that holds at least $1/K$ of all
   databases when a tier comes up receives none of that tier". It is
   stated as a rule of the partition; NIID-Bench is cited for the
   label-distribution skew in the sentence before.
2. Sources of the settings (4.5). The second paragraph says that the
   learning rate of SFT and the three epochs of centralized and local
   SFT are those of the LoRA fine-tuning that SPFT-SQL reports for
   this model, and that the preference rounds take their learning
   rate, pairs per update, single epoch and weight decay from
   CodeLutra, like $\beta$ and $\lambda$.
3. Questions without pairs. The paragraph left 4.1 and closes 4.2,
   after the setups of Table 2: the warm-up rounds and the SFT
   baselines train on every question of a client; a preference round
   constructs no pair for the two kinds of Section 3.4, with the
   counts. In 4.1 the two metrics now follow each other.
4. Seed and tests (4.5, 4.6). 4.5: the seed "sets the order of the
   training examples and the sampling of the preference rounds", and
   the second seed gives "two further rows of the main table of
   Section 5". 4.6 is rebuilt on the corrected ceiling: each table
   names the row its differences are tested against; FedAvg SFT in
   Section 5, where one table also tests the method against its
   variant without warm-up rounds; the method at the same number of
   rounds in Section 6; the two rows of the second seed against each
   other; no test for the Local SFT row, a mean over $K$ models.
5. Form.
   - "so that the comparison isolates these": the sentence now reads
     "\method{} differs from it only in the last 2 rounds, which are
     preference rounds."
   - "and the federated rows the same clients and number of rounds":
     now a sentence of its own, "The federated rows also share the
     clients and the number of rounds, $T = 4$."
   - The two differences of FedDPO: "its pairs and its reference model
     are not renewed, and its loss has no NLL term."
   - Section 6: "ablates the two separately, and also trains on the
     correct samples without the preference term."
   - "all but one of the ablations": 4.1 now says "every ablation
     except the one with pooled clients, which is run on Spider."
   - Appendix A lead-in: the prompt is the same for every model and is
     sent as the user message in the chat format of the model; for the
     main model this format also adds its default system message.
   - Appendix B lead-in: "Table B1 lists the settings of all
     experiments and the software used."

## Left out of the text

Taken out in this revision, for length:

- The sentence that the row "No training" is the pretrained model
  (4.4). The row name is no longer explained in Section 4.
- The sentence that the weights of the model stay frozen and only the
  LoRA adapter is trained (4.3). Section 3 says it; 4.5 gives the rank.
- The pointer to Section 6 in the opening. 4.1, 4.4 and 4.6 point to
  it.
- "so that the two are compared at an equal number of rounds" (4.4).
  RQ1 and the sentence on the federated rows say it.
- The three cuts you accepted (asterisk and unadjusted $p$-value; the
  clients of a round train one after another; the gloss of a test
  suite).

In the brief and not in the text, as in revision 1 unless marked:

- BIRD train: the questions whose gold SQL query exceeds the time
  limit in the first and the second preference round
  (`\fact{train.bird.gold_timeout.pref1}`, `.pref2`).
- The partitions keep their own seed (new in the brief; Table B1 can
  carry it).
- McNemar: "the test uses the questions that one model answers
  correctly and the other does not"; and "a test is counted once, in
  the first table that prints it".
- The SFT batch size and the other rows of Table B1 that 4.5 does not
  name.

## Doubts about a fact

1. "Section 6 ... also trains on the correct samples without the
   preference term" rests on your note and on Section 3.4, not on a
   row of my brief. Check the wording against the ablation of
   Section 6.
2. "the ablation with pooled clients" is named in 4.1 without a
   gloss. It is the wording of the brief; a reader meets it for the
   first time here.
3. "Its parser cannot read most queries of BIRD train" is the brief's
   sentence as it stands; I give no count.
4. Typed without a macro, because none exists: $\lambda = 0$, "three
   example rows", "four tiers", "ten clients", "single epoch" of the
   preference rounds.
5. 4.5 attributes to SPFT-SQL only the learning rate and the epochs,
   and to CodeLutra the four settings named in the brief; nothing else
   in Table B1 is attributed in the text.

## Placement

- The paragraph on the questions without pairs is in 4.2. Your first
  round kept its content in 4.1; your second said it belongs where the
  reader thinks about what the clients train on, which I read as the
  end of 4.2. It moves back as one paragraph if you prefer 4.1.
- Table 2 floats above the heading of 4.2 in my build and prints as
  "Table 1" until the table of Section 2 exists.
