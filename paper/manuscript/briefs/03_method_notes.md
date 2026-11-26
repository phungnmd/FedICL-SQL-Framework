# Notes to the editor: Section 3, Method (revision 2)

Draft in `sections/03_method.tex`. `make pdf` builds it: no undefined
reference, no overfull box. The section ends three lines into its sixth
page, as in revision 1.

## Length

Formulas, macros, floats and displayed equations not counted.

| Subsection | Words | Brief |
| --- | --- | --- |
| 3.1 | 275 | 240 |
| 3.2 | 153 | 150 |
| 3.3 | 163 | 170 |
| 3.4 | 761 | 740 |
| 3.5 | 133 | 120 |
| Total | 1,485 | 1,420, 1,490 at most |

The total is five words under the upper end. 3.4 came down from 787
to 761 while its paragraph on CodeLutra grew by about 20 words. 3.1
grew by what note 4 asks it to name, and 3.5 by the pass of the
reference model, which moved there from 3.4.

## What was done with each note

1. The paragraph on CodeLutra.
   - Order of importance. After the sentence on what CodeLutra does,
     the paragraph says: "The contribution of FedLS-SQL is to bring
     this execution-based supervision into federated training, where
     only a client can compute it", followed by what that consists of
     (a federated round is the step that renews samples, labels and
     pairs, its global model is the reference model of every client,
     warm-up rounds come first). Then "The rest are settings", and the
     settings followed and the two that differ. No "first" and no "to
     our knowledge".
   - $\lambda$ is no longer in the list of what is followed. The
     sentence on the token average ends: "the same $\lambda$ then
     weighs the NLL term less against the preference term than in
     CodeLutra, by a factor of $\lvert y^{+} \rvert$".
2. The reason for the warm-up rounds. The paragraph now has the
   missing step: the first preference round samples from a model
   already trained on the gold SQL query of every question, "which
   leaves fewer questions without a correct sample than the pretrained
   model does". Section 6 is named as the place of these counts and of
   the number of warm-up rounds. Nothing on execution accuracy, and
   nothing on the number of questions that yield pairs.
3. Questions without pairs, and the draw.
   - "For two kinds of question, no pair is constructed in any round,
     because execution cannot separate correct from incorrect
     samples", then the two kinds. "fixed by the data" is gone.
   - The draw: "It draws $M$ of the correct samples and, independently,
     $M$ of the incorrect samples of the question, uniformly over the
     samples rather than over the distinct queries, and pairs them in
     the order drawn". The rule of replacement is left to Appendix B,
     with a pointer.
   - "executes $y^\star$ once and every complete sample"; a truncated
     sample "is neither executed nor labeled".
4. 3.1 par. 4 says that a client sends its adapter and one integer
   "and nothing else", then names what stays: its questions, gold SQL
   queries and databases, and the samples, the execution results, the
   execution labels and the preference pairs that a preference round
   produces from them. "everything derived from them" is gone.
5. Form and length.
   - The reference model: "All clients thus share one reference model,
     the model with which each of them starts the round, so that the
     preference term measures the change made by local training." The
     pass moved to 3.5, where it says what it computes: "one pass
     without gradients computes the log-probabilities of the pairs
     under the reference model".
   - One pointer to Section 6 closes the paragraph on on-policy pairs
     and names the three ablations of 3.4 (the on-policy pairs, the
     two terms of the loss, the aggregation weights). The paragraph on
     the NLL term and the paragraph on the aggregation carry none. The
     aggregation now comes before the on-policy pairs, so the round is
     complete before the paragraph on what repeating it gives.
   - The adapter and the integer are stated in 3.1 only. The caption
     lost its last sentence; 3.3 and 3.4 give the weights of the
     aggregation without the upload; 3.5 says that the communication
     is unchanged and gives the size of the adapter.

## Changed beyond the notes, for length

- 3.4 no longer mentions the empty sample. An output without query
  text was the case the first reader stumbled on; the brief labels it
  incorrect, which is what the general rule gives a sample that fails
  to execute. If the code treats it apart from that rule, the sentence
  has to come back.
- "where queries that differ return the same result" (the empty
  database) is cut: the reason given for both kinds of question now
  covers it.
- That the questions which yield pairs change from round to round is
  no longer said in the paragraph on on-policy pairs; the paragraph on
  questions without pairs says it. The pointer to Section 5 for the
  counts is in 3.5 only.
- 3.1 par. 3: the initial adapter "leaves the output of the pretrained
  model unchanged"; the clause that $\pi_{\theta^{0}}$ is the
  pretrained model is dropped.
- 3.5: "each bounded by the time limit" is cut (3.4 gives the time
  limit), and the server is folded into the first sentence.

## Not changed

- The note inside Fig. 1 still reads "Only LoRA adapters travel",
  where the text says an adapter and one integer; the caption no
  longer speaks of it.
- 3.4 is 21 words above 740. What could still go: the clause on
  FedDPO (14 words), or the pointer sentence on the reason for $M$ if
  3.5 is judged to carry it.

## Doubts

- The pointer "Appendix B gives the rule of replacement" relies on
  Appendix B stating it.
- "as in evaluation (Section 4)" relies on Section 4 defining how the
  query is read from the output and how results are compared.
- "by a factor of $\lvert y^{+} \rvert$" is the brief's "by the number
  of tokens of $y^{+}$", written with the symbol.
- "Section 6 reports these counts" (3.3) relies on Section 6 printing
  the questions without a correct sample at the first preference
  round, after the warm-up rounds and from the pretrained model.
