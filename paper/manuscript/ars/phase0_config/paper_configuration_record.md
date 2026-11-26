# Paper Configuration Record

Phase 0 of the ARS `academic-paper` skill, mode `full`. Confirmed by
the owner on 2026-11-26.

| Parameter | Value |
|---|---|
| **Topic** | Federated fine-tuning of a small language model for Text-to-SQL, with preference rounds that use execution labels made at the clients |
| **Research Question** | The thesis of `CLAIMS.md`, section 1: in federated Text-to-SQL a client holds questions with gold SQL and the databases to run SQL on; FedAvg SFT learns from the first alone, and FedLS-SQL also learns from the second, by running the model's own queries at the client and training on which of them return the gold result |
| **Paper Type** | IMRaD, in the shape of `WRITING_PLAN.md`, section 5: Introduction, Related work, Method, Experimental setup, Results by research question, Ablation study, Discussion and limitations, Conclusion, Declarations, Appendix A and B |
| **Discipline** | Computer science: machine learning and natural language processing (Text-to-SQL), federated learning |
| **Target Journal** | Journal of Intelligent Information Systems (Springer). Second: Computers, Materials and Continua |
| **Venue Profile** | absent until confirmed. Limits the owner has declared, to be recorded as the profile: 25 pages in `sn-jnl`, references included; abstract of 150 to 250 words; 4 to 6 keywords; LaTeX source; compiled on TeX Live 2018. Review model: open |
| **Citation Format** | Numbered, Springer Basic (`sn-basic.bst`) through BibTeX. Of ARS's five formats the nearest is IEEE; the journal's style file sets the format |
| **Output Format** | LaTeX: `sections/*.tex` in the `sn-jnl` class, built with `make` |
| **Body Language** | EN |
| **Abstract** | EN-only |
| **Word Count Target** | about 8,500 words of body text. An estimate: the body sections have 18.3 pages in the plan, about 5 of them floats, at 650 words a page. The limit that binds is the 25 pages |
| **Existing Materials** | Thesis, contributions and claims with their evidence and ceilings (`CLAIMS.md`, approved). Results as generated tables and number macros (47 rows in, 34 waiting on the GPU). Literature notes (`LITERATURE.md`, `DPO_RESEARCH.md`) and 4 checked entries in `references.bib`. Section plan with page budgets. The journal's class and a build that compiles. A draft of Section 3.4. Passages from seven published papers (`voice/`) |
| **Co-Authors** | not filled in yet (owner, 2026-11-26); the author block and the CRediT statement wait for it |
| **Funding** | not filled in yet (owner, 2026-11-26); the funding and competing-interests statements wait for it |
| **Style Profile** | attached: `style_profile.md`. Built from published papers of the field and of the target journal, at the owner's decision, and not from papers of the author's own; it therefore stands for the conventions of the field and the journal |
| **Domain Evidence Profile** | `cs_ml` (admits arXiv preprints and proceedings beside journal papers) |
| **Citation Verification** | `strict` (an entry whose DOI or arXiv id fails lookup blocks finalization) |
| **Retraction Policy** | advisory (mark only, default) |
| **Operational Mode** | `full` |

## Notes

### Where the run departs from ARS's defaults

Each follows from a hard rule of the project or from the journal.

1. Numbers are macros. A result or a setting in the text is written
   with the generated macros (`\ex`, `\gain`, `\fact`, `\setting`),
   never typed, so that every number traces to a committed result.
2. The draft is LaTeX from the start, one file per section, and not
   Markdown converted at the end. The acronym check of ARS reads
   Markdown; the abbreviation check of `tools/lint.py` stands in for it.
3. The whole paper is drafted now (owner, 2026-11-26: it is a draft).
   34 result rows are not in yet; a number that waits is written with
   its macro and prints as a placeholder until its row is committed.
   A sentence that reads such a number says what the comparison is and
   leaves its direction and size to the number; it is revisited when
   the row is in.
4. The first person plural ("we") is used, as the papers of the field
   do; ARS puts the conventions of the discipline above its
   third-person default.
5. The drafting agent runs on Fable 5.2 at high effort; the other
   agents run on Opus.
6. The owner reads each section before it is committed, in addition to
   ARS's own checkpoints (this record, the outline).

### What becomes of the existing material

| ARS phase | Artefact | Built from |
|---|---|---|
| 1 Research | Annotated bibliography, each entry checked by DOI or arXiv id | `LITERATURE.md`, `DPO_RESEARCH.md`, `references.bib`; a search only where a section lacks a source |
| 2 Architecture | Paper outline with word allocation, evidence map | `WRITING_PLAN.md` section 5; the generated tables and figures |
| 3 Argumentation | Argument blueprint: claim, evidence, reasoning per section | `CLAIMS.md` (claims A1 to E2, ceilings, limitations) |
| 4 Drafting | The sections | the three artefacts above; the conventions shown in `voice/` |
| 5 Citations, abstract | Citation audit; abstract and keywords | the draft, `references.bib` |
| 6 Review | Review report, at most two revision rounds | the draft |
| 7 Format | The submission source | `make submit` (already built) |

`WRITER.md` and `packets/` are retired: ARS's drafting agent and its
artefacts take their place. `CLAIMS.md`, the generator, the lint and
the build stay as they are. The draft of Section 3.4 is an existing
draft and is written again.

### The owner's rules and the manuscript

Limited (they no longer shape the prose of the paper):

- "plain words, short documents" of `AGENTS.md`: for notes, reports and
  replies only;
- the role text of `WRITER.md`, with its instruction to claim "plainly";
- the packet as the writer's only source, written in the lab's words;
- the rule that the writer sees only its role, the voice folder and its
  packet: the drafting agent works from ARS's artefacts, under ARS's
  own rule that facts come from the supplied material and not from
  memory.

Kept:

- the hard rules (honesty, data roles, Git);
- the approved claims and their ceilings; what the paper prints and
  what stays in the lab log;
- "the model" for the trained model; no emojis, no em dashes;
- no hedge without a reason (ARS hedges uncertain claims only, which
  agrees);
- the journal's limits and the lint that checks them.
