# Questions to the editor: Section 3, Method

Filed with the outline. None blocks it; each decides the wording of the
passage named. Where no answer comes, the draft follows the default.

## 1. Net effect of warm-up on the number of questions that yield pairs

- Passage: Section 3.4, outline paragraphs 5 and 6 (point 4 of the brief).
- Question: for the pretrained model (the first preference round with
  $T_w = 0$), how many training questions yield preference pairs, and how
  many have samples that are all correct, on BIRD and on Spider? Are
  there macros for these counts?
- Why it is required: the brief gives one side of the effect. Warm-up
  lowers the number of questions without a correct sample (BIRD 4,035 to
  2,698), but it also raises the number whose samples are all correct,
  and those yield no pair either: after two warm-up rounds 416 on BIRD
  and 2,327 on Spider, against 557 Spider questions without a correct
  sample. A reviewer will ask whether warm-up increases the number of
  questions that yield pairs. The materials do not say, and on Spider the
  net change could be negative.
- Default: the paragraph states only the scoped count of the brief and
  makes no statement about the number of pairs.

## 2. Is $\pi_{\theta^{0}}$ the pretrained model?

- Passage: Section 3.4, outline paragraph 6; Algorithm 1, line 1.
- Question: does the initialization of the adapter leave the output of
  the pretrained model unchanged (the usual LoRA initialization), so that
  with $T_w = 0$ the first preference round samples from the pretrained
  model and uses it as reference model?
- Why it is required: the paragraph says that the pretrained model
  already yields pairs and that Algorithm 1 covers $T_w = 0$. The two
  statements connect only if $\pi_{\theta^{0}}$ is the pretrained model.
- Default: the two statements stand side by side without the identity.

## 3. Abbreviations at first use

- Passage: Sections 3.1 and 3.7.
- Question: `terms.md` wants SFT, FedAvg, DPO, NLL and LoRA in full at
  first use. Sections 1 and 2 are not in `sections/`. Do they expand all
  five, so that Section 3 uses the short forms throughout?
- Why it is required: it decides the wording of the first sentences of
  3.1 and of the definition in 3.7.
- Default: short forms throughout, no expansion in Section 3.

## 4. Section 4.2: label and content

- Passage: Section 3.5, outline paragraph 8; Section 3.6, paragraph 9.
- Question: the brief places the counts of questions without labels in
  Section 4.2, but the only label listed for Section 4 is `sec:setup`. Is
  there a label for that subsection? Does it also give the number of
  Spider training questions on databases without rows
  (`\fact{train.spider.no_rows}`)?
- Why it is required: the cross-reference must use a listed label, and
  the count has to appear in exactly one place.
- Default: `Section~\ref{sec:setup}` in both passages, and no count in
  Section 3.

## 5. Gold SQL query in place of a missing correct sample

- Passage: Section 3.6, outline paragraph 9.
- Question: does Section 5.3 report the variant that pairs the gold SQL
  query with incorrect samples for questions without a correct sample
  (row `k0gold`, a comparison of the "text" family)? May Section 3.6
  point to it?
- Why it is required: the rule that both sides of a pair are samples is
  the place where a reviewer asks why the gold SQL query is not used,
  which would make warm-up unnecessary. A forward reference answers that
  in a clause; without it the rule stands as a bare definition.
- Default: the rule is stated without a reference.
