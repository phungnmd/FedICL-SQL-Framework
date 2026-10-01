# FedLS-SQL — manuscript outline

What this file is: the paper's structure and what each section must contain.
It holds no results. Numbers come from `paper/results/MAIN_RESULTS.md` only.

Merged on 2026-09-29 from `MANUSCRIPT_SKELETON.md`, `PAPER_OUTLINE_TARGET.md`,
and `FEDLS_SQL_METHOD.md` (originals in `paper/archive/paper_planning_2026-09/`).
The final title and method subtitle stay open until the method is chosen.

## Target contributions

- A federated LLM-to-SLM Text-to-SQL workflow with explicit public, private,
  and evaluation data roles.
- A reproducible EX gain over pure FL with the same private budget.
- Primary endpoint: final Spider EX. CoT is optional; distinguish higher final
  accuracy from reaching a target accuracy in fewer private rounds.
- Matched evidence that shows where the gain comes from: teacher targets, soft
  KD, federated optimization, or their mix.
- Keep public-gold controls even if they tie KD. A pipeline-level contribution
  and a teacher-specific contribution have different evidence requirements;
  use the claim ladder in `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`.
- Results in both directions (Spider ↔ BIRD) that show how far transfer goes.
- Adapter communication, SLM-only deployment, and a clearly bounded privacy
  claim (structural isolation, not DP).

## Sections

1. Introduction: the accuracy / resource / privacy tension in federated
   Text-to-SQL.
2. Related work: federated PEFT and KD, LLM-to-SLM collaboration, Text-to-SQL
   distillation. Claim limits: `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`.
3. Problem setup: private clients, public server data, evidence and role
   rules.
4. Method (write only after the ablation supports each part). Must state:
   - private, public, and evaluation dataset roles;
   - Spider/BIRD profile and evidence use in every stage;
   - client objective and aggregation rule;
   - how teacher targets are built and checked by execution;
   - server objective and stage schedule;
   - what is communicated, the threat boundary, and SLM-only deployment;
   - the matched ablation that justifies every kept part.
5. Experimental setup: Spider, BIRD release, evidence policy, DB-disjoint
   splits, EX evaluator, models, budgets.
6. Results: centralized vs FL, the causal transfer ladder, both directions,
   ablation of the chosen method.
7. Robustness and efficiency: seeds, non-IID, optional second family,
   communication, resources, privacy boundary.
8. Limitations: structural (not DP) privacy, public-data assumption,
   evaluator and compute scope.
9. Conclusion.

Do not copy protocol-v1 accuracy numbers into the abstract or tables.
Protocol-v1 method prose: `paper/archive/protocol_v1_no_bird_evidence/FEDLS_SQL_METHOD_v1.md`.
