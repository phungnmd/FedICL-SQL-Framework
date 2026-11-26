# Notes: Section 6, Ablation study

Draft in `sections/06_ablation.tex`. This file describes revision 2,
written from the editor's notes of round 2 and the brief as corrected
for it.

## Revision 2

One heading, eight paragraphs in the same order as revision 1: the
opening, the fixed pairs and reference, the NLL term, the preference
term, the number of warm-up rounds, the questions without a correct
sample, the weights, the pooled clients. Table 8 after the first.

Length: 927 words by `tools/style_profile.py`; the limit is 930.

### The five notes

| Note | What changed |
|---|---|
| 1, warm-up rounds | The first sentence of paragraph 5 states the conclusion: EX on Spider test is level with no, two and three warm-up rounds (the three values and the tests in a parenthesis); what differs is test-suite accuracy and the number of training questions without a correct sample. The second sentence is the result the reader found most telling: without warm-up rounds the model is above FedAvg SFT in EX and below it in TS on the three sets, while `\method` is above in both. Then its basis: a comparison of values; the tested comparison is with `\method`, significant on Spider-Syn only. Spider-DK last. Paragraph 6 gives the basis of the second half (the counts) |
| 2, preference term | First sentence: with the preference term fewer predictions end in an execution error; a difference in EX is not established on either dataset. EX is given once, as the two differences to `\method` with their adjusted $p$; the order of three EX values is gone, and no EX value of Table 8 is repeated. Both kinds of incorrect prediction now have their test: execution errors (both significant), incorrect results (`\wrpval`: significant on BIRD dev, not on Spider test) |
| 3, $p$-values | One sentence in the opening: significance is stated after the correction; a $p$-value is unadjusted unless marked as adjusted. The comparison with the gold SQL query prints both ("p = 0.0073; adjusted, 0.065"). The counts follow as a sentence of their own, without the colon. The pairs are described as the gold SQL query, as the correct side, with $M$ incorrect samples of the question, drawn as in Section 3.4 |
| 4, fixed row | The row is described without "the first" and "which": the second preference round trains on the pairs of the first preference round, against the reference model of that round. FedDPO and Liu et al. have a sentence of their own. On BIRD dev the row stands beside `\method` after four rounds (tested) and after three (a value) |
| 5, opening and server | The opening names the parts in the order of the paragraphs, says which block compares at which number of rounds, and states the start of the variants in one plain sentence. Paragraph 7 opens on what was done: "Averaging the adapters of the first preference round again with other weights leads to no significant difference in EX". The percentages are two clauses, one per weighting |

Said once now: the sentence that no pair is constructed for a question
without a correct sample is gone (the text says that `\method` learns
from the gold SQL query of such a question in the warm-up rounds);
paragraph 3 no longer describes FedDPO (it names the loss of FedDPO and
of Liu et al.); the TS comparison with `\method` is one clause; the
caption gives the first row, the columns and "Clients pooled", and no
longer what the opening says about the blocks.

### Left to Table 8 or to the opening

| Statement | Not in the text |
|---|---|
| B1 | the questions correct with one row only |
| B4 | the EX values of the row and of the model before the round (Table 8 has both); that the row is above the model before the round in EX; the row after four rounds (waits) |
| B5 | the two BIRD rows (wait); the $p$ of the two Spider rows; two of the three TS differences |
| B6 | every EX difference but the largest; that no client trains again (the first sentence says the adapters are averaged again) |
| Table 8 | that the two rows on the warm-up rounds total four rounds is said in paragraph 5 ("at the same total of four rounds") and no longer in the caption; what the two blocks are is in the opening |

### Doubts

1. The waiting rows still have no sentence: "Without the preference
   term" after four rounds, the two warm-up rows on BIRD dev. The
   section stands 3 words under the limit.
2. Paragraph 4 no longer says that the row gains over the model before
   the round in EX (44.39 against 42.70, 75.87 against 74.10). The
   first row of Table 8 shows it; a reader who wants what the NLL term
   alone adds has to read it there.
3. Paragraph 5, first sentence: "what differs is test-suite accuracy".
   Its basis is stated right after it, and of the three tested TS
   differences one is significant; the sentence is read with that
   basis.
4. Paragraph 5 drops "which has no test suite" for Spider-DK; Table 6
   and Section 5.3 say it.
5. The adjusted $p$ of the comparison with the gold SQL query prints
   0.065 now (0.058 in revision 1), since the family of the comparisons
   quoted in the text has grown.
6. Two source lines of the file are longer than the others; the PDF is
   not affected.

### Checked

`main.tex` compiles with the section (compiled into the scratchpad, not
into `build/`): no error, no overfull box, no undefined reference. `??`
prints for six numbers: the row without the NLL term on BIRD dev and
the pooled row. Every number that prints was read in the PDF text
against `generated/numbers.md`. The lint was not run.

## Earlier rounds (for the record)

First draft: 874 words. Revision 1: 928 words, from the five notes of
round 1. Their departures and doubts were answered in the editor's
notes; nothing of them is open beyond what is listed above.
