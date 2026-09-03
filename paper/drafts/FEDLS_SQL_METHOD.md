# 3. FedLS-SQL — protocol-v2 method placeholder

The final method is intentionally not frozen. The current reference pipeline is
private client LoRA CE, sample-weighted factor-wise FedAvg, execution-verified
public teacher-target CE, and optional reverse KL. It will be written as the
proposed method only if the corrected protocol-v2 ablation supports its parts.

The final section must specify:

- private, public, and evaluation dataset roles;
- Spider/BIRD profile and evidence visibility at every stage;
- client objective and aggregation rule;
- teacher target construction and execution validation;
- server objective and round schedule;
- communicated objects, threat boundary, and SLM-only deployment;
- the matched ablation that justified every retained component.

Historical prose is archived at
`paper/archive/protocol_v1_no_bird_evidence/FEDLS_SQL_METHOD_v1.md`.
