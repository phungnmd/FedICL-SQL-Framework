# What the passages have in common

Read after the passages, not in place of them.

**The opening of a section says what it is for.** The DPO section
starts with its goal and its key insight in two sentences, before any
equation. The FedAvg section starts from the method everyone knows
(SGD) and says why it is the natural starting point.

**A limit of earlier work comes with its cause.** LoRA does not say
that adapters are worse; it says they add inference latency because
they extend the depth of the model. FedProx says FedAvg drops devices
that cannot finish their epochs, and that it diverges when data are
not identically distributed. Earlier work is named, credited with what
it achieved ("has demonstrated empirical success", "despite the
theoretical guarantees and practical efficiency"), and then the exact
point where it stops is stated.

**A formula is followed by what it does.** After the gradient of the
DPO loss comes "Intuitively, ..." and then the one property that
matters and the experiment that shows it matters. Symbols are
introduced in the sentence that first needs them.

**A method is built from the plain version.** FedAvg is reached from
SGD through a named baseline (FedSGD), one change at a time, so the
reader sees what each change is for.

**A definition can be an example.** The test-suite paper defines false
positives and false negatives by pointing at two predictions in a
figure.

**A result is a number, its place, and its meaning.** "Table [n] shows
the results. ESM leads to a nontrivial false negative rate of 2.6% on
average, and 8.1% in the worst case." Then one sentence on where it
gets worse. In the ablations each drop comes with a cause, and a cause
that was not tested is marked as a guess ("possibly because").
Results sections are organised by the questions they answer.

**Claims are sized to the evidence.** "Our initial results suggest
..., but more comprehensive study is needed." "We hypothesize that"
for the idea before it is tested; plain present tense for what a table
shows. Limits are stated as the scope of the work ("while we evaluate
models up to 6B parameters") and as open questions.

**Sentences.** Mostly 15 to 30 words, one idea each, subject first.
"We" for what the authors did and think. Connectives carry the
argument: "However", "Thus", "Instead", "In contrast", "For example".
Almost no adjectives of praise for the authors' own method in the
method and results passages.
