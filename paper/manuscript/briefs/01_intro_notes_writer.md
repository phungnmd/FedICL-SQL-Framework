# Writer's Notes: Section 1 (Introduction), Abstract, and Keywords (Round 2 Revision)

## 1. Summary of Round 2 revisions
1. **Paragraph 3 and Paragraph 5 (`01_intro.tex`)**:
   - Replaced the opening of Paragraph 3 with the shared factual statement that neither FedAvg SFT nor existing federated preference alignment executes model queries on client databases, and each has a distinct limitation for Text-to-SQL.
   - Scoped the limitation of static pairs and a fixed reference model explicitly to `FedDPO as published`, noting that even with execution-labeled initial pairs it cannot track errors of updated global models (`Section~\ref{sec:ablation}`).
   - Separated pair renewal (`on-policy pair construction`, Paragraph 5) from reference-model renewal (`preference objective`, Paragraph 5).
   - Trimmed the final sentence of Paragraph 3 to state concisely that centralized methods exploit execution feedback on pooled data whereas under federation only each client holds its databases.
2. **Paragraph 6 (`01_intro.tex`)**:
   - Standardized every $p$-value in Paragraph 6 to Holm-adjusted exact McNemar $p$-values (`\padj`, `\errpadj`, `\wrpadj`), defined once at the top of the results sentences.
   - Named round three explicitly as the peak round of FedAvg SFT on BIRD dev (`\ex{bird}{fedavg}{3}`\%).
   - Paired FedAvg SFT's fifth-round Spider test score (`\ex{spider}{fedavg}{5}`\%) with its comparison against four-round `\method` (`\gain{spider}{fedavg}{5}{k2}{4}`, `$p = {}$\padj{spider}{fedavg}{5}{k2}{4}`).
3. **Contribution 3 (`01_intro.tex`)**:
   - Split the single 82-word item into three concise sentences and framed predictions on other tables or columns clearly as *alternative queries that return the gold result and pass the test suite* (`\fact{form.bird.k2.4.other_right_ts}` vs.\ `\fact{form.bird.fedavg.4.other_right_ts}`, after the generated suite rejects `\fact{form.bird.k2.4.other_ts_fail_pct}`\% of EX matches in that group).
4. **Smaller facts (`01_intro.tex` and `00_abstract.tex`)**:
   - Removed "without query execution" from Paragraph 4 (avoiding both the Spider prompt-row inaccuracy and a fourth repetition of FedAvg SFT's limitation).
   - Replaced "prevailing paradigm" in Paragraph 2 with OpenFedLLM's computational and communication motivation for training LoRA adapters under FedAvg SFT.
   - Matched `sheng2025slmsql` in Paragraph 1 to fast inference and suitability for edge deployment, and `li2024codes` to deployment on local machines.
   - Specified the NLL term as acting `on the correct sample of each pair` in both the abstract and Paragraph 5 (with `weight~\setting{pref.nll}` in Paragraph 5).
   - Expanded `direct preference optimization (DPO)` at first occurrence in `00_abstract.tex` and compressed the FedAvg SFT sentence there so it does not repeat Paragraph 3.
5. **Length, sentence length, and repetition**:
   - Reduced `01_intro.tex` from 1,059 words to ~955 rendered words (excluding the Fig. 1 caption and `itemize` markup), with ~24 words per sentence across 41 sentences (matching the reference papers' ~26-word average).
   - Reduced `00_abstract.tex` to ~253 rendered words across 8 sentences (~31 words per sentence).
   - Eliminated cross-paragraph repetition of FedAvg SFT's defect, FedDPO's static pairs/fixed reference, the adapter-plus-weight upload, and the appositive phrase introducing `\method`.

## 2. Sources
- Web sources: None used; all cited-work statements trace to `briefs/02_related_rows.md`, `briefs/02_related_table1_rows.md`, and `.sources/abstracts.json`.
