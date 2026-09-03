# FedLS-SQL — protocol-v2 evidence plan

The advisor's large-to-small federated NL-to-SQL question remains the target,
but the method is not selected in advance.

The evidence sequence is:

1. reproduce standard Spider and BIRD-with-evidence baselines;
2. run pure FL under the same data and prompt contracts;
3. rerun the former FedLS workflow as a reference in both transfer directions;
4. attribute EX gain using matched public-gold, teacher-target CE, and soft-KD controls;
5. improve only the component exposed as limiting by these results;
6. confirm the selected method across seeds, one stronger split, and optionally a second family;
7. combine it with lineage-independent communication, resource, and privacy-boundary evidence.

A Q3 submission is feasible only if protocol v2 shows a reproducible EX gain
over matched FL and a defensible causal control. Protocol-v1 results establish
engineering feasibility but no longer satisfy that submission gate.
