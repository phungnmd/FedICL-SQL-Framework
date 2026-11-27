# Voice guide

This document specifies the register of the manuscript and the
rhetorical organization of each section. The register is that of
contemporary machine learning research papers: technically dense,
terminologically precise and assertive within the limits of the
evidence. The specification characterizes established practice in the
field; it is applied with judgment, and it prescribes neither vocabulary
nor numerical targets.

## 1. Register

**Technical density.** Concepts are expressed through the established
terminology of federated learning, preference optimization and
Text-to-SQL, and through nominal compounds that compress a relation into
a term (client-side execution, execution-derived supervision, on-policy
pair construction). A concept that possesses a term is denoted by that
term at every occurrence; it is not paraphrased in everyday vocabulary,
and it is not re-explained after its definition.

**Propositional compression.** Each sentence advances a proposition
about the problem, the method or the evidence. The chronology of the
research (what was attempted, observed and subsequently modified) is
absent from the text. Consecutive sentences are connected by explicit
logical relations (consequently, in contrast, specifically, whereas)
instead of temporal sequence.

**Assertiveness.** Properties of the method and empirical findings are
stated in the present indicative with precise verbs: a method
outperforms, reduces, eliminates, enables, preserves or yields.
Epistemic qualification is reserved for explanations that the
experiments do not isolate, which are introduced as attributions or
hypotheses. A finding supported by a table is never attenuated, and a
qualification is never repeated. Confidence resides in the formulation
(the principal result first, the active voice, a precise verb) and never
in an enlargement of the claim or the omission of its scope.

**Contribution orientation.** Wherever the method or one of its
components is introduced, the sentence identifies what distinguishes it
from prior approaches and what it achieves. Novelty is articulated
explicitly, in the introduction, in the contribution list and at the
opening of the method section, and it is located precisely: the text
states which element is new relative to which prior approach.

**Person and voice.** The first person plural with an active verb
conveys what the authors propose, formulate, design, evaluate, observe
and demonstrate. The passive voice describes procedural steps whose
agent is immaterial.

**Limitations.** Constraints on the scope of the study are consolidated
in the limitations subsection, where each is formulated once as a
boundary of the investigation and, where appropriate, as a direction for
subsequent research. The remaining sections do not anticipate objections
and contain no defensive disclaimers.

## 2. Rhetorical organization by section

### Abstract

A single paragraph progressing through five functions: the research
context, the limitation of existing approaches, the proposed framework
identified by name together with its central mechanism, the principal
quantitative results, and the implication. The method is characterized
by its mechanism, not by an enumeration of procedural steps.

### Introduction

The introduction narrows from the general research landscape to the
specific contribution.

1. *Context and significance.* The broader problem domain and the
   reason it matters.
2. *Specific setting.* The scenario under investigation and the
   prevailing paradigm for addressing it.
3. *Limitations of existing approaches.* Each limitation is identified
   as a limitation, attributed to its underlying cause and, where
   several exist, enumerated as distinct challenges.
4. *Key insight.* A single sentence articulating the observation that
   renders the limitation addressable.
5. *Proposed framework.* The framework by name, its constituent
   components by name, and the function of each component in relation to
   the identified challenges. The statement of purpose answers exactly
   the limitation established in the third function.
6. *Empirical validation.* The principal quantitative results,
   including the magnitude of the improvement over the strongest
   relevant baselines.
7. *Contributions.* An itemized list in parallel grammatical form, each
   item pairing a contribution with its significance.

### Related work

The section is organized by research direction, not by individual
publication. Each paragraph synthesizes one direction, characterizes its
representative methods collectively and concludes with the delimitation
that positions the present work: the specific capability that the
direction lacks in the setting under study.

### Method

The exposition is modular. It is structured by the components and
mechanisms of the framework, and the temporal order of a training run is
conveyed by the algorithm and the overview figure, not by the section
structure.

1. *Problem formulation.* The setting, the notation and the learning
   objective, stated formally.
2. *Framework overview.* A concise paragraph that designates each
   component, specifies its role and refers to the overview figure.
3. *Components.* One subsection per component, titled with a noun phrase
   that designates the mechanism. Each subsection proceeds from the
   motivation for the component (the deficiency it addresses) through
   its formal definition to the interpretation of that definition (the
   property it guarantees or the behavior it induces).
4. *Algorithm and complexity.* The complete procedure in an algorithm
   environment, followed by its communication and computation
   requirements.

Design decisions are justified by the properties they confer, not by the
history of their selection.

### Experimental setup

A compact, categorical specification: datasets, federated
configurations, models, baselines, evaluation metrics, implementation
details and the statistical protocol. Each category is stated
declaratively with its values; a justification, where one is required,
occupies a subordinate clause.

### Results

The section is organized into subsections, each of which answers one
question about the method, and each paragraph is organized around a
finding.

1. *Finding.* The opening sentence states the result together with its
   magnitude.
2. *Evidence.* The supporting table or figure and the decisive values.
3. *Interpretation.* The mechanism that accounts for the result, stated
   as established when an experiment isolates it and as an attribution
   otherwise.
4. *Implication.* What the finding establishes about the method or the
   setting.

The prose does not enumerate a table row by row; it extracts the pattern
that the table exhibits. The statistical protocol is defined once in the
experimental setup, test statistics are reported in the tables, and the
running text indicates significance concisely.

### Ablation study

A subsection of the results. Each paragraph isolates one component:
the variant that removes or replaces it, the resulting change in
performance, and the role of the component that this change
demonstrates. The subsection concludes by relating the components to
one another.

### Discussion

The discussion operates at the level of mechanisms and implications: why
the framework produces the observed behavior, and what this entails for
federated training in the setting under study. It does not restate
numerical results. The limitations subsection follows and conforms to
the principle stated in Section 1.

### Conclusion

An affirmative synthesis in three parts: the problem addressed, the
proposed framework and the principal findings, followed by concise
directions for future research. The conclusion introduces neither new
results nor new qualifications.

## 3. Illustrative contrasts

The following pairs, drawn from an unrelated domain, illustrate the
distinction between an explanatory register and the register specified
above. They exemplify the transformation, and their wording is not
material for the manuscript.

| Explanatory register | Research-paper register |
|---|---|
| The server never sees the pictures that stay on the phones, so it has no way to tell which of its guesses are wrong. | Because raw images remain on-device, the server receives no error signal for its predictions. |
| We first trained with a large batch, saw that training became unstable, and then lowered the learning rate. | A reduced learning rate stabilizes optimization at large batch sizes. |
| With the extra loss, the model is above the baseline on both sets. | The auxiliary objective yields consistent improvements over the baseline on both benchmarks. |
| In the first row the score is 71.2, in the second row it is 73.5, and in the third row it is 74.1. | Accuracy increases monotonically with the number of participating devices, from 71.2 to 74.1. |
| This part is there because some devices have very little data and would otherwise learn nothing useful. | The regularization term mitigates overfitting on data-scarce devices. |
