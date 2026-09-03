# FedLS-SQL — protocol-v2 manuscript skeleton

This is a structural outline only; result claims remain pending.

1. Introduction: accuracy/resource/privacy tension in federated NL-to-SQL.
2. Related work: federated PEFT/KD, LLM-to-SLM collaboration, Text-to-SQL knowledge use.
3. Problem formulation: private clients, public server corpus, explicit evidence and role contracts.
4. Method: reference loop first; final KD/Federated mechanism inserted after P2.3.
5. Experimental setup: Spider, BIRD release, evidence policy, DB-disjoint splits, EX evaluator, models and budgets.
6. Results: centralized/FL, causal transfer ladder, both directions, selected-method ablation.
7. Robustness and efficiency: seeds, non-IID, optional family, communication/resource/privacy boundary.
8. Limitations: structural rather than DP privacy, public-data assumptions, evaluator and compute scope.
9. Conclusion.

Do not copy protocol-v1 accuracy numbers into the abstract or main tables.
