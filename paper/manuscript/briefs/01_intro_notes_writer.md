# Writer's Notes: Section 1 (Introduction), Abstract, and Keywords (Round 3 Revision)

## 1. Summary of Round 3 revisions
1. **Caption of Fig. 1 (`01_intro.tex`)**: Updated to match the redrawn `figures/fig_idea.pdf` (`paper/figures/fig_idea.svg`) on the BIRD database `\texttt{language\_corpus}`: `$N = {}$\setting{pref.samples}` samples from the global model in the first preference round after `\setting{rounds.warmup}` warm-up rounds yield eight correct samples, one incorrect result, and one execution error; the table displays the samples of the `$M = {}$\setting{pref.pairs}` preference pairs built for this question beside the gold execution result, where two distinct correct samples with identical SQL text (first row) are paired against the incorrect result and the execution error (second and third rows) under the DPO plus NLL loss. Removed all traces of the earlier `student_loan` example.
2. **Contribution 3 (`01_intro.tex`)**: Scoped `\fact{form.bird.k2.4.other_ts_fail_pct}`\% explicitly to `\method's EX-correct answers on other tables or columns` rather than all EX matches.
3. **Paragraph 3 (`01_intro.tex`)**: Removed `"even with execution-labeled initial pairs"` and the `(Section~\ref{sec:ablation})` pointer on FedDPO, stating only the published design fact (`each client trains on a fixed dataset of external pairs under one reference model fixed throughout federation, so training never targets the outputs or evolving errors of updated global models`).
4. **Scope corrections (`00_abstract.tex` and `01_intro.tex`)**:
   - In `00_abstract.tex`, replaced `"existing federated alignment methods based on DPO, such as FedDPO"` with `federated direct preference optimization (FedDPO), which applies direct preference optimization (DPO) to general preference alignment`.
   - In Paragraph 5 of `01_intro.tex`, changed `"so every round forms one resampling step"` to `so every preference round forms one resampling step`.
5. **Voice (`01_intro.tex`)**: Restored active first-person `"we"` where design choices are introduced and findings reported, specifically across the four components of Paragraph 5 (`we run`, `we address`, `we draw`, `we renew ... and add`), the findings of Paragraph 6 (`We observe that \method{} outperforms...`, `we find that preference rounds halve...`), Paragraph 3 (`which we formulate`), Paragraph 4 (`We observe that...`), and Contribution 3 (`We further show that...`), raising `"we"` sentences to 19 of 41 sentences (~46%). Left the abstract and caption in their own registers and left all other passages unchanged.

## 2. Lengths and sources
- `sections/00_abstract.tex`: ~255 rendered words, zero citations, zero typed digits.
- `sections/01_intro.tex`: ~975 rendered words excluding the Fig. 1 caption and `itemize` markup (~24 words per sentence across 41 sentences), zero typed digits.
- Web sources: None used.
